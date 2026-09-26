"""
Episode 03B — "Noi suntem împreună (B)" (Lecția 3, second half)

The second half of Lecția 3. Where 3A pointed at things and named them, this
one places them: the prepositions pe (on) and lângă (next to), the linker de
(sală de curs), împreună (together), and the room-and-study words the first
half held back — the wall, the board, the picture, the bench, the building.

Scene: being walked round the classroom while someone says where everything
is. "Pe masă e... lângă fereastră e..." is what a person actually says
describing a room, so the repetition of pe and lângă is the realism, not an
exercise. The chapter's own synthesis text does exactly this, so it closes the
episode in full — by now every word in it has been taught across 3A and 3B.

The design goal is the same as 3A: every new word inside three or four whole
sentences, in different frames (name it, locate it, ask where it is, drill),
never as a bare word.

Continuity: acesta / aceasta and cine / ce from 3A are now ordinary speech,
used without re-teaching. Episode 1-2 spoken forms continue (e, domnu',
Poftiți, Mulțumesc). 3A's own new spoken items (Ce-i asta?) are now used, not
re-explained.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# The locating half of Lecția 3's VOCABULAR block, in the book's order, plus
# the prepositions and connectors this half is built on.
REQUIRED = [
    "pe", "lângă", "de", "împreună",
    "perete", "tablă", "tablou", "bancă",
    "sală", "clădire", "cretă", "burete",
    "curs", "lecție", "floare",
]

GLUE = {
    "frumos": "nice, lovely",
    "mare": "big",
    "bun": "good",
    "Mihai / Radu": "names",
}

ep = Episode(number=3, lesson=3, part="b", title="Noi suntem împreună (B)",
             source="Limba care ne unește, nivelul I — Lecția 3 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Deci, aceasta e sala de curs. Suntem împreună aici, la lecție."),
    ("radu",  "Frumos! E o clădire mare."),
    ("dana",  "Pe perete e o tablă, iar lângă tablă e un tablou."),
    ("radu",  "Dar pe masă? Ce e pe masă?"),
    ("dana",  "Pe masă e o floare. Lângă masă e o bancă."),
    ("radu",  "Și pe bancă? Ce e pe bancă?"),
    ("dana",  "Pe bancă e un burete și o cretă."),
    ("radu",  "Un curs bun!"),
    ("dana",  "Mulțumesc, domnu' Radu. Poftiți, lângă fereastră e un scaun."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The same room as last time, but now someone is saying where "
        "everything is — on the wall, next to the table, on the bench. Two "
        "words carry it: on, and next to. Everything else you can already "
        "name.", pause=P_SECTION)

# ═══ 1. Vocabulary — the room ════════════════════════════════════════════════
ep.narr("The room and what holds it up, each inside a sentence.",
        pause=800, chapter="This is...")
for r, e, v in [
    ("Aceasta e o sală de curs.", "This is a classroom.", "f"),
    ("Aceasta e o clădire.", "This is a building.", "f"),
    ("Acesta e un perete.", "This is a wall.", "m"),
    ("Aceasta e o tablă.", "This is a blackboard.", "f"),
    ("Acesta e un tablou.", "This is a picture.", "m"),
    ("Aceasta e o bancă.", "This is a bench.", "f"),
    ("Aceasta e o floare.", "This is a flower.", "f"),
    ("Aceasta e o cretă.", "This is chalk.", "f"),
    ("Acesta e un burete.", "This is a sponge.", "m"),
    ("Acesta e un curs.", "This is a course.", "m"),
    ("Aceasta e o lecție.", "This is a lesson.", "f"),
]:
    ep.teach(r, e, v)

# ═══ 2. Grammar — pe, lângă, de, împreună ════════════════════════════════════
ep.narr("Now the words that place them. Pe — on, on top of a surface.",
        pause=800, chapter="pe and lângă")
for r in ["Pe masă e o floare.", "Pe bancă e un caiet.", "Pe perete e un tablou."]:
    ep.ro(r, "m", NORMAL, 1200)
ep.narr("Lângă — next to, beside.")
for r in ["Lângă masă e un scaun.", "Lângă tablă e un perete.",
          "Lângă fereastră e o bancă."]:
    ep.ro(r, "m", NORMAL, 1200)
ep.narr("Pe is contact — resting on the surface. Lângă is alongside, not "
        "touching. Pe masă, the book is on the table. Lângă masă, the chair is "
        "beside it.", pause=600)

ep.narr("And where is a thing? Ask with ce, and answer with pe or lângă.",
        pause=600)
for r, e in [("Ce e pe masă? O floare.", "What is on the table? A flower."),
             ("Ce e lângă fereastră? O bancă.",
              "What is next to the window? A bench."),
             ("Ce e pe bancă? Un caiet și un creion.",
              "What is on the bench? A notebook and a pencil.")]:
    ep.teach(r, e, "f")

ep.narr("Two smaller words. De links two nouns into one idea: sală de curs, a "
        "room for a course. And împreună — together, the name of the whole "
        "chapter.", pause=600, chapter="de and împreună")
for r, e in [("o sală de curs", "a course room / classroom"),
             ("Suntem împreună la lecție.", "We are together at the lesson."),
             ("Noi suntem împreună.", "We are together.")]:
    ep.teach(r, e, "m" if "sală" in r else "f")

# ═══ 3. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How it really sounds. Two things this time.", pause=800,
        chapter="How people really say it")

ep.narr("First, the dropped L again — the one from lesson one, now on this "
        "chapter's things. The book writes dicționarul, manualul, scaunul. "
        "What comes out is:")
for r in ["dicționaru'", "manualu'", "scaunu'", "caietu'"]:
    ep.ro(r, "m", SLOW, 1000)
ep.narr("Same rule as domnu', birou'. Feminine words keep their ending — masa, "
        "not mas'.", pause=600)

ep.narr("Second, the room itself. Sală de curs is right for a course or a "
        "lecture hall, which is where we are. But in a school it is a clasă.")
for r, e in [("o clasă", "a classroom (in a school)")]:
    ep.teach(r, e, "f")
ep.narr("Pick by the building. Ours is a sală de curs.", pause=P_SECTION)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time — where the thing is, "
        "not just its name.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("This is a classroom.", "Aceasta e o sală de curs.", "f"),
    ("This is a building.", "Aceasta e o clădire.", "f"),
    ("On the wall there is a blackboard.", "Pe perete e o tablă.", "f"),
    ("Next to the blackboard there is a picture.",
     "Lângă tablă e un tablou.", "m"),
    ("On the table there is a flower.", "Pe masă e o floare.", "f"),
    ("Next to the table there is a bench.", "Lângă masă e o bancă.", "f"),
    ("On the bench there is a sponge and chalk.",
     "Pe bancă e un burete și o cretă.", "m"),
    ("What is on the table? — A flower.", "Ce e pe masă? O floare.", "f"),
    ("What is next to the window? — A bench.",
     "Ce e lângă fereastră? O bancă.", "f"),
    ("On the wall there is a picture.", "Pe perete e un tablou.", "m"),
    ("Next to the door there is a chair.", "Lângă ușă e un scaun.", "m"),
    ("This is a lesson.", "Aceasta e o lecție.", "f"),
    ("This is a good course.", "Acesta e un curs bun.", "m"),
    ("This is chalk, and this is a sponge.",
     "Aceasta e o cretă, iar acesta e un burete.", "f"),
    ("We are together at the lesson.", "Suntem împreună la lecție.", "f"),
    ("On the bench there is a book and a notebook.",
     "Pe bancă e o carte și un caiet.", "f"),
    ("Next to the school there is a building.",
     "Lângă școală e o clădire.", "f"),
    ("We are together.", "Noi suntem împreună.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Review of episode 2 and 3A ═══════════════════════════════════════════
ep.review([
    ("What is this? — A dictionary.", "Ce e acesta? Un dicționar.", "m"),
    ("This is a book, and this is a notebook.",
     "Aceasta e o carte, iar acesta e un caiet.", "f"),
    ("Who is this? — A course student.", "Cine e acesta? Un cursant.", "m"),
    ("He is at the theatre, she is at the doctor's.",
     "El e la teatru, ea e la medic.", "m"),
    ("What do you do for a living?", "Cu ce vă ocupați?", "f"),
    ("Nice to meet you.", "Îmi pare bine.", "f"),
])

# ═══ 6. Text — the chapter's own passage ═════════════════════════════════════
ep.narr("Now the chapter's own text, whole. Everything in it you have met "
        "across both halves. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Suntem împreună la lecție. Aceasta este o sală de curs.",
    "Aici este un profesor și acolo este un cursant.",
    "Acesta este un profesor, iar acesta-i un cursant.",
    "Cine este aceasta? Aceasta este Elena. Ea este la lecție.",
    "Ce este acesta? Acesta este un tablou.",
    "Acesta este un perete? Nu, acesta este un burete. Este pe masă.",
    "Aceasta este o masă. Lângă masă este un scaun.",
    "Aceasta e o tablă. Iar aceasta-i o carte.",
    "Ce este lângă fereastră? O bancă.",
    "Ce este pe bancă? Pe bancă sunt: un caiet, un creion, un dicționar, "
    "un manual, un stilou.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("The chapter's proverb. Unde-s doi, puterea crește — where there are "
        "two, the strength grows. The grammar in it is a way off; take it "
        "whole, it fits the lesson's name.", pause=800)
ep.ro("Unde-s doi, puterea crește.", "m", SLOW, 1400)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The walk round the room again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lecția 3. You can name the room and say where everything "
        "in it is.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: describe the room you are in. What is on the table, "
        "what is next to the window. Pe, lângă, and the words are all yours "
        "now. Pe curând!", pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("3", []))
