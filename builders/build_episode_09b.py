"""
Episode 09B — "Ședința e la zece" (Lecția 9 "O zi la serviciu", memory-first, part 2)

Six items from the chapter list: organizez and notez (-ez verbs, like 09A's),
verific (a verifica — in the chapter's list but conjugated WITHOUT -ez:
verific, verifici, verifică), ședință, agendă, calculator. verific is the point
of the rule section: two verbs that look alike in the dictionary behave
differently, which is exactly why each verb is learnt by its I-form. Rule
section in the 09A style: Romanian voice for every form, pattern first, one
short sentence, then the learner builds an unheard form.

Scene: two colleagues preparing a meeting — who organises, who takes notes,
who checks the computer — so the three verbs pass between persons.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["organizez", "notez", "verific", "ședință", "agendă", "calculator"]
GLUE = {}

ep = Episode(number=9, lesson=9, part="b", title="Ședința e la zece",
             source="Limba care ne unește, nivelul I — Lecția 9 (partea B)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("radu", "Cine organizează ședința de azi?"),
    ("dana", "Eu. Ședința e la zece."),
    ("radu", "Și cine notează?"),
    ("dana", "Notez eu, în agendă."),
    ("radu", "Bine. Eu verific calculatorul."),
    ("dana", "Mulțumesc!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "radu", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Two colleagues getting a meeting ready. Three verbs, three things at "
        "work.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("The six, one at a time.", pause=800, chapter="Six words")
ep.new_item("organizez", "I organise", "organizez", "m",
            teach_ro="Organizez o ședință.", teach_en="I'm organising a meeting.")
ep.new_item("ședință", "a meeting — at work", "o ședință", "f",
            teach_ro="Ședința e la zece.", teach_en="The meeting is at ten.")
ep.new_item("notez", "I note down", "notez", "m",
            teach_ro="Notez în agendă.", teach_en="I write it in the planner.")
ep.new_item("agendă", "a planner, a diary", "o agendă", "f",
            teach_ro="Am o agendă nouă.", teach_en="I have a new planner.")
ep.new_item("verific", "I check", "verific", "m",
            teach_ro="Verific calculatorul.", teach_en="I check the computer.")
ep.new_item("calculator", "a computer", "un calculator", "f",
            teach_ro="Calculatorul e vechi.", teach_en="The computer is old.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I check", "verific", "m"), ("a meeting", "o ședință", "f"), ("I organise", "organizez", "m"),
                    ("a computer", "un calculator", "f"), ("I note down", "notez", "m"),
                    ("a planner", "o agendă", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Which kind? ═══════════════════════════════════════════════════════════
ep.narr("Two of these have the extra piece, like work. Listen — note down:",
        pause=800, chapter="Which kind")
ep.ro("notez, notezi, notează", "f", SLOW, 1800)
ep.narr("Check doesn't — it goes like listen. Listen:", pause=P_SHORT)
ep.ro("verific, verifici, verifică", "m", SLOW, 1800)
ep.narr("Nothing in the word tells you. The I-form does — that's why you learn "
        "it first. Build the others.", pause=800)
for cue, ans, v in [("you note down — to a friend", "notezi", "m"), ("she checks", "verifică", "f"),
                    ("he organises", "organizează", "m"), ("you check — to a friend", "verifici", "f"),
                    ("we organise", "organizăm", "m"), ("you all check", "verificați", "f"),
                    ("they note down", "ei notează", "m"), ("we check", "verificăm", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Drill ════════════════════════════════════════════════════════════════
ep.narr("Whole sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Who is organising today's meeting?", "Cine organizează ședința de azi?", "m", {}),
    ("I'm organising the meeting.", "Eu organizez ședința.", "f", {"accept": ["Organizez eu ședința."]}),
    ("The meeting is at ten sharp.", "Ședința e la zece fix.", "m", {}),
    ("Are you writing it in the planner? To a friend.", "Notezi în agendă?", "f", {}),
    ("I check the forms.", "Verific formularele.", "m", {}),
    ("She checks the computer.", "Ea verifică calculatorul.", "f", {}),
    ("We write it in the planner.", "Notăm în agendă.", "m", {}),
    ("Do you all have a meeting today?", "Aveți ședință azi?", "f", {"accept": ["Aveți o ședință azi?"]}),
    ("They organise a lot of meetings.", "Ei organizează multe ședințe.", "m", {}),
    ("The computer is new, the planner is old.", "Calculatorul e nou, agenda e veche.", "f", {}),
    ("Who's taking notes? — I am.", "Cine notează? — Eu.", "m", {"accept": ["Cine notează? — Notez eu."]}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 3b. All of Lesson 9 so far ═══════════════════════════════════════════════
ep.narr("And the verbs from the first day, mixed in. The person and the verb; "
        "build the form.", pause=P_SECTION, chapter="Lesson 9 so far")
for cue, ans, v in [
    ("you work — to a friend", "lucrezi", "m"), ("she signs", "semnează", "f"),
    ("we fill in", "completăm", "m"), ("they check", "ei verifică", "f"),
    ("you all organise", "organizați", "m"), ("I note down", "notez", "f"),
    ("he works", "lucrează", "m"), ("you check — to a friend", "verifici", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. In many Bucharest offices the English word has "
        "moved in. Listen:", pause=800, chapter="How people really say it")
ep.ro("Am o ședință. Am un meeting.", "f", SLOW, 1800)
ep.narr("Both mean the same; the book's word is never wrong.", pause=P_SECTION)

# ═══ 5. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=10)

# ═══ 6. Cold open again ══════════════════════════════════════════════════════
ep.narr("The two colleagues again. Same recording.", pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 7. Close ════════════════════════════════════════════════════════════════
ep.narr("Organise, note down, check — and which kind each one is.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("9", []))
