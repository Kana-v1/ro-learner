"""
Episode 06D — "Rudele mele" (Lecția 6 "În familie", memory-first, part 4)

Six new items — părinte, rudă, unchi, mătușă, nepot, tanti — and the rest of
"my" (the plurals: părinții mei, rudele mele) plus "our" (familia noastră,
bunicul nostru). Forms from the book's own table: meu mei mea mele, nostru
noștri noastră noastre.

Scene: showing a colleague family photos. "Who is this? — My uncle. And this?
— My aunt." Pointing at people in a photo repeats "this is my…" naturally,
and brings back the demonstratives from Lecția 3.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["părinte", "rudă", "unchi", "mătușă", "nepot", "tanti"]
GLUE = {"Sanda / Radu / Ana": "names"}

ep = Episode(number=6, lesson=6, part="d", title="Rudele mele",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Cine sunt aceștia?"),
    ("dana",  "Aceștia sunt părinții mei."),
    ("radu",  "Și aceasta?"),
    ("dana",  "Aceasta e mătușa mea, tanti Ana. Iar acesta e unchiul meu."),
    ("radu",  "Și copilul?"),
    ("dana",  "E nepotul meu."),
    ("radu",  "O familie frumoasă!"),
    ("dana",  "Da. Aceasta e familia noastră."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Family photos, and who is who. Six more people, my for more than one, "
        "and our. Mostly you, out loud.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("părinte", "a parent", "un părinte", "f",
            teach_ro="Aceștia sunt părinții mei.", teach_en="These are my parents.")
ep.new_item("rudă", "a relative", "o rudă", "m",
            teach_ro="Noi avem rude.", teach_en="We have relatives.")
ep.new_item("unchi", "an uncle", "un unchi", "f",
            teach_ro="Acesta e unchiul meu.", teach_en="This is my uncle.")
ep.new_item("mătușă", "an aunt", "o mătușă", "f",
            teach_ro="Aceasta e mătușa mea.", teach_en="This is my aunt.")
ep.new_item("nepot", "a nephew, or a grandson", "un nepot", "f",
            teach_ro="Copilul e nepotul meu.", teach_en="The child is my nephew.")
ep.narr("And the word a child puts before an aunt's name — or any older woman "
        "they know well:", pause=P_SHORT)
ep.new_item("tanti", "auntie, before a name", "tanti", "f",
            teach_ro="Aceasta e tanti Ana.", teach_en="This is Auntie Ana.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("an uncle", "un unchi", "f"), ("a relative", "o rudă", "m"),
                    ("auntie, before a name", "tanti", "f"), ("a parent", "un părinte", "f"),
                    ("a nephew", "un nepot", "f"), ("an aunt", "o mătușă", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Grammar — my for more than one, and our ══════════════════════════════
ep.narr("Last time, my for one person. With more than one, it changes again. "
        "Listen:", pause=800, chapter="My, plural, and our")
ep.ro("părinții mei, rudele mele", "m", NORMAL, 1600)
ep.narr("My parents, my relatives: one plural for masculine words, one for "
        "feminine. All four forms of my, together:", pause=P_SHORT)
ep.ro("meu, mea, mei, mele", "m", SLOW, 1800)
ep.teach("Aceștia sunt frații mei.", "These are my brothers.", "m")
ep.teach("Acestea sunt surorile mele.", "These are my sisters.", "f")
ep.narr("And our — listen:", pause=P_SHORT)
ep.ro("familia noastră, bunicul nostru", "f", NORMAL, 1600)
ep.narr("Our family, our grandfather.", pause=P_SHORT)
ep.teach("Aceasta e familia noastră.", "This is our family.", "f")
ep.teach("Bunicul nostru e acasă.", "Our grandfather is at home.", "m")
ep.teach("Părinții noștri sunt acasă.", "Our parents are at home.", "f")
ep.narr("The drill sets the endings; no need to memorise a table.",
        pause=P_SECTION)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v, extra in [
    ("These are my parents.", "Aceștia sunt părinții mei.", "f", {}),
    ("This is my aunt.", "Aceasta e mătușa mea.", "f", {}),
    ("This is my uncle.", "Acesta e unchiul meu.", "m", {}),
    ("The child is my nephew.", "Copilul e nepotul meu.", "f", {}),
    ("This is Auntie Ana.", "Aceasta e tanti Ana.", "f", {}),
    ("We have relatives.", "Avem rude.", "m", {}),
    ("Who are these? — My parents.", "Cine sunt aceștia? Părinții mei.", "m", {}),
    ("My brothers are at home.", "Frații mei sunt acasă.", "m", {}),
    ("My sisters are at school.", "Surorile mele sunt la școală.", "f", {}),
    ("This is our family.", "Aceasta e familia noastră.", "f", {}),
    ("Our grandfather is a doctor.", "Bunicul nostru e medic.", "m", {}),
    ("Our parents are at home.", "Părinții noștri sunt acasă.", "f", {}),
    ("Do you have an uncle? — Yes, I have an uncle.", "Ai un unchi? Da, am un unchi.", "m",
     {"accept": ["Ai unchi? Da, am un unchi."]}),
    ("Is your aunt a teacher? — to a friend", "Mătușa ta e profesoară?", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. That word for auntie is not only for aunts. "
        "Children use it for any older woman the family knows — a neighbour, "
        "a friend's mother. Listen:", pause=800, chapter="How people really say it")
ep.ro("tanti Maria, de la etajul doi", "f", SLOW, 1600)
ep.narr("Auntie Maria from the second floor — very likely no relation at all. "
        "And the word for nephew also means grandson; the family around it "
        "tells you which.", pause=P_SECTION)

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Aceasta e familia noastră.",
    "Aceștia sunt părinții mei. Aceasta e mătușa mea.",
    "Acesta e unchiul meu. Copilul e nepotul meu.",
    "Noi avem rude.",
]
for line in TEXT:
    ep.ro(line, "f", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "f", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The photos again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("My, all four ways, and our. Next time: his, her and their — and what "
        "people are like: young, old, healthy, clever.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's part four of the family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
