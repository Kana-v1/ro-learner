"""
Episode 05B — "O bluză, bluza" (Lecția 5, memory-first, part 2 of 5)

Five new items — bluză, rochie, fustă, cravată, tricou — and the other half of
the definite article: the feminine -a, set against the masculine -ul from 05A.
o bluză, bluza. o rochie, rochia. And tricou is neuter, so it takes -ul like a
masculine: un tricou, tricoul. 05A's four garments and unde/iată come back on
the spacing schedule.

Scene: the same morning, now her things and his t-shirt. Every answer is a noun
wearing the article, so -a drills itself against the -ul already known.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["bluză", "rochie", "fustă", "cravată", "tricou"]
GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=5, lesson=5, part="b", title="O bluză, bluza",
             source="Limba care ne unește, nivelul I — Lecția 5 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Unde e bluza?"),
    ("radu",  "Bluza e pe scaun."),
    ("dana",  "Și rochia? Și fusta?"),
    ("radu",  "Rochia e în dulap. Iată fusta!"),
    ("dana",  "Mulțumesc. Unde e cravata?"),
    ("radu",  "Cravata e pe masă. Iar tricoul e pe scaun."),
    ("dana",  "Bun. Cravata, tricoul."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The same morning. Yesterday the coat and the sweater took -ul on the "
        "end for 'the'. Today the other ending — the feminine -a — on a blouse, "
        "a dress, a skirt. Most of this is you producing, out loud.",
        pause=P_SECTION)

# ═══ 1. Five garments — introduced then recalled at once ═════════════════════
ep.narr("Five things, one at a time. Say each back before we move on.",
        pause=800, chapter="Five garments")
ep.new_item("bluză", "a blouse", "o bluză", "f")
ep.new_item("rochie", "a dress", "o rochie", "f")
ep.new_item("fustă", "a skirt", "o fustă", "f")
ep.new_item("cravată", "a tie", "o cravată", "f")
ep.narr("And one that is neuter — it behaves like a masculine.", pause=P_SHORT)
ep.new_item("tricou", "a t-shirt", "un tricou", "m")

ep.narr("The five together, mixed. Just the word.", pause=800)
for cue, ans, v in [("a skirt", "o fustă", "f"),
                    ("a t-shirt", "un tricou", "m"),
                    ("a dress", "o rochie", "f"),
                    ("a tie", "o cravată", "f"),
                    ("a blouse", "o bluză", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Grammar — the feminine article -a, against -ul ═══════════════════════
ep.narr("Now the ending. A feminine noun swaps its final vowel for -a. Not in "
        "front of the word — on the end of it, the same place -ul goes.",
        pause=800, chapter="The article: -a")
for r, e in [("o bluză, bluza", "a blouse, the blouse"),
             ("o fustă, fusta", "a skirt, the skirt"),
             ("o cravată, cravata", "a tie, the tie")]:
    ep.teach(r, e, "f")
ep.narr("A word ending in -e, like rochie, shifts to -ia: rochie, rochia.",
        pause=P_SHORT)
ep.teach("o rochie, rochia", "a dress, the dress", "f")
ep.narr("And the neuter tricou takes -ul, exactly like the masculine paltonul: "
        "un tricou, tricoul.", pause=P_SHORT)
ep.teach("un tricou, tricoul", "a t-shirt, the t-shirt", "m")
ep.narr("So both endings now. Masculine and neuter -ul; feminine -a. Say each "
        "one both ways.", pause=800)
for cue, ans, v in [("a blouse, the blouse", "O bluză, bluza.", "f"),
                    ("a dress, the dress", "O rochie, rochia.", "f"),
                    ("a skirt, the skirt", "O fustă, fusta.", "f"),
                    ("a t-shirt, the t-shirt", "Un tricou, tricoul.", "m"),
                    ("a tie, the tie", "O cravată, cravata.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Sentence drill — where is it ═════════════════════════════════════════
ep.narr("Now the whole question and answer, out loud.", pause=P_SECTION,
        chapter="Drill")
for cue, ans, v in [
    ("Where is the blouse?", "Unde e bluza?", "f"),
    ("Where is the blouse? — On the chair.", "Unde e bluza? Pe scaun.", "f"),
    ("Where is the dress? — In the wardrobe.", "Unde e rochia? În dulap.", "f"),
    ("Here is the skirt!", "Iată fusta!", "f"),
    ("Where is the tie? — On the table.", "Unde e cravata? Pe masă.", "f"),
    ("Where is the t-shirt? — On the chair.", "Unde e tricoul? Pe scaun.", "m"),
    ("The dress is in the wardrobe.", "Rochia e în dulap.", "f"),
    ("Here is the blouse, and here is the skirt.",
     "Iată bluza, iar iată fusta.", "f"),
    ("The tie is on the table.", "Cravata e pe masă.", "f"),
    ("Where is the t-shirt?", "Unde e tricoul?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The masculine -ul gets clipped in speech — "
        "tricou' for tricoul — but the feminine -a stays put. Bluza, rochia, "
        "fusta, said in full. So the ending you have to hold onto is the "
        "feminine one; the masculine one you will often not even hear.",
        pause=P_SECTION, chapter="How people really say it")

# ═══ 5. Review — scheduled from earlier episodes ═════════════════════════════
ep.review_auto()

# ═══ 6. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Unde e bluza? Bluza e pe scaun.",
    "Rochia e în dulap. Iată fusta!",
    "Unde e cravata? Cravata e pe masă.",
    "Iar tricoul e pe scaun.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The morning again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Feminine -a, masculine -ul. Next time: what these things look like — "
        "white, black, blue.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: name three of your own things with 'the' on the "
        "end — bluza, tricoul, whatever they are. Pe curând!",
        pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("5", []))
