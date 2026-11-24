"""
Episode 12C — "Poftim? Nu înțeleg." (Lecția 12 "La teatru", memory-first, part 3)

Six items: cer, înțeleg, răspund, informație, spectator, interesant — the
chapter's "Dicționar de contexte minime" pairs them: a cere informații /
ajutor, a înțelege totul, and the text's box office and "mulți spectatori".

Understand goes exactly like go and arrive (înțeleg, înțelegi, înțelege), so
the learner builds its forms without hearing them first. Ask is plain (cer,
ceri, cere). Answer changes a sound like see from 11A: răspund → răspunzi —
heard first, then built; she-form răspunde is regular.

12B's spoken layer (diseară; "Ce faci? — Bine, tu?") is ordinary speech in
the dialogue.

12A's results: merg and ajung were swapped once ("Ajung" for I go), so the
drill mixes go, arrive and understand — three verbs of the same shape.

Scene: Dana works the theatre box office. Spectators ask her the same things
all evening, one doesn't catch the answer, and the phone rings — so
understand, ask and answer come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["cer", "înțeleg", "răspund", "informație", "spectator", "interesant"]
GLUE = {"la telefon": "on the phone — a chunk",
        "un bilet": "a ticket"}

ep = Episode(number=12, lesson=12, part="c", title="Poftim? Nu înțeleg.",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea C)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Ce faci, Dana?"),
    ("dana", "Bine, tu? Diseară lucrez la teatru."),
    ("radu", "Bună seara! O informație, vă rog. Când începe spectacolul?"),
    ("dana", "La ora șapte."),
    ("radu", "Poftim? Nu înțeleg."),
    ("dana", "La ora șapte! E un spectacol interesant."),
    ("elena", "Ce cere domnul?"),
    ("dana", "Un bilet. Mulți spectatori astă seară!"),
    ("elena", "Și cine răspunde la telefon?"),
    ("dana", "Eu răspund! Alo?"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Dana works the theatre box office tonight, and everyone wants "
        "something from her.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("înțeleg", "I understand", "înțeleg", "m",
            teach_ro="Nu înțeleg.", teach_en="I don't understand.")
ep.new_item("informație", "a piece of information", "o informație", "f",
            teach_ro="O informație, vă rog.", teach_en="Some information, please.")
ep.new_item("cer", "I ask for", "cer", "m",
            teach_ro="Cer ajutor.", teach_en="I ask for help.")
ep.new_item("interesant", "interesting", "interesant", "f",
            teach_ro="Un spectacol interesant.", teach_en="An interesting show.")
ep.new_item("răspund", "I answer", "răspund", "m",
            teach_ro="Răspund la telefon.", teach_en="I answer the phone.")
ep.new_item("spectator", "a spectator, someone in the audience", "un spectator", "f",
            teach_ro="Un spectator la teatru.", teach_en="A spectator at the theatre.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I answer", "răspund", "f"), ("interesting", "interesant", "m"),
                    ("I understand", "înțeleg", "f"), ("a spectator", "un spectator", "m"),
                    ("I ask for", "cer", "f"),
                    ("a piece of information", "o informație", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Understand goes like go ══════════════════════════════════════════════
ep.narr("Understand goes exactly like go and arrive. You haven't heard these "
        "— build them.", pause=800, chapter="Understand, like go")
ep.drill("you understand — to a friend", "înțelegi", "f")
ep.drill("Do you understand? To a friend.", "Înțelegi?", "m")
ep.drill("she understands", "înțelege", "f")
ep.drill("you understand — politely", "înțelegeți", "m")
ep.drill("I don't understand.", "Nu înțeleg.", "f")
ep.narr("Three verbs of the same shape. Mixed.", pause=800)
for cue, ans, v in [("I go", "merg", "m"), ("I understand", "înțeleg", "f"),
                    ("I arrive", "ajung", "m"), ("you go — to a friend", "mergi", "f"),
                    ("you understand — to a friend", "înțelegi", "m"),
                    ("he arrives", "ajunge", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Ask for ══════════════════════════════════════════════════════════════
ep.narr("Ask for is plain. Listen:", pause=800, chapter="Ask for")
ep.ro("Ce ceri?", "f", SLOW, 1700)
ep.drill("you ask for — to a friend", "ceri", "m")
ep.drill("she asks for", "cere", "f")
ep.drill("What is the gentleman asking for?", "Ce cere domnul?", "m")
ep.drill("He's asking for a ticket.", "Cere un bilet.", "f")
ep.drill("I'm asking for some information.", "Cer o informație.", "m")

# ═══ 4. Answer — a sound changes ═════════════════════════════════════════════
ep.narr("Answer changes a sound, the way see does. To a friend — listen:",
        pause=800, chapter="Answer, by ear")
ep.ro("Răspunzi la telefon?", "m", SLOW, 1900)
ep.drill("you answer — to a friend", "răspunzi", "f")
ep.drill("Are you answering the phone? To a friend.", "Răspunzi la telefon?", "m")
ep.narr("She answers is plain again. Build it.", pause=P_SHORT)
ep.drill("she answers", "răspunde", "f")
ep.drill("Who's answering the phone?", "Cine răspunde la telefon?", "m")
for cue, ans, v in [("I answer", "răspund", "f"), ("you answer — to a friend", "răspunzi", "m"),
                    ("he answers", "răspunde", "f")]:
    ep.drill(cue, ans, v)

# ═══ 5. Interesting, spectators ══════════════════════════════════════════════
ep.narr("Interesting, with a show and with a book. Listen to both:", pause=800,
        chapter="Interesting")
ep.ro("Un spectacol interesant. O carte interesantă.", "f", SLOW, 2400)
ep.drill("an interesting book", "o carte interesantă", "m")
ep.drill("It's an interesting show.", "E un spectacol interesant.", "f")
ep.narr("And many spectators — listen:", pause=800)
ep.ro("Mulți spectatori.", "m", SLOW, 1700)
ep.drill("many spectators", "mulți spectatori", "f")
ep.drill("Lots of spectators this evening!", "Mulți spectatori astă seară!", "m")

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Some information, please.", "O informație, vă rog.", "f", {}),
    ("When does the show begin?", "Când începe spectacolul?", "m", {}),
    ("Pardon? I don't understand.", "Poftim? Nu înțeleg.", "f", {}),
    ("Do you understand? Politely.", "Înțelegeți?", "m", {}),
    ("I'm asking for help.", "Cer ajutor.", "f", {}),
    ("I answer the phone.", "Răspund la telefon.", "m", {}),
    ("This evening I work at the theatre.", "Diseară lucrez la teatru.", "f",
     {"accept": ["Astă seară lucrez la teatru."]}),
    ("How are you? — Fine, you?", "Ce faci? — Bine, tu?", "m", {}),
    ("Every spectator asks for a ticket.", "Fiecare spectator cere un bilet.", "f", {}),
    ("The book is interesting.", "Cartea e interesantă.", "m", {}),
    ("I'm staying home this evening.", "Diseară rămân acasă.", "f",
     {"accept": ["Rămân acasă diseară.", "Astă seară rămân acasă.",
                 "Rămân acasă astă seară."]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. You know the word for here you are. Said as a "
        "question, it's how people say pardon? — listen:", pause=800,
        chapter="How people really say it")
ep.ro("Poftim?", "f", SLOW, 1400)
ep.narr("And politely, when you need it again: can you repeat, please? "
        "Listen:", pause=P_SHORT)
ep.ro("Puteți repeta, vă rog?", "m", SLOW, 1900)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The box office again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("Ask, understand, answer — and a box office full of spectators.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
