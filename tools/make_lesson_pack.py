"""
Episode JSON + cached clips  ->  packs/episode_NN.rolesson  for the iOS app.

The app stops playback the moment a drill cue ends, listens, then jumps to the
answer. That needs the exact position of every segment in the audio. The
podcast mp3 from render.py cannot give it: it is stitched from a few hundred
separate mp3 clips, each carrying encoder padding, so estimated times drift by
seconds over an episode. Here every clip is decoded to raw samples and joined
sample-exact, the designed pauses are inserted as exact runs of silence, and the
whole thing is encoded once. The positions written into the header are then
exact by construction.

The stops themselves come from the episode script, not from the audio: every
ep.drill() in the builders emits a `prompt` segment followed by its `answer`.

    python3 tools/make_lesson_pack.py episodes/episode_06a.json [more...]
    python3 tools/make_lesson_pack.py --all            # every rendered episode

With a sync folder configured (tools/sync_folder.py: iCloud Drive via iCloud
for Windows), each pack is also written into its lessons/, which the app picks
up the next time it is opened. render.py calls this itself after a full render.

File layout (read by PackStore.swift): b"ROLESSON1\\n", a 4-byte big-endian
header length, the JSON header, then the mp3 to the end of the file.
"""
import argparse
import json
import struct
import subprocess
import sys
from pathlib import Path

import render
from sync_folder import sync_folder

ROOT = Path(__file__).resolve().parent.parent   # the project root
PACKS = ROOT / "packs"
MAGIC = b"ROLESSON1\n"
# Mono 24 kHz is what Azure delivers for speech anyway; 48 kbps constant bitrate
# keeps a 10-minute episode near 3.5 MB and lets the player seek precisely.
RATE, BITRATE = 24000, "48k"


def pcm(clip: Path) -> bytes:
    return subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(clip), "-f", "s16le", "-ac", "1",
         "-ar", str(RATE), "-"], check=True, capture_output=True).stdout


def build(ep_path: Path) -> Path:
    ep = json.loads(ep_path.read_text(encoding="utf-8"))
    voices = ep["voices"]
    slug = f"{ep['episode']:02d}{ep.get('part') or ''}"

    audio = bytearray()
    segs = []
    for i, s in enumerate(ep["segments"]):
        clip = render.clip_for(s, voices[s["voice"]])
        if not clip.exists():
            sys.exit(f"{slug}: segment {s['id']} is not rendered yet — run render.py on it first")
        start = len(audio) / 2 / RATE
        audio += pcm(clip)
        end = len(audio) / 2 / RATE
        audio += bytes(2 * int(RATE * s["pause_after_ms"] / 1000))
        segs.append({"i": i, "type": s["type"], "lang": s["lang"], "text": s["text"],
                     "start": round(start, 3), "end": round(end, 3),
                     "pause": s["pause_after_ms"], "voice": s["voice"],
                     "chapter": s.get("chapter"),
                     **{k: s[k] for k in ("accept", "almost") if s.get(k)}})

    mp3 = subprocess.run(
        ["ffmpeg", "-v", "error", "-f", "s16le", "-ar", str(RATE), "-ac", "1", "-i", "-",
         "-c:a", "libmp3lame", "-b:a", BITRATE, "-f", "mp3", "-"],
        input=bytes(audio), check=True, capture_output=True).stdout

    header = json.dumps({
        "format": 1, "slug": slug, "title": ep["title"], "lesson": ep["lesson"],
        "duration": round(len(audio) / 2 / RATE, 3), "segments": segs,
    }, ensure_ascii=False).encode("utf-8")

    PACKS.mkdir(exist_ok=True)
    out = PACKS / f"episode_{slug}.rolesson"
    blob = MAGIC + struct.pack(">I", len(header)) + header + mp3
    out.write_bytes(blob)
    # Into the phone's sync folder too, if there is one: the app picks it up
    # from lessons/ the next time it is opened.
    folder = sync_folder()
    if folder:
        lessons = folder / "lessons"
        lessons.mkdir(parents=True, exist_ok=True)
        (lessons / out.name).write_bytes(blob)
        print(f"  -> {lessons / out.name}")

    drills = sum(1 for a, b in zip(segs, segs[1:])
                 if a["type"] == "prompt" and b["type"] == "answer")
    print(f"{out.name}: {len(segs)} segments, {drills} drills, "
          f"{len(audio) / 2 / RATE / 60:.1f} min, {out.stat().st_size / 1e6:.1f} MB")
    return out


def rendered_episodes():
    """Episodes whose every segment is already in the synthesis cache."""
    for p in sorted((ROOT / "episodes").glob("episode_*.json")):
        ep = json.loads(p.read_text(encoding="utf-8"))
        if all(render.clip_for(s, ep["voices"][s["voice"]]).exists() for s in ep["segments"]):
            yield p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", type=Path)
    ap.add_argument("--all", action="store_true", help="every fully rendered episode")
    args = ap.parse_args()
    paths = list(rendered_episodes()) if args.all else args.episodes
    if not paths:
        ap.error("name episode JSON files, or pass --all")
    for p in paths:
        build(p)


if __name__ == "__main__":
    main()
