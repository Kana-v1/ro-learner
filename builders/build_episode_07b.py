"""
Episode 07B — "Cum arată Victor?" (Lecția 7 "Portrete", memory-first, part 2)

Six new items from the chapter's portrait words: înalt, gras, blond, brunet,
păr, ochi. Descriptions follow the book's synthesis text ("El este înalt și
slab. Are ochi negri și păr blond", "are nas mic, ochi mari, părul negru")
and its antonym exercise ("Victor este gras? — Nu, Victor este slab"). The
agreement from 07A carries on: înaltă, blondă, brunetă for her; ochi is
already plural, so its colours take the plural (ochi negri, ochi albaștri,
ochi mari).

Scene: meeting someone you've never seen, on the phone to the friend who
knows him — "what does he look like?", then checking each stranger against
the description, so the portrait words come round again and again.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["înalt", "gras", "blond", "brunet", "păr", "ochi"]
GLUE = {"Cum arată?": "What does he look like? — a chunk",
        "Victor / Radu": "names"}

ep = Episode(number=7, lesson=7, part="b", title="Cum arată Victor?",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Radu, cum arată Victor?"),
    ("radu", "E înalt și slab. Are păr blond și ochi negri."),
    ("dana", "Acesta e înalt, dar e gras și brunet."),
    ("radu", "Nu, Victor nu e gras."),
    ("dana", "Și acesta? E înalt, slab, blond…"),
    ("radu", "Da, acesta e Victor!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Meeting someone you've never seen, with a friend on the phone telling "
        "you what he looks like. Six words for a portrait.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("înalt", "tall", "înalt", "m",
            teach_ro="Victor e înalt.", teach_en="Victor is tall.")
ep.new_item("gras", "fat", "gras", "m",
            teach_ro="Acesta e gras.", teach_en="This one is fat.")
ep.new_item("blond", "fair-haired, blond", "blond", "f",
            teach_ro="Victor e blond.", teach_en="Victor is fair-haired.")
ep.new_item("brunet", "dark-haired", "brunet", "f",
            teach_ro="Fratele lui e brunet.", teach_en="His brother is dark-haired.")
ep.new_item("păr", "hair", "păr", "m",
            teach_ro="Are păr blond.", teach_en="He has fair hair.")
ep.new_item("ochi", "eyes", "ochi", "f",
            teach_ro="Are ochi negri.", teach_en="He has black eyes.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("hair", "păr", "m"), ("dark-haired", "brunet", "f"), ("tall", "înalt", "m"),
                    ("eyes", "ochi", "f"), ("fat", "gras", "m"), ("fair-haired", "blond", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. For her ══════════════════════════════════════════════════════════════
ep.narr("For a woman, the ending you know from the last episode. Listen:",
        pause=800, chapter="For her")
ep.example(None, "El e înalt. Ea e înaltă.", "m", 1600)
ep.example(None, "El e blond. Ea e blondă.", "f", 1600)
ep.example(None, "El e brunet. Ea e brunetă.", "m", 1600)
for cue, ans, v in [
    ("He is tall.", "El e înalt.", "m"),
    ("She is tall.", "Ea e înaltă.", "f"),
    ("He is dark-haired.", "El e brunet.", "m"),
    ("She is dark-haired.", "Ea e brunetă.", "f"),
    ("She is fair-haired.", "Ea e blondă.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. Has hair, has eyes ═══════════════════════════════════════════════════
ep.narr("Hair and eyes go with has. Eyes is already plural, so its colour gets "
        "the plural ending. Listen:", pause=800, chapter="Hair and eyes")
ep.example(None, "Are păr negru. Are ochi negri.", "m", 1800)
ep.example(None, "Are păr lung. Are ochi mari.", "f", 1800)
ep.example(None, "Are ochi albaștri.", "m", 1600)
for cue, ans, v, extra in [
    ("He has fair hair.", "Are păr blond.", "m", {"accept": ["Are părul blond."]}),
    ("He has black eyes.", "Are ochi negri.", "f", {"accept": ["Are ochii negri."]}),
    ("She has long hair.", "Are păr lung.", "m", {"accept": ["Are părul lung."]}),
    ("She has big eyes.", "Are ochi mari.", "f", {"accept": ["Are ochii mari."]}),
    ("He has blue eyes.", "Are ochi albaștri.", "m", {"accept": ["Are ochii albaștri."]}),
    ("She has black hair.", "Are păr negru.", "f", {"accept": ["Are părul negru."]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v, extra in [
    ("He is tall and thin.", "El e înalt și slab.", "m", {}),
    ("Is Victor fat? — No, Victor is thin.", "Victor e gras? — Nu, Victor e slab.", "f", {}),
    ("He has fair hair and black eyes.", "Are păr blond și ochi negri.", "m",
     {"accept": ["Are părul blond și ochii negri."]}),
    ("My brother is tall.", "Fratele meu e înalt.", "f", {}),
    ("My sister is short and fair-haired.", "Sora mea e scundă și blondă.", "m", {}),
    ("She is tall and beautiful.", "Ea e înaltă și frumoasă.", "f", {}),
    ("Is he tall? — No, he's short.", "E înalt? — Nu, e scund.", "m", {}),
    ("Their children are tall.", "Copiii lor sunt înalți.", "f", {}),
    ("Victor has blue eyes.", "Victor are ochi albaștri.", "m",
     {"accept": ["Victor are ochii albaștri."]}),
    ("His wife is dark-haired.", "Soția lui e brunetă.", "f", {}),
    ("My daughter has long hair.", "Fiica mea are păr lung.", "m",
     {"accept": ["Fiica mea are părul lung."]}),
    ("He isn't fat.", "Nu e gras.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The question at the start — what does he look "
        "like — is the one to know. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Cum arată?", "f", SLOW, 1600)
ep.narr("Say it:", pause=P_SHORT)
ep.drill("What does he look like?", "Cum arată?", "f")
ep.narr("And fat, said about a person to their face, is blunt — close to rude. "
        "The kind way — a bit chubby. Listen:", pause=P_SHORT)
ep.ro("E mai plinuț.", "m", SLOW, 1600)
ep.narr("Between fair and dark, people also say brown-haired. Listen:", pause=P_SHORT)
ep.ro("E șaten.", "f", SLOW, 1600)
ep.narr("Just to recognise; you don't need to say them yet.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The phone call again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's a portrait: tall, fat, fair, dark, hair and eyes.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
