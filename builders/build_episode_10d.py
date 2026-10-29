"""
Episode 10D — "O cutie de bomboane" (Lecția 10 "După cumpărături", memory-first, part 4)

Six chapter items for groceries: zahăr, făină, bomboană, băutură,
cumpărături, and kilogram (from the chapter's own price structure, "Cât costă
un kilogram de făină?"). The point: after an amount — a kilo, a box — the
thing follows de and stays bare, as after nevoie de in 07C (un kilogram de
zahăr, o cutie de bomboane). Taught in the 09A rule style.

The dialogue is the book's own shopping exchange from its synthesis text
("Cât costă zahărul? — 5 lei. — E de calitate? … — La ce preț e făina? — 3
lei. — Vreau și o cutie de bomboane. — Poftim. 15 lei."), with the sugar
from Romania rather than Moldova.

Scene: buying groceries at a counter — the price and quality of each thing,
one after another.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["zahăr", "făină", "bomboană", "băutură", "kilogram", "cumpărături"]
GLUE = {"rece": "cold — in 'o băutură rece'"}

ep = Episode(number=10, lesson=10, part="d", title="O cutie de bomboane",
             source="Limba care ne unește, nivelul I — Lecția 10 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Cât costă zahărul?"),
    ("dana", "Cinci lei."),
    ("radu", "E de calitate?"),
    ("dana", "Da, e din România."),
    ("radu", "La ce preț e făina?"),
    ("dana", "Trei lei."),
    ("radu", "Vreau și o cutie de bomboane."),
    ("dana", "Poftim. Cincisprezece lei."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The book's own shopping scene: sugar, flour, a box of sweets. Six "
        "words for the grocery list.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("zahăr", "sugar", "zahăr", "m",
            teach_ro="Zahărul e dulce.", teach_en="Sugar is sweet.")
ep.new_item("făină", "flour", "făină", "f",
            teach_ro="Făina e ieftină.", teach_en="Flour is cheap.")
ep.new_item("kilogram", "a kilo", "un kilogram", "m",
            teach_ro="un kilogram de făină", teach_en="a kilo of flour")
ep.new_item("bomboană", "a sweet, a chocolate — one piece", "o bomboană", "f",
            teach_ro="o cutie de bomboane", teach_en="a box of chocolates")
ep.new_item("băutură", "a drink", "o băutură", "m",
            teach_ro="Ce băutură preferi?", teach_en="What drink do you prefer?")
ep.new_item("cumpărături", "shopping — the things you buy", "cumpărături", "f",
            teach_ro="Sunt la cumpărături.", teach_en="I'm out shopping.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("flour", "făină", "m"), ("a drink", "o băutură", "f"), ("sugar", "zahăr", "m"),
                    ("a kilo", "un kilogram", "f"), ("shopping", "cumpărături", "m"),
                    ("a sweet", "o bomboană", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. An amount of something ═══════════════════════════════════════════════
ep.narr("After an amount, the thing comes after of, and stays bare. Listen:",
        pause=800, chapter="An amount of something")
ep.ro("un kilogram de zahăr, o cutie de bomboane, două kilograme de făină", "m", SLOW, 2800)
ep.narr("The same as after need, from the shop episode. Build them.", pause=P_SHORT)
for cue, ans, v in [("a kilo of sugar", "un kilogram de zahăr", "f"),
                    ("a box of sweets", "o cutie de bomboane", "m"),
                    ("two kilos of flour", "două kilograme de făină", "f"),
                    ("a can of beer", "o cutie de bere", "m"),
                    ("a kilo of sweets", "un kilogram de bomboane", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("How much is the sugar?", "Cât costă zahărul?", "m", {}),
    ("Is it good quality? — Yes, it's from Romania.", "E de calitate? — Da, e din România.", "f", {}),
    ("At what price is the flour? — Three lei.", "La ce preț e făina? — Trei lei.", "m", {}),
    ("I want a box of sweets too.", "Vreau și o cutie de bomboane.", "f", {}),
    ("The sweets are delicious.", "Bomboanele sunt delicioase.", "m", {}),
    ("All the sweets are expensive.", "Toate bomboanele sunt scumpe.", "f", {}),
    ("What drink do you prefer? To a friend.", "Ce băutură preferi?", "m", {}),
    ("I prefer a cold drink.", "Prefer o băutură rece.", "f", {}),
    ("I'm out shopping.", "Sunt la cumpărături.", "m", {}),
    ("I need two kilos of sugar.", "Am nevoie de două kilograme de zahăr.", "f", {}),
    ("Flour is cheap, sugar is expensive.", "Făina e ieftină, zahărul e scump.", "m", {}),
    ("How much is a kilo of flour?", "Cât costă un kilogram de făină?", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. Lesson 10's verbs ═══════════════════════════════════════════════════
ep.narr("Lesson 10's verbs, with the shopping. Build the one asked for.",
        pause=P_SECTION, chapter="Lesson 10's verbs")
for cue, ans, v in [
    ("I'll take a kilo of sugar.", "Iau un kilogram de zahăr.", "m"),
    ("She gives fifteen lei.", "Ea dă cincisprezece lei.", "f"),
    ("We find out the price.", "Aflăm prețul.", "m"),
    ("They go into the shop.", "Ei intră în magazin.", "f"),
    ("You prefer sweets. To a friend.", "Preferi bomboanele.", "m"),
    ("We take all the boxes.", "Luăm toate cutiile.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. At the counter nobody says the whole of kilo; "
        "listen:", pause=800, chapter="How people really say it")
ep.ro("Un kil de zahăr. Jumătate de kil de făină.", "f", SLOW, 2200)
ep.narr("A kilo of sugar, half a kilo of flour. And the seller's here you are "
        "was the friendly one; in a smart shop you'd hear the polite one. "
        "Listen:", pause=P_SHORT)
ep.ro("Poftim. Poftiți.", "m", SLOW, 1600)
ep.narr("Friendly, then polite.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=9)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The counter again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("The grocery list, and how much of each.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("10", []))
