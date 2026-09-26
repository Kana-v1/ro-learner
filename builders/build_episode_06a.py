"""
Episode 06A — "Ai frați?" (Lecția 6 "În familie", memory-first, part 1)

Lecția 6 is the family, and the verb the whole lesson runs on: a avea, to have.
This first part takes four core people — mamă, tată, frate, soră — and the
singular of a avea: am, ai, are. Possession is exactly where 'to have' repeats
itself naturally ("Ai un frate? — Am un frate și o soră"), so the verb drills
itself against the family words.

Three things are new in how this is built, and every later episode follows:
  1. The production pause is proportional to the answer (recall_pause) — a short
     reply gets a short silence, a whole sentence gets several seconds.
  2. The narrator never speaks Romanian. Grammar is set up in English and then
     spoken by the Romanian voice (ep.example / ep.ro / ep.teach).
  3. No between-episodes task at the close — just a sign-off.

The plural of a avea (avem, aveți, au) and more of the family are 06B onward.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["mamă", "tată", "frate", "soră"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=6, lesson=6, part="a", title="Ai frați?",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună, Radu! Ai frați?"),
    ("radu",  "Da. Am un frate și o soră."),
    ("dana",  "Și mama, tata? Ce sunt?"),
    ("radu",  "Mama e profesoară. Tata e medic."),
    ("radu",  "Dar tu, Sanda? Ai frați?"),
    ("dana",  "Am o soră. Ea e medic, de asemenea."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two people asking about each other's families. Four words for the "
        "people — mother, father, brother, sister — and one verb, to have. Most "
        "of this is you answering out loud, and the silence now stretches to fit "
        "the answer.", pause=P_SECTION)

# ═══ 1. Four people — introduced then recalled at once ═══════════════════════
ep.narr("The four people, one at a time. Say each back before we move on.",
        pause=800, chapter="Four people")
ep.new_item("mamă", "mother", "mamă", "f")
ep.new_item("tată", "father", "tată", "m")
ep.new_item("frate", "brother", "frate", "m")
ep.new_item("soră", "sister", "soră", "f")

ep.narr("With 'the' on the end — the way you actually say them, mum and dad, "
        "the brother, the sister. Listen:", pause=P_SHORT)
ep.ro("mama, tata, fratele, sora", "f", NORMAL, 1600)

ep.narr("The four together, mixed. Just the word.", pause=800)
for cue, ans, v in [("sister", "soră", "f"), ("father", "tată", "m"),
                    ("mother", "mamă", "f"), ("brother", "frate", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Grammar — a avea, to have (singular) ═════════════════════════════════
ep.narr("Now the verb the whole lesson runs on: to have. Three forms for now — "
        "listen:", pause=800, chapter="a avea: to have")
ep.ro("am, ai, are", "m", NORMAL, 1600)
ep.narr("That was: I have, you have, he or she has. Each one in a sentence:",
        pause=P_SHORT)
ep.teach("Eu am un frate.", "I have a brother.", "m")
ep.teach("Tu ai o soră.", "You have a sister.", "f")
ep.teach("Ea are un frate.", "She has a brother.", "f")
ep.narr("In real speech the 'eu', 'tu' drop away — the verb form already says "
        "who. You just say:", pause=P_SHORT)
ep.ro("Am un frate. Ai o soră.", "m", NORMAL, 1600)

# ═══ 3. Drill — asking and answering about family ════════════════════════════
ep.narr("The work. English in, the whole Romanian out loud, then the answer.",
        pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("I have a brother.", "Am un frate.", "m"),
    ("I have a sister.", "Am o soră.", "f"),
    ("Do you have a brother?", "Ai un frate?", "m"),
    ("Do you have a sister?", "Ai o soră?", "f"),
    ("She has a brother.", "Ea are un frate.", "f"),
    ("The mother is a teacher.", "Mama e profesoară.", "f"),
    ("The father is a doctor.", "Tata e medic.", "m"),
    ("I have a brother and a sister.", "Am un frate și o soră.", "m"),
    ("Do you have a sister? — Yes, I have a sister.",
     "Ai o soră? Da, am o soră.", "f"),
    ("She has a mother and a father.", "Ea are o mamă și un tată.", "f"),
    ("Do you have a brother? — No, but I have a sister.",
     "Ai un frate? Nu, dar am o soră.", "m"),
    ("The sister is a doctor, the brother is a teacher.",
     "Sora e medic, fratele e profesor.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("One real-speech note. The book gives you frate, brother. But this "
        "question — listen —", pause=800, chapter="How people really say it")
ep.ro("Ai frați?", "m", SLOW, 1200)
ep.narr("— literally 'do you have brothers?' is how you ask about brothers and "
        "sisters both. Siblings, in one word. You answer with what you have — a "
        "brother, a sister, or both.", pause=P_SECTION)

# ═══ 5. Review — scheduled from earlier episodes ═════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Am un frate și o soră.",
    "Mama e profesoară. Tata e medic.",
    "Ai frați? Da, am un frate.",
    "Ea are o soră. Sora e medic.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The two of them again. Same recording — notice how much more you "
        "follow.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Four people, and the verb to have in the singular. Next time: we and "
        "you and they have — the plural — and more of the family.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's part one of the family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
