"""
Episode 10A — "Iau o bere" (Lecția 10 "După cumpărături", memory-first, part 1)

Lecția 10's first grammar point: the irregular verbs a lua and a da
("Prezentul indicativ al verbelor neregulate"): iau, iei, ia, luăm, luați,
iau; dau, dai, dă, dăm, dați, dau. Both are learnt whole — and, like stau from
08D, their they-form sounds like I, not like she. Taught in the 09A rule
style: Romanian voice for every form, the pattern heard first, one short
sentence, then built.

Also the chapter's communicative intention "Cum precizăm prețul unei mărfi"
— the book's "Cât costă…?", "La ce preț e…?" — with four of its words: preț,
scump, ieftin, cutie. Plus two idioms from the book's own models that make
these verbs earn their keep: a lua masa (have a meal — "El ia masa la ora
cinci") and a da examen (take an exam — "Eu dau examen la matematică").

Scene: buying at a kiosk — what will you have, how much, too expensive, here's
the money — which is what take and give are for.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["iau", "dau", "preț", "scump", "ieftin", "cutie"]
GLUE = {"mai ieftin": "cheaper — a chunk",
        "Vă dau": "I give you — politely, a chunk",
        "restul": "the change"}

ep = Episode(number=10, lesson=10, part="a", title="Iau o bere",
             source="Limba care ne unește, nivelul I — Lecția 10 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună dimineața! Ce doriți?"),
    ("radu", "Iau o ciocolată. Cât costă?"),
    ("dana", "Doisprezece lei."),
    ("radu", "E scump! Aveți ceva mai ieftin?"),
    ("dana", "Da, ciocolata aceasta e la un preț bun: șase lei."),
    ("radu", "Bine, iau ciocolata aceasta. Și o cutie de bere. Vă dau zece lei."),
    ("dana", "Poftiți restul."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A kiosk in the morning. Lesson 10 is shopping: what you take, what you "
        "give, and what it costs.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("iau", "I take — and, ordering, I'll have", "iau", "m",
            teach_ro="Iau o bere.", teach_en="I'll have a beer.")
ep.new_item("dau", "I give", "dau", "f",
            teach_ro="Dau zece lei.", teach_en="I give ten lei.")
ep.new_item("preț", "a price", "un preț", "m",
            teach_ro="La un preț bun.", teach_en="At a good price.")
ep.new_item("scump", "expensive", "scump", "f",
            teach_ro="E scump!", teach_en="It's expensive!")
ep.new_item("ieftin", "cheap", "ieftin", "m",
            teach_ro="Pâinea e ieftină.", teach_en="The bread is cheap.")
ep.new_item("cutie", "a box — or a can", "o cutie", "f",
            teach_ro="o cutie de bere", teach_en="a can of beer")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("cheap", "ieftin", "m"), ("I give", "dau", "f"), ("a price", "un preț", "m"),
                    ("I take", "iau", "f"), ("a box", "o cutie", "m"), ("expensive", "scump", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Take and give ════════════════════════════════════════════════════════
ep.narr("Take and give don't follow a pattern; each is learnt whole. Listen to "
        "take — I, you, she:", pause=800, chapter="Take and give")
ep.ro("iau, iei, ia", "m", SLOW, 1800)
ep.narr("Then we, you all, they:", pause=P_SHORT)
ep.ro("luăm, luați, iau", "m", SLOW, 1800)
ep.narr("They sounds like I — as with live. Give does the same. Listen:", pause=P_SHORT)
ep.ro("dau, dai, dă — dăm, dați, dau", "f", SLOW, 2400)
for cue, ans, v in [("you take — to a friend", "iei", "f"), ("she takes", "ia", "m"),
                    ("we take", "luăm", "f"), ("they take", "ei iau", "m"),
                    ("you give — to a friend", "dai", "f"), ("he gives", "dă", "m"),
                    ("you all give", "dați", "f"), ("they give", "ei dau", "m")]:
    ep.drill(cue, ans, v)

ep.narr("Two everyday uses from the book. Take a meal means have lunch or "
        "dinner; give an exam means take one. Listen:", pause=800)
ep.ro("Luăm masa la unu. Azi dau examen.", "f", SLOW, 2200)
for cue, ans, v in [("We have lunch at one.", "Luăm masa la unu.", "m"),
                    ("Today I'm taking an exam.", "Azi dau examen.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. The price ════════════════════════════════════════════════════════════
ep.narr("Asking the price: the question you know, and the book's second one — "
        "at what price. Listen:", pause=800, chapter="The price")
ep.ro("Cât costă? La ce preț e berea?", "m", SLOW, 2200)
ep.narr("Cheap and expensive agree, like every describing word. Listen:", pause=P_SHORT)
ep.ro("un produs scump, o bere ieftină", "f", SLOW, 2000)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'll have a beer.", "Iau o bere.", "m", {}),
    ("What will you have? To a friend.", "Ce iei?", "f", {}),
    ("It's expensive! Do you have something cheaper? Politely.", "E scump! Aveți ceva mai ieftin?", "m", {}),
    ("At what price is the beer?", "La ce preț e berea?", "f", {}),
    ("The bread is cheap.", "Pâinea e ieftină.", "m", {}),
    ("I'll take this chocolate.", "Iau ciocolata aceasta.", "f", {}),
    ("She takes a can of beer.", "Ea ia o cutie de bere.", "m", {}),
    ("I'll give you ten lei. Politely.", "Vă dau zece lei.", "f", {}),
    ("We'll take two beers.", "Luăm două beri.", "m", {}),
    ("A good price.", "Un preț bun.", "f", {}),
    ("The ice cream is expensive.", "Înghețata e scumpă.", "m", {}),
    ("Here's your change. Politely.", "Poftiți restul.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. At a market stall, the book's way of asking a "
        "price is still the one you hear — literally, how do you give it. "
        "Listen:", pause=800, chapter="How people really say it")
ep.ro("Cum dați pâinea?", "f", SLOW, 1600)
ep.drill("How much is the bread? At a market stall.", "Cum dați pâinea?", "m")

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=9)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The kiosk again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Take, give, and the price.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("10", []))
