"""
Episode 07E — "Cât costă?" (Lecția 7 "Portrete", memory-first, part 5)

Seven new items: six to ten (șase, șapte, opt, nouă, zece) as one run, and
the chapter's money words, leu (Romanian currency, plural lei) and ban, met
in its plural bani — money. The book's own drills supply the sentences ("Câte
ciocolate vrea ea? (trei)", "Câți ani are fratele lui? (nouă)", "Dvs. aveți
bani?"). nouă (nine) sounds exactly like nouă (new, from 07A) — said aloud as a
pair, since the learner will hear both. 07C's food words get prices here, and
07D's one-to-five come back in every count.

Scene: a market stall — the buyer asks the price of one thing after another,
so the numbers repeat because that is shopping. The dialogue uses 07A's spoken
layer as ordinary speech (Ce doriți?, Aș vrea).
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["șase", "șapte", "opt", "nouă", "zece", "leu", "bani"]
GLUE = {"Cât costă? / costă": "How much is it? / it costs — a chunk"}

ep = Episode(number=7, lesson=7, part="e", title="Cât costă?",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună ziua! Ce doriți?"),
    ("radu", "Aș vrea o pâine. Cât costă?"),
    ("dana", "Șase lei."),
    ("radu", "Și o ciocolată?"),
    ("dana", "Zece lei."),
    ("radu", "Și două beri?"),
    ("dana", "Opt lei."),
    ("radu", "Poftiți banii."),
    ("dana", "Mulțumesc!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A market stall: how much is it. Six to ten, and money.", pause=P_SECTION)

# ═══ 1. Seven items — introduced then recalled at once ═══════════════════════
ep.narr("Six to ten first, as a run, then the money words.", pause=800,
        chapter="New words")
ep.new_item("șase", "six", "șase", "m",
            teach_ro="Pâinea costă șase lei.", teach_en="The bread costs six lei.")
ep.new_item("șapte", "seven", "șapte", "f",
            teach_ro="Berea costă șapte lei.", teach_en="The beer costs seven lei.")
ep.new_item("opt", "eight", "opt", "m",
            teach_ro="Fiul meu are opt ani.", teach_en="My son is eight.")
ep.new_item("nouă", "nine", "nouă", "f",
            teach_ro="Fiica ei are nouă ani.", teach_en="Her daughter is nine.")
ep.new_item("zece", "ten", "zece", "m",
            teach_ro="Ciocolata costă zece lei.", teach_en="The chocolate costs ten lei.")
ep.new_item("leu", "one unit of Romanian money", "un leu", "f",
            teach_ro="un leu, doi lei", teach_en="one, two — of Romanian money")
ep.new_item("bani", "money", "bani", "m",
            teach_ro="Am nevoie de bani.", teach_en="I need money.")

ep.narr("Count with him, six to ten.", pause=P_SHORT)
ep.drill("Six to ten.", "șase, șapte, opt, nouă, zece", "m")
ep.narr("And all the way, one to ten.", pause=P_SHORT)
ep.drill("One to ten.", "unu, doi, trei, patru, cinci, șase, șapte, opt, nouă, zece", "f")
ep.narr("Mixed, just the word.", pause=800)
for cue, ans, v in [("eight", "opt", "m"), ("money", "bani", "f"), ("six", "șase", "m"),
                    ("ten", "zece", "f"), ("one unit of Romanian money", "un leu", "m"), ("nine", "nouă", "f"),
                    ("seven", "șapte", "m"), ("four", "patru", "f"), ("two", "doi", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Nine and new ═════════════════════════════════════════════════════════
ep.narr("Nine sounds exactly like new for a her-word from the shop episode. "
        "Listen — a new dress, nine lei:", pause=800, chapter="Nine and new")
ep.example(None, "O rochie nouă, nouă lei.", "f", 2000)
ep.narr("Which one it is, the place in the sentence tells you. Say it:", pause=P_SHORT)
ep.drill("A new dress, nine lei.", "O rochie nouă, nouă lei.", "m")

# ═══ 3. Prices ═══════════════════════════════════════════════════════════════
ep.narr("The money word has its own plural, and asking the price is a fixed "
        "phrase — how much is it. Listen:", pause=800, chapter="Prices")
ep.example(None, "Cât costă? Șase lei.", "m", 1800)
ep.example(None, "Cât costă berea? Șapte lei.", "f", 1800)
for cue, ans, v in [
    ("two lei", "doi lei", "m"), ("ten lei", "zece lei", "f"),
    ("How much is it?", "Cât costă?", "m"),
    ("How much is the bread? — Six lei.", "Cât costă pâinea? — Șase lei.", "f"),
    ("How much is the ice cream? — Five lei.", "Cât costă înghețata? — Cinci lei.", "m"),
    ("The chocolate costs ten lei.", "Ciocolata costă zece lei.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I need money.", "Am nevoie de bani.", "m", {}),
    ("I don't have money.", "Nu am bani.", "f", {"accept": ["N-am bani."]}),
    ("I have ten lei.", "Am zece lei.", "m", {}),
    ("My son is eight.", "Fiul meu are opt ani.", "f", {}),
    ("Her daughter is nine.", "Fiica ei are nouă ani.", "m", {}),
    ("How many chocolates do you want? — Eight.", "Câte ciocolate vrei? — Opt.", "f", {}),
    ("I'd like two beers.", "Aș vrea două beri.", "m", {"accept": ["Vreau două beri."]}),
    ("We need money.", "Avem nevoie de bani.", "f", {}),
    ("The beer costs seven lei.", "Berea costă șapte lei.", "m", {}),
    ("How old is his brother? — Nine.", "Câți ani are fratele lui? — Nouă.", "f", {}),
    ("Seven children.", "Șapte copii.", "m", {}),
    ("Here's the money. Politely.", "Poftiți banii.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. At the till, for the total of everything, people "
        "don't ask the price — they ask what it comes to. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Cât face?", "m", SLOW, 1600)
ep.drill("What does it come to?", "Cât face?", "f")
ep.narr("And handing over the money, the word you heard at the end of the "
        "dialogue — here you are. Between friends it's shorter. Listen:", pause=P_SHORT)
ep.ro("Poftiți. Poftim.", "f", SLOW, 1800)
ep.narr("Polite, then friendly.", pause=P_SECTION)

# ═══ 6. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The market again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("One to ten, and what things cost.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
