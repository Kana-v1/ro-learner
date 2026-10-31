"""
Episode 10S — "Recapitulare (6–10), partea II" (consolidation after Lecția 10)

The second recap part: verbs, time and prices from Lecții 8–10, drilled from
the learner's own misses (90 of the 152 still wrong at the end of Lecția 10
came from these three lessons). One by-ear reminder of the four kinds of verb
met so far — plain (ascult), with the extra piece (lucrez), the short-u
I-form (aflu), and the ones learnt whole (stau, iau, dau) — then the misses:
verb forms first, then whole sentences.

Closes as 05R did, with a whole self-introduction — Radu's, a character's,
said line by line from English cues — using only what the block has taught:
name, where from, where he lives, his work, his studies, his family, his
day, what he prefers.

Drill list read from state.json at build time (recap_kit); getting one right
here clears it on the next ingest.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW
from recap_kit import misses, Picker, words, sentence

REQUIRED = ["învăț", "sfert", "repet",                 # L8
            "lucrez", "translator", "studiez",         # L9
            "iau", "intru", "librărie", "scump"]       # L10
GLUE = {"Cluj": "a city in Transylvania"}

ep = Episode(number=10, lesson=10, part="s", title="Recapitulare (6–10), partea II",
             source="Limba care ne unește, nivelul I — Recapitulare, lecțiile 6–10",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Unde lucrezi acum?"),
    ("radu", "Lucrez ca translator. Și studiez chimia la facultate."),
    ("dana", "Și cum e ziua ta?"),
    ("radu", "Iau trenul la opt fără un sfert. Lucrez toată ziua."),
    ("dana", "Și după serviciu?"),
    ("radu", "Intru în librărie, iau o carte și repet lecția acasă."),
    ("dana", "Ești harnic! Dar cărțile nu sunt scumpe?"),
    ("radu", "Ba da, sunt scumpe! Dar prefer cărțile, nu înghețata."),
]

pick = Picker(misses({"08", "09", "10"}))

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Part two of the recap: doing things — the verbs — and time and money. "
        "All from your own misses, then an introduction you build yourself.",
        pause=P_SECTION)

# ═══ 1. Four kinds of verb ═══════════════════════════════════════════════════
ep.narr("Four kinds of verb so far. Listen — I, then you, for each:", pause=800,
        chapter="Four kinds of verb")
ep.ro("ascult, asculți — lucrez, lucrezi — aflu, afli — iau, iei", "m", SLOW, 3000)
ep.narr("Plain; with the extra piece; a short extra sound in I only; and the "
        "few learnt whole. Which kind a verb is, its I-form tells you. Now the "
        "forms you've missed.", pause=800)
for s in pick.take(lambda s: words(s) <= 2, 16):
    ep.drill(s["cue"], s["answer"], s["g"])

# ═══ 2. Whole sentences ══════════════════════════════════════════════════════
ep.narr("Whole sentences you've missed, from Lessons 8, 9 and 10. Take your "
        "time.", pause=P_SECTION, chapter="Whole sentences")
for s in pick.take(sentence, 24):
    ep.drill(s["cue"], s["answer"], s["g"])

# ═══ 3. An introduction ══════════════════════════════════════════════════════
ep.narr("Last, a whole introduction — Radu's. You say it, one line at a time, "
        "using everything from Lessons 6 to 10.", pause=P_SECTION, chapter="An introduction")
INTRO = [
    ("My surname is Popescu, my first name is Radu.", "Numele meu e Popescu, prenumele meu e Radu.", "m"),
    ("I'm from Cluj.", "Sunt din Cluj.", "m"),
    ("I live near the university.", "Stau lângă universitate.", "m"),
    ("I work as a translator.", "Lucrez ca translator.", "m"),
    ("And I study chemistry at the faculty.", "Și studiez chimia la facultate.", "m"),
    ("I have a sister and two brothers.", "Am o soră și doi frați.", "m"),
    ("My sister is tall and fair-haired.", "Sora mea e înaltă și blondă.", "m"),
    ("I take the train at a quarter to eight.", "Iau trenul la opt fără un sfert.", "m"),
    ("I'm learning Romanian: I listen a lot and repeat.", "Învăț limba română: ascult mult și repet.", "m"),
    ("After work I go into the bookshop.", "După serviciu intru în librărie.", "m"),
    ("I prefer chocolate, but it's expensive.", "Prefer ciocolata, dar e scumpă.", "m"),
]
for cue, ans, v in INTRO:
    ep.drill(cue, ans, v)
ep.narr("And the whole of it, at speed. Listen:", pause=800)
for _, ans, v in INTRO:
    ep.ro(ans, v, NORMAL, 350)

# ═══ 4. Cold open again ══════════════════════════════════════════════════════
ep.narr("Radu's day again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That's Lessons 6 to 10: family and looks, clothes and numbers, your "
        "first verbs, work, and shopping.", pause=600)

# ═══ 5. Close ════════════════════════════════════════════════════════════════
ep.narr("The end of the second block. Next time, Lesson 11.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=[])
