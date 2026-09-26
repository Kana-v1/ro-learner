"""
Turn data/spoken.json into a markdown sheet a native speaker can mark up.

    python tools/make_review_sheet.py > out/spoken_review.md

The colloquial layer is the part of this project a language model is least
reliable about, and the part where an error is most socially expensive. Build
it for all forty lessons first, then have one native speaker go through the
whole sheet in a single sitting rather than second-guessing each episode.
"""
import json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent.parent   # the project root
data = json.loads((HERE / "data" / "spoken.json").read_text(encoding="utf-8"))
meta = data.pop("_meta", {})

LABEL = {
    "written_vs_spoken": "Book form vs spoken form",
    "missing_from_book": "Not in the book at all",
    "register_scale": "Register",
    "filler": "Filler / discourse marker",
    "moldovanism": "Moldovan → Romanian",
}

out = [f"# Spoken Romanian — review sheet\n",
       f"**Target:** {meta.get('target_variety','')} · {meta.get('target_register','')}\n",
       "Please mark anything that is wrong, dated, too formal, too casual, or "
       "regional. Crossing an item out is as useful as correcting it.\n"]

flagged = 0
for lesson in sorted(data, key=int):
    out.append(f"\n## Lesson {lesson}\n")
    for e in data[lesson]:
        mark = " ⚠️" if e.get("confidence") == "check" else ""
        flagged += mark != ""
        out.append(f"### {LABEL.get(e['type'], e['type'])}{mark}\n")
        if e.get("book"):
            out.append(f"- book: `{e['book']}`")
        out.append(f"- spoken: **{e['spoken']}**")
        out.append(f"- meaning: {e['gloss']}")
        out.append(f"- {e['note']}")
        out.append("- [ ] correct  [ ] needs changing: ______________________\n")

out.append(f"\n---\n{sum(len(v) for v in data.values())} items, "
           f"{flagged} marked for particular attention.\n")
sys.stdout.write("\n".join(out))
