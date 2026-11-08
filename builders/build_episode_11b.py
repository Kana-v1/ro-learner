"""
Episode 11B — "Ce beți?" (Lecția 11 "La munte", memory-first, part 2)

Six items: apă, lapte, beau, mănânc, repede, încet. Lapte comes from the
chapter's own drink list ("A bea: lapte, apă minerală, limonadă, ceai, cafea,
bere") and încet from its "Cum descriem o acțiune" section (repede, încet,
bine, rău, atent; mult, puțin) rather than its VOCABULAR.

Grammar: a bea, which changes its sound like a vedea — beau, bei, bea, bem,
beți, beau — taught one form at a time in the 11A way (each heard in a short
sentence, recalled bare, used, then the next), then drilled out of order. See
gets its we-form, which 11A left out. Eat gets I, you and she only — its we
and you-all forms change the start of the word, so they wait.

The communicative point is the book's "Cum?": how you do something goes
straight after the verb — "El vede bine", "Bunicul mănâncă încet".

11A's spoken layer (Ne vedem!) comes back as an ordinary drill.

Scene: a waitress taking drinks round a family table — "Ce beți?" is her
job, so drink comes round for everyone at the table.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["apă", "lapte", "beau", "mănânc", "repede", "încet"]
GLUE = {"Bună seara": "good evening — a chunk",
        "minerală": "mineral — in 'apă minerală', the book's phrase"}

ep = Episode(number=11, lesson=11, part="b", title="Ce beți?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună seara! Ce beți?"),
    ("radu", "Eu beau apă. Copilul bea lapte."),
    ("dana", "Și bunicul?"),
    ("radu", "Bunicul bea bere."),
    ("elena", "Tata, bunicul mănâncă încet!"),
    ("radu", "Da, dar tu mănânci repede!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Dinner at the mountain hotel: a waitress, a father, a child, and a "
        "grandfather who takes his time. Drink and eat, fast and slowly.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("apă", "water", "apă", "f",
            teach_ro="Apă, vă rog.", teach_en="Water, please.")
ep.new_item("lapte", "milk", "lapte", "m",
            teach_ro="Lapte și pâine.", teach_en="Milk and bread.")
ep.new_item("beau", "I drink", "beau", "f",
            teach_ro="Beau apă.", teach_en="I drink water.")
ep.new_item("mănânc", "I eat", "mănânc", "m",
            teach_ro="Mănânc pâine.", teach_en="I'm eating bread.")
ep.new_item("repede", "quickly, fast", "repede", "f",
            teach_ro="Mănânc repede.", teach_en="I eat quickly.")
ep.new_item("încet", "slowly", "încet", "m",
            teach_ro="Beau încet.", teach_en="I drink slowly.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I eat", "mănânc", "f"), ("slowly", "încet", "m"), ("water", "apă", "f"),
                    ("I drink", "beau", "m"), ("quickly", "repede", "f"), ("milk", "lapte", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Drink — one form at a time ═══════════════════════════════════════════
ep.narr("Drink changes its sound like see, so again one form at a time. To a "
        "friend: what are you drinking? Listen:", pause=800,
        chapter="Drink, one form at a time")
ep.ro("Ce bei?", "f", SLOW, 1600)
ep.drill("you drink — to a friend", "bei", "m")
ep.drill("You drink milk. To a friend.", "Bei lapte.", "f")

ep.narr("She drinks, he drinks. Listen:", pause=800)
ep.ro("Copilul bea lapte.", "m", SLOW, 1800)
ep.drill("she drinks", "bea", "f")
ep.drill("Grandpa drinks beer.", "Bunicul bea bere.", "m")

ep.narr("Politely, or to a group — the waitress's word. Listen:", pause=800)
ep.ro("Ce beți?", "f", SLOW, 1600)
ep.drill("you drink — politely", "beți", "m")
ep.drill("Do you drink milk? Politely.", "Beți lapte?", "f")

ep.narr("We drink — short. Listen:", pause=800)
ep.ro("Bem apă.", "m", SLOW, 1500)
ep.drill("we drink", "bem", "f")
ep.drill("We drink beer.", "Bem bere.", "m")

ep.narr("And they sounds like I — as with see. Listen:", pause=800)
ep.ro("Ei beau apă.", "f", SLOW, 1600)
ep.drill("they drink", "ei beau", "m")

ep.narr("Now mixed, and not in order.", pause=800)
for cue, ans, v in [("we drink", "bem", "f"), ("she drinks", "bea", "m"),
                    ("you drink — to a friend", "bei", "f"), ("I drink", "beau", "m"),
                    ("they drink", "ei beau", "f"), ("you drink — politely", "beți", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. See, we — and eat ════════════════════════════════════════════════════
ep.narr("See, from last time, has a we-form too — short, like we drink. Listen:",
        pause=800, chapter="See and eat")
ep.ro("Vedem muntele.", "m", SLOW, 1800)
ep.drill("we see", "vedem", "f")
ep.drill("We see the peak.", "Vedem vârful.", "m")

ep.narr("Eat, to a friend. Listen:", pause=800)
ep.ro("Mănânci repede!", "f", SLOW, 1800)
ep.drill("you eat — to a friend", "mănânci", "m")
ep.narr("He eats, she eats. Listen:", pause=800)
ep.ro("Bunicul mănâncă încet.", "m", SLOW, 1800)
ep.drill("he eats", "mănâncă", "f")
for cue, ans, v in [("I eat", "mănânc", "m"), ("she eats", "mănâncă", "f"),
                    ("you eat — to a friend", "mănânci", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. How you do it ════════════════════════════════════════════════════════
ep.narr("How you do something comes straight after the verb. From the book — "
        "listen:", pause=800, chapter="How you do it")
ep.ro("El vede bine.", "f", SLOW, 1600)
ep.narr("He sees well. Fast, slowly, carefully, a lot, a little — they all go "
        "there. Build them.", pause=P_SHORT)
for cue, ans, v in [("I eat slowly.", "Mănânc încet.", "m"),
                    ("The child eats fast.", "Copilul mănâncă repede.", "f"),
                    ("She draws carefully.", "Ea desenează atent.", "m"),
                    ("We drink a lot.", "Bem mult.", "f"),
                    ("My colleague works well.", "Colegul meu lucrează bine.", "m"),
                    ("They eat a little.", "Ei mănâncă puțin.", "f"),
                    ("How does grandpa eat?", "Cum mănâncă bunicul?", "m")]:
    ep.drill(cue, ans, v)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I drink water.", "Beau apă.", "m", {}),
    ("What are you drinking? Politely.", "Ce beți?", "f", {}),
    ("The child drinks milk.", "Copilul bea lapte.", "m", {}),
    ("Grandpa eats slowly.", "Bunicul mănâncă încet.", "f", {}),
    ("You eat fast! To a friend.", "Mănânci repede!", "m", {}),
    ("We drink mineral water.", "Bem apă minerală.", "f", {}),
    ("They don't drink beer.", "Ei nu beau bere.", "m", {}),
    ("Do you drink a lot of milk? To a friend.", "Bei mult lapte?", "f", {}),
    ("I drink milk and eat bread.", "Beau lapte și mănânc pâine.", "m", {}),
    ("She sees well.", "Ea vede bine.", "f", {}),
    ("We see the mountain.", "Vedem muntele.", "m", {}),
    ("See you! To a friend.", "Ne vedem!", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Before eating, and when the waitress brings the "
        "food, you'll hear — listen:", pause=800, chapter="How people really say it")
ep.ro("Poftă bună!", "f", SLOW, 1500)
ep.narr("Enjoy your meal! And the everyday invitation at work uses we drink — "
        "listen:", pause=P_SHORT)
ep.ro("Bem o cafea?", "m", SLOW, 1500)
ep.narr("Shall we have a coffee? Just to recognise for now.", pause=P_SECTION)

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("Dinner again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Drink and eat — fast, slowly, and one form at a time.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
