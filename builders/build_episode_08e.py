"""
Episode 08E — "Sesiunea e aproape" (Lecția 8 "La studii", memory-first, part 5)

The last of Lecția 8. Six items — orar, materie, sesiune, după, spațios, and
mulți/multe (many: the plural of mult, which the synthesis text needs for
"mulți studenți", "multe facultăți") — then the chapter as a whole: every verb
in every person on the 08D rule, the time, the synthesis text "La studii" and
the proverb "Ai carte, ai parte."

The text is the book's, cut where it runs into untaught words; four chunks
are glue (instituție de învățământ superior, specialități, ziaristică,
bibliotecă). The rarer chapter words — absolvent, catedră, colegiu, gimnaziu,
frecvență, licență, juridic, secție — are left out: names for parts of the
Moldovan education system a learner in Bucharest rarely needs, and not worth
an episode's memory load.

Scene: two students in the library before exams — the timetable, the subject
each is going over, how much time is left.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["orar", "materie", "sesiune", "după", "spațios", "mulți"]
GLUE = {"bibliotecă": "library",
        "instituție de învățământ superior": "an institution of higher education — in the text",
        "specialități, ziaristică": "specialities, journalism — in the text",
        "timp": "time — in 'puțin timp'"}

ep = Episode(number=8, lesson=8, part="e", title="Sesiunea e aproape",
             source="Limba care ne unește, nivelul I — Lecția 8 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Sesiunea e aproape. Am puțin timp."),
    ("dana", "Și eu. După cursuri stau la bibliotecă."),
    ("radu", "Ce materie repeți?"),
    ("dana", "Chimie. Am multe exerciții."),
    ("radu", "Ai orarul?"),
    ("dana", "Da. Azi avem cursuri la nouă și la unsprezece și jumătate."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The library before exams. The last six words of Lesson 8, then the "
        "whole lesson together, and the book's own text.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("orar", "a timetable", "un orar", "m",
            teach_ro="Ai orarul?", teach_en="Have you got the timetable?")
ep.new_item("materie", "a subject — or the material to learn", "o materie", "f",
            teach_ro="Repet materia.", teach_en="I'm going over the material.")
ep.new_item("sesiune", "exam season", "sesiune", "m",
            teach_ro="Sesiunea e aproape.", teach_en="Exams are close.")
ep.new_item("după", "after", "după", "f",
            teach_ro="După cursuri stau la bibliotecă.", teach_en="After classes I stay in the library.")
ep.new_item("spațios", "spacious, roomy", "spațios", "m",
            teach_ro="Un apartament spațios.", teach_en="A spacious flat.")
ep.new_item("mulți", "many — before a his-word", "mulți", "f",
            teach_ro="mulți studenți, multe exerciții", teach_en="many students, many exercises")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("after", "după", "m"), ("a timetable", "un orar", "f"), ("many, his-words", "mulți", "m"),
                    ("exam season", "sesiune", "f"), ("spacious", "spațios", "m"),
                    ("a subject", "o materie", "f")]:
    ep.recall_word(cue, ans, v)

ep.narr("A lot, after a verb, never changes. Before a word, it agrees — many "
        "his-words, many her-words. Listen:", pause=P_SHORT)
ep.example(None, "Învăț mult. Mulți studenți, multe facultăți.", "m", 2200)
ep.example(None, "o sală spațioasă, un birou spațios", "f", 2000)
for cue, ans, v in [("many students", "mulți studenți", "m"), ("many exercises", "multe exerciții", "f"),
                    ("a spacious room", "o sală spațioasă", "m"), ("I study a lot.", "Învăț mult.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 2. Lesson 8 together: every verb, every person ══════════════════════════
ep.narr("Now the whole lesson's verbs, on the rule from last time. The person, "
        "the verb; you build the form.", pause=P_SECTION, chapter="Every verb, every person")
for cue, ans, v in [
    ("we learn", "noi învățăm", "m"), ("they explain", "ei explică", "f"),
    ("you all ask", "voi întrebați", "m"), ("I solve", "eu rezolv", "f"),
    ("she repeats", "ea repetă", "m"), ("you listen — to a friend", "tu asculți", "f"),
    ("we live", "noi stăm", "m"), ("they're late", "ei întârzie", "f"),
    ("you learn — to a friend", "tu înveți", "m"), ("he asks", "el întreabă", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences, from across the lesson.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Exams are close. I have little time.", "Sesiunea e aproape. Am puțin timp.", "m", {}),
    ("After classes I stay in the library.", "După cursuri stau la bibliotecă.", "f", {}),
    ("What subject are you going over? To a friend.", "Ce materie repeți?", "m", {}),
    ("The students go over the material.", "Studenții repetă materia.", "f", {}),
    ("The teacher asks who is late.", "Profesorul întreabă cine întârzie.", "m", {}),
    ("He explains the lesson, and the students listen.", "El explică lecția, iar studenții ascultă.", "f",
     {"accept": ["El explică lecția și studenții ascultă."]}),
    ("We have classes according to the timetable.", "Avem cursuri după orar.", "m", {}),
    ("The university has many faculties.", "Universitatea are multe facultăți.", "f", {}),
    ("Today we have class at half past eleven.", "Azi avem curs la unsprezece și jumătate.", "m", {}),
    ("The room is spacious.", "Sala e spațioasă.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Exam season has its own word, and every student "
        "in Romania uses it: you'll hear people say they're in exams. Listen:",
        pause=800, chapter="How people really say it")
ep.ro("Sunt în sesiune.", "f", SLOW, 1600)
ep.narr("I'm in exam season — busy, don't ask.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 6. Text — the chapter's own ═════════════════════════════════════════════
ep.narr("Now the chapter's own text, about studying at a university. A few "
        "words in it are new and clear from the story: an institution of higher "
        "education, specialities, journalism, the library. Slowly first.",
        pause=800, chapter="Text")
BOOK_TEXT = [
    "Universitatea este o instituție de învățământ superior.",
    "Ea are multe facultăți și specialități: biologie, chimie, ziaristică.",
    "La universitate învață mulți studenți. Ei au cursuri după orar.",
    "Astăzi studenții sunt într-o sală spațioasă. Ei stau la mese.",
    "Profesorul întreabă cine întârzie. El explică lecția, iar studenții ascultă.",
    "După ore studenții sunt la bibliotecă. Ei repetă materia.",
    "Sesiunea e aproape. Studenții au puțin timp.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("And the chapter's proverb. Listen:", pause=800, chapter="Proverb")
ep.ro("Ai carte, ai parte.", "f", SLOW, 1600)
ep.narr("If you have learning, you have your share — study, and it pays. Once more:",
        pause=P_SHORT)
ep.ro("Ai carte, ai parte.", "f", NORMAL, 1400)

# ═══ 7. Cold open again ══════════════════════════════════════════════════════
ep.narr("The library again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("That closes Lesson 8: your first verbs and their rule, the time, and "
        "studying.", pause=600)

# ═══ 8. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the whole of Lesson 8.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("8", []))
