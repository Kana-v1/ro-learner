"""
Episode 06C — "Numele meu" (Lecția 6 "În familie", memory-first, part 3)

Six new items — nume, prenume, soț, soție, fiu, fiică — and the first half of
the possessive: "my" and "your" in the singular (meu/mea, tău/ta), plus the
polite dumneavoastră. The possessive comes after the noun, and the noun keeps
its "the" ending: fratele meu, sora mea. Modelled on the book's own drills:
"Fratele tău este inginer? — Nu, fratele meu este economist."

Scene: a registration desk. The clerk has to ask everyone the same things —
your name, your first name, your family — so the possessive repeats because
it is the clerk's job, not because the script needs it.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["nume", "prenume", "soț", "soție", "fiu", "fiică"]
GLUE = {"Sanda / Radu / Popescu": "names", "vă rog": "please — a fixed chunk"}

ep = Episode(number=6, lesson=6, part="c", title="Numele meu",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Bună ziua! Numele dumneavoastră, vă rog?"),
    ("dana",  "Popescu. Prenumele meu e Sanda."),
    ("radu",  "Aveți familie?"),
    ("dana",  "Da. Soțul meu e aici. El e medic."),
    ("radu",  "Și copii?"),
    ("dana",  "Am un fiu și o fiică."),
    ("radu",  "Fiul dumneavoastră e acasă?"),
    ("dana",  "Da. Iar fiica mea e la școală."),
    ("radu",  "Mulțumesc, doamnă Popescu."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A registration desk: a name, a first name, a family. Six new words, "
        "and how to say my and your. Mostly you, out loud.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six words, one at a time. Say each back before we move on.",
        pause=800, chapter="Six words")
ep.new_item("nume", "a name", "un nume", "m",
            teach_ro="Numele meu e Popescu.", teach_en="My name is Popescu.")
ep.new_item("prenume", "a first name", "un prenume", "f",
            teach_ro="Prenumele meu e Sanda.", teach_en="My first name is Sanda.")
ep.narr("On a form, the first of those means your surname, the second your "
        "first name.", pause=P_SHORT)
ep.new_item("soț", "a husband", "un soț", "f",
            teach_ro="Soțul meu e medic.", teach_en="My husband is a doctor.")
ep.new_item("soție", "a wife", "o soție", "m",
            teach_ro="Soția mea e profesoară.", teach_en="My wife is a teacher.")
ep.new_item("fiu", "a son", "un fiu", "f",
            teach_ro="Fiul meu e acasă.", teach_en="My son is at home.")
ep.new_item("fiică", "a daughter", "o fiică", "f",
            teach_ro="Fiica mea e la școală.", teach_en="My daughter is at school.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("a wife", "o soție", "m"), ("a first name", "un prenume", "f"),
                    ("a son", "un fiu", "f"), ("a husband", "un soț", "f"),
                    ("a daughter", "o fiică", "f"), ("a name", "un nume", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Grammar — my and your ════════════════════════════════════════════════
ep.narr("Now my and your. They come after the word, and the word keeps its "
        "'the' ending. Listen:", pause=800, chapter="My and your")
ep.ro("fratele meu, sora mea", "m", NORMAL, 1600)
ep.narr("That was: my brother, my sister. One form for a masculine word, one "
        "for a feminine one. Your, to a friend — listen:", pause=P_SHORT)
ep.ro("fratele tău, sora ta", "m", NORMAL, 1600)
ep.narr("Your brother, your sister. In sentences:", pause=P_SHORT)
ep.teach("Fratele tău e inginer?", "Is your brother an engineer?", "f")
ep.teach("Nu, fratele meu e economist.", "No, my brother is an economist.", "m")
ep.teach("Soția ta e aici?", "Is your wife here?", "f")
ep.narr("And when you are being polite, one word covers every case, and it "
        "never changes. Listen:", pause=P_SHORT)
ep.ro("numele dumneavoastră, soția dumneavoastră", "m", NORMAL, 1800)
ep.narr("Your name, your wife — said politely.", pause=P_SECTION)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v, extra in [
    ("My name is Popescu.", "Numele meu e Popescu.", "f", {}),
    ("My first name is Sanda.", "Prenumele meu e Sanda.", "f", {}),
    ("My husband is a doctor.", "Soțul meu e medic.", "f", {}),
    ("My wife is a teacher.", "Soția mea e profesoară.", "m", {}),
    ("My son is at home.", "Fiul meu e acasă.", "f", {}),
    ("My daughter is at school.", "Fiica mea e la școală.", "f", {}),
    ("I have a son and a daughter.", "Am un fiu și o fiică.", "f", {}),
    ("Is your brother an engineer? — to a friend", "Fratele tău e inginer?", "f", {}),
    ("No, my brother is an economist.", "Nu, fratele meu e economist.", "m", {}),
    ("Your sister is a doctor. — to a friend", "Sora ta e medic.", "m", {}),
    ("Is your father a doctor? — to a friend", "Tatăl tău e medic?", "f",
     {"almost": ["Tata tău e medic?"]}),
    ("My mother is a teacher.", "Mama mea e profesoară.", "m",
     {"accept": ["Mama e profesoară."]}),
    ("Your first name, please? — politely", "Prenumele dumneavoastră, vă rog?", "m", {}),
    ("Do you have a husband? — to a friend", "Ai soț?", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Nobody asks for your name like a form does. "
        "Casually, to someone your age — listen:", pause=800,
        chapter="How people really say it")
ep.ro("Cum te cheamă?", "f", SLOW, 1400)
ep.narr("And politely, to a stranger or someone older:", pause=P_SHORT)
ep.ro("Cum vă numiți?", "m", SLOW, 1400)
ep.narr("Both mean what's your name. And with close family, my is often left "
        "out altogether. This simply means my mum is at home:", pause=P_SHORT)
ep.ro("Mama e acasă.", "f", SLOW, 1400)
ep.narr("The possessive is there when you need to be clear whose.",
        pause=P_SECTION)

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Numele meu e Popescu. Prenumele meu e Sanda.",
    "Soțul meu e medic.",
    "Am un fiu și o fiică.",
    "Fiul meu e acasă. Fiica mea e la școală.",
]
for line in TEXT:
    ep.ro(line, "f", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "f", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The desk again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("My and your, in the singular. Next time: more than one — my parents, "
        "my relatives — and our.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's part three of the family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
