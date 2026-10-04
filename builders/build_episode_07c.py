"""
Episode 07C — "Am nevoie de pâine" (Lecția 7 "Portrete", memory-first, part 3)

Six new items: the chapter's communicative intention, "Cum spunem că avem
nevoie de ceva" — am nevoie de … (I need …) — and the food words it is used
with in the book's own dialogues: pâine, bere, ciocolată, înghețată, plus
dulce. Forms follow the book's model ("Eu am nevoie de caiete", "De ce ai
nevoie? — Am nevoie de creioane", "Nu, eu nu am nevoie de cărți"): after de
the noun takes no article. dulce is a two-ending adjective like mare from 07A
(dulce for him and her alike).

Also a block the results asked for: the noun in its "the" form before a
possessive — sora mea, not soră mea. 6C mentioned it once; in 06G the learner
took "My sister is thin → Sora mea e slabă" for a translation error. Here it is
said plainly, then drilled as a ladder: a sister / the sister / my sister.

Scene: someone at the shop phoning home to ask what everyone needs — "De ce
ai nevoie?" asked again and again because that is the call.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["nevoie", "pâine", "bere", "ciocolată", "înghețată", "dulce"]
GLUE = {"ceva": "something — in 'ceva dulce'",
        "Sunt la magazin.": "I'm at the shop — a chunk"}

ep = Episode(number=7, lesson=7, part="c", title="Am nevoie de pâine",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Sunt la magazin. De ce ai nevoie?"),
    ("dana", "Am nevoie de pâine."),
    ("radu", "Și de bere?"),
    ("dana", "Nu, n-am nevoie de bere. Vreau o ciocolată."),
    ("radu", "Și Elena?"),
    ("dana", "Elena are nevoie de înghețată."),
    ("radu", "Acum?"),
    ("dana", "Da, acum. Vrea ceva dulce."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A call from the shop: what do you need? The book's way of saying you "
        "need something, and five things to need.", pause=P_SECTION)

# ═══ 1. Six items — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time. The first is a whole phrase.", pause=800,
        chapter="Six words")
ep.new_item("nevoie", "I need — before the thing", "am nevoie de", "f",
            teach_ro="Am nevoie de pâine.", teach_en="I need bread.")
ep.new_item("pâine", "bread", "pâine", "m",
            teach_ro="Am nevoie de pâine.", teach_en="I need bread.")
ep.new_item("bere", "beer", "bere", "m",
            teach_ro="Vreau o bere.", teach_en="I want a beer.")
ep.new_item("ciocolată", "chocolate", "ciocolată", "f",
            teach_ro="Vreau o ciocolată.", teach_en="I want a chocolate bar.")
ep.new_item("înghețată", "ice cream", "înghețată", "f",
            teach_ro="Copilul vrea o înghețată.", teach_en="The child wants an ice cream.")
ep.new_item("dulce", "sweet", "dulce", "m",
            teach_ro="Ciocolata e dulce.", teach_en="Chocolate is sweet.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("beer", "bere", "m"), ("sweet", "dulce", "f"), ("I need", "am nevoie de", "m"),
                    ("ice cream", "înghețată", "f"), ("bread", "pâine", "m"),
                    ("chocolate", "ciocolată", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. I need, you need ═════════════════════════════════════════════════════
ep.narr("I need is literally I have need of — so it moves like I have. And "
        "after of, the thing stays bare. Listen:", pause=800, chapter="I need")
ep.example(None, "Am nevoie de pâine. Ai nevoie de pâine?", "m", 1800)
ep.example(None, "El are nevoie de bere. Avem nevoie de ciocolată.", "f", 1800)
ep.narr("And the question from the shop — what do you need:", pause=P_SHORT)
ep.example(None, "De ce ai nevoie?", "m", 1600)
for cue, ans, v, extra in [
    ("I need bread.", "Am nevoie de pâine.", "m", {"accept": ["Am nevoie de o pâine."]}),
    ("Do you need beer? To a friend.", "Ai nevoie de bere?", "f", {}),
    ("What do you need? To a friend.", "De ce ai nevoie?", "m", {}),
    ("We need bread.", "Avem nevoie de pâine.", "f", {"accept": ["Avem nevoie de o pâine."]}),
    ("She needs chocolate.", "Ea are nevoie de ciocolată.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3. My sister — the "the" form ═══════════════════════════════════════════
ep.narr("Now something that sounded like a mistake in the last episodes but "
        "isn't. A sister, the sister, and my sister. Listen to all three:",
        pause=800, chapter="My sister")
ep.example(None, "o soră, sora, sora mea", "f", 2000)
ep.narr("My sister is built on the sister, not on a sister — literally the "
        "sister mine. The same for every family word. Listen:", pause=P_SHORT)
ep.example(None, "un frate, fratele, fratele meu", "m", 2000)
ep.example(None, "o fiică, fiica, fiica mea", "f", 2000)
ep.narr("So the word for my, your, his always comes after the the form. In "
        "threes: a, the, my.", pause=800)
for cue, ans, v in [
    ("a sister", "o soră", "f"), ("the sister", "sora", "f"), ("my sister", "sora mea", "f"),
    ("a brother", "un frate", "m"), ("my brother", "fratele meu", "m"),
    ("a daughter", "o fiică", "f"), ("my daughter", "fiica mea", "f"),
    ("an uncle", "un unchi", "m"), ("my uncle", "unchiul meu", "m"),
    ("a name", "un nume", "m"), ("my name", "numele meu", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v, extra in [
    ("I need bread and beer.", "Am nevoie de pâine și bere.", "m", {}),
    ("I don't need beer.", "Nu am nevoie de bere.", "f", {"accept": ["N-am nevoie de bere."]}),
    ("My daughter wants an ice cream.", "Fiica mea vrea o înghețată.", "m", {}),
    ("Chocolate is sweet.", "Ciocolata e dulce.", "f", {}),
    ("Do you need bread? — Yes, I need bread.", "Ai nevoie de pâine? — Da, am nevoie de pâine.", "m", {}),
    ("My brother wants a beer.", "Fratele meu vrea o bere.", "f", {}),
    ("What does she need? — Ice cream.", "De ce are nevoie? — De înghețată.", "m", {}),
    ("I don't want beer, I want chocolate.", "Nu vreau bere, vreau ciocolată.", "f",
     {"accept": ["Nu vreau bere, vreau o ciocolată."]}),
    ("The ice cream is sweet.", "Înghețata e dulce.", "m", {}),
    ("My sister needs chocolate.", "Sora mea are nevoie de ciocolată.", "f", {}),
    ("We need bread, not ice cream.", "Avem nevoie de pâine, nu de înghețată.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. In the call you heard the short form of I don't "
        "have — the not and the have run together. Listen to the full form, "
        "then the spoken one:", pause=800, chapter="How people really say it")
ep.ro("Nu am nevoie.", "m", SLOW, 1200)
ep.ro("N-am nevoie.", "m", SLOW, 1600)
ep.narr("The book itself writes it that way. Say it:", pause=P_SHORT)
ep.drill("I don't need bread. The short way.", "N-am nevoie de pâine.", "f",
         accept=["Nu am nevoie de pâine."])

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The call again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's what you need, and whose it is.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
