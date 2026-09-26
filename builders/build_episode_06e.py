"""
Episode 06E — "Bunicul lui" (Lecția 6 "În familie", memory-first, part 5)

Six new items — tânăr, bătrân, sănătos, bolnav, harnic, deștept — and the easy
possessives: his, her, their (lui, ei, lor), which never change. The adjectives
agree with their noun like the Lecția 5 colours; the forms follow the book's
own exercise "fiu deștept, fiică deșteaptă, copii deștepți" and its synthesis
text "Bunicii noștri sunt bătrâni, dar sănătoși". tânăr has an irregular
plural (tineri), taken from the book's "Ei sunt tineri".

Scene: telling a friend about a neighbour's family. Talking about someone
else's relatives is exactly where his, her and their come up again and again,
along with what each person is like.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["tânăr", "bătrân", "sănătos", "bolnav", "harnic", "deștept"]
GLUE = {"Sanda / Radu / Mihai": "names", "vecinul meu": "my neighbour — a chunk",
        "Îmi pare rău": "I'm sorry — a fixed phrase"}

ep = Episode(number=6, lesson=6, part="e", title="Bunicul lui",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Cine e Mihai?"),
    ("dana",  "E vecinul meu. Bunicul lui e bătrân, dar sănătos."),
    ("radu",  "Și soția lui?"),
    ("dana",  "Soția lui e tânără și harnică."),
    ("radu",  "Au copii?"),
    ("dana",  "Da, un fiu. Fiul lor e deștept, dar acum e bolnav."),
    ("radu",  "Îmi pare rău."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A neighbour's family, and what everyone is like. Six describing words, "
        "and his, her and their. Mostly you, out loud.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time, the plain form first.", pause=800,
        chapter="Six words")
ep.new_item("tânăr", "young", "tânăr", "m",
            teach_ro="Fratele lui e tânăr.", teach_en="His brother is young.")
ep.new_item("bătrân", "old — about a person", "bătrân", "m",
            teach_ro="Bunicul lui e bătrân.", teach_en="His grandfather is old.")
ep.new_item("sănătos", "healthy", "sănătos", "m",
            teach_ro="Bunicul e sănătos.", teach_en="The grandfather is healthy.")
ep.new_item("bolnav", "ill", "bolnav", "m",
            teach_ro="Fiul lor e bolnav.", teach_en="Their son is ill.")
ep.new_item("harnic", "hardworking", "harnic", "m",
            teach_ro="Fiul ei e harnic.", teach_en="Her son is hardworking.")
ep.new_item("deștept", "clever", "deștept", "m",
            teach_ro="Copilul e deștept.", teach_en="The child is clever.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans in [("ill", "bolnav"), ("clever", "deștept"), ("young", "tânăr"),
                 ("hardworking", "harnic"), ("old", "bătrân"), ("healthy", "sănătos")]:
    ep.recall_word(cue, ans, "m")

# ═══ 2. Grammar — his, her, their ════════════════════════════════════════════
ep.narr("Now his, her and their. These are the easy ones: they never change, "
        "whatever they belong to. His — listen:", pause=800,
        chapter="His, her, their")
ep.ro("fratele lui, sora lui", "m", NORMAL, 1600)
ep.narr("His brother, his sister — the same word for both. Her:", pause=P_SHORT)
ep.ro("fratele ei, sora ei", "f", NORMAL, 1600)
ep.narr("Her brother, her sister. And their:", pause=P_SHORT)
ep.ro("părinții lor", "m", NORMAL, 1400)
ep.narr("Their parents.", pause=P_SECTION)

# ═══ 3. Agreement, with people ═══════════════════════════════════════════════
ep.narr("The describing words agree, like the colours did. Clever — for a son, "
        "a daughter, children:", pause=800, chapter="Agreement")
ep.ro("fiu deștept, fiică deșteaptă, copii deștepți", "m", SLOW, 2000)
ep.narr("Young changes more than most. Listen to all four:", pause=P_SHORT)
ep.ro("tânăr, tânără, tineri, tinere", "m", SLOW, 2000)
ep.teach("Soția lui e tânără.", "His wife is young.", "f")
ep.teach("Părinții lor sunt tineri.", "Their parents are young.", "m")
ep.teach("Bunica ei e bătrână, dar sănătoasă.", "Her grandmother is old, but healthy.", "f")

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v in [
    ("His grandfather is old.", "Bunicul lui e bătrân.", "m"),
    ("Her grandmother is old, but healthy.", "Bunica ei e bătrână, dar sănătoasă.", "f"),
    ("His wife is young.", "Soția lui e tânără.", "f"),
    ("Their son is clever.", "Fiul lor e deștept.", "m"),
    ("Her daughter is hardworking.", "Fiica ei e harnică.", "f"),
    ("Their son is ill now.", "Fiul lor e bolnav acum.", "m"),
    ("His brother is young and hardworking.", "Fratele lui e tânăr și harnic.", "m"),
    ("Their parents are young.", "Părinții lor sunt tineri.", "m"),
    ("How is her mother? — She's healthy.", "Cum e mama ei? E sănătoasă.", "f"),
    ("His sister is ill.", "Sora lui e bolnavă.", "f"),
    ("Our grandparents are old, but healthy.", "Bunicii noștri sunt bătrâni, dar sănătoși.", "m"),
    ("A clever daughter.", "O fiică deșteaptă.", "f"),
    ("Clever children.", "Copii deștepți.", "m"),
    ("The child is clever.", "Copilul e deștept.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Calling someone old to their face, or their "
        "family's, sounds blunt. The polite way to say it — listen:", pause=800,
        chapter="How people really say it")
ep.ro("Bunicul e în vârstă.", "m", SLOW, 1400)
ep.narr("Grandfather is getting on, elderly. Keep the plain word for things, "
        "or for your own grandparents among friends. And the answer to bad "
        "news, as in the dialogue — listen:", pause=P_SHORT)
ep.ro("Îmi pare rău.", "f", SLOW, 1400)
ep.narr("I'm sorry — for sympathy. Bumping into someone is a different "
        "sorry, and that comes later.", pause=P_SECTION)

# ═══ 6. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 7. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Mihai e vecinul meu.",
    "Bunicul lui e bătrân, dar sănătos.",
    "Soția lui e tânără și harnică.",
    "Fiul lor e deștept, dar acum e bolnav.",
]
for line in TEXT:
    ep.ro(line, "f", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "f", NORMAL, 300)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The neighbour's family again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("His, her and their, and six ways to describe a person. Next time, the "
        "last of the family — and the chapter's own text.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("That's part five of the family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
