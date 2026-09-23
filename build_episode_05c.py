"""
Episode 05C — "În cuier" (Lecția 5, memory-first, part 3 of 5)

Five new items — fular, impermeabil, căciulă, mănușă, îmbrăcăminte — the outdoor
things and the collective word for clothing. No new grammar: this part
consolidates the definite article on both genders and adds the plural article
(mănuși, mănușile). 05A's and 05B's garments come back on the schedule.

Scene: the coat rack in the hall (cuier, raft, from episode 4), the things you
put on to go out.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["fular", "impermeabil", "căciulă", "mănușă", "îmbrăcăminte"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=5, lesson=5, part="c", title="În cuier",
             source="Limba care ne unește, nivelul I — Lecția 5 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Unde e fularul?"),
    ("dana",  "Fularul e în cuier."),
    ("radu",  "Și căciula? Și mănușile?"),
    ("dana",  "Căciula e pe raft. Iată mănușile!"),
    ("radu",  "Unde e impermeabilul?"),
    ("dana",  "Impermeabilul e în dulap. Îmbrăcămintea e aici."),
    ("radu",  "Mulțumesc!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The hall now, and the things you put on to go out — a scarf, a hat, "
        "gloves, a raincoat. No new rule today, just more words wearing the "
        "article you already know. Mostly you, out loud.", pause=P_SECTION)

# ═══ 1. Five items — introduced then recalled at once ════════════════════════
ep.narr("Five things, one at a time.", pause=800, chapter="Five things")
ep.new_item("fular", "a scarf", "un fular", "m")
ep.new_item("impermeabil", "a raincoat", "un impermeabil", "m")
ep.new_item("căciulă", "a winter hat", "o căciulă", "f")
ep.new_item("mănușă", "a glove", "o mănușă", "f")
ep.narr("And the collective word for clothing as a whole — feminine.",
        pause=P_SHORT)
ep.new_item("îmbrăcăminte", "clothing", "îmbrăcăminte", "f")

ep.narr("The five together, mixed. Just the word.", pause=800)
for cue, ans, v in [("a glove", "o mănușă", "f"),
                    ("a raincoat", "un impermeabil", "m"),
                    ("a winter hat", "o căciulă", "f"),
                    ("a scarf", "un fular", "m"),
                    ("clothing", "îmbrăcăminte", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. The article again, both genders, plus the plural ═════════════════════
ep.narr("The article, on today's words. Masculine -ul, feminine -a — same as "
        "before.", pause=800, chapter="The article again")
for r, e, v in [("un fular, fularul", "a scarf, the scarf", "m"),
                ("un impermeabil, impermeabilul", "a raincoat, the raincoat", "m"),
                ("o căciulă, căciula", "a hat, the hat", "f"),
                ("o mănușă, mănușa", "a glove, the glove", "f")]:
    ep.teach(r, e, v)
ep.narr("Gloves come in pairs, so you will want the plural. Some gloves — niște "
        "mănuși. And 'the gloves' puts the article on the plural: mănușile.",
        pause=P_SHORT)
ep.teach("niște mănuși, mănușile", "some gloves, the gloves", "f")
ep.narr("Say each one with 'the'.", pause=800)
for cue, ans, v in [("the scarf", "Fularul.", "m"),
                    ("the raincoat", "Impermeabilul.", "m"),
                    ("the hat", "Căciula.", "f"),
                    ("the glove", "Mănușa.", "f"),
                    ("the gloves", "Mănușile.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Sentence drill ═══════════════════════════════════════════════════════
ep.narr("The whole thing now. Where is it, and the answer.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v in [
    ("Where is the scarf? — In the coat rack.", "Unde e fularul? În cuier.", "m"),
    ("Where is the hat? — On the shelf.", "Unde e căciula? Pe raft.", "f"),
    ("Where are the gloves?", "Unde sunt mănușile?", "f"),
    ("Here are the gloves!", "Iată mănușile!", "f"),
    ("Where is the raincoat? — In the wardrobe.",
     "Unde e impermeabilul? În dulap.", "m"),
    ("The scarf is in the coat rack.", "Fularul e în cuier.", "m"),
    ("The clothing is in the wardrobe.", "Îmbrăcămintea e în dulap.", "f"),
    ("Here is the scarf, and here is the hat.",
     "Iată fularul, iar iată căciula.", "m"),
    ("Some gloves.", "Niște mănuși.", "f"),
    ("Where is the clothing?", "Unde e îmbrăcămintea?", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The chapter's word îmbrăcăminte is the formal "
        "one — shop signs, forms. What people actually say for clothes is "
        "haine: unde sunt hainele. On its own, o haină is a coat or a jacket. "
        "Keep îmbrăcăminte for reading; say haine.", pause=P_SECTION,
        chapter="How people really say it")
ep.teach("Unde sunt hainele?", "Where are the clothes?", "f")

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Unde e fularul? Fularul e în cuier.",
    "Căciula e pe raft. Iată mănușile!",
    "Impermeabilul e în dulap.",
    "Îmbrăcămintea e aici.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The hall again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That is the whole wardrobe named. Next time we stop naming things and "
        "start describing them — the colours.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: at your own door, name what you would put on to go "
        "out — fularul, căciula, mănușile. Pe curând!",
        pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("5", []))
