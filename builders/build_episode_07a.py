"""
Episode 07A — "Vreau o rochie nouă" (Lecția 7 "Portrete", memory-first, part 1)

Six new items: vreau (the book's a vrea, first person — the one a learner
needs in a shop), and the chapter's adjectives for things: mare, mic, nou,
lung, larg. The chapter's grammar point is adjective agreement — exactly
where the 6C–6F results were weakest — so this part spends its drill time on
it, using the Lecția 5 clothes the learner already has: mic / mică / mici is
the book's "adjectiv cu 3 terminații", mare / mari its "cu 2 terminații".
Forms follow the book's tables (mic, mică, mici; nou, nouă, noi; mare, mari).

Scene: a clothes shop. The assistant shows one thing after another and the
customer says what's wrong with each — too long, too small — which is
exactly where the size words repeat themselves.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["vreau", "mare", "mic", "nou", "lung", "larg"]
GLUE = {"Ce doriți?": "What would you like? — what a shop assistant says",
        "prea": "too — as in too long",
        "Și aceasta?": "And this one? — a chunk"}

ep = Episode(number=7, lesson=7, part="a", title="Vreau o rochie nouă",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună ziua. Ce doriți?"),
    ("elena", "Vreau o rochie nouă."),
    ("dana",  "Iată o rochie lungă."),
    ("elena", "E prea lungă. Vreau o rochie scurtă."),
    ("dana",  "Și aceasta?"),
    ("elena", "E prea mică."),
    ("dana",  "Aceasta e mare și largă."),
    ("elena", "Da, e bună. Și vreau un pulover larg."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A clothes shop. Lesson 7 starts with saying what you want, and whether "
        "it's big, small, new, long or loose. You have the clothes already.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("vreau", "I want", "vreau", "f",
            teach_ro="Vreau o rochie nouă.", teach_en="I want a new dress.")
ep.new_item("mare", "big", "mare", "m",
            teach_ro="Paltonul e mare.", teach_en="The coat is big.")
ep.new_item("mic", "small", "mic", "m",
            teach_ro="Tricoul e mic.", teach_en="The t-shirt is small.")
ep.new_item("nou", "new", "nou", "f",
            teach_ro="Un costum nou.", teach_en="A new suit.")
ep.new_item("lung", "long", "lung", "m",
            teach_ro="Un palton lung.", teach_en="A long coat.")
ep.new_item("larg", "loose, wide", "larg", "f",
            teach_ro="Un pulover larg.", teach_en="A loose sweater.")

ep.narr("The six together, mixed. Just the word.", pause=800)
for cue, ans, v in [("small", "mic", "m"), ("I want", "vreau", "f"), ("long", "lung", "m"),
                    ("new", "nou", "f"), ("loose", "larg", "m"), ("big", "mare", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. I want ═══════════════════════════════════════════════════════════════
ep.narr("I want, then the thing. Just like I have. Listen:", pause=800,
        chapter="I want")
ep.example(None, "Vreau un tricou. Vreau o cămașă.", "f", 1600)
ep.narr("Asking a friend what they want — listen:", pause=P_SHORT)
ep.example(None, "Ce vrei?", "m", 1400)
ep.narr("And he wants, she wants:", pause=P_SHORT)
ep.example(None, "El vrea un palton. Ea vrea o fustă.", "f", 1600)
for cue, ans, v in [
    ("I want a t-shirt.", "Vreau un tricou.", "f"),
    ("What do you want? To a friend.", "Ce vrei?", "m"),
    ("I want a dress.", "Vreau o rochie.", "f"),
    ("She wants a skirt.", "Ea vrea o fustă.", "m"),
    ("My son wants a sweater.", "Fiul meu vrea un pulover.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. For a dress: the ending ══════════════════════════════════════════════
ep.narr("Now the ending, the thing you mixed up in Lesson 6. For a coat, a "
        "t-shirt, a sweater: the plain form. For a dress, a skirt, a shirt: an "
        "extra sound at the end. Listen:", pause=800, chapter="The ending")
ep.example(None, "un tricou mic, o rochie mică", "m", 1800)
ep.example(None, "un costum nou, o rochie nouă", "f", 1800)
ep.example(None, "un palton lung, o fustă lungă", "m", 1800)
ep.example(None, "un pulover larg, o bluză largă", "f", 1800)
ep.narr("Big is the easy one: it doesn't change. Listen:", pause=P_SHORT)
ep.example(None, "un palton mare, o cămașă mare", "m", 1800)
ep.narr("Your turn. Him first, then her.", pause=800)
for cue, ans, v in [
    ("a small t-shirt", "un tricou mic", "m"),
    ("a small dress", "o rochie mică", "f"),
    ("a new suit", "un costum nou", "m"),
    ("a new dress", "o rochie nouă", "f"),
    ("a long coat", "un palton lung", "m"),
    ("a long skirt", "o fustă lungă", "f"),
    ("a loose sweater", "un pulover larg", "m"),
    ("a loose blouse", "o bluză largă", "f"),
    ("a big coat", "un palton mare", "m"),
    ("a big shirt", "o cămașă mare", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. More than one ════════════════════════════════════════════════════════
ep.narr("More than one: an i at the end — and the same for his things and "
        "hers. Listen:", pause=800, chapter="More than one")
ep.example(None, "pantaloni lungi, pantaloni largi", "m", 1800)
ep.example(None, "tricouri noi, mănuși mici", "f", 1800)
ep.narr("Big: an i as well.", pause=P_SHORT)
ep.example(None, "pantaloni mari", "m", 1600)
for cue, ans, v in [
    ("long trousers", "pantaloni lungi", "m"),
    ("new t-shirts", "tricouri noi", "f"),
    ("small gloves", "mănuși mici", "m"),
    ("big trousers", "pantaloni mari", "f"),
    ("loose trousers", "pantaloni largi", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time, the app waits while you "
        "think.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I want a new dress.", "Vreau o rochie nouă.", "f", {}),
    ("The dress is too long.", "Rochia e prea lungă.", "m", {}),
    ("The t-shirt is small.", "Tricoul e mic.", "f", {}),
    ("The coat is big.", "Paltonul e mare.", "m", {}),
    ("The skirt is too small.", "Fusta e prea mică.", "f", {}),
    ("I want a loose sweater.", "Vreau un pulover larg.", "m", {}),
    ("My daughter wants a long dress.", "Fiica mea vrea o rochie lungă.", "f", {}),
    ("The trousers are too long.", "Pantalonii sunt prea lungi.", "m", {}),
    ("The shirt is new and loose.", "Cămașa e nouă și largă.", "f", {}),
    ("I don't want a big coat.", "Nu vreau un palton mare.", "m", {}),
    ("She wants a white blouse.", "Ea vrea o bluză albă.", "f", {}),
    ("What do you want? — A new t-shirt.", "Ce vrei? — Un tricou nou.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. I want is fine with friends; in a shop it can "
        "sound blunt. What people say there instead — I'd like. Listen:",
        pause=800, chapter="How people really say it")
ep.ro("Aș vrea o rochie.", "f", SLOW, 1800)
ep.narr("I'd like a dress. Take it as a whole phrase. Say it:", pause=P_SHORT)
ep.drill("I'd like a sweater.", "Aș vrea un pulover.", "f")
ep.narr("And the assistant's question you heard at the start — what would you "
        "like? Listen:", pause=P_SHORT)
ep.ro("Ce doriți?", "m", SLOW, 1400)
ep.narr("That's what you'll hear walking into any shop.", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The shop again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("That's big, small, new, long and loose.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
