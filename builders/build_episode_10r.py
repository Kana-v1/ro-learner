"""
Episode 10R — "Recapitulare (6–10), partea I" (consolidation after Lecția 10)

No new vocabulary. The second block of five lessons, in two recap parts:
this one is the nouns and their describing words (Lecții 6–7: family, looks,
clothes, numbers, shopping), 10S the verbs, time and prices (Lecții 8–10)
and a closing self-introduction.

Unlike 05R, the drills are the learner's own misses: by the end of Lecția 10,
state.json "struggles" held 152 answers still wrong — none left from Lecția
6 (cleared by the reviews), 62 from Lecția 7. They fall into patterns — a
dropped un/o before a noun with a describing word (o rochie mică → "rochie
mică"), endings for her and for more than one (ochi negri, case mici, scaune
verzi), and whole sentences — and each pattern gets a by-ear reminder in the
09A style before its drills. The drill list is read from state.json at build
time (recap_kit), asked with each item's canonical cue; getting one right
here clears it on the next ingest.

Closes with the spoken-register chunks of Lecția 7 as ordinary speech —
Ce doriți? Aș vrea… Cât face? Poftiți. Cum arată?
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW
from recap_kit import misses, Picker, with_article, short_form, sentence

REQUIRED = ["fiica", "fiul", "deștept",              # L6
            "vreau", "rochie", "verde", "nevoie", "câte"]   # L7
GLUE = {"Una.": "one — her-form, on its own"}

ep = Episode(number=10, lesson=10, part="r", title="Recapitulare (6–10), partea I",
             source="Limba care ne unește, nivelul I — Recapitulare, lecțiile 6–10",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Ce noutăți? Cum e familia ta?"),
    ("radu", "Bine! Fiica mea are opt ani. E înaltă și blondă."),
    ("dana", "Și fiul tău?"),
    ("radu", "Fiul meu are doisprezece ani. E scund, dar deștept."),
    ("dana", "Și ce vrei azi?"),
    ("radu", "Vreau o rochie nouă pentru fiica mea. Și am nevoie de pâine."),
    ("dana", "Rochiile sunt scumpe! Câte rochii vrei?"),
    ("radu", "Una. Mică și verde."),
]

pick = Picker(misses({"06", "07"}))

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("No new words. Lessons 6 to 10 are done, so this is a recap — built "
        "from your own misses. Part one: people, things, and how they're "
        "described.", pause=P_SECTION)

# ═══ 1. A and an stay ════════════════════════════════════════════════════════
ep.narr("The miss that comes back most: a or an dropped when a describing word "
        "follows. Listen — the small word stays:", pause=800, chapter="A and an stay")
ep.ro("o rochie mică, un pulover larg, o masă verde", "f", SLOW, 2400)
for s in pick.take(with_article, 10):
    ep.drill(s["cue"], s["answer"], s["g"])

# ═══ 2. The ending follows the word ══════════════════════════════════════════
ep.narr("Next: the ending of a describing word follows its word — for her, and "
        "for more than one. Listen — one, then more:", pause=800,
        chapter="The ending follows the word")
ep.ro("un ochi negru, ochi negri — o casă mică, case mici — un scaun verde, scaune verzi",
      "m", SLOW, 3000)
ep.narr("And for her, with the her-words:", pause=P_SHORT)
ep.ro("un băiat scund, o fată scundă — un frate blond, o soră blondă", "f", SLOW, 2600)
for s in pick.take(short_form, 14):
    ep.drill(s["cue"], s["answer"], s["g"])

# ═══ 3. Whole sentences ══════════════════════════════════════════════════════
ep.narr("Now whole sentences you've missed, from across Lesson 7. Take your "
        "time — the app waits.", pause=P_SECTION, chapter="Whole sentences")
for s in pick.take(sentence, 22):
    ep.drill(s["cue"], s["answer"], s["g"])

# ═══ 4. How people really say it — now as ordinary speech ════════════════════
ep.narr("And the shop and street phrases from the how-people-say-it parts, as "
        "ordinary speech now.", pause=P_SECTION, chapter="Everyday phrases")
for cue, ans, v in [
    ("What would you like? A shop assistant, politely.", "Ce doriți?", "f"),
    ("I'd like a sweater.", "Aș vrea un pulover.", "m"),
    ("What does it come to?", "Cât face?", "f"),
    ("Here you are. Politely.", "Poftiți.", "m"),
    ("What does he look like?", "Cum arată?", "f"),
    ("I don't need bread. The short way.", "N-am nevoie de pâine.", "m"),
    ("How old are you? Politely.", "Câți ani aveți?", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Cold open again ══════════════════════════════════════════════════════
ep.narr("The two friends again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 6. Close ════════════════════════════════════════════════════════════════
ep.narr("Part one of the recap. Part two: the verbs, time and prices.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=[])
