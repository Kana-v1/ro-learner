"""
Shared machinery for episode builders. Each build_episode_NN.py imports this,
declares its content, and calls emit().

Keeping the content in plain Python lists rather than hand-written JSON means
the pedagogy stays readable and the checks the skill asks for run on every
build instead of being remembered.
"""
import json
import pathlib
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent     # the project root
DATA = ROOT / "data"
EPISODES = ROOT / "episodes"

SLOW, NORMAL = 0.80, 1.0
# The production pause is proportional to the answer, not a flat value: a
# one-word reply needs a moment, a whole sentence needs real time to assemble,
# and any fixed pause is wrong for one of them. recall_pause() sizes it from the
# answer's word count; P_RECALL/P_WORD remain as anchors and for callers that
# pass an explicit pause. The repeat-after pause (P_REPEAT) stays short — you
# are echoing, not retrieving.
P_REPEAT, P_SHORT, P_WORD, P_RECALL, P_SECTION = 1400, 400, 3000, 5000, 1000


def recall_pause(romanian):
    """Silence to produce `romanian` from memory, scaled to its length.

    ~2.5 s for a single word, rising ~0.85 s per word to a 9 s ceiling. Tuned
    long on purpose: the learner is walking and producing out loud, and running
    out of time before the answer forms is what makes a drill useless.
    """
    words = len(romanian.split())
    return max(2500, min(9000, 1400 + 850 * words))

# Memory-first budget: how many genuinely new items one episode may introduce.
# Above this, retention collapses — the failure that prompted the rebuild. The
# cap counts everything in `required`; keep content words near six and let the
# odd function word (unde, cum) use the headroom to eight.
NEW_ITEM_CAP = 8

VOICE = {"nar": "en_narrator", "m": "ro_male", "f": "ro_female",
         "dana": "ro_dana", "radu": "ro_radu", "elena": "ro_elena"}

VOICES = {
    "en_narrator": {"provider": "azure", "lang": "en-US",
                    "voice_id": "en-US-AndrewNeural"},
    "ro_male":     {"provider": "azure", "lang": "ro-RO",
                    "voice_id": "ro-RO-EmilNeural", "rate_scale": 0.90},
    "ro_female":   {"provider": "azure", "lang": "ro-RO",
                    "voice_id": "ro-RO-AlinaNeural"},
    # Three characters, two native Romanian voices. Elena and Radu borrow the
    # same two at shifted pitch so the dialogue has distinguishable speakers.
    "ro_dana":     {"provider": "azure", "lang": "ro-RO",
                    "voice_id": "ro-RO-AlinaNeural"},
    "ro_radu":     {"provider": "azure", "lang": "ro-RO",
                    "voice_id": "ro-RO-EmilNeural", "rate_scale": 0.92},
    "ro_elena":    {"provider": "azure", "lang": "ro-RO",
                    "voice_id": "ro-RO-AlinaNeural", "pitch": "+12%"},
}


def fold(text):
    """Text as the app's grader compares it: no case, diacritics or punctuation."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c if c.isalpha() else " " for c in text
                   if unicodedata.category(c) != "Mn")
    return " ".join(text.split())


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


# ── spaced-retrieval state ───────────────────────────────────────────────────
# state.json maps every taught item to the episode that introduced it, plus a
# canonical English->Romanian pair reused verbatim in later review blocks. What
# is "due" in a given episode is a pure function of the episode `sequence` and
# the `intervals`, so a build only ever reads the schedule and appends its own
# new items — there is no per-build mutation of due dates to get out of sync.
STATE = DATA / "state.json"


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def save_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1),
                     encoding="utf-8")


class Episode:
    def __init__(self, number, lesson, title, source, required, glue,
                 level="A1", part=None):
        # part is "a"/"b" for a chapter split across two episodes; it only
        # changes the output filename (episode_03a.json) and rides along in the
        # JSON. number stays the lesson's integer so ordering still works.
        self.number, self.lesson = number, lesson
        self.title, self.source = title, source
        self.required, self.glue, self.level = required, glue, level
        self.part = part
        self.seg = []
        # New items this episode introduces, registered into state.json on emit
        # with a canonical cue/answer for later review. Populated by new_item().
        self.new = []

    @property
    def slug(self):
        return f"{self.number:02d}{self.part or ''}"

    # ── segment primitives ───────────────────────────────────────────────────
    def add(self, type_, text, lang="en", voice="nar", rate=NORMAL,
            pause=P_SHORT, chapter=None):
        s = {"id": f"s{len(self.seg) + 1:03d}", "type": type_, "lang": lang,
             "voice": VOICE[voice], "text": text, "rate": rate,
             "pause_after_ms": pause}
        if chapter:
            s["chapter"] = chapter
        self.seg.append(s)

    def narr(self, text, pause=P_SHORT, chapter=None):
        self.add("narration", text, "en", "nar", NORMAL, pause, chapter)

    def ro(self, text, voice="m", rate=NORMAL, pause=P_REPEAT, type_="target"):
        self.add(type_, text, "ro", voice, rate, pause)

    def teach(self, romanian, english, voice="m"):
        """Bilingual sandwich: hear it, guess, confirm, hear it slowly, repeat."""
        self.ro(romanian, voice, NORMAL, P_REPEAT)
        self.add("gloss", english, "en", "nar", NORMAL, P_SHORT)
        self.ro(romanian, voice, SLOW, P_REPEAT)

    def example(self, setup_en, romanian, voice="m", pause=P_REPEAT):
        """Narrator sets it up in English; the Romanian voice speaks the Romanian.

        Rule: Romanian words are always heard from a Romanian voice, never from
        the English narrator — a learner cannot parse target-language forms in
        an L1 accent. Grammar and paradigms use this instead of quoting Romanian
        inside a narration segment.
        """
        if setup_en:
            self.narr(setup_en, pause=P_SHORT)
        self.ro(romanian, voice, NORMAL, pause)

    def drill(self, cue, romanian, voice="m", pause=None, accept=None, almost=None):
        """Retrieval: cue, silence to produce, correct answer, silence to repeat.

        The production pause defaults to recall_pause(romanian) — proportional
        to the answer — unless an explicit pause is passed.

        accept: other phrasings that are fully right (a different word order,
        a synonym the chapter teaches). almost: phrasings a listener would
        understand but that the lesson should correct. Neither is spoken; they
        ride on the answer segment into the app's grader. Missing articles,
        dropped subject pronouns, e/este and diacritics are handled by the
        grader's own rules, so list only what those rules can't know.
        """
        self.add("prompt", cue, "en", "nar", NORMAL,
                 recall_pause(romanian) if pause is None else pause)
        self.add("answer", romanian, "ro", voice, NORMAL, P_REPEAT)
        if accept:
            self.seg[-1]["accept"] = list(accept)
        if almost:
            self.seg[-1]["almost"] = list(almost)

    def recall_word(self, cue, word, voice="m"):
        """Bare-word retrieval: the first, easiest recall of a new item.

        Graded practice — before a learner can produce a whole sentence, the
        word itself has to be retrievable. This asks for the single word (or
        short chunk) from an English cue, right after the item is introduced;
        the pause is proportional, so a one-word answer gets the short floor.
        The sentence-level drill() comes later in the episode.
        """
        self.drill(cue, word, voice)

    def new_item(self, name, cue, answer, voice="m", teach_ro=None, teach_en=None):
        """Introduce one new item: sandwich it, retrieve the bare word at once,
        and register it for spaced review in later episodes.

        `name` is the headword (used for coverage and as the state key). `cue`
        and `answer` are the canonical English->Romanian pair reused verbatim
        when this item comes due in a future episode's review block, so it must
        stand on its own out of context. teach_ro/teach_en override the sandwich
        phrase if it should differ from the review pair.
        """
        self.teach(teach_ro or answer, teach_en or cue, voice)
        self.recall_word(cue, answer, voice)
        self.new.append({"name": name, "cue": cue, "answer": answer,
                         "voice": voice})

    def dialogue(self, lines, pause=650):
        for who, line in lines:
            self.ro(line, who, NORMAL, pause, type_=f"line_{who}")

    # ── review of earlier episodes ───────────────────────────────────────────
    def review(self, items, intro=None):
        """Spaced retrieval of items introduced in previous episodes."""
        self.narr(intro or "Before we finish, a few things from earlier. Same "
                           "rules — answer out loud before you hear it.",
                  pause=P_SECTION, chapter="Review")
        for cue, ans, v in items:
            self.drill(cue, ans, v)

    def review_auto(self, cap=7, intro=None, struggle_cap=4):
        """Spaced retrieval, scheduled from state.json rather than hand-picked.

        First the learner's own misses: drills the Vorbește app recorded as
        still wrong (state.json "struggles", written by ingest_results.py), most
        missed first, up to `struggle_cap`. Then every item that comes due this
        episode (introduced +1, +3, +7 or +16 episodes back, per the intervals),
        oldest gap first, filling the block up to `cap` in total. The schedule
        turns a heard word into a recallable one; the struggles make the course
        answer to what the learner actually got wrong.
        """
        state = load_state()
        seq, intervals = state["sequence"], state["_meta"]["intervals"]
        if self.slug not in seq:
            print(f"  note: {self.slug} not in sequence; no scheduled review")
            return
        ci = seq.index(self.slug)
        # Misses already asked by an earlier episode built since the last
        # ingest are skipped, so consecutive episodes work down the list
        # instead of all repeating its top few. (ingest_results.py resets this.)
        used = {fold(a) for slug, answers in state.get("struggles_used", {}).items()
                if slug in seq and seq.index(slug) < ci for a in answers}
        # Only misses from episodes played before this one: an episode cannot
        # review drills the learner has not met yet.
        struggles = [s for s in state.get("struggles", {}).values()
                     if s["intro"] in seq and seq.index(s["intro"]) < ci
                     and fold(s["answer"]) not in used][:struggle_cap]
        taken = {s["answer"] for s in struggles}
        due = []
        for it in state["items"].values():
            if it["intro"] not in seq or it["answer"] in taken:
                continue
            gap = ci - seq.index(it["intro"])
            if gap in intervals:
                due.append((gap, it))
        due.sort(key=lambda gi: -gi[0])          # oldest gap surfaces first
        due = struggles + [it for _, it in due][:max(cap - len(struggles), 0)]
        if struggles:
            print(f"  review: {len(struggles)} of your recent misses first")
        if not due:
            return
        self.narr(intro or "Before we finish, things from earlier episodes come "
                          "back — answer each out loud before you hear it.",
                  pause=P_SECTION, chapter="Review")
        for it in due:
            self.drill(it["cue"], it["answer"], it["g"])

    # ── emit and check ───────────────────────────────────────────────────────
    def emit(self, spoken_layer=None):
        EPISODES.mkdir(exist_ok=True)
        slug = f"{self.number:02d}{self.part or ''}"
        ep = {
            "episode": self.number, "part": self.part, "lesson": self.lesson,
            "title": self.title, "source": self.source,
            "l1": "en", "l2": "ro", "level": self.level,
            "glue": self.glue,
            "spoken_layer": spoken_layer or [],
            "voices": VOICES,
            "segments": self.seg,
        }
        path = EPISODES / f"episode_{slug}.json"
        path.write_text(json.dumps(ep, ensure_ascii=False, indent=1),
                        encoding="utf-8")
        self._register()
        self._report(path)
        return path

    def _register(self):
        """Record this episode's new items in state.json so later episodes can
        schedule them for review. Idempotent: re-running a build overwrites the
        item's record with the same values."""
        state = load_state()
        if self.slug not in state["sequence"]:
            state["sequence"].append(self.slug)
            print(f"  note: appended {self.slug} to sequence (was missing)")
        for it in self.new:
            state["items"][it["name"]] = {
                "intro": self.slug, "g": it["voice"],
                "cue": it["cue"], "answer": it["answer"]}
        # Which of the learner's misses this episode asks anywhere (a repair
        # episode asks most of them outside any review block), for
        # review_auto() in later episodes to skip.
        asked = {fold(s["text"]) for s in self.seg if s["type"] == "answer"}
        state.setdefault("struggles_used", {})[self.slug] = [
            s["answer"] for s in state.get("struggles", {}).values()
            if fold(s["answer"]) in asked]
        save_state(state)

    def _report(self, path):
        def fold(s):
            return "".join(c for c in unicodedata.normalize("NFD", s.lower())
                           if unicodedata.category(c) != "Mn")

        ro_text = fold(" ".join(s["text"] for s in self.seg if s["lang"] == "ro"))
        missing = [w for w in self.required if fold(w) not in ro_text]

        chars = {"ro": 0, "en": 0}
        for s in self.seg:
            chars[s["lang"]] += len(s["text"])
        silence = sum(s["pause_after_ms"] for s in self.seg) / 1000
        speech = sum(len(s["text"].split()) for s in self.seg) / 2.3
        runtime = speech + silence
        l1 = 100 * chars["en"] / sum(chars.values())

        print(f"wrote           : {path}")
        print(f"segments        : {len(self.seg)}")
        print(f"coverage        : {len(self.required) - len(missing)}"
              f"/{len(self.required)}"
              + (f"  MISSING: {missing}" if missing else "  ok"))
        print(f"glue items      : {len(self.glue)} ({', '.join(self.glue)})")
        print(f"L1 share        : {l1:.0f}%")
        print(f"silence         : {100 * silence / runtime:.0f}% of runtime")
        print(f"estimated run   : {runtime / 60:.1f} min")
        print(f"characters      : {sum(chars.values())}")

        # The budget is on items actually introduced (new_item), not on the
        # coverage list: a recap references many anchor words but introduces
        # none, so len(required) is the wrong thing to cap.
        introduced = [it["name"] for it in self.new]
        print(f"new items       : {len(introduced)} "
              f"(cap {NEW_ITEM_CAP})  {', '.join(introduced) or '—'}")

        # Rule: the English narrator never speaks Romanian. Catch the diacritic
        # forms left in an English-voice segment (narration/gloss/prompt); the
        # fix is to move that Romanian into a Romanian-voice segment (example(),
        # ro(), teach()). A heuristic — it cannot see diacritic-free Romanian —
        # so authoring discipline still matters, but it catches the common slip.
        ro_in_en = [s["text"] for s in self.seg
                    if s["voice"] == VOICE["nar"]
                    and any(ch in s["text"] for ch in "ăâîșțĂÂÎȘȚ")]
        if ro_in_en:
            print(f"romanian-in-narrator: {len(ro_in_en)} segment(s) — e.g. "
                  f"{ro_in_en[0][:60]!r}")

        warn = []
        if missing:
            warn.append("coverage incomplete")
        if ro_in_en:
            warn.append(f"{len(ro_in_en)} English-voice segment(s) contain "
                        f"Romanian — move it to a Romanian voice (example()/ro())")
        if len(introduced) > NEW_ITEM_CAP:
            warn.append(f"new-item budget exceeded — {len(introduced)} > "
                        f"{NEW_ITEM_CAP}; move items to another episode, do not "
                        f"thin the recall")
        if runtime / 60 > 20:
            warn.append("over the 20-minute cap — cut explanation, not drill")
        if len(self.glue) > 4:
            warn.append("glue budget exceeded")
        if warn:
            raise SystemExit("FAILED: " + "; ".join(warn))
