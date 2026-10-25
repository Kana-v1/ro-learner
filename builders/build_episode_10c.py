"""
Episode 10C — "Toate produsele" (Lecția 10 "După cumpărături", memory-first, part 3)

Lecția 10's third grammar point, "Adjectivul tot": tot, toată, toți, toate —
with the noun after it in its the-form (toți copiii, toate produsele, toată
ziua, tot timpul). Five chapter nouns and adjectives to carry it: produs,
marfă, calitate, cumpărător, necesar. Book models: "Toată marfa este de
calitate? — Nu toată marfa este de calitate", "Toți managerii sunt
punctuali? — Nu, nu toți managerii sunt punctuali", "Toate bomboanele sunt
scumpe", "a examina marfa", "a verifica prețul, calitatea".

Rule in the 09A style; the one new thing said is that the noun after all
keeps its the-form — like the noun before my in 07C.

Scene: a shop owner showing off his new shop — all the products, all the
goods, all the customers — the word all repeats because that's boasting.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["tot", "produs", "marfă", "calitate", "cumpărător", "necesar"]
GLUE = {"mulțumiți": "pleased, satisfied", "tot ce": "everything that — a chunk"}

ep = Episode(number=10, lesson=10, part="c", title="Toate produsele",
             source="Limba care ne unește, nivelul I — Lecția 10 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Iată magazinul meu. Toate produsele sunt de calitate."),
    ("dana", "Și toată marfa e nouă?"),
    ("radu", "Da, toată. Și toți cumpărătorii sunt mulțumiți."),
    ("dana", "Toate prețurile sunt convenabile?"),
    ("radu", "Nu toate. Dar tot ce e necesar e aici."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A shop owner showing off. One small word that changes four ways — all "
        "— and the words of a shop.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("tot", "all — before a his-word", "tot", "m",
            teach_ro="tot timpul", teach_en="all the time")
ep.new_item("produs", "a product", "un produs", "f",
            teach_ro="un produs, două produse", teach_en="one product, two products")
ep.new_item("marfă", "goods — on sale", "marfă", "m",
            teach_ro="Marfa e nouă.", teach_en="The goods are new.")
ep.new_item("calitate", "quality", "calitate", "f",
            teach_ro="Produse de calitate.", teach_en="Quality products.")
ep.new_item("cumpărător", "a customer", "un cumpărător", "m",
            teach_ro="Cumpărătorul examinează marfa.", teach_en="The customer looks over the goods.")
ep.new_item("necesar", "necessary", "necesar", "f",
            teach_ro="Pâinea e necesară.", teach_en="Bread is necessary.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("quality", "calitate", "m"), ("all, before a his-word", "tot", "f"),
                    ("a customer", "un cumpărător", "m"), ("goods", "marfă", "f"),
                    ("necessary", "necesar", "m"), ("a product", "un produs", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. All ══════════════════════════════════════════════════════════════════
ep.narr("All changes like a describing word. Listen — the time, the day, the "
        "children, the products:", pause=800, chapter="All")
ep.ro("tot timpul, toată ziua, toți copiii, toate produsele", "m", SLOW, 2600)
ep.narr("And the word after it keeps its the-form — the children, not "
        "children. Like the word before my.", pause=P_SHORT)
for cue, ans, v in [("all day", "toată ziua", "f"), ("all the time", "tot timpul", "m"),
                    ("all the children", "toți copiii", "f"), ("all the products", "toate produsele", "m"),
                    ("all the customers", "toți cumpărătorii", "f"), ("all the goods", "toată marfa", "m"),
                    ("not all", "nu toți", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("All the products are quality products.", "Toate produsele sunt de calitate.", "m", {}),
    ("Are all the goods new?", "Toată marfa e nouă?", "f", {}),
    ("Not all managers are punctual.", "Nu toți managerii sunt punctuali.", "m", {}),
    ("The customer looks over the goods.", "Cumpărătorul examinează marfa.", "f", {}),
    ("I check the price and the quality.", "Verific prețul și calitatea.", "m", {}),
    ("I study all day.", "Studiez toată ziua.", "f", {}),
    ("All the customers are here.", "Toți cumpărătorii sunt aici.", "m", {}),
    ("Everything that's necessary is here.", "Tot ce e necesar e aici.", "f", {}),
    ("Are all the prices reasonable? — Not all.", "Toate prețurile sunt convenabile? — Nu toate.", "m", {}),
    ("Quality goods at a good price.", "Marfă de calitate la un preț bun.", "f", {}),
    ("The bread is necessary, the chocolate isn't.", "Pâinea e necesară, ciocolata nu.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. Him, her, all ════════════════════════════════════════════════════
ep.narr("The describing words of this lesson, with all. Say the whole phrase.",
        pause=P_SECTION, chapter="Him, her, all")
for cue, ans, v in [
    ("all the products are expensive", "toate produsele sunt scumpe", "m"),
    ("all the goods are cheap", "toată marfa e ieftină", "f"),
    ("all the customers are friendly", "toți cumpărătorii sunt amabili", "m"),
    ("all the prices are reasonable", "toate prețurile sunt convenabile", "f"),
    ("all the chocolate is delicious", "toată ciocolata e delicioasă", "m"),
    ("all day at the shop", "toată ziua la magazin", "f"),
    ("I'll take all the boxes.", "Iau toate cutiile.", "m"),
    ("We find out all the prices.", "Aflăm toate prețurile.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. All the time, said about someone who's always "
        "doing something — you'll hear it constantly. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Lucrează tot timpul.", "f", SLOW, 1600)
ep.narr("He works all the time. And people say goods for what's in a shop far "
        "less than products; the book's word is mostly for traders.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=10)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The shop owner again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("All, in four forms — and the words of a shop.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("10", []))
