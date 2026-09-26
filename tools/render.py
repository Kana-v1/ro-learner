"""
Render an episode JSON into an mp3 with pauses, chapter marks and an .srt.

    export AZURE_SPEECH_KEY=...
    export AZURE_SPEECH_REGION=westeurope
    export ELEVENLABS_API_KEY=...

    python tools/render.py episode_01.json
    python tools/render.py episode_01.json --only 0:20    # first 20 segments only
    python tools/render.py episode_01.json --dry-run      # silent stubs, no API calls

Each voice declares its own provider in the episode JSON. Azure carries the
bulk — narration, vocabulary, drills — on its 500k free characters a month.
ElevenLabs handles only the dialogue: about 300 unique characters an episode,
and the one place that has to sound like two people actually talking.

Segments are cached by content hash in cache/, so re-running after an edit only
re-synthesises what changed. The provider is part of the key, so moving a voice
between providers re-renders that voice and nothing else.
"""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent   # the project root
CACHE = ROOT / ".cache"      # synthesised segments, keyed by content hash
WORK = ROOT / ".build"       # ffmpeg scratch: silence clips, concat lists
OUT = ROOT / "out"           # finished audio, subtitles and the feed

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVEN_MODEL = "eleven_multilingual_v2"

# Higher stability than the default: in the vocabulary block the same word is
# heard three times and must sound the same each time. Expressive variation is
# a bug there, not a feature.
ELEVEN_SETTINGS = {"stability": 0.55, "similarity_boost": 0.75,
                   "style": 0.0, "use_speaker_boost": True}


# ── synthesis ────────────────────────────────────────────────────────────────
# Azure's free F0 tier allows roughly 20 requests a minute. Retrying a 429
# after one second just spends another request inside the same window, so
# space the calls out instead and back off hard when one still comes back.
_last_call = 0.0
MIN_INTERVAL = 3.2


def _throttle():
    global _last_call
    wait = MIN_INTERVAL - (time.time() - _last_call)
    if wait > 0:
        time.sleep(wait)
    _last_call = time.time()


def _request(req, throttle: bool = False) -> bytes:
    import urllib.error, urllib.request
    for attempt in range(6):
        if throttle:
            _throttle()
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            # wait out the rest of the quota window, not a token second
            wait = 15 * (attempt + 1)
            print(f"      rate limited, waiting {wait}s", file=sys.stderr)
            time.sleep(wait)
        except Exception as e:
            if attempt == 5:
                raise
            wait = 2 ** attempt
            print(f"      retry in {wait}s ({e})", file=sys.stderr)
            time.sleep(wait)


def synth_azure(text: str, voice_id: str, rate: float, lang: str,
                pitch: str = "") -> bytes:
    """Azure speaks SSML, so the slow rate here is a real prosody change
    rather than a hint the model may ignore. pitch lets one voice stand in
    for a second character — Romanian has only two native voices."""
    import urllib.request
    region = os.environ.get("AZURE_SPEECH_REGION", "westeurope")
    inner = escape(text)
    attrs = ""
    if abs(rate - 1.0) > 0.01:
        attrs += f' rate="{rate:.2f}"'
    if pitch:
        attrs += f' pitch="{pitch}"'
    if attrs:
        inner = f"<prosody{attrs}>{inner}</prosody>"
    ssml = ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
            f'xml:lang="{lang}"><voice name="{voice_id}">{inner}</voice></speak>')
    return _request(urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode("utf-8"),
        headers={"Ocp-Apim-Subscription-Key": os.environ["AZURE_SPEECH_KEY"],
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "audio-24khz-160kbitrate-mono-mp3",
                 "User-Agent": "romanian-podcast"}), throttle=True)


def synth_elevenlabs(text: str, voice_id: str, rate: float) -> bytes:
    import urllib.request
    settings = dict(ELEVEN_SETTINGS)
    if abs(rate - 1.0) > 0.01:
        settings["speed"] = rate            # accepted range is roughly 0.7–1.2
    body = json.dumps({"text": text, "model_id": ELEVEN_MODEL,
                       "voice_settings": settings}).encode()
    return _request(urllib.request.Request(
        f"{ELEVEN_URL}/{voice_id}?output_format=mp3_44100_128", data=body,
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                 "Content-Type": "application/json"}))


def synth(voice: dict, text: str, rate: float) -> bytes:
    # rate_scale slows one voice everywhere without editing every segment —
    # useful when a particular voice runs words together at full speed.
    rate = round(rate * voice.get("rate_scale", 1.0), 3)
    if voice["provider"] == "azure":
        return synth_azure(text, voice["voice_id"], rate, voice["lang"],
                           voice.get("pitch", ""))
    return synth_elevenlabs(text, voice["voice_id"], rate)


# ── audio helpers ────────────────────────────────────────────────────────────
def silence(ms: int, path: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
         "-t", f"{ms / 1000:.3f}", "-c:a", "libmp3lame", "-b:a", "128k", str(path)],
        check=True, capture_output=True)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)], check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def srt_time(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def clip_for(seg: dict, voice: dict) -> Path:
    """The cache file for one segment. Keyed by everything that changes the
    sound — provider, voice, effective rate, pitch and text — so the player
    builder (make_player.py) finds exactly the clips a render produced."""
    eff = round(seg["rate"] * voice.get("rate_scale", 1.0), 3)
    h = hashlib.sha1(
        f"{voice['provider']}|{voice['voice_id']}|{eff}|{voice.get('pitch','')}|"
        f"{seg['text']}".encode()).hexdigest()[:16]
    return CACHE / f"{h}.mp3"


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode", help="path to episodes/episode_NN.json")
    ap.add_argument("--out", default=None,
                    help=f"directory for the finished mp3 (default {OUT.name}/)")
    ap.add_argument("--only", help="segment slice, e.g. 0:20, for a cheap trial")
    ap.add_argument("--dry-run", action="store_true",
                    help="silent stubs instead of API calls")
    ap.add_argument("--delay", type=float, default=3.2,
                    help="seconds between Azure calls; the free F0 tier allows "
                         "about 20 a minute (default 3.2)")
    args = ap.parse_args()

    globals()["MIN_INTERVAL"] = args.delay

    ep = json.load(open(args.episode, encoding="utf-8"))
    voices = ep["voices"]
    segments = ep["segments"]
    if args.only:
        a, b = (int(x) if x else None for x in args.only.split(":"))
        segments = segments[a:b]

    out_dir = Path(args.out) if args.out else OUT
    for d in (CACHE, WORK, out_dir):
        d.mkdir(parents=True, exist_ok=True)
    stem = (f"episode_{ep['episode']:02d}{ep.get('part') or ''}"
            + ("_part" if args.only else ""))

    # Work out what this run will actually spend before spending it.
    plan, spend = [], {}
    for s in segments:
        v = voices[s["voice"]]
        clip = clip_for(s, v)
        if not clip.exists():
            spend[v["provider"]] = spend.get(v["provider"], 0) + len(s["text"])
        plan.append((s, v, clip))

    todo = sum(1 for _s, _v, c in plan if not c.exists())
    print(f"{stem}: {len(segments)} segments")
    for prov, n in sorted(spend.items()):
        print(f"  {prov:11} {n:6d} new characters")
    if not spend:
        print("  everything already cached")
    elif not args.dry_run and "azure" in spend:
        print(f"  {todo} calls at {MIN_INTERVAL:.1f}s apart "
              f"≈ {todo * MIN_INTERVAL / 60:.0f} min")

    if not args.dry_run:
        for prov, env in [("azure", "AZURE_SPEECH_KEY"),
                          ("elevenlabs", "ELEVENLABS_API_KEY")]:
            if prov in spend and not os.environ.get(env):
                sys.exit(f"{env} is not set (needed for provider '{prov}')")

    # ── synthesise ───────────────────────────────────────────────────────────
    made = 0
    for s, v, clip in plan:
        if clip.exists():
            continue
        if args.dry_run:
            silence(max(500, len(s["text"]) * 60), clip)
        else:
            made += 1
            print(f"  [{made}/{todo}] {s['id']} {v['provider']:9} "
                  f"{s['voice']:14} {s['text'][:38]}")
            clip.write_bytes(synth(v, s["text"], s["rate"]))
            continue
        made += 1
    print(f"synthesised {made}, reused {len(plan) - made}")

    # ── assemble ─────────────────────────────────────────────────────────────
    order, srt, chapters, t, n = [], [], [], 0.0, 0
    for s, _v, clip in plan:
        d = duration(clip)
        if "chapter" in s:
            chapters.append((t, s["chapter"]))
        if s["lang"] == "ro":
            n += 1
            srt.append(f"{n}\n{srt_time(t)} --> {srt_time(t + d)}\n{s['text']}\n")
        order.append(clip)
        t += d
        if s["pause_after_ms"]:
            gap = WORK / f"gap_{s['pause_after_ms']}.mp3"
            if not gap.exists():
                silence(s["pause_after_ms"], gap)
            order.append(gap)
            t += duration(gap)

    listfile = WORK / "concat.txt"
    listfile.write_text("".join(f"file '{p.resolve()}'\n" for p in order))

    meta = WORK / "chapters.txt"
    lines = [";FFMETADATA1", f"title={ep['title']}",
             f"artist=Romanian — {ep['source']}"]
    for i, (start, name) in enumerate(chapters):
        end = chapters[i + 1][0] if i + 1 < len(chapters) else t
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(start * 1000)}",
                  f"END={int(end * 1000)}", f"title={name}"]
    meta.write_text("\n".join(lines) + "\n")

    out = out_dir / f"{stem}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-i", str(meta), "-map_metadata", "1", "-c:a", "libmp3lame",
         "-b:a", "128k", str(out)], check=True, capture_output=True)
    (out_dir / f"{stem}.srt").write_text("\n".join(srt), encoding="utf-8")

    print(f"\n{out}  {duration(out) / 60:.1f} min")
    print(f"{out_dir / (stem + '.srt')}  {n} Romanian lines")
    if chapters:
        print("chapters: " + ", ".join(c[1] for c in chapters))


if __name__ == "__main__":
    main()
