"""
Episode 06G — "Din nou: familia" (Lecția 6 "În familie", repair)

No new words. The app's results for 6C–6F (first time right: 10/38, 6/34,
12/33, 6/33) showed Lecția 6 was not held, and piling Lecția 7 on top would
repeat the 5A failure. So this episode is only the words and patterns that
kept coming back wrong, asked again and again at growing gaps:

- words never produced at all: nume, prenume, elev, fiică, bogat, sărac,
  deștept, tanti, tată; nume and prenume confused; fiică said as soră
- agreement, both directions: acesta for aceasta, bolnav for bolnavă, slabă
  for slab, săracă for sărac
- plurals: părinții, frații, tineri, membri, copii deștepți
- an article before a profession (e un medic), which English puts in

Drill answers reuse the exact strings the app marked wrong, so getting one
right here clears it from state.json "struggles" on the next ingest.

Each weak word follows an expanding ladder: heard, recalled at once, recalled
again after the next word, again in the mixed round, and once more at the end.

Scene: a school office registering a pupil — the secretary has to ask every
parent for surname, first name, and who is who, so the repetition is her job.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

# Anchors for the coverage check: nothing is introduced, all of it is repaired.
REQUIRED = ["nume", "prenume", "elev", "fiică", "nepot", "unchi",
            "bogat", "sărac", "deștept", "slab", "tânăr", "bolnav", "tanti"]
GLUE = {"Popescu / Radu / Ana": "names", "aici": "here"}

ep = Episode(number=6, lesson=6, part="g", title="Din nou: familia",
             source="Limba care ne unește, nivelul I — Lecția 6 (recapitulare)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Bună ziua. Numele, vă rog?"),
    ("radu", "Popescu."),
    ("dana", "Și prenumele?"),
    ("radu", "Radu. Am un fiu și o fiică."),
    ("dana", "Fiul dumneavoastră e elev aici?"),
    ("radu", "Da, e elev. Și fiica mea e elevă."),
    ("dana", "Sunt deștepți?"),
    ("radu", "Da, și harnici."),
]


def ladder(words, voice_for):
    """Teach each word, recall it at once, then recall the one before it —
    the gap before each recall grows by one word every step."""
    prev = None
    for cue, ans, teach_ro, teach_en in words:
        v = voice_for(ans)
        ep.teach(teach_ro, teach_en, v)
        ep.recall_word(cue, ans, v)
        if prev:
            ep.recall_word(prev[0], prev[1], voice_for(prev[1]))
        prev = (cue, ans)


def alternate():
    state = {"n": 0}

    def pick(_):
        state["n"] += 1
        return "m" if state["n"] % 2 else "f"
    return pick


# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("No new words today. Your answers from the last four episodes say part "
        "of Lesson 6 didn't stick, so this episode is those words, over and "
        "over, until they come out without a search.", pause=P_SECTION)

# ═══ 1. People ═══════════════════════════════════════════════════════════════
ep.narr("First, six words for people. Each one: hear it, then say it, then say "
        "the one before it.", pause=800, chapter="People")
ep.narr("One pair to keep apart. The first word is your family name. The "
        "second starts with pre, like before — the name that comes before it, "
        "your first name.", pause=P_SHORT)
ladder([
    ("a name, a surname", "un nume", "Numele meu e Popescu.", "My surname is Popescu."),
    ("a first name", "un prenume", "Prenumele meu e Radu.", "My first name is Radu."),
    ("a daughter", "o fiică", "Am o fiică.", "I have a daughter."),
    ("a pupil", "un elev", "Fiul meu e elev.", "My son is a pupil."),
    ("a nephew, or a grandson", "un nepot", "Copilul e nepotul meu.", "The child is my nephew."),
    ("an uncle", "un unchi", "Am un unchi.", "I have an uncle."),
], alternate())

ep.narr("Daughter is not sister. You said sister twice where daughter was "
        "asked. Listen to the two:", pause=P_SHORT)
ep.ro("o fiică, o soră", "f", SLOW, 1800)
ep.narr("Daughter, sister. Again, and say them with her.", pause=P_SHORT)
ep.ro("o fiică, o soră", "f", SLOW, 2400)

ep.narr("The six, mixed. With un or o, each time.", pause=800)
for cue, ans, v in [("a first name", "un prenume", "m"), ("an uncle", "un unchi", "f"),
                    ("a name", "un nume", "m"), ("a daughter", "o fiică", "f"),
                    ("a nephew", "un nepot", "m"), ("a pupil, a schoolboy", "un elev", "f"),
                    ("a parent", "un părinte", "m"), ("a husband", "un soț", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. What people are like ═════════════════════════════════════════════════
ep.narr("Now six describing words, the same way. The plain form, as for a man.",
        pause=800, chapter="What they are like")
ladder([
    ("rich", "bogat", "Unchiul meu e bogat.", "My uncle is rich."),
    ("poor", "sărac", "El nu e sărac.", "He isn't poor."),
    ("clever", "deștept", "Copilul e deștept.", "The child is clever."),
    ("thin", "slab", "E slab, dar sănătos.", "He's thin, but healthy."),
    ("young", "tânăr", "Fratele lui e tânăr.", "His brother is young."),
    ("ill", "bolnav", "Fiul lor e bolnav.", "Their son is ill."),
], lambda _: "m")

ep.narr("Mixed.", pause=800)
for cue, ans in [("poor", "sărac"), ("clever", "deștept"), ("rich", "bogat"),
                 ("ill", "bolnav"), ("young", "tânăr"), ("thin", "slab")]:
    ep.recall_word(cue, ans, "m")

# ═══ 3. For him, for her ═════════════════════════════════════════════════════
ep.narr("For a woman these words take an ending, and you mixed the two up in "
        "both directions. Listen to him, then her:", pause=800,
        chapter="Him and her")
ep.example(None, "El e bogat. Ea e bogată.", "m", 1600)
ep.example(None, "Fiul e deștept. Fiica e deșteaptă.", "m", 1600)
ep.narr("And this one, for him and for her:", pause=P_SHORT)
ep.example(None, "Acesta e unchiul meu. Aceasta e mătușa mea.", "f", 1800)
ep.narr("So in pairs. Him first, then her.", pause=800)
for cue, ans, v in [
    ("He is poor.", "El e sărac.", "m"),
    ("She is poor.", "Ea e săracă.", "f"),
    ("My brother is thin.", "Fratele meu e slab.", "m"),
    ("My sister is thin.", "Sora mea e slabă.", "f"),
    ("His brother is ill.", "Fratele lui e bolnav.", "m"),
    ("His sister is ill.", "Sora lui e bolnavă.", "f"),
    ("The child is clever.", "Copilul e deștept.", "m"),
    ("A clever daughter.", "O fiică deșteaptă.", "f"),
    ("This is my uncle.", "Acesta e unchiul meu.", "m"),
    ("This is my aunt.", "Aceasta e mătușa mea.", "f"),
    ("This is Auntie Ana.", "Aceasta e tanti Ana.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. More than one ════════════════════════════════════════════════════════
ep.narr("More than one person: the ending is an i. Listen:", pause=800,
        chapter="More than one")
ep.example(None, "părinții mei, frații mei, copii deștepți", "m", 1800)
for cue, ans, v in [
    ("My parents are young.", "Părinții mei sunt tineri.", "m"),
    ("My brothers are at home.", "Frații mei sunt acasă.", "f"),
    ("Clever children.", "Copii deștepți.", "m"),
    ("Their parents are young.", "Părinții lor sunt tineri.", "f"),
    ("Who are these? — My parents.", "Cine sunt aceștia? Părinții mei.", "m"),
    ("We have relatives.", "Avem rude.", "f"),
    ("My family has hardworking members.", "Familia mea are membri harnici.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. No article before a job ══════════════════════════════════════════════
ep.narr("One more habit from English. English says he is a doctor; Romanian "
        "says he is doctor, with nothing in between. Listen:", pause=800,
        chapter="Jobs")
ep.example(None, "Bunicul nostru e medic.", "m", 1600)
for cue, ans, v in [
    ("Is your father a doctor? To a friend.", "Tatăl tău e medic?", "m"),
    ("My son is a pupil.", "Fiul meu e elev.", "f"),
    ("Our grandfather is a doctor.", "Bunicul nostru e medic.", "m"),
    ("Is your aunt a teacher? To a friend.", "Mătușa ta e profesoară?", "f"),
    ("Her daughter is a pupil.", "Fiica ei e elevă.", "m"),
    ("She is a shop assistant, he is a journalist.", "Ea e vânzătoare, el e ziarist.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 6. Whole sentences ══════════════════════════════════════════════════════
ep.narr("Now everything at once. Whole sentences, take your time — the app "
        "waits while you think.", pause=P_SECTION, chapter="Whole sentences")
for cue, ans, v in [
    ("My surname is Popescu.", "Numele meu e Popescu.", "m"),
    ("Your first name, please? Politely.", "Prenumele dumneavoastră, vă rog?", "f"),
    ("I have a son and a daughter.", "Am un fiu și o fiică.", "m"),
    ("The child is my nephew.", "Copilul e nepotul meu.", "f"),
    ("Do you have an uncle? — Yes, I have an uncle.", "Ai un unchi? Da, am un unchi.", "m"),
    ("My son is short and thin.", "Fiul meu e scund și slab.", "f"),
    ("His wife is young and clever.", "Soția lui e tânără și deșteaptă.", "m"),
    ("Her daughter is hardworking.", "Fiica ei e harnică.", "f"),
    ("He isn't poor.", "El nu e sărac.", "m"),
    ("My uncle is rich.", "Unchiul meu e bogat.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 7. Last sweep ═══════════════════════════════════════════════════════════
ep.narr("A last sweep: just the word, with un or o where it has one. A few "
        "clothes from Lesson 5 are mixed in.", pause=P_SECTION, chapter="Last sweep")
for cue, ans, v in [("a name", "un nume", "m"), ("rich", "bogat", "f"),
                    ("a t-shirt", "un tricou", "m"), ("a daughter", "o fiică", "f"),
                    ("poor", "sărac", "m"), ("a first name", "un prenume", "f"),
                    ("a dress", "o rochie", "m"), ("clever", "deștept", "f"),
                    ("father", "tată", "m"), ("a pupil, a schoolboy", "un elev", "f"),
                    ("auntie, before a name", "tanti", "m"), ("a raincoat", "un impermeabil", "f"),
                    ("an uncle", "un unchi", "m"), ("thin", "slab", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The school office again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("That's the family, again. Next time, Lesson 7.", pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=[])
