"""
Episode 05E — "Un palton bun" (Lecția 5, memory-first, part 5 of 5)

The last of Lecția 5: the qualities — bun, rău, frumos, elegant, comod, scurt,
modern — and one more turn on adjective agreement, now with describing words
rather than colours. These lean heavily on recognition (elegant, comod, modern
are near-cognates; bun/rău are a pair), so the new load is lighter than seven
suggests and most of the episode is recall. The chapter's own synthesis text
and proverb close it, by which point every word of Lecția 5 is taught.

Scene: the wardrobe once more, this time an opinion on how each thing is — good,
comfortable, elegant, short.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["bun", "rău", "frumos", "elegant", "comod", "scurt", "modern"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=5, lesson=5, part="e", title="Un palton bun",
             source="Limba care ne unește, nivelul I — Lecția 5 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Cum e paltonul?"),
    ("radu",  "Paltonul e negru. E elegant."),
    ("dana",  "Și puloverul?"),
    ("radu",  "Puloverul e comod. E bun."),
    ("dana",  "Dar pantalonii? Cum sunt?"),
    ("radu",  "Pantalonii sunt scurți."),
    ("dana",  "Iată o rochie modernă. E frumoasă!"),
    ("radu",  "Da. O îmbrăcăminte bună."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The wardrobe a last time, now with a verdict on each thing — good, "
        "comfortable, elegant, short. Several of these you will half-recognise "
        "already. Same agreement rule as the colours; mostly you, out loud.",
        pause=P_SECTION)

# ═══ 1. The qualities — introduced then recalled at once ═════════════════════
ep.narr("The describing words, one at a time. Two of them are a pair — good and "
        "bad.", pause=800, chapter="Qualities")
ep.new_item("bun", "good", "bun", "m", teach_ro="Un palton bun.",
            teach_en="A good coat.")
ep.new_item("rău", "bad", "rău", "m", teach_ro="Un palton rău.",
            teach_en="A bad coat.")
ep.new_item("frumos", "nice, beautiful", "frumos", "m",
            teach_ro="Un fular frumos.", teach_en="A nice scarf.")
ep.new_item("elegant", "elegant", "elegant", "m", teach_ro="Paltonul e elegant.",
            teach_en="The coat is elegant.")
ep.new_item("comod", "comfortable", "comod", "m", teach_ro="Puloverul e comod.",
            teach_en="The sweater is comfortable.")
ep.new_item("scurt", "short", "scurt", "m", teach_ro="Pantalonii sunt scurți.",
            teach_en="The trousers are short.")
ep.new_item("modern", "modern", "modern", "m", teach_ro="Apartamentul e modern.",
            teach_en="The apartment is modern.")

ep.narr("Mixed, just the word.", pause=800)
for cue, ans in [("comfortable", "comod"), ("short", "scurt"),
                 ("good", "bun"), ("nice", "frumos"),
                 ("bad", "rău"), ("elegant", "elegant"),
                 ("modern", "modern")]:
    ep.recall_word(cue, ans, "m")

# ═══ 2. Agreement again, with describing words ═══════════════════════════════
ep.narr("The same four-form rule as the colours. Bun, good:", pause=800,
        chapter="Agreement again")
for r, e in [("un băiat bun, o fată bună", "a good boy, a good girl"),
             ("niște băieți buni, niște fete bune", "good boys, good girls")]:
    ep.teach(r, e, "m")
ep.narr("Bun, bună, buni, bune. Frumos shifts a little in the feminine — "
        "frumos, frumoasă:", pause=P_SHORT)
ep.teach("un fular frumos, o cămașă frumoasă", "a nice scarf, a nice shirt", "m")
ep.narr("Elegant, comod, modern, scurt all follow the plain pattern. The drill "
        "sets them.", pause=P_SECTION)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. A whole sentence out loud each time.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v in [
    ("a good coat, a bad coat", "Un palton bun, un palton rău.", "m"),
    ("The coat is elegant.", "Paltonul e elegant.", "m"),
    ("The sweater is comfortable.", "Puloverul e comod.", "m"),
    ("The trousers are short.", "Pantalonii sunt scurți.", "m"),
    ("The shirt is elegant.", "Cămașa e elegantă.", "f"),
    ("The dress is modern.", "Rochia e modernă.", "f"),
    ("a nice scarf, a nice shirt", "Un fular frumos, o cămașă frumoasă.", "m"),
    ("The dress is nice, the blouse is nice too.",
     "Rochia e frumoasă, bluza e frumoasă de asemenea.", "f"),
    ("How is the coat? — It's black and elegant.",
     "Cum e paltonul? E negru și elegant.", "m"),
    ("The apartment is modern.", "Apartamentul e modern.", "m"),
    ("The skirt is short.", "Fusta e scurtă.", "f"),
    ("A good coat and a comfortable one.", "Un palton bun și comod.", "m"),
    ("The clothing is good and comfortable.",
     "Îmbrăcămintea e bună și comodă.", "f"),
    ("The sweater is nice too.", "Puloverul e frumos, de asemenea.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book's word for bad is rău, and it is right "
        "as the plain opposite of bun. But about clothes, rău sounds off — a "
        "garment you dislike is urât, ugly, or you just say nu-mi place, I "
        "don't like it.", pause=800, chapter="How people really say it")
for r in ["urât", "nu-mi place"]:
    ep.ro(r, "m", SLOW, 1000)
ep.narr("Keep rău for good-versus-bad. Reach for urât in front of the mirror.",
        pause=P_SECTION)

# ═══ 5. Review — scheduled ═══════════════════════════════════════════════════
ep.review_auto()

# ═══ 6. Text — the chapter's own passage ═════════════════════════════════════
ep.narr("Now the chapter's own text, whole. Slowly first.", pause=800,
        chapter="Text")
BOOK_TEXT = [
    "Iată un dulap. Ce este în dulap? În dulap este îmbrăcăminte.",
    "Este îmbrăcăminte pentru bărbați și îmbrăcăminte pentru femei.",
    "Cămașa, pantalonii, cravata sunt pentru bărbați. "
    "Bluza, rochia, fusta sunt pentru femei.",
    "Căciula, paltonul, impermeabilul, puloverul și fularul sunt "
    "și pentru bărbați și pentru femei.",
    "Sunt pantaloni și pentru femei. Ei sunt negri, albi, albaștri.",
    "Îmbrăcămintea din dulap este modernă. Ea e comodă.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)
ep.narr("The chapter's proverb, and it needs no grammar to enjoy. Frumusețea "
        "va salva lumea — beauty will save the world.", pause=800)
ep.ro("Frumusețea va salva lumea.", "m", SLOW, 1400)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The wardrobe a last time. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lecția 5 across its five short parts. You can name a "
        "garment, put the article on it, and say what colour and cut it is. "
        "Next is a recap — no new words, all retrieval.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: describe three things you are wearing — the noun, "
        "the colour, the quality, endings matching. Cămașa e albă și frumoasă. "
        "Pe curând!", pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("5", []))
