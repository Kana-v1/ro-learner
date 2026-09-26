"""
Results from the Vorbește app  ->  the review schedule, plus a note back to the app.

The app writes one JSON file per finished session into the linked Drive folder's
results/ (or hands over an export bundle through the share sheet). This script:

  1. archives every session it finds under data/results/ (private, gitignored:
     it holds transcripts of your speech),
  2. works out which drills you are still getting wrong — the latest outcome of
     each drill across all sessions — and writes them to state.json as
     "struggles", which review_auto() in episode_kit.py puts at the front of
     the next episodes' review blocks, ahead of the fixed +1/+3/+7/+16 schedule,
  3. prints a summary for Claude to analyse,
  4. with --note, writes a .roanalysis file into the Drive folder's notes/ so
     the app marks those sessions analysed and shows the note.

    python3 ingest_results.py                  # read, update state.json, summarise
    python3 ingest_results.py --note "text"    # ...and send a note back to the app

The Drive folder comes from $VORBESTE_DRIVE (a Google Drive for desktop "Mirror
files" folder, e.g. "/mnt/c/Users/you/My Drive/Vorbește"); --results-dir points
somewhere else, e.g. files fetched through the Google Drive connector.
"""
import argparse
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "data" / "results"
STATE = ROOT / "data" / "state.json"
GENDER = {"ro_male": "m", "ro_radu": "m", "ro_female": "f", "ro_dana": "f", "ro_elena": "f"}


def drive_dir():
    d = os.environ.get("VORBESTE_DRIVE")
    return Path(d) if d else None


def load_sessions(paths):
    """Session dicts from app result files: one session per file, or an export
    bundle {"sessions": [...]}."""
    out = []
    for p in paths:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"  skipped {p.name}: {e}")
            continue
        out.extend(data["sessions"] if isinstance(data, dict) and "sessions" in data else [data])
    return out


def key(s):
    started = datetime.fromisoformat(s["started"].replace("Z", "+00:00"))
    return f"{s['episode']}_{int(started.timestamp())}"


def outcome(item):
    return item.get("correction") or (item["attempts"][-1]["verdict"] if item.get("attempts") else "unmarked")


def answer_gender(slug, seg):
    """The voice that speaks a drill's answer, so a review drill keeps it."""
    p = ROOT / "episodes" / f"episode_{slug}.json"
    try:
        segs = json.loads(p.read_text(encoding="utf-8"))["segments"]
        return GENDER.get(segs[seg + 1]["voice"], "m")
    except (OSError, KeyError, IndexError, json.JSONDecodeError):
        return "m"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", type=Path, help="where the app's result files are")
    ap.add_argument("--note", help="write this report back to the app as a .roanalysis")
    args = ap.parse_args()

    drive = drive_dir()
    source = args.results_dir or (drive / "results" if drive else None)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    incoming = sorted(source.glob("*.json")) if source and source.exists() else []
    new = 0
    for s in load_sessions(incoming):
        dest = ARCHIVE / f"{key(s)}.json"
        if not dest.exists():
            new += 1
        dest.write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"read {len(incoming)} file(s) from {source or '(no source)'}; {new} new session(s)")

    sessions = sorted(load_sessions(sorted(ARCHIVE.glob("*.json"))), key=lambda s: s["started"])
    if not sessions:
        print("no sessions archived yet")
        return

    # latest outcome of every drill, across all sessions, in time order
    history = defaultdict(list)          # (episode, seg) -> [(started, outcome, item)]
    for s in sessions:
        for it in s["items"]:
            o = outcome(it)
            if o != "unmarked":
                history[(s["episode"], it["seg"])].append((s["started"], o, it))

    struggles = {}
    for (slug, seg), events in history.items():
        misses = sum(1 for _, o, _ in events if o != "correct")
        last_time, last, it = events[-1]
        if last == "correct" or misses == 0:
            continue
        struggles[f"{slug}:{seg}"] = {
            "intro": slug, "g": answer_gender(slug, seg),
            "cue": it["cue"], "answer": it["expected"],
            "misses": misses, "seen": len(events), "last": last,
            "heard": (it.get("attempts") or [{}])[-1].get("heard"),
            "last_seen": last_time,
        }

    state = json.loads(STATE.read_text(encoding="utf-8"))
    state["struggles"] = dict(sorted(struggles.items(), key=lambda kv: -kv[1]["misses"]))
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    # summary for Claude to read and analyse
    print("\nsessions:")
    for s in sessions[-12:]:
        main_items = [i for i in s["items"] if i.get("round", 0) == 0]
        first = sum(1 for i in main_items if outcome(i) == "correct" and len(i.get("attempts", [])) <= 1)
        print(f"  {s['started'][:16]}  {s['episode']:4} {s['mode']:5} {first}/{len(main_items)} right first time")
    print(f"\nstill wrong ({len(struggles)}), now first in the next review blocks:")
    for k, v in list(state["struggles"].items())[:25]:
        print(f"  {k:9} x{v['misses']}  {v['answer']!r:45} heard {v['heard']!r}")

    if args.note is not None:
        target = (drive / "notes") if drive else (ROOT / "packs")
        target.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        note = {"format": 1, "created": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "analyzed": [key(s) for s in sessions], "report": args.note}
        out = target / f"claude-note_{now.strftime('%Y-%m-%d_%H%M')}.roanalysis"
        out.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nnote for the app: {out}")


if __name__ == "__main__":
    main()
