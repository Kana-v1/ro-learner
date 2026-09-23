"""
Episode 06B — "Avem o familie" (Lecția 6 "În familie", memory-first, part 2)

Four more of the family — bunic, bunică, copil, familie — and the plural of
a avea: avem, aveți, au. With 06A's am/ai/are, that completes the verb. The
family words from 06A come back drilled, and a avea now runs through everything.

Scene: talking about the whole household — who they have, who is where.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["bunic", "bunică", "copil", "familie"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=6, lesson=6, part="b", title="Avem o familie",
             source="Limba care ne unește, nivelul I — Lecția 6 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Aveți copii?"),
    ("radu",  "Da, avem un copil."),
    ("dana",  "Și bunicii?"),
    ("radu",  "Bunica e aici. Bunicul e acasă."),
    ("dana",  "O familie frumoasă!"),
    ("radu",  "Da. Avem o familie bună."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The whole household now — a child, the grandparents, the family. And "
        "the rest of the verb to have: we have, you have, they have. Mostly you, "
        "out loud.", pause=P_SECTION)

# ═══ 1. Four more people — introduced then recalled at once ══════════════════
ep.narr("Four more, one at a time.", pause=800, chapter="Four more")
ep.new_item("bunic", "grandfather", "bunic", "m")
ep.new_item("bunică", "grandmother", "bunică", "f")
ep.new_item("copil", "child", "copil", "m")
ep.new_item("familie", "family", "familie", "f")

ep.narr("With 'the' on the end, the everyday forms — the grandfather, the "
        "grandmother, the child, the family. Listen:", pause=P_SHORT)
ep.ro("bunicul, bunica, copilul, familia", "f", NORMAL, 1600)

ep.narr("The four together, mixed. Just the word.", pause=800)
for cue, ans, v in [("child", "copil", "m"), ("grandmother", "bunică", "f"),
                    ("family", "familie", "f"), ("grandfather", "bunic", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Grammar — a avea, the plural ═════════════════════════════════════════
ep.narr("Last time: I have, you have, he or she has. Now the rest — we, you all, "
        "they. Listen:", pause=800, chapter="a avea: the plural")
ep.ro("avem, aveți, au", "m", NORMAL, 1600)
ep.narr("That was: we have, you all have, they have. Each in a sentence:",
        pause=P_SHORT)
ep.teach("Noi avem un copil.", "We have a child.", "m")
ep.teach("Voi aveți o casă.", "You all have a house.", "f")
ep.teach("Ei au o bunică.", "They have a grandmother.", "m")
ep.narr("And all six together now — the whole verb. Listen once:", pause=P_SHORT)
ep.ro("am, ai, are, avem, aveți, au", "m", SLOW, 1800)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v in [
    ("We have a child.", "Avem un copil.", "m"),
    ("They have a family.", "Au o familie.", "f"),
    ("Do you all have children?", "Aveți copii?", "m"),
    ("The child is at home.", "Copilul e acasă.", "m"),
    ("We have a grandmother and a grandfather.",
     "Avem o bunică și un bunic.", "f"),
    ("The family is nice.", "Familia e frumoasă.", "f"),
    ("The grandmother is here, the grandfather is at home.",
     "Bunica e aici, bunicul e acasă.", "f"),
    ("They have a house.", "Au o casă.", "m"),
    ("We have a good family.", "Avem o familie bună.", "f"),
    ("Do you all have a brother? — We have a brother and a sister.",
     "Aveți un frate? Avem un frate și o soră.", "m"),
    ("I have a grandmother, she has a grandfather.",
     "Am o bunică, ea are un bunic.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("A real-speech note. Grandparents together, both at once, is one word — "
        "listen:", pause=800, chapter="How people really say it")
ep.ro("bunicii", "m", SLOW, 1200)
ep.narr("The grandparents. And kids, more than one child — listen:", pause=P_SHORT)
ep.ro("copiii", "m", SLOW, 1200)
ep.narr("The children. So this question —", pause=P_SHORT)
ep.ro("Aveți copii?", "m", SLOW, 1200)
ep.narr("— asks whether you have children at all.", pause=P_SECTION)

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Avem o familie bună.",
    "Bunica e aici. Bunicul e acasă.",
    "Avem un copil. Copilul e acasă.",
    "Aveți copii? Da, avem un copil.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The household again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That's the whole verb to have, and six of the family. Next time: whose "
        "it is — my mother, your brother — the possessives.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's part two of the family.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("6", []))
