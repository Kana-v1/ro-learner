"""
Episode 11D — "Încape în portbagaj?" (Lecția 11 "La munte", memory-first, part 4)

Six items: autocar, valiză, portbagaj, plec, urc, încape. Verbs one form at a
time, as in 11A: the coach leaves (pleacă), we leave (plecăm); get on,
politely (urcați), he gets on (urcă), and we climb built from we leave
(urcăm). Încape is taught as "it fits" — things fit, people rarely say "I
fit". The you-to-a-friend forms (pleci, urci) wait.

Three fixes from the 11A and 11B results:
- the learner's feedback on 11A — "how is frumos different from frumoasă"
  (Soarele e frumos) — answered by ear: the small word before a noun
  decides the describing word, and you can't tell it from the noun's end, so
  each word is learnt with its small word;
- she sees came out as I see in 11A, five times (Ea nu vede → "Ea nu văd"),
  so the two are drilled as a pair;
- examinez, missed twelve times across five sessions, nearly always as the
  you-form examinezi (the other -ez verbs are heard fine), drilled as a pair;
- bei and beți, which Apple's recogniser heard as băi and băieți all through
  11B (Whisper wasn't downloaded), asked again with those accepted.

11C's spoken layer (Călătorie plăcută!, Pot să rezerv) comes back as
ordinary drills.

Scene: a coach driver loading luggage before the trip to the mountains —
does it fit, get on, we're leaving — said to each passenger in turn.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["autocar", "valiză", "portbagaj", "plec", "urc", "încape"]
GLUE = {"Gata": "right then, ready — a chunk",
        "turiștii": "the tourists — the book's word"}

ep = Episode(number=11, lesson=11, part="d", title="Încape în portbagaj?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Autocarul pleacă la opt. Urcați, vă rog!"),
    ("dana", "Și valiza? Încape în portbagaj?"),
    ("radu", "Da, încape."),
    ("elena", "Și valiza mea? E mare."),
    ("radu", "Nu încape. Dar e loc aici."),
    ("elena", "Mulțumesc!"),
    ("radu", "Gata, plecăm!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Eight in the morning, a coach to the mountains, and a driver loading "
        "suitcases. Leave, get on — and does it fit?", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("autocar", "a coach — a long-distance bus", "un autocar", "f",
            teach_ro="Un autocar mare.", teach_en="A big coach.")
ep.new_item("valiză", "a suitcase", "o valiză", "m",
            teach_ro="O valiză mică.", teach_en="A small suitcase.")
ep.new_item("portbagaj", "the boot — of a car or a coach", "portbagajul", "f",
            teach_ro="Portbagajul e mare.", teach_en="The boot is big.")
ep.new_item("plec", "I leave, I'm off", "plec", "m",
            teach_ro="Plec la munte.", teach_en="I'm off to the mountains.")
ep.new_item("urc", "I get on — and I climb", "urc", "f",
            teach_ro="Urc în autocar.", teach_en="I get on the coach.")
ep.new_item("încape", "it fits — in the boot, in the case", "încape", "m",
            teach_ro="Valiza încape.", teach_en="The suitcase fits.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I get on", "urc", "m"), ("a suitcase", "o valiză", "f"), ("it fits", "încape", "m"),
                    ("a coach", "un autocar", "f"), ("I leave", "plec", "m"),
                    ("the boot", "portbagajul", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Leave and get on — one form at a time ════════════════════════════════
ep.narr("Leave: the coach leaves. Listen:", pause=800, chapter="Leave and get on")
ep.ro("Autocarul pleacă la opt.", "f", SLOW, 1800)
ep.drill("it leaves — the coach", "pleacă", "m")
ep.drill("The train leaves at nine.", "Trenul pleacă la nouă.", "f")

ep.narr("We leave. Listen:", pause=800)
ep.ro("Plecăm acum.", "m", SLOW, 1600)
ep.drill("we leave", "plecăm", "f")
ep.drill("We leave at eight.", "Plecăm la opt.", "m")

ep.narr("Get on — the driver, politely. Listen:", pause=800)
ep.ro("Urcați, vă rog!", "f", SLOW, 1600)
ep.drill("you get on — politely", "urcați", "m")
ep.drill("Do you get on here? Politely.", "Urcați aici?", "f")

ep.narr("He gets on. Listen:", pause=800)
ep.ro("Dan urcă în autocar.", "m", SLOW, 1800)
ep.drill("he gets on", "urcă", "f")
ep.drill("Mum gets on the coach.", "Mama urcă în autocar.", "m")

ep.narr("Get on also means climb. We climb — build it like we leave.", pause=P_SHORT)
ep.drill("we climb", "urcăm", "f")
ep.drill("We climb slowly.", "Urcăm încet.", "m")

ep.narr("And fits, said of things. Listen:", pause=800)
ep.ro("Nu încape.", "f", SLOW, 1500)
ep.drill("It doesn't fit.", "Nu încape.", "m")
ep.drill("The suitcase fits in the boot.", "Valiza încape în portbagaj.", "f")

ep.narr("Now mixed, and not in order.", pause=800)
for cue, ans, v in [("the coach leaves", "autocarul pleacă", "m"), ("I get on", "urc", "f"),
                    ("we leave", "plecăm", "m"), ("it fits", "încape", "f"),
                    ("you get on — politely", "urcați", "m"), ("I leave", "plec", "f"),
                    ("he gets on", "urcă", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. His-word or her-word ═════════════════════════════════════════════════
ep.narr("A question from last time: why does the sun take this form of lovely? "
        "Listen:", pause=800, chapter="His-word or her-word")
ep.ro("Soarele e frumos.", "f", SLOW, 1600)
ep.narr("Because sun is a his-word — listen to the small word before it:",
        pause=P_SHORT)
ep.ro("un soare", "m", SLOW, 1400)
ep.narr("A her-word has the other small word, and the other form of lovely. "
        "Listen:", pause=P_SHORT)
ep.ro("o valiză frumoasă", "f", SLOW, 1600)
ep.narr("You can't tell from how a word ends. So learn each word with its small "
        "word — that decides the describing word.", pause=800)
for cue, ans, v in [("a lovely suitcase", "o valiză frumoasă", "m"),
                    ("a lovely mountain", "un munte frumos", "f"),
                    ("a new coach", "un autocar nou", "m"),
                    ("a new suitcase", "o valiză nouă", "f"),
                    ("The sun is lovely.", "Soarele e frumos.", "m"),
                    ("The suitcase is small.", "Valiza e mică.", "f"),
                    ("The boot is small.", "Portbagajul e mic.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 4. I see, she sees ══════════════════════════════════════════════════════
ep.narr("Your results mix I see and she sees. Just the two — listen:", pause=800,
        chapter="I see, she sees")
ep.ro("Eu văd. Ea vede.", "m", SLOW, 2000)
for cue, ans, v in [("she sees", "vede", "f"), ("I see", "văd", "m"),
                    ("She sees the coach.", "Ea vede autocarul.", "f"),
                    ("I see the suitcase.", "Văd valiza.", "m"),
                    ("He doesn't see the suitcase.", "Nu vede valiza.", "f"),
                    ("I don't see the coach.", "Nu văd autocarul.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 5. I examine ════════════════════════════════════════════════════════════
ep.narr("And the word you've missed most: I examine. You've been giving the "
        "you-form. Listen to the two:", pause=800, chapter="I examine")
ep.ro("Eu examinez. Tu examinezi.", "f", SLOW, 2200)
for cue, ans, v in [("I examine", "examinez", "m"),
                    ("you examine — to a friend", "examinezi", "f"),
                    ("I examine the documents.", "Examinez actele.", "m"),
                    ("I'm looking over your documents. Politely.",
                     "Examinez actele dumneavoastră.", "f"),
                    ("I examine", "examinez", "m")]:
    ep.drill(cue, ans, v)

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'm off to the mountains.", "Plec la munte.", "m", {}),
    ("The coach leaves at eight.", "Autocarul pleacă la opt.", "f", {}),
    ("Does the suitcase fit in the boot?", "Valiza încape în portbagaj?", "m", {}),
    ("Yes, it fits.", "Da, încape.", "f", {}),
    ("My suitcase is big.", "Valiza mea e mare.", "m", {}),
    ("There's room here.", "E loc aici.", "f", {}),
    ("Can I get on?", "Pot urca?", "m", {}),
    ("Where's the coach leaving for?", "Unde pleacă autocarul?", "f", {}),
    ("The tourists climb fast.", "Turiștii urcă repede.", "m", {}),
    ("Have a good trip!", "Călătorie plăcută!", "f", {}),
    # Apple's recogniser turns these into the common words băi and băieți
    # (11B: the learner said them right and was marked wrong), so the
    # mishearings are accepted — nobody answering "you drink" means "boys".
    ("you drink — to a friend", "bei", "m", {"accept": ["băi"]}),
    ("What are you drinking? Politely.", "Ce beți?", "f", {"accept": ["Ce băieți?"]}),
    ("you drink — politely", "beți", "m", {"accept": ["băieți"]}),
    ("Can I book? The way people say it.", "Pot să rezerv?", "m",
     {"accept": ["Pot rezerva?"]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. To get people moving, you'll hear this "
        "everywhere — listen:", pause=800, chapter="How people really say it")
ep.ro("Hai, plecăm!", "m", SLOW, 1600)
ep.narr("Come on, we're off! And when it's time to leave a place, between "
        "friends — listen:", pause=P_SHORT)
ep.ro("Plecăm?", "f", SLOW, 1400)
ep.narr("Shall we go? Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The coach again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("The coach, the suitcase — leave, get on, and does it fit.", pause=P_SHORT,
        chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
