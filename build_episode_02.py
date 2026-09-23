"""
Episode 02 — "Eu sunt manager" (Lecția 2, Limba care ne unește I)

Scene: Radu visits an office and is shown who is who. Introducing a room full
of people one by one is the situation that makes "el e X, ea e Y" repeat four
times without sounding like an exercise — and it puts un and o side by side
naturally, because you point at things as you name them.

Note what the dialogue does with episode one's spoken layer: domnu', e instead
of este, Îmi pare bine and deci all appear, unannounced, as ordinary speech.
Last episode's "how people really talk" section becomes this episode's input.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# The chapter's own vocabulary block, in the book's order.
REQUIRED = [
    "actor", "arhitect", "birou", "contabil", "economist", "educatoare",
    "funcționar", "inginer", "jurist", "magazin", "manager", "medic",
    "ministru", "oraș", "președinte", "profesor", "profesoară", "sat",
    "sportiv", "școală", "șofer", "teatru", "țară", "vânzător", "ziarist",
    "la", "acolo", "aici", "ba da", "un", "o",
]

GLUE = {
    "poftiți": "come in / here you are",
    "mulțumesc": "thank you",
    "bine": "good, fine",
    "Andreea / Dan / Mihai": "names",
}

ep = Episode(number=2, lesson=2, title="Eu sunt manager",
             source="Limba care ne unește, nivelul I — Lecția 2",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună ziua, domnu' Radu! Poftiți."),
    ("radu",  "Bună ziua! Îmi pare bine."),
    ("dana",  "Aici e biroul. Acolo e Andreea. Ea e arhitect."),
    ("radu",  "Dar el?"),
    ("dana",  "El e Dan, e jurist. Iar aici e Mihai. Mihai e inginer."),
    ("radu",  "Dumneavoastră sunteți manager?"),
    ("dana",  "Da. Dar dumneavoastră? Sunteți economist?"),
    ("radu",  "Nu, nu sunt economist. Sunt contabil."),
    ("dana",  "Nu sunteți din oraș?"),
    ("radu",  "Ba da, sunt din oraș."),
    ("dana",  "Deci... Andreea e la teatru, Dan e la medic, "
              "iar Mihai e în magazin."),
    ("radu",  "Bine. Mulțumesc!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("An office, and someone being shown around it. You will have caught "
        "more than last time — the greetings are yours now. By the end you "
        "will have the jobs too.", pause=P_SECTION)

# ═══ 1. Vocabulary ═══════════════════════════════════════════════════════════
ep.narr("Jobs. There are a lot of them, but most you can almost guess.",
        pause=800, chapter="Jobs")
for r, e, v in [
    ("El e manager.", "He is a manager.", "m"),
    ("El e inginer.", "He is an engineer.", "m"),
    ("El e arhitect.", "He is an architect.", "m"),
    ("El e economist.", "He is an economist.", "m"),
    ("El e contabil.", "He is an accountant.", "m"),
    ("El e jurist.", "He is a lawyer.", "m"),
    ("El e medic.", "He is a doctor.", "m"),
    ("El e actor.", "He is an actor.", "m"),
    ("El e ziarist.", "He is a journalist.", "m"),
    ("El e sportiv.", "He is a sportsman.", "m"),
]:
    ep.teach(r, e, v)

ep.narr("Notice how many of those you understood before I said them. Romanian "
        "is a Romance language and the professional vocabulary is largely "
        "shared with English. Lean on that.", pause=600)

for r, e, v in [
    ("El e funcționar.", "He is a clerk.", "m"),
    ("El e vânzător.", "He is a shop assistant.", "m"),
    ("El e șofer.", "He is a driver.", "m"),
    ("El e ministru.", "He is a minister.", "m"),
    ("El e președinte.", "He is a president.", "m"),
    ("El e profesor.", "He is a teacher.", "m"),
    ("Ea e profesoară.", "She is a teacher.", "f"),
    ("Ea e educatoare.", "She is a nursery teacher.", "f"),
]:
    ep.teach(r, e, v)

ep.narr("Profesor, profesoară. Same move as moldovean, moldoveancă last time — "
        "the feminine adds an ending. Ziarist becomes ziaristă, contabil "
        "becomes contabilă.", pause=P_SECTION)

ep.narr("Now places.", pause=600, chapter="Places")
for r, e, v in [
    ("Aici e un birou.", "Here is an office.", "m"),
    ("Acolo e un magazin.", "There is a shop.", "m"),
    ("Aici e un teatru.", "Here is a theatre.", "m"),
    ("Acolo e un oraș.", "There is a city.", "m"),
    ("Aici e un sat.", "Here is a village.", "m"),
    ("Acolo e o școală.", "There is a school.", "f"),
    ("Aici e o țară.", "Here is a country.", "f"),
]:
    ep.teach(r, e, v)

# ═══ 2. Grammar ══════════════════════════════════════════════════════════════
ep.narr("You just heard two little words doing the same job: un and o. Both "
        "mean 'a'. Which one you use depends on the gender of the noun.",
        pause=800, chapter="un and o")
ep.narr("Un for masculine and for neuter.")
for r in ["un contabil", "un ministru", "un birou", "un sat"]:
    ep.ro(r, "m", NORMAL, 900)
ep.narr("O for feminine.")
for r in ["o țară", "o profesoară", "o educatoare", "o școală"]:
    ep.ro(r, "f", NORMAL, 900)
ep.narr("Romanian has three genders, not two. The third one, neuter, covers "
        "most inanimate things: birou, sat, oraș, magazin, teatru. In the "
        "singular it takes un, exactly like masculine, so for now you have a "
        "simple choice between un and o. The neuter will show its true colours "
        "when we reach plurals.", pause=600)

ep.narr("There is no reliable rule for guessing gender, so learn each noun "
        "with its article attached. Not birou but un birou. Not școală but "
        "o școală. It costs nothing now and saves a great deal later.",
        pause=P_SECTION)

ep.narr("And one thing the book shows but never says out loud. Look at these "
        "two sentences.", pause=600, chapter="No article for jobs")
ep.ro("Aici e un inginer.", "m", NORMAL, 900)
ep.ro("Eu sunt inginer.", "m", NORMAL, 900)
ep.narr("Pointing at a person: un inginer. Saying what you are: inginer, with "
        "no article at all. Never eu sunt un inginer. English puts one in, "
        "Russian leaves it out — here Romanian sides with Russian. If you are "
        "translating from English in your head, this is the mistake you will "
        "make.", pause=600)
for r, e in [("Eu sunt contabil.", "I am an accountant."),
             ("Ea e profesoară.", "She is a teacher."),
             ("Dumneavoastră sunteți medic?", "Are you a doctor?")]:
    ep.teach(r, e, "m" if "Ea" not in r else "f")

# ═══ 3. în and la ════════════════════════════════════════════════════════════
ep.narr("Two prepositions, and the difference is not the one English gives you.",
        pause=800, chapter="în and la")
ep.narr("În is inside something — a country, a building, a room.")
for r in ["în România", "în birou", "în magazin", "în oraș"]:
    ep.ro(r, "m", NORMAL, 900)
ep.narr("La is at a place you go to for a purpose, and with towns.")
for r in ["la București", "la teatru", "la școală", "la medic"]:
    ep.ro(r, "m", NORMAL, 900)
ep.narr("So: în România, la București. The country takes în, the city takes "
        "la. And la medic means at the doctor's — you went there to be seen, "
        "not merely to stand inside the building.", pause=P_SECTION)

# ═══ 4. ba da ════════════════════════════════════════════════════════════════
ep.narr("Now a word English simply does not have, and you heard it in the "
        "dialogue.", pause=600, chapter="ba da")
ep.ro("Nu sunteți din oraș?", "dana", NORMAL, 900)
ep.ro("Ba da, sunt din oraș.", "radu", NORMAL, 1200)
ep.narr("The question was negative: aren't you from the city. In English you "
        "answer 'yes' and hope to be understood, because yes is ambiguous "
        "there. Romanian has a dedicated word: ba da, meaning 'no — on the "
        "contrary, I am'. French does the same thing with si.", pause=600)
ep.teach("Ba da.", "Yes I am — contradicting a negative question.", "m")
ep.narr("Answering just da to a negative question is confusing. Use ba da.",
        pause=P_SECTION)

# ═══ 5. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("The part that is not from the book. Bucharest, not Chișinău, and how "
        "people actually talk.", pause=800, chapter="How people really say it")

ep.narr("First, the biggest gap in this chapter: it teaches you to say your "
        "job, but never to ask about someone else's. There is no question form "
        "anywhere in it. Here it is.")
ep.teach("Cu ce vă ocupați?", "What do you do for a living?", "f")
ep.narr("Literally, what do you occupy yourself with. Polite and neutral — "
        "safe with anyone.", pause=600)
ep.teach("Unde lucrați?", "Where do you work?", "f")
ep.narr("And that one you can already answer: la teatru, în magazin, la "
        "școală.", pause=600)

ep.narr("Second, two words the book has still not given you.")
ep.teach("Mulțumesc.", "Thank you.", "m")
ep.teach("Cu plăcere.", "You're welcome.", "f")

ep.narr("And poftiți, which does several jobs at once — here you are, come in, "
        "go ahead. You will hear it in every shop and office in the country.")
ep.teach("Poftiți.", "Here you are. / Come in.", "f")

ep.narr("Last, the dropped L from episode one, now on this chapter's nouns. "
        "The book writes biroul, magazinul, orașul. What comes out is:")
for r in ["birou'", "magazinu'", "orașu'"]:
    ep.ro(r, "m", SLOW, 1100)
ep.narr("Same rule, more places to use it.", pause=P_SECTION)

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Now the work. English in, Romanian out loud, then the answer. Do not "
        "wait until you are certain.", pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("I am a manager.", "Eu sunt manager.", "m"),
    ("She is an architect.", "Ea e arhitect.", "f"),
    ("He is a lawyer.", "El e jurist.", "m"),
    ("She is a teacher.", "Ea e profesoară.", "f"),
    ("I am not an economist, I am an accountant.",
     "Nu sunt economist, sunt contabil.", "m"),
    ("Here is an office.", "Aici e un birou.", "m"),
    ("There is a school.", "Acolo e o școală.", "f"),
    ("Here is a village, there is a city.", "Aici e un sat, acolo e un oraș.", "m"),
    ("We are in the office.", "Noi suntem în birou.", "m"),
    ("He is at the theatre.", "El e la teatru.", "m"),
    ("They are at the doctor's.", "Ei sunt la medic.", "m"),
    ("I am in Romania, in Bucharest.", "Sunt în România, la București.", "m"),
    ("Are you a driver? Politely.", "Dumneavoastră sunteți șofer?", "m"),
    ("What do you do for a living?", "Cu ce vă ocupați?", "f"),
    ("Where do you work?", "Unde lucrați?", "f"),
    ("Aren't you from the city? — Yes I am.", "Ba da, sunt din oraș.", "m"),
    ("She is a shop assistant, he is a journalist.",
     "Ea e vânzătoare, el e ziarist.", "f"),
    ("Thank you. — You're welcome.", "Mulțumesc. Cu plăcere.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 7. Review of episode 1 ══════════════════════════════════════════════════
ep.review([
    ("I am Moldovan — a woman speaking.", "Eu sunt moldoveancă.", "f"),
    ("He is Ukrainian.", "El e ucrainean.", "m"),
    ("Good morning, madam!", "Bună dimineața, doamnă!", "f"),
    ("She is not from Russia.", "Ea nu e din Rusia.", "f"),
    ("Nice to meet you.", "Îmi pare bine.", "f"),
    ("Well... I am not from Chișinău.", "Păi, nu sunt din Chișinău.", "m"),
    ("Are you English? Respectfully.", "Dumneavoastră sunteți englez?", "m"),
])

# ═══ 8. Text ═════════════════════════════════════════════════════════════════
ep.narr("The chapter's own text. Slowly first.", pause=800, chapter="Text")
BOOK_TEXT = [
    "Aici este un birou. În birou sunt: un inginer, un arhitect și un jurist.",
    "El este Dan. Dan este jurist.",
    "Ea e Andreea. Andreea este arhitect, iar eu sunt manager.",
    "Noi suntem din oraș. Ei sunt Ion și Mihai. Ei sunt din sat.",
    "Aici este un teatru. Dumneavoastră sunteți actor. Noi suntem la teatru.",
    "Dumneata ești vânzător, iar el este medic.",
    "Ei sunt în magazin. Voi sunteți la medic.",
    "Aici este un sportiv. Acolo este un ziarist.",
]
for line in BOOK_TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in BOOK_TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("The book also gives a proverb for this chapter. Meseria este brățară "
        "de aur — a trade is a bracelet of gold. Worth having, even if the "
        "grammar in it is months away.", pause=800)
ep.ro("Meseria este brățară de aur.", "m", SLOW, 1400)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The office again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Notice what Dana said without our ever teaching it as grammar: domnu' "
        "instead of domnul, e instead of este, deci while she thought. That "
        "was last episode's spoken section, used as ordinary speech.",
        pause=600)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("Before next time: say what you do. Sunt, then your job, no article. "
        "Then ask it back — cu ce vă ocupați. Pe curând!", pause=1500,
        chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("2", []))
