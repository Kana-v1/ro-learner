"""
Episode 09C — "Postul e vacant" (Lecția 9 "O zi la serviciu", memory-first, part 3)

The chapter's second communicative intention, "Cum precizăm profesia
cuiva", and the vocabulary of applying for a job: post, vacant, cerere,
translator, punctual, atent (all from the chapter list). The book's formal
"în calitate de" is set against the everyday "ca", and against plain "Sunt
translator" — with no article in any of them, the slip the results showed for
weeks ("e un medic").

punctual and atent agree like the Lecția 7 adjectives (punctuală, atentă for
her); said as a rule in the 09A style — heard first, one sentence, built.

Scene: a candidate at a company's front desk asking about a vacant post —
what do you do now, fill in an application, are you punctual — which is the
whole conversation of applying for a job.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["post", "vacant", "cerere", "translator", "punctual", "atent"]
GLUE = {"concursul": "the selection — the exam-like interview for a post",
        "ca": "as — in 'lucrez ca translator'"}

ep = Episode(number=9, lesson=9, part="c", title="Postul e vacant",
             source="Limba care ne unește, nivelul I — Lecția 9 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Bună ziua. Postul de translator e vacant?"),
    ("dana",  "Da. Cu ce vă ocupați acum?"),
    ("elena", "Lucrez ca translator, la o școală."),
    ("dana",  "Completați o cerere, vă rog."),
    ("elena", "Sunt punctuală și atentă!"),
    ("dana",  "Bine. Concursul e la nouă fix."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "elena", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Applying for a job at a front desk: what you do, and what you're like.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("post", "a post, a job opening", "un post", "m",
            teach_ro="Postul de translator.", teach_en="The translator's post.")
ep.new_item("vacant", "vacant, open", "vacant", "f",
            teach_ro="Postul e vacant.", teach_en="The post is open.")
ep.new_item("cerere", "an application, a request", "o cerere", "m",
            teach_ro="Completez o cerere.", teach_en="I fill in an application.")
ep.new_item("translator", "a translator", "un translator", "f",
            teach_ro="Sunt translator.", teach_en="I'm a translator.")
ep.new_item("punctual", "punctual", "punctual", "m",
            teach_ro="El e punctual.", teach_en="He is punctual.")
ep.new_item("atent", "attentive, careful", "atent", "f",
            teach_ro="El e atent la lecție.", teach_en="He pays attention in class.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("an application", "o cerere", "m"), ("punctual", "punctual", "f"), ("a post", "un post", "m"),
                    ("attentive", "atent", "f"), ("vacant", "vacant", "m"), ("a translator", "un translator", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Saying what someone does ═════════════════════════════════════════════
ep.narr("Three ways to say what you do. Listen:", pause=800, chapter="Saying what you do")
ep.ro("Sunt translator. Lucrez ca translator. Lucrez în calitate de translator.", "m", SLOW, 2600)
ep.narr("I am, I work as, and the formal one you'd write on a CV. None of them "
        "has a word for a.", pause=P_SHORT)
for cue, ans, v, extra in [("I'm a translator.", "Sunt translator.", "f", {}),
                           ("I work as a translator.", "Lucrez ca translator.", "m",
                            {"accept": ["Lucrez în calitate de translator."]}),
                           ("My sister works as a teacher.", "Sora mea lucrează ca profesoară.", "f", {}),
                           ("He is a doctor.", "El e medic.", "m", {})]:
    ep.drill(cue, ans, v, **extra)

ep.narr("Punctual and attentive agree, like the describing words of Lesson 7. "
        "Listen — him, her:", pause=800)
ep.ro("punctual, punctuală — atent, atentă", "f", SLOW, 2000)
for cue, ans, v in [("She is punctual.", "Ea e punctuală.", "m"), ("He is attentive.", "El e atent.", "f"),
                    ("She is attentive.", "Ea e atentă.", "m")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Is the translator's post open?", "Postul de translator e vacant?", "m", {}),
    ("What do you do? Politely.", "Cu ce vă ocupați?", "f", {}),
    ("I work as a translator at a school.", "Lucrez ca translator la o școală.", "m",
     {"accept": ["Lucrez ca translator, la o școală."]}),
    ("Please fill in an application. Politely.", "Completați o cerere, vă rog.", "f", {}),
    ("I'm punctual and attentive. A woman says it.", "Sunt punctuală și atentă.", "m", {}),
    ("I sign the application.", "Semnez cererea.", "f", {}),
    ("Is the post open? — Yes.", "Postul e vacant? — Da.", "m", {}),
    ("We need a translator.", "Avem nevoie de un translator.", "f", {}),
    ("The selection is at nine sharp.", "Concursul e la nouă fix.", "m", {}),
    ("He is punctual, but he isn't attentive.", "El e punctual, dar nu e atent.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. Lesson 9's verbs ═══════════════════════════════════════════════════
ep.narr("All of Lesson 9's verbs so far. Which kind each is, you know from its "
        "I-form; build the one asked for.", pause=P_SECTION, chapter="Lesson 9's verbs")
for cue, ans, v in [
    ("she works", "lucrează", "m"), ("we sign", "semnăm", "f"), ("you check — to a friend", "verifici", "m"),
    ("they fill in", "ei completează", "f"), ("you all note down", "notați", "m"),
    ("he organises", "organizează", "f"), ("we check", "verificăm", "m"), ("you sign — to a friend", "semnezi", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. What do you do — between friends it's shorter. "
        "Listen:", pause=800, chapter="How people really say it")
ep.ro("Ce lucrezi?", "m", SLOW, 1400)
ep.drill("What do you do? To a friend.", "Ce lucrezi?", "f")

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=10)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The front desk again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("A job, an application, and what you're like.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("9", []))
