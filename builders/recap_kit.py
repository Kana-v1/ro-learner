"""
The learner's own misses, for a recap episode to drill verbatim.

A recap's job after a block of five lessons is retrieval across the block —
and by then state.json "struggles" holds exactly what didn't stick, so the
recap drills those rather than a hand-picked sample. Each is asked with its
item's canonical cue when it has one (the clearer cue, as in review_auto),
and getting it right in the recap clears it on the next ingest.
"""
from episode_kit import load_state, fold

ARTICLES = ("un ", "o ")
PRONOUNS = {"eu", "tu", "el", "ea", "noi", "voi", "ei", "ele"}


def key(answer):
    """An answer for de-duplicating: 'tu repeți' and 'repeți' are one drill."""
    w = fold(answer).split()
    return " ".join(w[1:] if len(w) > 1 and w[0] in PRONOUNS else w)


def misses(lessons):
    """The struggles from these lessons ("07", "08", …), most-missed first,
    each with its canonical cue."""
    state = load_state()
    canon = {fold(it["answer"]): it["cue"] for it in state["items"].values()}
    out = []
    for s in sorted(state.get("struggles", {}).values(), key=lambda s: -s["misses"]):
        if s["intro"][:2] in lessons:
            out.append(dict(s, cue=canon.get(fold(s["answer"]), s["cue"])))
    return out


class Picker:
    """Hands out misses by kind, never the same answer twice in an episode."""

    def __init__(self, items):
        self.items = items
        self.taken = set()

    def take(self, test, limit):
        out = []
        for s in self.items:
            k = key(s["answer"])
            if k in self.taken or not test(s):
                continue
            self.taken.add(k)
            out.append(s)
            if len(out) >= limit:
                break
        return out


def words(s):
    return len(s["answer"].split())


def with_article(s):
    return s["answer"].lower().startswith(ARTICLES) and words(s) <= 4


def short_form(s):
    return words(s) <= 3 and not s["answer"].lower().startswith(ARTICLES)


def sentence(s):
    return words(s) >= 3
