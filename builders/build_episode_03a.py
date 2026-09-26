"""
Episode 03A — "Noi suntem împreună (A)" (Lecția 3, first half)

Lecția 3 is 32 items — too many to consolidate in one sitting with the
repetition this course wants, so it splits along the chapter's own two grammar
points. This half is the first: the demonstratives acesta / aceasta, the
question words cine / ce, and the classroom objects you point at up close.
Half B takes the prepositions pe / lângă and the room-and-study words.

Scene: the first class. A newcomer is shown who is who and what is what.
"Cine e acesta? Ce e aceasta?" is a question a person genuinely asks over and
over on a first day, so the pedagogical repetition sounds like someone doing
exactly what you do in a new room — pointing and naming.

The design goal for this episode: every new word appears in three or four whole
sentences, in different frames (point-and-name, question-and-answer, contrast
pair, then the drill), never as a bare dictionary word. Nobody produces
isolated words in their own language; the drill produces sentences.

Continuity: the dialogue uses episodes 1-2's spoken forms as ordinary speech —
e (not este), domnu', Îmi pare bine, Poftiți, Mulțumesc, Cu plăcere, deci, and
a role stated with no article (E cursant). This episode's own spoken items
(Ce-i asta?, cum se spune) are taught here and become ordinary speech in 3B/4.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# The identifying half of Lecția 3's VOCABULAR block, in the book's order,
# plus the demonstratives and question words this half is built on.
REQUIRED = [
    "acesta", "aceasta", "cine", "ce",
    "cursant",
    "carte", "caiet", "creion", "pix", "stilou", "radieră",
    "dicționar", "manual",
    "masă", "scaun", "ușă", "fereastră",
]

GLUE = {
    "Mihai / Elena / Radu": "names",
}

ep = Episode(number=3, lesson=3, part="a", title="Noi suntem împreună (A)",
             source="Limba care ne unește, nivelul I — Lecția 3 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună ziua! Poftiți, domnu' Radu."),
    ("radu",  "Bună ziua! Mulțumesc."),
    ("dana",  "Acesta e Mihai. E cursant."),
    ("radu",  "Îmi pare bine. Dar aceasta? Cine e?"),
    ("dana",  "Aceasta e Elena. E profesoară."),
    ("elena", "Bună! Îmi pare bine."),
    ("radu",  "Ce e acesta? Un dicționar?"),
    ("dana",  "Da, e un dicționar. Iar acesta e un manual."),
    ("radu",  "Și aceasta ce e? O radieră?"),
    ("dana",  "Nu, nu e o radieră. E o carte."),
    ("dana",  "Deci: aici e un caiet, un creion și un pix."),
    ("radu",  "Mulțumesc!"),
    ("dana",  "Cu plăcere."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The first class. Someone new is being shown round — who the people "
        "are, what the things on the desk are. Two questions do all the work: "
        "who is this, and what is this. By the end they will be yours.",
        pause=P_SECTION)

# ═══ 1. Vocabulary — point and name ══════════════════════════════════════════
ep.narr("The things on a desk. Each one inside a full sentence — this is a X, "
        "that is a Y — never on its own. Say the sentence out loud in the gap.",
        pause=800, chapter="This is...")
for r, e, v in [
    ("Acesta e un dicționar.", "This is a dictionary.", "m"),
    ("Acesta e un manual.", "This is a textbook.", "m"),
    ("Aceasta e o carte.", "This is a book.", "f"),
    ("Acesta e un caiet.", "This is a notebook.", "m"),
    ("Acesta e un creion.", "This is a pencil.", "m"),
    ("Acesta e un pix.", "This is a pen.", "m"),
    ("Acesta e un stilou.", "This is a fountain pen.", "m"),
    ("Aceasta e o radieră.", "This is an eraser.", "f"),
]:
    ep.teach(r, e, v)

ep.narr("And the room itself.", pause=600)
for r, e, v in [
    ("Aceasta e o masă.", "This is a table.", "f"),
    ("Acesta e un scaun.", "This is a chair.", "m"),
    ("Aceasta e o ușă.", "This is a door.", "f"),
    ("Aceasta e o fereastră.", "This is a window.", "f"),
    ("Acesta e un cursant.", "This is a course student.", "m"),
]:
    ep.teach(r, e, v)

# ═══ 2. Same words, second frame ═════════════════════════════════════════════
ep.narr("Now the same things again, but this time here and there, one against "
        "another. Listen for how the words come back inside a different "
        "sentence — that is how you will actually meet them.",
        pause=800, chapter="Here and there")
for r in [
    "Aici e un caiet, iar acolo e un dicționar.",
    "Acesta e un pix, iar aceasta e o radieră.",
    "Aceasta e o carte, iar acesta e un manual.",
    "Aici e o masă, acolo e un scaun.",
    "Aceasta e o ușă, iar aceasta e o fereastră.",
    "Acesta e un creion. Acolo e un stilou.",
]:
    ep.ro(r, "m", NORMAL, 1200)

# ═══ 3. Grammar — acesta / aceasta, cine / ce ════════════════════════════════
ep.narr("Two pairs of little words ran through all of that. First: this.",
        pause=800, chapter="acesta and aceasta")
ep.narr("Acesta for a masculine or neuter thing. Aceasta for a feminine one. "
        "It is the same masculine-neuter-together pattern as un from last time "
        "— acesta goes with un, aceasta goes with o.")
for r in ["Acesta e un creion.", "Acesta e un scaun.", "Acesta e un dicționar."]:
    ep.ro(r, "m", NORMAL, 900)
for r in ["Aceasta e o carte.", "Aceasta e o masă.", "Aceasta e o ușă."]:
    ep.ro(r, "f", NORMAL, 900)

ep.narr("Second pair: the questions they answer. Cine for a person, ce for a "
        "thing. Cine — who. Ce — what.", pause=600, chapter="cine and ce")
for r, e in [("Cine e acesta? Un cursant.", "Who is this? A course student."),
             ("Ce e acesta? Un dicționar.", "What is this? A dictionary."),
             ("Cine e aceasta? Elena.", "Who is this? Elena."),
             ("Ce e aceasta? O carte.", "What is this? A book.")]:
    ep.teach(r, e, "m" if "acesta?" in r else "f")
ep.narr("Cine only for people, ce only for things. Ask ce about a person and "
        "you have asked what they are, not who — occasionally useful, usually "
        "not what you meant.", pause=P_SECTION)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("The part that is not from the book — how this actually sounds in "
        "Bucharest, and the questions the chapter forgot to give you.",
        pause=800, chapter="How people really say it")

ep.narr("The book asks ce este aceasta. Nobody says all of that about a mug on "
        "a table. Este collapses onto the word before it, and aceasta becomes "
        "asta:")
ep.teach("Ce-i asta?", "What's this?", "f")
ep.narr("Ce-i asta. Completely neutral for objects — you will hear it "
        "constantly. For a person, though, asta or ăsta turns familiar, even "
        "dismissive — who's this guy. With someone you have just met, keep "
        "cine e.", pause=600)
ep.teach("Cine e?", "Who is it?", "f")

ep.narr("And the real gap. The chapter teaches you to ask what is this when "
        "the thing is in front of you — but not how to ask for a word you do "
        "not know. These two unblock every class:")
ep.teach("Cum se spune... în română?", "How do you say... in Romanian?", "f")
ep.teach("Ce înseamnă...?", "What does... mean?", "m")
ep.narr("Grammar far beyond this lesson. Take both whole.", pause=600)

ep.narr("Last, two words the book treats as equals but life does not. A pix is "
        "the ballpoint everyone writes with. A stilou is a fountain pen — you "
        "will rarely need it. And the book's radieră is correct, but almost "
        "everyone says gumă.")
for r in ["un pix", "o gumă"]:
    ep.ro(r, "m", SLOW, 1000)
ep.narr("Keep radieră for the drill, because the book uses it. Expect gumă in "
        "the room.", pause=P_SECTION)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Now the work, and it is longer this time. English in, a whole "
        "Romanian sentence out loud, then the answer. Every word you just met, "
        "several times over, never bare.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("This is a dictionary.", "Acesta e un dicționar.", "m"),
    ("This is a textbook.", "Acesta e un manual.", "m"),
    ("This is a dictionary, and this is a textbook.",
     "Acesta e un dicționar, iar acesta e un manual.", "m"),
    ("This is a book.", "Aceasta e o carte.", "f"),
    ("This is a notebook.", "Acesta e un caiet.", "m"),
    ("This is a pen, and this is a notebook.",
     "Acesta e un pix, iar acesta e un caiet.", "m"),
    ("This is a pencil.", "Acesta e un creion.", "m"),
    ("This is a fountain pen.", "Acesta e un stilou.", "m"),
    ("This is an eraser.", "Aceasta e o radieră.", "f"),
    ("This is a pen, and this is an eraser.",
     "Acesta e un pix, iar aceasta e o radieră.", "m"),
    ("This is a table.", "Aceasta e o masă.", "f"),
    ("This is a chair, and this is a table.",
     "Acesta e un scaun, iar aceasta e o masă.", "m"),
    ("This is a door, and this is a window.",
     "Aceasta e o ușă, iar aceasta e o fereastră.", "f"),
    ("What is this? — A pencil.", "Ce e acesta? Un creion.", "m"),
    ("What is this? — A book.", "Ce e aceasta? O carte.", "f"),
    ("Who is this? — A course student.", "Cine e acesta? Un cursant.", "m"),
    ("Is this a dictionary? — No, it's a textbook.",
     "Acesta e un dicționar? Nu, e un manual.", "m"),
    ("Is this a book? — Yes, it's a book.",
     "Aceasta e o carte? Da, e o carte.", "f"),
    ("What's this? — casually.", "Ce-i asta?", "f"),
    ("How do you say 'notebook' in Romanian?",
     "Cum se spune 'notebook' în română?", "f"),
    ("What does 'caiet' mean?", "Ce înseamnă 'caiet'?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 6. Review of episodes 1-2 ═══════════════════════════════════════════════
ep.review([
    ("She is an architect.", "Ea e arhitect.", "f"),
    ("What do you do for a living?", "Cu ce vă ocupați?", "f"),
    ("I'm not an economist, I'm an accountant.",
     "Nu sunt economist, sunt contabil.", "m"),
    ("He is a lawyer, she is a teacher.", "El e jurist, ea e profesoară.", "m"),
    ("Aren't you from the city? — Yes I am.", "Ba da, sunt din oraș.", "m"),
    ("Nice to meet you.", "Îmi pare bine.", "f"),
    ("I am Moldovan — a man speaking.", "Eu sunt moldovean.", "m"),
])

# ═══ 7. A few sentences at speed ═════════════════════════════════════════════
ep.narr("A handful of sentences run together, the way the book's own text "
        "will in the second half. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Bună ziua! Acesta e un cursant. Aceasta e o profesoară.",
    "Ce e acesta? Acesta e un dicționar. Iar acesta e un manual.",
    "Aceasta e o carte. Aici e un caiet, un creion și un pix.",
    "Cine e aceasta? Aceasta e Elena.",
    "Ce e aceasta? O radieră. Iar aceasta e o masă.",
    "Acesta e un scaun. Aceasta e o ușă, iar aceasta e o fereastră.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The first class again. Same recording — only your ear has changed.",
        pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Every question in it was one of two: cine e, ce e. Next time, the "
        "other half — where everything is in the room.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: pick five things near you and name each one out "
        "loud. Acesta e un..., aceasta e o... And when you do not know the "
        "word — cum se spune. Pe curând!", pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("3", []))
