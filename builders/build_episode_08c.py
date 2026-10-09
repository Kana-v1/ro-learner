"""
Episode 08C — "Cât e ceasul?" (Lecția 8 "La studii", memory-first, part 3)

The chapter's communicative intention, "Cum precizăm timpul": asking and
telling the time. Six items — ora, fix, jumătate, sfert, fără, and întârzii
(the chapter's a întârzia, in the form a learner says: I'm late). Times follow
the book's own list ("Este ora nouă fix", "E ora nouă și jumătate", "E ora
douăsprezece și un sfert", "E ora optsprezece fără un sfert", "E ora opt fără
zece minute"), and its two questions, "Ce oră e?" and "Cât e ceasul?". The
numbers come from 07D–07F; ora is a her-word, so two o'clock is ora două.

Scene: a student late for class stopping a stranger to ask the time — the
question and the answer are the whole exchange, and the time decides
whether she's late.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["ora", "fix", "jumătate", "sfert", "fără", "întârzii"]
GLUE = {"Cât e ceasul?": "What time is it? — the book's question, as a chunk"}

ep = Episode(number=8, lesson=8, part="c", title="Cât e ceasul?",
             source="Limba care ne unește, nivelul I — Lecția 8 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Scuzați, cât e ceasul?"),
    ("radu",  "E ora nouă fără un sfert."),
    ("elena", "Fără un sfert? Întârzii!"),
    ("radu",  "La ce oră aveți curs?"),
    ("elena", "La nouă fix."),
    ("radu",  "Aveți un sfert de oră."),
    ("elena", "Mulțumesc!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "elena", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A student, late for class, stopping a stranger. Asking the time, and "
        "telling it.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("ora", "the hour — as in it's nine o'clock", "ora", "m",
            teach_ro="E ora nouă.", teach_en="It's nine o'clock.")
ep.new_item("fix", "exactly, sharp — of a time", "fix", "f",
            teach_ro="E ora nouă fix.", teach_en="It's nine sharp.")
ep.new_item("jumătate", "half", "jumătate", "m",
            teach_ro="E ora zece și jumătate.", teach_en="It's half past ten.")
ep.new_item("sfert", "a quarter", "un sfert", "f",
            teach_ro="E ora zece și un sfert.", teach_en="It's a quarter past ten.")
ep.new_item("fără", "without — and, in a time, to", "fără", "m",
            teach_ro="E ora opt fără un sfert.", teach_en="It's a quarter to eight.")
ep.new_item("întârzii", "I'm late", "întârzii", "f",
            teach_ro="Întârzii la curs!", teach_en="I'm late for class!")

ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("half", "jumătate", "m"), ("I'm late", "întârzii", "f"), ("a quarter", "un sfert", "m"),
                    ("sharp, of a time", "fix", "f"), ("to, in a time", "fără", "m"),
                    ("the hour", "ora", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Telling the time ═════════════════════════════════════════════════════
ep.narr("The pattern: it's, the hour, the number. Past is and; to is without. "
        "Listen:", pause=800, chapter="Telling the time")
ep.example(None, "E ora nouă. E ora nouă și un sfert. E ora nouă și jumătate.", "m", 2400)
ep.example(None, "E ora zece fără un sfert.", "f", 1800)
ep.narr("And minutes, the same way:", pause=P_SHORT)
ep.example(None, "E ora nouă și cinci. E ora opt fără zece.", "m", 2200)
ep.narr("The hour is a her-word, so two o'clock uses two's her-form. And one "
        "o'clock is the counting one. Listen:", pause=P_SHORT)
ep.example(None, "E ora două. E ora unu.", "f", 1800)
ep.narr("The question — two ways, both from the book. Listen:", pause=P_SHORT)
ep.example(None, "Cât e ceasul? Ce oră e?", "m", 1800)
for cue, ans, v, extra in [
    ("What time is it?", "Cât e ceasul?", "f", {"accept": ["Ce oră e?"]}),
    ("It's nine sharp.", "E ora nouă fix.", "m", {}),
    ("It's half past ten.", "E ora zece și jumătate.", "f", {}),
    ("It's a quarter past twelve.", "E ora douăsprezece și un sfert.", "m", {}),
    ("It's a quarter to eight.", "E ora opt fără un sfert.", "f", {}),
    ("It's two o'clock.", "E ora două.", "m", {}),
    ("It's one o'clock.", "E ora unu.", "f", {}),
    ("It's five past nine.", "E ora nouă și cinci.", "m", {}),
    ("It's ten to eight.", "E ora opt fără zece.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3. Late ═════════════════════════════════════════════════════════════════
ep.narr("Late moves like the verbs from the last two episodes. Listen — I'm "
        "late, he's late, we're late:", pause=800, chapter="Late")
ep.example(None, "întârzii, întârzie, întârziem", "m", 2000)
for cue, ans, v in [("he's late", "întârzie", "f"), ("we're late", "întârziem", "m"),
                    ("I'm not late.", "Nu întârzii.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Excuse me, what time is it?", "Scuzați, cât e ceasul?", "m", {}),
    ("At what time? — At nine.", "La ce oră? — La nouă.", "f", {}),
    ("I have class at nine sharp.", "Am curs la nouă fix.", "m", {}),
    ("A quarter to? I'm late!", "Fără un sfert? Întârzii!", "f", {}),
    ("You have a quarter of an hour. Politely.", "Aveți un sfert de oră.", "m", {}),
    ("The teacher is late.", "Profesorul întârzie.", "f", {}),
    ("We have half an hour.", "Avem o jumătate de oră.", "m", {"accept": ["Avem jumătate de oră."]}),
    ("It's a quarter to nine, and I'm late.", "E ora nouă fără un sfert și întârzii.", "f", {}),
    ("Today we have class at ten.", "Azi avem curs la zece.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Of the two questions, the first — how much is "
        "the clock — is the everyday one. And the answer usually skips the "
        "hour word. Listen:", pause=800, chapter="How people really say it")
ep.ro("Cât e ceasul? — Nouă și jumătate.", "f", SLOW, 2000)
ep.narr("Just the time, nothing else.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The late student again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the time — and whether you're late.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("8", []))
