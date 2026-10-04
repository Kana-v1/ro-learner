"""
Episode 07D — "Câți ani are?" (Lecția 7 "Portrete", memory-first, part 4)

Seven new items: the numbers one to five (unu, doi, trei, patru, cinci), an
(year), and câți (how many). Numbers come as a run, which is why seven is
within the budget here — five of them are one memorised sequence. Forms follow
the book's table ("1 – unu, una; 2 – doi, două") and its pronoun box ("Câți
băieți sunt aici? Câte fete sunt acolo?"); age is the book's "Câți ani are
copilul lor?" — literally how many years he has, so it moves like a avea.

Scene: registering children at a nursery. The clerk has to ask every parent
how many children and how old each one is — so the counting repeats because
it is her job, and small children's ages stay inside one to five.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["unu", "doi", "trei", "patru", "cinci", "an", "câți"]
GLUE = {"Andrei / Mihai / Ana": "names"}

ep = Episode(number=7, lesson=7, part="d", title="Câți ani are?",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună ziua. Câți copii aveți?"),
    ("radu", "Trei. Doi băieți și o fată."),
    ("dana", "Câți ani are fata?"),
    ("radu", "Ana are un an."),
    ("dana", "Și băieții?"),
    ("radu", "Andrei are trei ani, Mihai are cinci."),
    ("dana", "Deci trei copii: un an, trei ani și cinci ani."),
    ("radu", "Da. Mulțumesc."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Registering children at a nursery: how many, and how old. Numbers one "
        "to five, and how to ask.", pause=P_SECTION)

# ═══ 1. Seven items — introduced then recalled at once ═══════════════════════
ep.narr("One to five first — a run you say in one breath — then year, and how "
        "many.", pause=800, chapter="New words")
ep.new_item("unu", "one — counting", "unu", "m",
            teach_ro="unu, doi, trei", teach_en="one, two, three")
ep.new_item("doi", "two", "doi", "f",
            teach_ro="doi băieți", teach_en="two boys")
ep.new_item("trei", "three", "trei", "m",
            teach_ro="trei copii", teach_en="three children")
ep.new_item("patru", "four", "patru", "f",
            teach_ro="Apartamentul are patru camere.", teach_en="The flat has four rooms.")
ep.new_item("cinci", "five", "cinci", "m",
            teach_ro="Mihai are cinci ani.", teach_en="Mihai is five.")
ep.new_item("an", "a year", "un an", "f",
            teach_ro="Ana are un an.", teach_en="Ana is one.")
ep.new_item("câți", "how many — before a his-word: boys, years", "câți", "m",
            teach_ro="Câți copii aveți?", teach_en="How many children do you have?")

ep.narr("Count with her, one to five.", pause=P_SHORT)
ep.drill("One to five.", "unu, doi, trei, patru, cinci", "f")
ep.narr("Mixed, just the word.", pause=800)
for cue, ans, v in [("four", "patru", "m"), ("a year", "un an", "f"), ("two", "doi", "m"),
                    ("five", "cinci", "f"), ("how many", "câți", "m"), ("three", "trei", "f"),
                    ("one, counting", "unu", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. How old ══════════════════════════════════════════════════════════════
ep.narr("Age is like need from the last episode: you have years. How old is "
        "he — literally, how many years does he have. Listen:", pause=800,
        chapter="How old")
ep.example(None, "Câți ani are? Are trei ani.", "m", 1800)
ep.example(None, "Fiica mea are un an. Fiul meu are cinci ani.", "f", 1800)
for cue, ans, v in [
    ("He's three.", "Are trei ani.", "m"),
    ("She's one.", "Are un an.", "f"),
    ("My son is five.", "Fiul meu are cinci ani.", "m"),
    ("How old is he?", "Câți ani are?", "f"),
    ("How old are you? To a child.", "Câți ani ai?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. Two for her ══════════════════════════════════════════════════════════
ep.narr("One and two change for a her-word, the way the word for a does. And "
        "how many changes too. Listen — boys, then girls:", pause=800,
        chapter="For her")
ep.example(None, "un băiat, o fată; doi băieți, două fete", "m", 2200)
ep.example(None, "Câți băieți? Câte fete?", "f", 1800)
for cue, ans, v in [
    ("two boys", "doi băieți", "m"), ("two girls", "două fete", "f"),
    ("two brothers", "doi frați", "m"), ("two sisters", "două surori", "f"),
    ("How many boys?", "Câți băieți?", "m"), ("How many girls?", "Câte fete?", "f"),
    ("How many rooms?", "Câte camere?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("How many children do you have? Politely.", "Câți copii aveți?", "f"),
    ("We have three children: two boys and a girl.", "Avem trei copii: doi băieți și o fată.", "m"),
    ("How old is your son? Politely.", "Câți ani are fiul dumneavoastră?", "f"),
    ("I have two sisters.", "Am două surori.", "m"),
    ("The flat has four rooms.", "Apartamentul are patru camere.", "f"),
    ("How many rooms? — Five.", "Câte camere? — Cinci.", "m"),
    ("How many boys are here?", "Câți băieți sunt aici?", "f"),
    ("My daughter is one.", "Fiica mea are un an.", "m"),
    ("I have two brothers.", "Am doi frați.", "f"),
    ("Andrei is three, Mihai is five.", "Andrei are trei ani, Mihai are cinci ani.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. To a child, or a friend, how old are you is the "
        "short form you drilled. To an adult you don't know, the polite one — "
        "and, as in English, it's a personal question. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Câți ani aveți?", "f", SLOW, 1600)
ep.drill("How old are you? Politely.", "Câți ani aveți?", "m")

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The nursery again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("One to five, and how old. Next time, six to ten.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
