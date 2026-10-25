"""
Episode 10B — "Intrăm?" (Lecția 10 "După cumpărături", memory-first, part 2)

Lecția 10's second grammar point, "verbele de conjugarea I cu unele forme
specifice": aflu, intru (and umblu, in 10E) — a-group verbs whose I-form
ends in a short -u (aflu, afli, află, aflăm, aflați, află). With prefer, a
plain a-group verb, as the contrast. Three of the chapter's adjectives:
delicios, amabil, convenabil — agreement as in Lecția 7 (delicioasă,
amabilă, convenabilă; plural delicioși/-oase, amabili/-e, convenabili/-e).
Book models: "Eu aflu o noutate", "Eu intru în magazin", "Eu prefer
ciocolata", "Noi preferăm magazinele mici".

Rule section in the 09A style: Romanian voice for every form, pattern first,
one sentence, built at once.

Scene: two friends finding a new shop near home and going in — find out,
go in, what do you prefer.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["prefer", "aflu", "intru", "delicios", "amabil", "convenabil"]
GLUE = {"că": "that — in 'aflu că…'",
        "vânzătoarea": "the shop assistant (her)"}

ep = Episode(number=10, lesson=10, part="b", title="Intrăm?",
             source="Limba care ne unește, nivelul I — Lecția 10 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Aflu că e un magazin nou, aproape."),
    ("radu", "Intrăm?"),
    ("dana", "Intrăm! Prețurile sunt convenabile."),
    ("radu", "Ce preferi: ciocolată sau înghețată?"),
    ("dana", "Prefer înghețata. E delicioasă."),
    ("radu", "Și vânzătoarea e amabilă."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A new shop near home. Finding out, going in, and what you prefer.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("prefer", "I prefer", "prefer", "m",
            teach_ro="Prefer înghețata.", teach_en="I prefer ice cream.")
ep.new_item("aflu", "I find out", "aflu", "f",
            teach_ro="Aflu prețul.", teach_en="I find out the price.")
ep.new_item("intru", "I go in", "intru", "m",
            teach_ro="Intru în magazin.", teach_en="I go into the shop.")
ep.new_item("delicios", "delicious", "delicios", "f",
            teach_ro="Înghețata e delicioasă.", teach_en="The ice cream is delicious.")
ep.new_item("amabil", "friendly, kind — of staff, strangers", "amabil", "m",
            teach_ro="Vânzătorul e amabil.", teach_en="The shop assistant is friendly.")
ep.new_item("convenabil", "affordable, reasonable — of a price", "convenabil", "f",
            teach_ro="Prețul e convenabil.", teach_en="The price is reasonable.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I go in", "intru", "m"), ("delicious", "delicios", "f"), ("I prefer", "prefer", "m"),
                    ("reasonable, of a price", "convenabil", "f"), ("I find out", "aflu", "m"),
                    ("friendly", "amabil", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. A short extra sound ══════════════════════════════════════════════════
ep.narr("Listen to I for find out and go in — then for prefer:", pause=800,
        chapter="A short extra sound")
ep.ro("aflu, intru — prefer", "m", SLOW, 1800)
ep.narr("The first two end with a short extra sound, only in the I-form. Every "
        "other form goes as usual. Listen:", pause=P_SHORT)
ep.ro("aflu, afli, află — aflăm, aflați, află", "f", SLOW, 2400)
for cue, ans, v in [("you find out — to a friend", "afli", "m"), ("she goes in", "intră", "f"),
                    ("we go in", "intrăm", "m"), ("you all find out", "aflați", "f"),
                    ("he prefers", "preferă", "m"), ("you prefer — to a friend", "preferi", "f"),
                    ("we prefer", "preferăm", "m"), ("they go in", "ei intră", "f")]:
    ep.drill(cue, ans, v)

ep.narr("And the three describing words, for her and for more than one. Listen:",
        pause=800)
ep.ro("delicios, delicioasă — amabil, amabilă — prețuri convenabile", "m", SLOW, 2600)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I find out that there's a new shop nearby.", "Aflu că e un magazin nou aproape.", "m",
     {"accept": ["Aflu că e un magazin nou, aproape."]}),
    ("Shall we go in?", "Intrăm?", "f", {}),
    ("I go into the shop.", "Intru în magazin.", "m", {}),
    ("What do you prefer? To a friend.", "Ce preferi?", "f", {}),
    ("I prefer ice cream.", "Prefer înghețata.", "m", {"accept": ["Prefer înghețată."]}),
    ("The ice cream is delicious.", "Înghețata e delicioasă.", "f", {}),
    ("The shop assistant is friendly — a woman.", "Vânzătoarea e amabilă.", "m", {}),
    ("The prices are reasonable.", "Prețurile sunt convenabile.", "f", {}),
    ("He goes into the office.", "El intră în birou.", "m", {}),
    ("We find out the price.", "Aflăm prețul.", "f", {}),
    ("They prefer small shops.", "Ei preferă magazinele mici.", "m", {}),
    ("A friendly seller, a delicious chocolate.", "Un vânzător amabil, o ciocolată delicioasă.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. Lesson 10's verbs so far ═══════════════════════════════════════════
ep.narr("Take and give, mixed in with this episode's three. Build the one asked "
        "for.", pause=P_SECTION, chapter="Lesson 10's verbs")
for cue, ans, v in [
    ("you take — to a friend", "iei", "m"), ("she finds out", "află", "f"), ("they give", "ei dau", "m"),
    ("I go in", "intru", "f"), ("we take", "luăm", "m"), ("you all prefer", "preferați", "f"),
    ("he gives", "dă", "m"), ("I find out", "aflu", "f"), ("they take", "ei iau", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. For news you've picked up, people often say "
        "I heard instead of I find out. Listen:", pause=800, chapter="How people really say it")
ep.ro("Am auzit că e un magazin nou.", "f", SLOW, 1800)
ep.narr("I heard there's a new shop. Just to recognise for now.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=10)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The new shop again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("Find out, go in, prefer.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("10", []))
