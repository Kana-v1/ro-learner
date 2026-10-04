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

    python3 tools/ingest_results.py                  # read, update state.json, summarise
    python3 tools/ingest_results.py --note "text"    # ...and send a note back to the app

Results come from the private GitHub repo when it is set up (tools/data_repo.py,
pulled first), otherwise from the iCloud sync folder (tools/sync_folder.py);
--results-dir reads result files from anywhere else.
"""
import argparse
import json
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import data_repo
from sync_folder import sync_folder

ROOT = Path(__file__).resolve().parent.parent   # the project root
ARCHIVE = ROOT / "data" / "results"
FEEDBACK = ROOT / "data" / "feedback"          # notes sent from the app's feedback button
STATE = ROOT / "data" / "state.json"
GENDER = {"ro_male": "m", "ro_radu": "m", "ro_female": "f", "ro_dana": "f", "ro_elena": "f"}


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


def fold(text):
    """An answer as the grader compares it: no case, diacritics or punctuation."""
    text = unicodedata.normalize("NFD", text.lower().replace("ş", "ș").replace("ţ", "ț"))
    text = "".join(c if c.isalpha() else " " for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.split())


def outcome(item):
    """The drill's result. A no-answer while the mic did hear a voice is the
    recogniser's miss, not the learner's: "unheard", which counts neither way."""
    if item.get("correction"):
        return item["correction"]
    if not item.get("attempts"):
        return "unmarked"
    last = item["attempts"][-1]
    if last["verdict"] == "no_answer" and last.get("voiced"):
        return "unheard"
    return last["verdict"]


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

    drive = None if data_repo.available() else sync_folder()
    if args.results_dir:
        source = args.results_dir
    elif data_repo.available():
        source = data_repo.pull()
    else:
        source = drive / "results" if drive else None
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

    # Latest outcome of every answer, across all sessions, in time order. Keyed
    # by the answer itself, not the drill's place in an episode: the same
    # answer is asked in the vocabulary block, the mixed recall, the second
    # chance and later reviews, and getting it right in any of them (a review
    # in a later episode included) is what clears it.
    history = defaultdict(list)          # folded answer -> [(started, outcome, item, episode)]
    for s in sessions:
        for it in s["items"]:
            o = outcome(it)
            if o not in ("unmarked", "unheard"):
                history[fold(it["expected"])].append((s["started"], o, it, s["episode"]))

    struggles = {}
    last_heard = {}      # for the printout only: transcripts never go into state.json
    for events in history.values():
        misses = sum(1 for _, o, _, _ in events if o != "correct")
        _, last, it, _ = events[-1]
        if last == "correct" or misses == 0:
            continue
        # the episode that first asked it: a review can only come after that
        slug, seg = events[0][3], events[0][2]["seg"]
        struggles[f"{slug}:{seg}"] = {
            "intro": slug, "g": answer_gender(slug, seg),
            "cue": it["cue"], "answer": it["expected"],
            "misses": misses, "seen": len(events), "last": last,
        }
        last_heard[f"{slug}:{seg}"] = (it.get("attempts") or [{}])[-1].get("heard")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    # state.json is committed to the public repo: it holds which answers are
    # still wrong, never what was heard (that stays in data/results/).
    state["struggles"] = dict(sorted(struggles.items(), key=lambda kv: -kv[1]["misses"]))
    # which episodes already ask which misses: stale once new sessions arrive
    if new:
        state["struggles_used"] = {}
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

    # summary for Claude to read and analyse
    print("\nsessions:")
    for s in sessions[-12:]:
        main_items = [i for i in s["items"] if i.get("round", 0) == 0]
        first = sum(1 for i in main_items if outcome(i) == "correct" and len(i.get("attempts", [])) <= 1)
        unheard = sum(1 for i in s["items"] for a in i.get("attempts", [])
                      if a["verdict"] == "no_answer" and a.get("voiced"))
        print(f"  {s['started'][:16]}  {s['episode']:4} {s['mode']:5} {first}/{len(main_items)} right first time"
              + (f", {unheard} answer(s) said but not recognised" if unheard else ""))
    print(f"\nstill wrong ({len(struggles)}), now first in the next review blocks:")
    for k, v in list(state["struggles"].items())[:25]:
        print(f"  {k:9} x{v['misses']}  {v['answer']!r:45} heard {last_heard.get(k)!r}")

    # feedback notes from the app: print the new ones, keep them all locally
    fb_source = (source.parent / "feedback") if source else None
    new_fb = []
    if fb_source and fb_source.exists():
        FEEDBACK.mkdir(parents=True, exist_ok=True)
        for f in sorted(fb_source.glob("*.json")):
            dest = FEEDBACK / f.name
            if not dest.exists():
                new_fb.append(json.loads(f.read_text(encoding="utf-8")))
            dest.write_bytes(f.read_bytes())
    if new_fb:
        print(f"\nfeedback from the app ({len(new_fb)} new):")
        for n in new_fb:
            where = " ".join(x for x in (n.get("episode"), n.get("drill")) if x)
            print(f"  {n['created'][:16]}  [{n['kind']}] {where}: {n.get('text') or '(no text)'}")
            if n.get("current"):
                c = n["current"]
                print(f"      on screen: {c['cue']!r} -> {c['expected']!r} heard {c['heard']}")
            for r in n.get("recent", []):
                print(f"      before:    {r['cue']!r} -> {r['expected']!r} heard {r['heard']}")

    if args.note is not None:
        target = (drive / "notes") if drive else (ROOT / "packs")
        target.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc)
        note = {"format": 1, "created": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "analyzed": [key(s) for s in sessions], "report": args.note}
        out = target / f"claude-note_{now.strftime('%Y-%m-%d_%H%M')}.roanalysis"
        out.write_text(json.dumps(note, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nnote for the app: {out}")
        if data_repo.available():
            data_repo.push_note(out)


if __name__ == "__main__":
    main()
