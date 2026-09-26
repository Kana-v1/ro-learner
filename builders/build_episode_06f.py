"""
Episode 06F — "Familia noastră" (Lecția 6 "În familie", memory-first, part 6)

The last of Lecția 6: bogat, sărac, scund, slab, elev, membru — and the
chapter's own synthesis text, "Familia noastră", by which point every word of
the chapter is taught. Adjective forms follow the book: "familie bogată",
"Mama este scundă, dar frumoasă", "Fiica … este elevă". Also the contrast
with Lecția 5: short about a person (scund) is not short about a thing (scurt).

Two book words are handled in the spoken layer instead of being drilled:
fecior (son) is Moldovan and old-fashioned — in Bucharest it is fiu, or just
băiatul meu — and noroc (luck) is used as "Cheers!", not as a greeting.

Scene: showing someone a family photo and describing each person — the
natural home for rich, poor, short, thin.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["bogat", "sărac", "scund", "slab", "elev", "membru"]
GLUE = {"Sanda / Radu": "names", "ca": "like, as — in 'ca mama lui'"}

ep = Episode(number=6, lesson=6, part="f", title="Familia noastră",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea F)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Aceasta e familia mea."),
    ("dana",  "Și acesta cine e?"),
    ("radu",  "Fiul meu. E elev."),
    ("dana",  "E slab!"),
    ("radu",  "Da, e slab, dar sănătos. Și e scund, ca mama lui."),
    ("dana",  "Și unchiul tău?"),
    ("radu",  "Unchiul meu e bogat. Noi nu suntem bogați, dar suntem bine."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A family photo, the last of the family words, and at the end the "
        "chapter's own text. Mostly you, out loud.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("bogat", "rich", "bogat", "m",
            teach_ro="Unchiul meu e bogat.", teach_en="My uncle is rich.")
ep.new_item("sărac", "poor", "sărac", "m",
            teach_ro="El nu e sărac.", teach_en="He isn't poor.")
ep.new_item("scund", "short — about a person", "scund", "m",
            teach_ro="Fiul meu e scund.", teach_en="My son is short.")
ep.new_item("slab", "thin", "slab", "m",
            teach_ro="E slab, dar sănătos.", teach_en="He's thin, but healthy.")
ep.new_item("elev", "a pupil, a schoolboy", "un elev", "f",
            teach_ro="Fiul meu e elev.", teach_en="My son is a pupil.")
ep.new_item("membru", "a member", "un membru", "f",
            teach_ro="Familia mea are membri harnici.",
            teach_en="My family has hardworking members.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("thin", "slab", "m"), ("a member", "un membru", "f"), ("rich", "bogat", "m"),
                    ("a pupil", "un elev", "f"), ("poor", "sărac", "m"),
                    ("short, about a person", "scund", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Short and short ══════════════════════════════════════════════════════
ep.narr("Two words for short. About a person, the new one; about a thing, the "
        "one from the clothes. Listen:", pause=800, chapter="Two kinds of short")
ep.ro("un băiat scund, o fustă scurtă", "m", SLOW, 1800)
ep.narr("A short boy, a short skirt. The new words agree like any other: the "
        "book's own example —", pause=P_SHORT)
ep.teach("Mama mea e scundă, dar frumoasă.", "My mother is short, but pretty.", "m")
ep.teach("O familie bogată.", "A rich family.", "f")
ep.teach("Fiica ei e elevă.", "Her daughter is a pupil.", "m")

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v, extra in [
    ("My uncle is rich.", "Unchiul meu e bogat.", "m", {}),
    ("We are not rich.", "Noi nu suntem bogați.", "f", {}),
    ("He isn't poor.", "El nu e sărac.", "m", {}),
    ("My son is short and thin.", "Fiul meu e scund și slab.", "m", {}),
    ("My mother is short, but pretty.", "Mama mea e scundă, dar frumoasă.", "m",
     {"accept": ["Mama e scundă, dar frumoasă."]}),
    ("My son is a pupil.", "Fiul meu e elev.", "f", {}),
    ("Her daughter is a pupil.", "Fiica ei e elevă.", "m", {}),
    ("A rich family.", "O familie bogată.", "f", {}),
    ("A short boy, a short skirt.", "Un băiat scund, o fustă scurtă.", "m", {}),
    ("My family has hardworking members.", "Familia mea are membri harnici.", "f", {}),
    ("He's thin, but healthy.", "E slab, dar sănătos.", "f", {}),
    ("We are fine.", "Suntem bine.", "m", {}),
    ("His wife is young and clever.", "Soția lui e tânără și deșteaptă.", "f", {}),
    ("Our grandparents are old, but healthy.", "Bunicii noștri sunt bătrâni, dar sănătoși.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book has a second word for son. It is "
        "Moldovan and old-fashioned; in Bucharest you won't need it. What "
        "people say instead — listen:", pause=800, chapter="How people really say it")
ep.ro("băiatul meu, fata mea", "m", SLOW, 1600)
ep.narr("My boy, my girl — meaning my son, my daughter. And the chapter's word "
        "for luck, said as a toast — listen:", pause=P_SHORT)
ep.ro("Noroc!", "m", NORMAL, 1200)
ep.narr("Cheers! In Moldova it is also a hello; in Romania only the toast, or "
        "good luck. And to be lucky — listen:", pause=P_SHORT)
ep.ro("Am noroc.", "f", SLOW, 1400)
ep.narr("I'm lucky.", pause=P_SECTION)

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. Text — the chapter's own passage ═════════════════════════════════════
ep.narr("Now the chapter's own text, whole. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Aceasta este familia noastră. Eu am părinți, un frate, surori și bunici.",
    "Părinții mei sunt medici, fratele meu este student.",
    "Bunicii noștri sunt bătrâni, dar sănătoși.",
    "Bunicul este scund. Tatăl meu este tânăr.",
    "Avem o familie mare și rude cu prenumele Dan, Daniela, Dorin, Dana, Dumitru.",
    "Apartamentul nostru este bun.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The photo again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lesson 6 across its six parts. You can say who is in your "
        "family, whose they are, and what they are like.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the whole family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
