"""
Episode 07G — "Copii cuminți" (Lecția 7 "Portrete", memory-first, part 7)

The last of Lecția 7: four new items — cuminte, față, ajutor, atenție — so
this part has room for the chapter as a whole: its "Generalizăm" models
("Am nevoie de ajutorul tău", "Ei au nevoie de atenția noastră", "Aceasta
este o familie mare", "Câți ani are el?"), a round of every adjective the
chapter taught for him, her and more than one, the synthesis text and the
proverb. cuminte is a two-ending adjective like mare (cuminte / cuminți,
the book's "Ei sunt copii cuminți").

The synthesis text "Portret de bărbat, portret de femeie" is read as an
excerpt: the sentences about the car, garage, firm and stadium use words the
course has not taught and are left out; colegul and nas are the only words
added, as glue.

Scene: parents leaving their children with a babysitter — introducing each
child, what they're like and what they need, which is where cuminte,
atenție and ajutor come up naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["cuminte", "față", "ajutor", "atenție"]
GLUE = {"colegul": "my colleague — in the book's text",
        "nas": "nose — in the book's text",
        "N-aduce anul ce aduce ceasul.": "the chapter's proverb, as a whole"}

ep = Episode(number=7, lesson=7, part="g", title="Copii cuminți",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea G)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Aceștia sunt copiii noștri: Andrei și Mihaela."),
    ("dana", "Sunt cuminți?"),
    ("radu", "Da, sunt copii cuminți. Andrei are zece ani, Mihaela are opt."),
    ("dana", "Au nevoie de ceva?"),
    ("radu", "Mihaela are nevoie de atenție. E mică."),
    ("dana", "Și Andrei?"),
    ("radu", "Atenție: Andrei vrea înghețată. Dar nu acum!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Leaving the children with a babysitter. Four last words of Lesson 7, "
        "then the whole lesson together, and the book's own portrait.",
        pause=P_SECTION)

# ═══ 1. Four words — introduced then recalled at once ════════════════════════
ep.narr("The four, one at a time.", pause=800, chapter="Four words")
ep.new_item("cuminte", "well-behaved, quiet — of a child", "cuminte", "m",
            teach_ro="Copilul e cuminte.", teach_en="The child is well-behaved.")
ep.new_item("față", "a face", "o față", "f",
            teach_ro="Are o față frumoasă.", teach_en="She has a pretty face.")
ep.new_item("ajutor", "help", "ajutor", "m",
            teach_ro="Am nevoie de ajutor.", teach_en="I need help.")
ep.new_item("atenție", "attention — and, alone, watch out", "atenție", "f",
            teach_ro="Mihaela are nevoie de atenție.", teach_en="Mihaela needs attention.")
ep.narr("Said on its own, the last one is a warning. Listen:", pause=P_SHORT)
ep.ro("Atenție!", "m", NORMAL, 1400)
ep.narr("Watch out! The four, mixed.", pause=800)
for cue, ans, v in [("help", "ajutor", "m"), ("a face", "o față", "f"),
                    ("watch out", "atenție", "m"), ("well-behaved, of a child", "cuminte", "f")]:
    ep.recall_word(cue, ans, v)
ep.narr("Well-behaved works like big: the same for her, an i for more than one. "
        "Listen:", pause=P_SHORT)
ep.example(None, "un băiat cuminte, o fată cuminte, copii cuminți", "m", 2200)
for cue, ans, v in [("well-behaved children", "copii cuminți", "f"),
                    ("a well-behaved girl", "o fată cuminte", "m")]:
    ep.drill(cue, ans, v)

# ═══ 2. Help and attention — with whose ══════════════════════════════════════
ep.narr("The book's own sentences. With my, your, our, the word takes its the "
        "form, as my sister did a few episodes ago. Listen:", pause=800, chapter="Your help")
ep.example(None, "Am nevoie de ajutorul tău.", "m", 1800)
ep.example(None, "Ei au nevoie de atenția noastră.", "f", 1800)
for cue, ans, v in [
    ("I need help.", "Am nevoie de ajutor.", "m"),
    ("I need your help. To a friend.", "Am nevoie de ajutorul tău.", "f"),
    ("He doesn't need help.", "El nu are nevoie de ajutor.", "m"),
    ("The children need our attention.", "Copiii au nevoie de atenția noastră.", "f"),
    ("Do you need help? Politely.", "Aveți nevoie de ajutor?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. The lesson together: him, her, more than one ════════════════════════
ep.narr("Now all of Lesson 7's describing words, the way the book sums them up: "
        "him, her, more than one. You'll hear the plain form; say the one asked "
        "for.", pause=P_SECTION, chapter="Lesson 7 together")
for cue, ans, v in [
    ("a small house", "o casă mică", "m"), ("small houses", "case mici", "f"),
    ("a new book", "o carte nouă", "m"), ("new books", "cărți noi", "f"),
    ("a big family", "o familie mare", "m"), ("an old dress", "o rochie veche", "f"),
    ("green chairs", "scaune verzi", "m"), ("a tall woman", "o femeie înaltă", "f"),
    ("long hair", "păr lung", "m"), ("black eyes", "ochi negri", "f"),
    ("well-behaved children", "copii cuminți", "m"), ("a loose blouse", "o bluză largă", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("And whole sentences, from across the lesson.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("This is a big family.", "Aceasta e o familie mare.", "m", {}),
    ("I want a new book.", "Vreau o carte nouă.", "f", {}),
    ("How old is he?", "Câți ani are?", "m", {}),
    ("How many children are here?", "Câți copii sunt aici?", "f", {}),
    ("The children are well-behaved.", "Copiii sunt cuminți.", "m", {}),
    ("She has a pretty face and big eyes.", "Are o față frumoasă și ochi mari.", "f",
     {"accept": ["Are o față frumoasă și ochii mari."]}),
    ("Do you need new textbooks? Politely.", "Aveți nevoie de manuale noi?", "m", {}),
    ("Andrei is ten, Mihaela is eight.", "Andrei are zece ani, Mihaela are opt ani.", "f",
     {"accept": ["Andrei are zece ani, Mihaela are opt."]}),
    ("Watch out, the table is old!", "Atenție, masa e veche!", "m", {}),
    ("What does he need? — Help.", "De ce are nevoie? — De ajutor.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The warning word is what's written on signs and "
        "said in announcements. Said to a person — careful! — people more often "
        "use this. Listen:", pause=800, chapter="How people really say it")
ep.ro("Ai grijă! Aveți grijă!", "f", SLOW, 1800)
ep.narr("To a friend, then politely. Just to recognise for now.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 7. Text — the chapter's own portrait ════════════════════════════════════
ep.narr("Now the chapter's own text, a portrait of a man and his family. Two "
        "words in it are new and you'll understand them from the story: "
        "colleague, at the start, and nose. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Acesta este colegul meu. Numele lui este Victor Dumbravă.",
    "El este inginer. El este înalt și slab. Are ochi negri și păr blond.",
    "El are familie. Familia lui nu este mare.",
    "Aici este casa lui. Este o casă mare și frumoasă.",
    "Iată și soția lui. Ea este înaltă și frumoasă: are nas mic, ochi mari, "
    "părul negru și fața albă.",
    "Ea este o femeie harnică. Ea este profesoară.",
    "Aceștia sunt copiii lor: Radu și Mihaela. Radu are zece ani, iar Mihaela opt ani.",
    "Ei sunt elevi. Ei sunt copii cuminți. Lângă casă este școala lor.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("N-aduce anul ce aduce ceasul.", "f", SLOW, 1600)
ep.narr("What a year doesn't bring, an hour can — things can change in a moment. "
        "Once more:", pause=P_SHORT)
ep.ro("N-aduce anul ce aduce ceasul.", "f", NORMAL, 1400)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The babysitter again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lesson 7 across its seven parts: what you want and need, "
        "what people and things are like, and counting to nineteen.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 7.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
