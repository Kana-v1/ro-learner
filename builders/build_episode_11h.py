"""
Episode 11H — "Când pleacă autocarul?" (Lecția 11 "La munte", memory-first, part 8)

The last of Lecția 11. Seven items, two of them question words: când, de ce,
traseu, aranjez, balnear (as "o stațiune balneară"), limbă, străin. Then the
chapter's synthesis text "La munte" and the proverb "Minte sănătoasă în corp
sănătos."

Aranjez is an -ez verb, set beside examinez — the learner's most-missed answer
(13 times, mostly heard as examinezi or examinează). So the I-form and the
she-form of both are drilled as pairs, and "Examinez actele dumneavoastră"
(said with voastre or tale instead) is asked here after the pairs.

Taci, the friend-form 11G held back, comes with why: "De ce taci?" — the sound
changes like vezi and cazi.

Străin goes like curat (11F): un turist străin, o limbă străină. Limbi
străine (foreign languages) is heard as a chunk, from the book's "Dana poate
studia limbi străine".

The text keeps the book's wording except one sentence: "Tata dă un telefon la
agenția de turism și rezervă bilete" becomes "Tata rezervă bilete la agenția
de turism", and "Apoi ei stau la aer curat" becomes the book's own question
wording "După masă ei stau la aer curat" — dă un telefon and apoi would push
the glue past four.

11G's spoken layer (Sunt obosit / Sunt obosită) comes back as ordinary drills.

Scene: a guide on the coach at the start of a trip — tourists ask when, why,
how far, so the question words come round for each passenger.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["când", "de ce", "traseu", "aranjez", "balneară", "limbă", "străin"]
GLUE = {"pentru că": "because — a chunk",
        "ape minerale": "mineral springs — in the book's text",
        "serpentină": "hairpin bends — in the book's text",
        "ia masa": "has a meal — in the book's text"}

ep = Episode(number=11, lesson=11, part="h", title="Când pleacă autocarul?",
             source="Limba care ne unește, nivelul I — Lecția 11 (partea H)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Când pleacă autocarul?"),
    ("dana", "Acum. Aranjez valizele în portbagaj."),
    ("radu", "Traseul e lung?"),
    ("dana", "Da, e lung. Plecăm la o stațiune balneară."),
    ("radu", "De ce acolo?"),
    ("dana", "Pentru că acolo sunt ape minerale."),
    ("elena", "Și de ce tace domnul?"),
    ("dana", "E străin. Studiază limba română."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A guide on a coach, and tourists with questions. The last part of "
        "Lesson 11 — when, why, and the chapter's own text.", pause=P_SECTION)

# ═══ 1. Seven words — introduced then recalled at once ═══════════════════════
ep.narr("Seven words, one at a time. Two are small question words.", pause=800,
        chapter="Seven words")
ep.new_item("când", "when?", "când", "f",
            teach_ro="Când pleacă autocarul?", teach_en="When does the coach leave?")
ep.new_item("de ce", "why?", "de ce", "m",
            teach_ro="De ce acolo?", teach_en="Why there?")
ep.new_item("traseu", "a route", "un traseu", "f",
            teach_ro="Traseul e lung.", teach_en="The route is long.")
ep.new_item("aranjez", "I arrange, I put in order", "aranjez", "m",
            teach_ro="Aranjez valizele.", teach_en="I arrange the suitcases.")
ep.new_item("balneară", "a spa resort", "o stațiune balneară", "f",
            teach_ro="O stațiune balneară.", teach_en="A spa resort.")
ep.new_item("limbă", "a language", "o limbă", "m",
            teach_ro="Limba română.", teach_en="The Romanian language.")
ep.new_item("străin", "foreign; a foreigner", "străin", "f",
            teach_ro="E străin.", teach_en="He's a foreigner.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("why?", "de ce", "m"), ("a language", "o limbă", "f"),
                    ("I arrange", "aranjez", "m"), ("when?", "când", "f"),
                    ("a route", "un traseu", "m"), ("foreign", "străin", "f"),
                    ("a spa resort", "o stațiune balneară", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. When? Why? ═══════════════════════════════════════════════════════════
ep.narr("When goes first, then the verb — as with where. Build them.", pause=800,
        chapter="When? Why?")
for cue, ans, v in [("When does the coach leave?", "Când pleacă autocarul?", "m"),
                    ("When do we leave?", "Când plecăm?", "f"),
                    ("Where does the coach leave from?", "De unde pleacă autocarul?", "m")]:
    ep.drill(cue, ans, v)
ep.narr("Why. And the answer starts with because — listen:", pause=800)
ep.ro("De ce acolo? — Pentru că e frumos.", "f", SLOW, 2000)
ep.drill("Why there?", "De ce acolo?", "m")
ep.drill("Because it's lovely.", "Pentru că e frumos.", "f")
ep.narr("Keep quiet, to a friend, changes its sound — like you see, you fall. "
        "Listen:", pause=800)
ep.ro("De ce taci?", "m", SLOW, 1800)
ep.drill("you keep quiet — to a friend", "taci", "f")
ep.drill("Why are you quiet? To a friend.", "De ce taci?", "m")
ep.drill("Why is the gentleman quiet?", "De ce tace domnul?", "f")

# ═══ 3. Arrange, examine ═════════════════════════════════════════════════════
ep.narr("Arrange is like examine, from the newsroom. I — listen to both:",
        pause=800, chapter="Arrange, examine")
ep.ro("Aranjez. Examinez.", "m", SLOW, 2000)
ep.narr("I ends just like that — nothing after it. Now she. Listen:", pause=800)
ep.ro("Mama aranjează hainele.", "f", SLOW, 1800)
ep.drill("she arranges", "aranjează", "m")
ep.narr("Examine goes the same way. Build it.", pause=P_SHORT)
ep.drill("she examines", "examinează", "f")
ep.narr("Now in pairs — I, then she.", pause=800)
for cue, ans, v in [("I examine", "examinez", "m"), ("he examines", "examinează", "f"),
                    ("I arrange", "aranjez", "m"), ("she arranges", "aranjează", "f"),
                    ("I examine", "examinez", "m")]:
    ep.drill(cue, ans, v)
ep.narr("Your, politely, is the same word as you, politely. Listen:", pause=800)
ep.ro("Examinez actele dumneavoastră.", "m", SLOW, 2400)
ep.drill("I'm looking over your documents. Politely.",
         "Examinez actele dumneavoastră.", "f")
ep.drill("Mum arranges the clothes in the suitcase.",
         "Mama aranjează hainele în valiză.", "m")

# ═══ 4. Foreign, language ════════════════════════════════════════════════════
ep.narr("Foreign goes like clean: a his-word, a her-word. Listen:", pause=800,
        chapter="Foreign, language")
ep.ro("Un turist străin. O limbă străină.", "f", SLOW, 2200)
for cue, ans, v in [("a foreign language", "o limbă străină", "m"),
                    ("He's a foreigner.", "E străin.", "f"),
                    ("She's a foreigner.", "E străină.", "m")]:
    ep.drill(cue, ans, v)
ep.narr("And more than one — foreign languages. Listen:", pause=800)
ep.ro("Studiez limbi străine.", "m", SLOW, 1800)
for cue, ans, v in [("I study foreign languages.", "Studiez limbi străine.", "f"),
                    ("What language are you studying? Politely.", "Ce limbă studiați?", "m"),
                    ("I'm learning the Romanian language.", "Învăț limba română.", "f",)]:
    ep.drill(cue, ans, v, accept=["Studiez limba română."] if "Romanian" in cue else None)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("When does the coach leave?", "Când pleacă autocarul?", "m", {}),
    ("The route is long.", "Traseul e lung.", "f", {}),
    ("We're leaving for a spa resort.", "Plecăm la o stațiune balneară.", "m", {}),
    ("Why there?", "De ce acolo?", "f", {}),
    ("Because there are mineral springs there.", "Pentru că acolo sunt ape minerale.", "m",
     {"accept": ["Pentru că sunt ape minerale acolo."]}),
    ("I arrange the suitcases in the boot.", "Aranjez valizele în portbagaj.", "f", {}),
    ("Why are you quiet? To a friend.", "De ce taci?", "m", {}),
    ("He's a foreigner. He's studying Romanian.", "E străin. Studiază limba română.", "f", {}),
    ("I'm tired. A man.", "Sunt obosit.", "m", {}),
    ("I'm tired. A woman.", "Sunt obosită.", "f", {}),
    ("When do we leave?", "Când plecăm?", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 6. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Why, with not, is the everyday yes to an "
        "offer. Shall we have a coffee? — Why not? Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Bem o cafea? — De ce nu?", "f", SLOW, 1800)
ep.narr("And when you can't answer a question, say so — I don't know. Listen:",
        pause=P_SHORT)
ep.ro("Nu știu.", "m", SLOW, 1400)
ep.drill("Why not?", "De ce nu?", "f")
ep.drill("I don't know.", "Nu știu.", "m")

# ═══ 7. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 8. Text — the chapter's own ═════════════════════════════════════════════
ep.narr("Now the chapter's own text: the Ionescu family goes to the mountains. "
        "Two things are new and clear from the story — hairpin bends, and has a "
        "meal. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Familia Ionescu pleacă la munte. Mama aranjează hainele în valiză.",
    "Tata rezervă bilete la agenția de turism. Mama rezervă locuri la hotel.",
    "Ei pleacă la o stațiune balneară. Acolo sunt ape minerale.",
    "La munte este frumos. Dimineața soarele apare de după un vârf de munte.",
    "Autocarul urcă în serpentină. Peisajul este fermecător.",
    "Iată stațiunea. Aici este un hotel și un restaurant. Dan ia cheia de la recepție.",
    "După cazare familia Ionescu ia masa. După masă ei stau la aer curat.",
    "După o plimbare lungă ei cad de oboseală. La aer curat somnul este adânc.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("Minte sănătoasă în corp sănătos.", "f", SLOW, 1600)
ep.narr("A healthy mind in a healthy body. Once more:", pause=P_SHORT)
ep.ro("Minte sănătoasă în corp sănătos.", "f", NORMAL, 1400)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The coach again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 11 — the mountains, and verbs that change "
        "their sound. Next, Lesson 12: the theatre.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("11", []))
