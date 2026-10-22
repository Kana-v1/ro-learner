"""
Episode 09D — "Vă angajez!" (Lecția 9 "O zi la serviciu", memory-first, part 4)

Six items from the chapter list: examinez, studiez, angajez (-ez verbs), act,
secretară, exigent. Forms follow the book's table (studiez, studiezi,
studiază, studiem, studiați, studiază) and its models ("Noi studiem limba
română", "Voi examinați agenda", "Ei semnează contractul", "Șeful angajează
un translator").

Two points, in the 09A rule style (Romanian voice for every form, pattern
first, one sentence, then the learner builds):
- studiez against învăț: learn anything, versus study a subject properly —
  the learner reached for studiez on his own in 8A;
- studiez's we-form, studiem, which rhymes with 08C's întârziem rather than
  with lucrăm.

Scene: a boss interviewing a candidate — he looks over her documents, asks
what she studies, and hires her.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["examinez", "studiez", "angajez", "act", "secretară", "exigent"]
GLUE = {"șeful": "the boss — the book's conducător, as people say it",
        "contractul": "the contract"}

ep = Episode(number=9, lesson=9, part="d", title="Vă angajez!",
             source="Limba care ne unește, nivelul I — Lecția 9 (partea D)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu",  "Bună ziua. Examinez actele dumneavoastră."),
    ("elena", "Poftiți."),
    ("radu",  "Ce studiați acum?"),
    ("elena", "Studiez chimia la facultate."),
    ("radu",  "Sunt exigent. Dar sunteți punctuală și atentă. Vă angajez!"),
    ("elena", "Mulțumesc! Unde semnez?"),
    ("radu",  "Secretara are contractul."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A job interview that ends well. Six words for getting hired.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("examinez", "I look over, I examine", "examinez", "m",
            teach_ro="Examinez actele.", teach_en="I look over the documents.")
ep.new_item("act", "an official document", "un act", "f",
            teach_ro="un act, două acte", teach_en="one document, two documents")
ep.new_item("studiez", "I study — a subject, properly", "studiez", "m",
            teach_ro="Studiez chimia.", teach_en="I study chemistry.")
ep.new_item("angajez", "I hire, I take on", "angajez", "f",
            teach_ro="Angajez o secretară.", teach_en="I'm hiring a secretary.")
ep.new_item("secretară", "a secretary", "o secretară", "m",
            teach_ro="Secretara notează.", teach_en="The secretary takes notes.")
ep.new_item("exigent", "demanding, strict", "exigent", "f",
            teach_ro="Șeful e exigent.", teach_en="The boss is demanding.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I hire", "angajez", "m"), ("a document", "un act", "f"), ("I study", "studiez", "m"),
                    ("demanding", "exigent", "f"), ("I look over", "examinez", "m"),
                    ("a secretary", "o secretară", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Learn and study ══════════════════════════════════════════════════════
ep.narr("Two verbs for study. Listen:", pause=800, chapter="Learn and study")
ep.ro("Învăț limba română. Studiez chimia la facultate.", "m", SLOW, 2200)
ep.narr("The first is for learning anything; the second, for a subject you study "
        "properly — at university, or in depth.", pause=P_SHORT)
for cue, ans, v in [("I'm learning Romanian.", "Învăț limba română.", "f"),
                    ("I study chemistry at the faculty.", "Studiez chimia la facultate.", "m")]:
    ep.drill(cue, ans, v)

ep.narr("Study's we-form is its own. Listen — work, then study and be late:",
        pause=800)
ep.ro("noi lucrăm — noi studiem, noi întârziem", "f", SLOW, 2200)
ep.narr("Study sounds like be late, from the lesson on time. The rest are as "
        "usual. Build them.", pause=P_SHORT)
for cue, ans, v in [("we study", "noi studiem", "m"), ("she studies", "ea studiază", "f"),
                    ("you all study", "voi studiați", "m"), ("we hire", "noi angajăm", "f"),
                    ("he looks over", "el examinează", "m"), ("you study — to a friend", "tu studiezi", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("I'm looking over your documents. Politely.", "Examinez actele dumneavoastră.", "m", {}),
    ("What are you studying? Politely.", "Ce studiați?", "f", {}),
    ("We study Romanian.", "Noi studiem limba română.", "m", {"accept": ["Studiem limba română."]}),
    ("The boss is hiring a translator.", "Șeful angajează un translator.", "f", {}),
    ("The secretary writes the names in the planner.", "Secretara notează numele în agendă.", "m", {}),
    ("She is demanding.", "Ea e exigentă.", "f", {}),
    ("You all look over the planner.", "Voi examinați agenda.", "m", {}),
    ("They sign the contract.", "Ei semnează contractul.", "f", {}),
    ("Where do I sign?", "Unde semnez?", "m", {}),
    ("Do you study or work? To a friend.", "Studiezi sau lucrezi?", "f", {}),
    ("The documents are on the table.", "Actele sunt pe masă.", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. Lesson 9's verbs ════════════════════════════════════════════════════
ep.narr("All of Lesson 9's verbs. Build the one asked for.", pause=P_SECTION,
        chapter="Lesson 9's verbs")
for cue, ans, v in [
    ("they hire", "ei angajează", "m"), ("you check — to a friend", "verifici", "f"),
    ("we fill in", "completăm", "m"), ("she notes down", "notează", "f"),
    ("we study", "studiem", "m"), ("you all sign", "semnați", "f"),
    ("he organises", "organizează", "m"), ("I look over", "examinez", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. The book calls the head of an office by a formal "
        "word. In an office in Bucharest, people say the boss, or borrow the "
        "English. Listen:", pause=800, chapter="How people really say it")
ep.ro("Șeful. Managerul.", "f", SLOW, 1600)
ep.narr("And the book's word for documents is the everyday one — your ID and "
        "papers, at any office. Listen:", pause=P_SHORT)
ep.ro("Aveți actele la dumneavoastră?", "m", SLOW, 1800)
ep.narr("Do you have your documents on you? You'll hear it at any counter.",
        pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=9)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The interview again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("Hired. Next time, the last of Lesson 9.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("9", []))
