"""
Episode 05D — "Cum e cămașa?" (Lecția 5, memory-first, part 4 of 5)

Six new items — the four book colours alb, negru, albastru, galben, plus cum
(how, what is it like) and de asemenea (as well) — and the grammar that runs
under all of them: adjective agreement. A Romanian adjective is four words, not
one; it changes to match its noun in gender and number. Cămașa e albă, paltonul
e negru, mănușile sunt negre.

Correctness note: agreement is the most error-prone thing in the course, so
every target combination here is lifted from or directly modelled on Lecția 5's
own exercises. The wardrobe (05A–05C) is the backdrop; it comes back drilled.

Scene: going through the wardrobe with an opinion on the colour of each thing.
Commenting on colour is exactly where the endings have to line up, over and over.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["alb", "negru", "albastru", "galben", "cum", "de asemenea"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=5, lesson=5, part="d", title="Cum e cămașa?",
             source="Limba care ne unește, nivelul I — Lecția 5 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Cum e cămașa?"),
    ("radu",  "Cămașa e albă."),
    ("dana",  "Și paltonul?"),
    ("radu",  "Paltonul e negru."),
    ("dana",  "Dar cravata? Cum e?"),
    ("radu",  "Cravata e albastră. Și tricoul e albastru, de asemenea."),
    ("dana",  "Iată o rochie galbenă!"),
    ("radu",  "Da. O rochie galbenă."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The wardrobe again, now with an opinion on the colour of everything — "
        "white, black, blue, yellow. Listen to how the colour word changes its "
        "ending to match the thing. That matching is today.", pause=P_SECTION)

# ═══ 1. Four colours — introduced then recalled at once ══════════════════════
ep.narr("Four colours, each on a thing. The plain form first.", pause=800,
        chapter="Four colours")
ep.new_item("alb", "white", "alb", "m", teach_ro="Tricoul e alb.",
            teach_en="The t-shirt is white.")
ep.new_item("negru", "black", "negru", "m", teach_ro="Paltonul e negru.",
            teach_en="The coat is black.")
ep.new_item("albastru", "blue", "albastru", "m", teach_ro="Tricoul e albastru.",
            teach_en="The t-shirt is blue.")
ep.new_item("galben", "yellow", "galben", "m", teach_ro="Puloverul e galben.",
            teach_en="The sweater is yellow.")

ep.narr("The four together, mixed. Just the colour.", pause=800)
for cue, ans in [("blue", "albastru"), ("yellow", "galben"),
                 ("white", "alb"), ("black", "negru")]:
    ep.recall_word(cue, ans, "m")

# ═══ 2. cum and de asemenea ══════════════════════════════════════════════════
ep.narr("Two words for describing. Cum — how, what is it like. And de asemenea "
        "— as well, too.", pause=800, chapter="cum and de asemenea")
ep.new_item("cum", "how / what is it like", "cum", "f",
            teach_ro="Cum e cămașa?", teach_en="How is the shirt?")
ep.new_item("de asemenea", "as well, too", "de asemenea", "m",
            teach_ro="Tricoul e albastru, de asemenea.",
            teach_en="The t-shirt is blue too.")

# ═══ 3. Grammar — adjective agreement, four forms ════════════════════════════
ep.narr("Now the rule under all of this. A Romanian adjective has four forms — "
        "it matches its noun, masculine or feminine, one or many. Take alb, "
        "white:", pause=800, chapter="Agreement")
ep.narr("Alb, albă, albi, albe.")
for r, e in [("un tricou alb, o cămașă albă", "a white t-shirt, a white shirt"),
             ("niște tricouri albe, niște cămăși albe",
              "some white t-shirts, some white shirts")]:
    ep.teach(r, e, "m")
ep.narr("The colours ending in -u shift a little more. Negru, black — negru, "
        "neagră, negri, negre:", pause=P_SHORT)
for r, e in [("un pulover negru, o mănușă neagră",
              "a black sweater, a black glove"),
             ("niște pulovere negre, niște mănuși negre",
              "some black sweaters, some black gloves")]:
    ep.teach(r, e, "m")
ep.narr("Albastru works the same — albastru, albastră, albaștri, albastre. Do "
        "not memorise the table; the drill sets it.", pause=P_SECTION)

# ═══ 4. Drill — the endings have to match ════════════════════════════════════
ep.narr("The work, and the ending has to match the thing. A whole sentence out "
        "loud each time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("The shirt is white.", "Cămașa e albă.", "f"),
    ("The coat is black.", "Paltonul e negru.", "m"),
    ("The tie is blue.", "Cravata e albastră.", "f"),
    ("The dress is yellow.", "Rochia e galbenă.", "f"),
    ("How is the shirt? — It's white.", "Cum e cămașa? E albă.", "f"),
    ("How are the trousers? — They're black.",
     "Cum sunt pantalonii? Sunt negri.", "m"),
    ("The t-shirt is blue, the tie is blue too.",
     "Tricoul e albastru, cravata e albastră de asemenea.", "m"),
    ("The sweater is white, the shirt is white.",
     "Puloverul e alb, cămașa e albă.", "m"),
    ("some black gloves", "Niște mănuși negre.", "f"),
    ("some yellow dresses", "Niște rochii galbene.", "f"),
    ("How is the coat? — It's black.", "Cum e paltonul? E negru.", "m"),
    ("The blouse is white, the skirt is black.",
     "Bluza e albă, fusta e neagră.", "f"),
    ("The t-shirt is yellow.", "Tricoul e galben.", "m"),
    ("The gloves are black too.", "Mănușile sunt negre de asemenea.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book gives you four colours; you will want "
        "more at once — at least red and green.", pause=800,
        chapter="How people really say it")
for r, e, v in [("o rochie roșie", "a red dress", "f"),
                ("un pulover verde", "a green sweater", "m")]:
    ep.teach(r, e, v)
ep.narr("Roșu behaves like negru — roșu, roșie, roșii. Verde barely changes — "
        "verde, verzi. And maro, brown, and gri, grey, never change at all: o "
        "rochie maro, niște pantaloni gri.", pause=P_SECTION)

# ═══ 6. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 7. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Cum e cămașa? Cămașa e albă.",
    "Paltonul e negru. Cravata e albastră.",
    "Tricoul e albastru, de asemenea.",
    "Iată o rochie galbenă!",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The wardrobe again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Every ending matched its thing. Next time, the last of it — how a "
        "thing is beyond its colour: good, nice, elegant, short.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: pick three things you can see and say the colour, "
        "endings matching. Cămașa e albă. Pe curând!",
        pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("5", []))
