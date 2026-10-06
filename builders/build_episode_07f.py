"""
Episode 07F — "Masa veche" (Lecția 7 "Portrete", memory-first, part 6)

Six new items: eleven to nineteen taught as one rule — the unit plus
-sprezece, "on ten" — with its two irregulars and the gendered twelve
registered as items (unsprezece, doisprezece, paisprezece, șaisprezece), and
the chapter's last adjectives for things, vechi and verde. 13, 15, 17, 18, 19
follow the rule and are drilled, not counted as new. Forms follow the book's
table (11 unsprezece … 19 nouăsprezece, "12 doisprezece, douăsprezece") and its
agreement models: "bloc vechi – blocuri vechi", "canapea veche – canapele
vechi", "perete verde – pereți verzi", "tablă verde – table verzi".

Scene: a second-hand stall. Everything is old, the buyer asks the price of
one piece after another, and the seller haggles — so the teen numbers and
old/green repeat because that is buying furniture at a flea market. 07E's
spoken layer (Poftiți) is ordinary speech here.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["unsprezece", "doisprezece", "paisprezece", "șaisprezece", "vechi", "verde"]
GLUE = {}

ep = Episode(number=7, lesson=7, part="f", title="Masa veche",
             source="Limba care ne unește, nivelul I — Lecția 7 (partea F)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Bună ziua! Cât costă masa veche?"),
    ("radu",  "Unsprezece lei."),
    ("elena", "Și scaunul verde?"),
    ("radu",  "Paisprezece lei."),
    ("elena", "E vechi!"),
    ("radu",  "Da, e vechi, dar e bun. Doisprezece lei."),
    ("elena", "Bine. Și tabloul?"),
    ("radu",  "Șaisprezece lei."),
    ("elena", "Poftiți banii."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "elena", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A second-hand stall: old things, green things, and prices from eleven "
        "to nineteen.", pause=P_SECTION)

# ═══ 1. Eleven to nineteen: one rule ═════════════════════════════════════════
ep.narr("Eleven to nineteen are one rule: the small number, then a piece that "
        "means on ten. One on ten, two on ten. Listen:", pause=800,
        chapter="Eleven to nineteen")
ep.example(None, "unsprezece, doisprezece, treisprezece", "m", 2200)
ep.narr("Four of them to learn as words: eleven, twelve, and two that bend the "
        "rule.", pause=P_SHORT)
ep.new_item("unsprezece", "eleven", "unsprezece", "m",
            teach_ro="Masa costă unsprezece lei.", teach_en="The table costs eleven lei.")
ep.new_item("doisprezece", "twelve", "doisprezece", "f",
            teach_ro="doisprezece lei", teach_en="twelve lei")
ep.new_item("paisprezece", "fourteen", "paisprezece", "m",
            teach_ro="Scaunul costă paisprezece lei.", teach_en="The chair costs fourteen lei.")
ep.new_item("șaisprezece", "sixteen", "șaisprezece", "f",
            teach_ro="Fiul meu are șaisprezece ani.", teach_en="My son is sixteen.")
ep.narr("Fourteen and sixteen shorten the small number. The rest follow the "
        "rule exactly. Thirteen, fifteen, seventeen — listen:", pause=P_SHORT)
ep.example(None, "treisprezece, cincisprezece, șaptesprezece", "m", 2200)
ep.example(None, "optsprezece, nouăsprezece", "f", 1800)
ep.narr("Count with him, eleven to nineteen. Take your time.", pause=P_SHORT)
ep.drill("Eleven to nineteen.",
         "unsprezece, doisprezece, treisprezece, paisprezece, cincisprezece, "
         "șaisprezece, șaptesprezece, optsprezece, nouăsprezece", "m")
ep.narr("Mixed, just the number.", pause=800)
for cue, ans, v in [("fourteen", "paisprezece", "m"), ("eleven", "unsprezece", "f"),
                    ("seventeen", "șaptesprezece", "m"), ("sixteen", "șaisprezece", "f"),
                    ("twelve", "doisprezece", "m"), ("thirteen", "treisprezece", "f"),
                    ("nineteen", "nouăsprezece", "m"), ("fifteen", "cincisprezece", "f"),
                    ("eighteen", "optsprezece", "m"), ("ten", "zece", "f")]:
    ep.recall_word(cue, ans, v)
ep.narr("Twelve has a her-form, like two. Listen:", pause=P_SHORT)
ep.example(None, "doisprezece băieți, douăsprezece fete", "m", 2000)
ep.drill("twelve girls", "douăsprezece fete", "f")

# ═══ 2. Old and green ════════════════════════════════════════════════════════
ep.narr("Two more words, for things.", pause=800, chapter="Old and green")
ep.new_item("vechi", "old — about a thing", "vechi", "m",
            teach_ro="Scaunul e vechi.", teach_en="The chair is old.")
ep.new_item("verde", "green", "verde", "f",
            teach_ro="un scaun verde", teach_en="a green chair")
ep.narr("For her, old changes its ending; green, like big, does not. For more "
        "than one, both end in an i sound. Listen:", pause=P_SHORT)
ep.example(None, "un palton vechi, o rochie veche, case vechi", "m", 2200)
ep.example(None, "un scaun verde, o masă verde, scaune verzi", "f", 2200)
for cue, ans, v in [
    ("an old coat", "un palton vechi", "m"), ("an old dress", "o rochie veche", "f"),
    ("old houses", "case vechi", "m"), ("a green table", "o masă verde", "f"),
    ("green chairs", "scaune verzi", "m"), ("old and green", "vechi și verde", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("The old table costs eleven lei.", "Masa veche costă unsprezece lei.", "m", {}),
    ("The green chair costs fourteen lei.", "Scaunul verde costă paisprezece lei.", "f", {}),
    ("The chair is old, but good.", "Scaunul e vechi, dar bun.", "m",
     {"accept": ["Scaunul e vechi, dar e bun."]}),
    ("My son is sixteen.", "Fiul meu are șaisprezece ani.", "f", {}),
    ("Her daughter is twelve.", "Fiica ei are doisprezece ani.", "m", {}),
    ("How much is the green table? — Thirteen lei.", "Cât costă masa verde? — Treisprezece lei.", "f", {}),
    ("I have fifteen lei.", "Am cincisprezece lei.", "m", {}),
    ("The flat is old.", "Apartamentul e vechi.", "f", {}),
    ("I want an old picture.", "Vreau un tablou vechi.", "m", {}),
    ("The dress is old, but pretty.", "Rochia e veche, dar frumoasă.", "f",
     {"accept": ["Rochia e veche, dar e frumoasă."]}),
    ("We need green chairs.", "Avem nevoie de scaune verzi.", "m", {}),
    ("Here's the money. Politely.", "Poftiți banii.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Nobody says these numbers in full. The on-ten "
        "part shrinks to a short ending. Listen — eleven, twelve, fourteen, "
        "sixteen, the way you'll hear them:", pause=800, chapter="How people really say it")
ep.ro("unșpe, doișpe, paișpe, șaișpe", "m", SLOW, 2200)
ep.narr("And at a normal pace — prices at a stall:", pause=P_SHORT)
ep.ro("Unșpe lei. Paișpe lei.", "f", NORMAL, 1600)
ep.narr("Recognise them; say the full ones until they come easily.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto()

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The stall again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("Up to nineteen, and old and green.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("7", []))
