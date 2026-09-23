"""
Episode 05A — "Unde e paltonul?" (Lecția 5, memory-first re-cut, part 1 of 5)

The rebuild. The old 05A crammed sixteen clothing words plus the definite
article into one sitting and nothing stuck — a heard-once word buried in a pile
of fifteen similar words cannot be produced. Lecția 5 is now five short
episodes of about six new items each, and most of every episode is retrieval,
not new material.

This first part takes just four garments — palton, pulover, cămașă, pantaloni —
plus unde and iată, and states the masculine/neuter half of the definite
article (-ul). Each item is introduced, then recalled bare on the spot, then
assembled into whole sentences later, then it returns on the spacing schedule
in 05B and beyond. The feminine -a, the rest of the wardrobe, colours and
adjectives are their own parts.

Scene: a morning, someone who can't find his things. "Unde e paltonul?" — the
question repeats because a person hunting for clothes really does ask it over
and over, and every answer is a noun wearing the article, so the form drills
itself. Rooms and furniture from episode 4 (dulap, scaun) are ordinary speech.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

# Six new items — four garments plus unde and iată. The article is grammar,
# not a vocab-list item. Everything else from Lecția 5 waits for 05B-05E.
REQUIRED = ["palton", "pulover", "cămașă", "pantaloni", "unde", "iată"]

GLUE = {"Sanda / Radu": "names"}

ep = Episode(number=5, lesson=5, part="a", title="Unde e paltonul?",
             source="Limba care ne unește, nivelul I — Lecția 5 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună dimineața, Radu!"),
    ("radu",  "Bună dimineața, Sanda! Unde e paltonul?"),
    ("dana",  "Paltonul e în dulap."),
    ("radu",  "Și puloverul?"),
    ("dana",  "Puloverul e pe scaun. Iată puloverul."),
    ("radu",  "Unde e cămașa?"),
    ("dana",  "Cămașa e în dulap, de asemenea."),
    ("radu",  "Dar pantalonii?"),
    ("dana",  "Pantalonii sunt pe scaun."),
    ("radu",  "Mulțumesc!"),
    ("dana",  "Cu plăcere."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A morning, and someone who cannot find his clothes. Just four things "
        "today — a coat, a sweater, a shirt, trousers — and the word for 'the' "
        "that rides on the end of each. Most of this episode is you producing, "
        "not me explaining.", pause=P_SECTION)

# ═══ 1. The four garments — each introduced, then recalled at once ════════════
# new_item() does the sandwich AND an immediate bare-word retrieval, so the word
# is retrieved seconds after it is first heard, not ten minutes later in a pile.
ep.narr("Four things, one at a time. You will say each one back before we move "
        "on.", pause=800, chapter="Four garments")
ep.new_item("palton", "a coat", "un palton", "m")
ep.new_item("pulover", "a sweater", "un pulover", "m")
ep.new_item("cămașă", "a shirt", "o cămașă", "f")
ep.narr("And the one that is always plural, like in English — trousers.",
        pause=P_SHORT)
ep.new_item("pantaloni", "trousers", "niște pantaloni", "m",
            teach_ro="niște pantaloni", teach_en="a pair of trousers")

# A first mixed retrieval of the bare words, cues out of order, before any
# grammar — proving the four are held before we add the article.
ep.narr("The four together now, mixed up. Just the word.", pause=800)
for cue, ans, v in [("a shirt", "o cămașă", "f"),
                    ("trousers", "niște pantaloni", "m"),
                    ("a coat", "un palton", "m"),
                    ("a sweater", "un pulover", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. unde and iată ════════════════════════════════════════════════════════
ep.narr("Two small words for looking. Unde — where. And iată — here it is, "
        "said as you find or point at something.", pause=800,
        chapter="unde and iată")
ep.new_item("unde", "where", "unde", "f",
            teach_ro="Unde e paltonul?", teach_en="Where is the coat?")
ep.new_item("iată", "here it is", "iată", "m",
            teach_ro="Iată paltonul!", teach_en="Here is the coat!")

# ═══ 3. Grammar — the definite article, masculine/neuter -ul ═════════════════
ep.narr("Now that little ending. Since episode one you have heard -ul stuck on "
        "the end of words, and I called it 'the' and moved on. Here it is: "
        "Romanian's word for 'the' does not stand in front of the noun, it "
        "rides on the back of it. Masculine and neuter add -ul.",
        pause=800, chapter="The article: -ul")
for r, e in [("un palton, paltonul", "a coat, the coat"),
             ("un pulover, puloverul", "a sweater, the sweater")]:
    ep.teach(r, e, "m")
ep.narr("Trousers, being plural, take -i on the end: pantaloni, pantalonii.",
        pause=P_SHORT)
ep.teach("niște pantaloni, pantalonii", "some trousers, the trousers", "m")
ep.narr("So: the ending is the article. Say each one both ways.", pause=800)
for cue, ans, v in [("a coat, the coat", "Un palton, paltonul.", "m"),
                    ("a sweater, the sweater", "Un pulover, puloverul.", "m"),
                    ("the trousers", "Pantalonii.", "m")]:
    ep.drill(cue, ans, v)
ep.narr("The feminine ending is different — that is next episode. Today you "
        "have heard cămașa; just hold it.", pause=P_SECTION)

# ═══ 4. Sentence drill — where is it, it's here ══════════════════════════════
# Only now, once the words are retrievable, do we ask for whole sentences.
ep.narr("Now the whole thing out loud — where is it, and the answer with the "
        "article on the end.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("Where is the coat?", "Unde e paltonul?", "m"),
    ("Where is the coat? — In the wardrobe.", "Unde e paltonul? În dulap.", "m"),
    ("Where is the sweater? — On the chair.",
     "Unde e puloverul? Pe scaun.", "m"),
    ("Here is the sweater.", "Iată puloverul!", "m"),
    ("Where is the shirt?", "Unde e cămașa?", "f"),
    ("Where are the trousers?", "Unde sunt pantalonii?", "m"),
    ("Where are the trousers? — On the chair.",
     "Unde sunt pantalonii? Pe scaun.", "m"),
    ("Here is the coat!", "Iată paltonul!", "m"),
    ("The coat is in the wardrobe.", "Paltonul e în dulap.", "m"),
    ("The trousers are on the chair.", "Pantalonii sunt pe scaun.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes in Bucharest. The -ul ending you just learned is "
        "exactly the one speech clips off. You learn paltonul, you hear:",
        pause=800, chapter="How people really say it")
for r in ["paltonu'", "puloveru'"]:
    ep.ro(r, "m", SLOW, 1000)
ep.narr("Same word, dropped L. The full form is the careful one; the clipped "
        "one is the street. And the word for clothes as a whole is haine — "
        "unde sunt hainele — but that is for later.", pause=P_SECTION)

# ═══ 6. Review — scheduled retrieval from earlier episodes ═══════════════════
# Pulled automatically from state.json: whatever is due at 05A on the +1/+3/...
# schedule (here, items from episodes 4B and 3B). This is the engine the old
# design lacked — earlier words come back instead of being taught once and lost.
ep.review_auto()

# ═══ 7. A short passage ══════════════════════════════════════════════════════
ep.narr("A few sentences run together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Unde e paltonul? Paltonul e în dulap.",
    "Puloverul e pe scaun. Iată puloverul.",
    "Unde e cămașa? Cămașa e în dulap.",
    "Pantalonii sunt pe scaun.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The morning again. Same recording — notice how much of it you now "
        "follow.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Four words, and every answer wore the article — paltonul, puloverul. "
        "Next time: the feminine ending, and more of the wardrobe.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: open your own wardrobe and, out loud, ask unde e — "
        "then answer with the article on the end. Pe curând!", pause=1500,
        chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("5", []))
