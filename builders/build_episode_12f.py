"""
Episode 12F — "Troleibuzul acela" (Lecția 12 "La teatru", memory-first, part 6)

The last of Lecția 12. Six items: acela, aceea, propunere, lucru, până la,
ziua. Then the chapter's synthesis text "Prietenii merg la teatru" and the
proverb "Orice lucru este bun la timpul său."

That is set beside this, which the learner has held since 3A: "Trenul acesta.
Trenul acela." — two forms side by side, the man-and-thing form first, the
woman form after it has been built. The plural (aceia, acelea) is left out:
one point at a time. The chapter's own pairs: "Acesta este fratele tău sau
acela?" and exercise 19's "bărbatul acela, femeia aceea".

Ziua completes the book's "Când?" table beside dimineața (known since 2) and
seara (11F): "Ziua sunt la serviciu." Până la is heard for a place ("până la
teatru", the text's trolleybus) and then for a time ("până la ora șase").

The text keeps the book's story but drops what would push the glue past
four: the stop and the boulevard's names, the cloakroom, the stalls, the lead
role and the tea in the interval. Kept as glue: the trolleybus, the box
office, the curtain, and Mihai.

12E's spoken layer (Bravo!, un prieten de-al meu) is ordinary speech here.

Scene: Dana proposes the theatre; Elena works in the daytime but is free in
the evening, and won't take that trolleybus — so that, proposal, until and
daytime come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["acela", "aceea", "propunere", "lucru", "până la", "ziua"]
GLUE = {"troleibuzul": "the trolleybus",
        "casa de bilete": "the box office — a chunk",
        "cortina": "the curtain — in the book's text",
        "Mihai": "a man's name"}

ep = Episode(number=12, lesson=12, part="f", title="Troleibuzul acela",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea F)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Elena, am o propunere. Diseară mergem la teatru?"),
    ("elena", "Ziua lucrez, dar seara pot."),
    ("dana", "Vezi troleibuzul acela? Merge până la teatru."),
    ("elena", "Nu troleibuzul acela. Mergem pe jos!"),
    ("dana", "Bravo! Și cine e fata aceea?"),
    ("elena", "Fata aceea? Nu știu."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Dana has an idea for the evening. The last part of Lesson 12 — and "
        "the chapter's own text.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("propunere", "a suggestion, a proposal", "o propunere", "m",
            teach_ro="Am o propunere.", teach_en="I have a suggestion.")
ep.new_item("ziua", "in the daytime", "ziua", "f",
            teach_ro="Ziua sunt la serviciu.", teach_en="In the daytime I'm at work.")
ep.new_item("acela", "that train — over there", "trenul acela", "m",
            teach_ro="Trenul acela.", teach_en="That train.")
ep.new_item("până la", "as far as", "până la", "f",
            teach_ro="Merg pe jos până la teatru.",
            teach_en="I walk as far as the theatre.")
ep.new_item("lucru", "a thing", "un lucru", "m",
            teach_ro="Un lucru necesar.", teach_en="A necessary thing.")
ep.new_item("aceea", "that girl — over there", "fata aceea", "f",
            teach_ro="Fata aceea.", teach_en="That girl.")
ep.narr("Mixed. Just the words.", pause=800)
for cue, ans, v in [("a thing", "un lucru", "f"), ("that train", "trenul acela", "m"),
                    ("in the daytime", "ziua", "f"), ("a suggestion", "o propunere", "m"),
                    ("that girl", "fata aceea", "f"), ("as far as", "până la", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. This and that ════════════════════════════════════════════════════════
ep.narr("You know this. That is the one over there. Listen to both:",
        pause=800, chapter="This and that")
ep.ro("Trenul acesta. Trenul acela.", "m", SLOW, 2200)
ep.drill("that boy", "băiatul acela", "f")
ep.drill("that show", "spectacolul acela", "m")
ep.drill("Is this your brother, or that one? To a friend.",
         "Acesta e fratele tău sau acela?", "f")
ep.narr("For a woman, or a feminine thing, it's the other one. Listen to both:",
        pause=800)
ep.ro("Cartea aceasta. Cartea aceea.", "f", SLOW, 2200)
ep.drill("that book", "cartea aceea", "m")
ep.drill("that woman", "femeia aceea", "f")
ep.drill("Is this your book, or that one? To a friend.",
         "Aceasta e cartea ta sau aceea?", "m")
for cue, ans, v in [("that train", "trenul acela", "f"), ("that girl", "fata aceea", "m"),
                    ("this train", "trenul acesta", "f"), ("that suggestion", "propunerea aceea", "m"),
                    ("this book", "cartea aceasta", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. When? ════════════════════════════════════════════════════════════════
ep.narr("Morning, daytime, evening — the same shape. Listen:", pause=800,
        chapter="When?")
ep.ro("Dimineața. Ziua. Seara.", "f", SLOW, 2400)
ep.drill("In the daytime I'm at work.", "Ziua sunt la serviciu.", "m",
         accept=["Sunt la serviciu ziua."])
ep.drill("In the evening I stay home.", "Seara rămân acasă.", "f",
         accept=["Rămân acasă seara."])
ep.drill("In the daytime I work, but in the evening I can.",
         "Ziua lucrez, dar seara pot.", "m")
ep.drill("every day", "în fiecare zi", "f")

# ═══ 4. As far as, until ═════════════════════════════════════════════════════
ep.narr("As far as works for a place — and for a time, as until. Listen to "
        "both:", pause=800, chapter="As far as, until")
ep.ro("Până la teatru. Până la ora șase.", "m", SLOW, 2400)
ep.drill("The bus goes as far as the theatre.", "Autobuzul merge până la teatru.", "f")
ep.drill("I work until six.", "Lucrez până la ora șase.", "m",
         accept=["Lucrez până la șase."])
ep.drill("We walk as far as the school.", "Mergem pe jos până la școală.", "f")

# ═══ 5. Suggestions and things ═══════════════════════════════════════════════
ep.narr("A suggestion goes like a book. Listen:", pause=800,
        chapter="A suggestion, a thing")
ep.ro("O propunere interesantă.", "f", SLOW, 1900)
ep.drill("an interesting suggestion", "o propunere interesantă", "m")
ep.drill("His suggestion is interesting.", "Propunerea lui e interesantă.", "f")
ep.drill("I have a suggestion.", "Am o propunere.", "m")
ep.drill("a necessary thing", "un lucru necesar", "f")

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("This evening we're going to the theatre.", "Diseară mergem la teatru.", "f",
     {"accept": ["Astă seară mergem la teatru.", "Mergem la teatru diseară.",
                 "În seara asta mergem la teatru.", "Seara asta mergem la teatru."]}),
    ("Do you see that bus? To a friend.", "Vezi autobuzul acela?", "m", {}),
    ("Not that bus. We're walking!", "Nu autobuzul acela. Mergem pe jos!", "f", {}),
    ("Who is that girl?", "Cine e fata aceea?", "m", {}),
    ("A friend of mine.", "Un prieten de-al meu.", "f", {}),
    ("Do you know that man? To a friend.", "Cunoști bărbatul acela?", "m", {}),
    ("When does the show begin?", "Când începe spectacolul?", "f", {}),
    ("I'm taking the book back as far as the library.",
     "Duc cartea înapoi până la bibliotecă.", "m", {}),
    ("Everyone arrives home late.", "Fiecare ajunge acasă târziu.", "f",
     {"accept": ["Fiecare ajunge târziu acasă."]}),
    ("Well done!", "Bravo!", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Over there, in everyday speech, the that-word "
        "often comes as a shorter one. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Trenul ăla. Fata aia.", "m", SLOW, 2000)
ep.narr("Fine with friends; with strangers, keep the long one. Just to "
        "recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Text — the chapter's own ═════════════════════════════════════════════
ep.narr("Now the chapter's own text: two friends go to the theatre. Three "
        "things are new and clear from the story — a trolleybus, the box "
        "office, and the curtain. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Prietenii merg la teatru.",
    "Radu și Mihai sunt mari amatori de teatru. Astăzi, după serviciu, ei merg la teatru.",
    "Ei iau troleibuzul până la teatru.",
    "Când ajung la teatru, ei întreabă la casa de bilete:",
    "Aveți bilete la spectacolul de astă seară? — Da, avem. Avem locuri la balcon.",
    "Prietenii iau două bilete și intră în sală. Aici sunt mulți spectatori.",
    "E ora șapte și cinci minute. La ora șapte și un sfert începe spectacolul.",
    "Este un spectacol interesant, cu un decor frumos.",
    "Când cade cortina, spectatorii aplaudă.",
    "După spectacol, prietenii merg împreună pe jos. Seara târziu ajung acasă.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("Orice lucru este bun la timpul său.", "f", SLOW, 1800)
ep.narr("Everything is good in its own time. Once more:", pause=P_SHORT)
ep.ro("Orice lucru este bun la timpul său.", "f", NORMAL, 1600)

# ═══ 10. Cold open again ═════════════════════════════════════════════════════
ep.narr("Dana and Elena again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 11. Close ═══════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 12 — the theatre, and verbs like go. "
        "Next, Lesson 13: visiting friends.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
