"""
Episode 10E — "Ce noutăți?" (Lecția 10 "După cumpărături", memory-first, part 5)

The last of Lecția 10. Six items: librărie (a bookshop — a false friend,
library is bibliotecă from 08E), știre, noutate, tren, umblu (the third of the
chapter's short-u verbs, like aflu and intru in 10B), adevăr. Then the chapter
together: every verb, all, prices; the synthesis text "După cumpărături"
(nearly whole — ambalaj and varietate are glue); and the proverb "Cinstea nu
se cumpără."

The spoken layer flags a Moldovan use the chapter teaches: "umblu la lecții /
umblu pe jos" (I attend classes / I walk) — in Bucharest a umbla is to wander,
roam ("umblu prin magazin"), and walking is "merg pe jos".

Scene: two friends catching up — what's new, a new bookshop, is that true.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["librărie", "știre", "noutate", "tren", "umblu", "adevăr"]
GLUE = {"Adevărat?": "Really? True? — a chunk",
        "prin": "through, around — in 'umblu prin magazin'",
        "ambalaj": "packaging — in the book's text",
        "varietate": "variety — in the book's text"}

ep = Episode(number=10, lesson=10, part="e", title="Ce noutăți?",
             source="Limba care ne unește, nivelul I — Lecția 10 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Ce noutăți?"),
    ("radu", "Am o știre bună: e o librărie nouă lângă universitate."),
    ("dana", "Adevărat?"),
    ("radu", "Da! Umblu prin librărie toată ziua."),
    ("dana", "Iei trenul?"),
    ("radu", "Nu, e aproape."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two friends catching up. The last six words of Lesson 10, then the "
        "whole lesson, and the book's own text.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("librărie", "a bookshop", "o librărie", "m",
            teach_ro="O librărie nouă.", teach_en="A new bookshop.")
ep.new_item("știre", "a piece of news", "o știre", "f",
            teach_ro="O știre bună.", teach_en="Good news.")
ep.new_item("noutate", "something new", "o noutate", "m",
            teach_ro="Ce noutăți?", teach_en="What's new?")
ep.new_item("tren", "a train", "un tren", "f",
            teach_ro="Iau trenul.", teach_en="I take the train.")
ep.new_item("umblu", "I wander, I walk around", "umblu", "m",
            teach_ro="Umblu prin magazin.", teach_en="I wander round the shop.")
ep.new_item("adevăr", "the truth", "adevărul", "f",
            teach_ro="Acesta e adevărul.", teach_en="That's the truth.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("a train", "un tren", "m"), ("the truth", "adevărul", "f"), ("a bookshop", "o librărie", "m"),
                    ("I wander around", "umblu", "f"), ("a piece of news", "o știre", "m"),
                    ("something new", "o noutate", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Two things to keep straight ══════════════════════════════════════════
ep.narr("A bookshop is not a library. Listen — bookshop, library:", pause=800,
        chapter="Two to keep straight")
ep.ro("o librărie, o bibliotecă", "m", SLOW, 1800)
ep.narr("You buy books in the first, borrow them in the second. And wander goes "
        "like find out — the short extra sound in the I-form only. Listen:",
        pause=P_SHORT)
ep.ro("umblu, umbli, umblă", "f", SLOW, 1800)
for cue, ans, v in [("a bookshop", "o librărie", "m"), ("a library", "o bibliotecă", "f"),
                    ("you wander — to a friend", "umbli", "m"), ("she wanders", "umblă", "f"),
                    ("we wander", "umblăm", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. Lesson 10 together ═══════════════════════════════════════════════════
ep.narr("Now all of Lesson 10 — the verbs, all, the prices.", pause=P_SECTION,
        chapter="Lesson 10 together")
for cue, ans, v, extra in [
    ("What's new?", "Ce noutăți?", "m", {}),
    ("I have good news.", "Am o știre bună.", "f", {}),
    ("Really?", "Adevărat?", "m", {}),
    ("I take the train.", "Iau trenul.", "f", {}),
    ("They take the train at nine.", "Ei iau trenul la nouă.", "m", {}),
    ("I wander round the bookshop all day.", "Umblu prin librărie toată ziua.", "f", {}),
    ("I find out a piece of news.", "Aflu o știre.", "m", {}),
    ("We go into the bookshop.", "Intrăm în librărie.", "f", {}),
    ("That's the truth.", "Acesta e adevărul.", "m", {}),
    ("All the goods are good quality.", "Toate mărfurile sunt de calitate bună.", "f", {}),
    ("The prices are reasonable.", "Prețurile sunt convenabile.", "m", {}),
    ("I'll take some products.", "Iau niște produse.", "f", {}),
    ("The shop assistants are friendly.", "Vânzătorii sunt amabili.", "m", {}),
    ("I prefer expensive, good ice cream.", "Prefer înghețată scumpă și bună.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book also uses wander for walking, and for "
        "going to classes. That's Moldovan. In Bucharest, walking is said like "
        "this — listen:", pause=800, chapter="How people really say it")
ep.ro("Merg pe jos.", "f", SLOW, 1400)
ep.narr("I walk, on foot. Wander stays for wandering round a shop or a town. "
        "And in the book's text you'll hear that's the truth said short, the "
        "way people do. Listen:", pause=P_SHORT)
ep.ro("Acesta-i adevărul.", "m", SLOW, 1600)
ep.narr("Just to recognise.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 6. Text — the chapter's own ═════════════════════════════════════════════
ep.narr("Now the chapter's own text: going shopping. Two words are new and "
        "clear from the story — packaging and variety. Slowly first.",
        pause=800, chapter="Text")
BOOK_TEXT = [
    "Am nevoie de produse. Vreau produse de calitate și în ambalaj frumos.",
    "Aflu că la magazinul de lângă casa mea sunt produse ieftine. Intru.",
    "E o varietate mare de mărfuri. Toate mărfurile sunt de calitate bună.",
    "Sunt mulți cumpărători. Umblu prin magazin. Prețurile sunt convenabile.",
    "Eu iau niște produse.",
    "— Cât costă zahărul? — Cinci lei. — E de calitate? — Da, e din Moldova.",
    "— La ce preț e făina? — Trei lei. — Vreau și o cutie de bomboane. — Poftim. Cincisprezece lei.",
    "Vânzătorii sunt amabili. Vreau o înghețată. Prefer înghețată scumpă și bună.",
    "Acesta-i adevărul. Eu iau cumpărătura.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("Cinstea nu se cumpără.", "f", SLOW, 1600)
ep.narr("Honesty can't be bought. Once more:", pause=P_SHORT)
ep.ro("Cinstea nu se cumpără.", "f", NORMAL, 1400)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The two friends again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lesson 10 — and with it the second block of five. Next, a "
        "recap of Lessons 6 to 10, built from what you still miss.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 10.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("10", []))
