"""
Episode 12E — "Un decor frumos" (Lecția 12 "La teatru", memory-first, part 5)

Six items: cunosc, trec, aplaudă, decor, amator, prieten — from the book's
exercises "Cunoști orașul acesta?", "Fiecare cunoaște bine orașul?", "A trece
– eu, pe lângă școală", and the text's "mari amatori de teatru" and
"spectatorii aplaudă".

Know changes its sound twice (cunosc → cunoști → cunoaște), so each form is
heard alone before it is built, as in 11A; the polite form is then built from
she, the way spuneți came from spune. Know is set beside nu știu (11H) once —
two forms side by side — because English has one verb where Romanian has two.
Go past is plain like go, so the learner builds it. Fan and friend make their
plural like spectator from 12C (spectator → spectatori), so the learner builds
amatori and prieteni after hearing one.

12D's results: înainte and înapoi were swapped ("Mergeți înapoi" for straight
on, twice), so the dialogue's directions end on înainte and the drill asks
both. 12D's spoken layer (Ce zici?, Îți scriu.) is ordinary speech here.

Scene: the theatre foyer after the show. Elena is new in town; Radu is a
theatre fan who knows the way — so applaud, scenery, fan, friend, know and go
past come round naturally.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["cunosc", "trec", "aplaudă", "decor", "amator", "prieten"]
GLUE = {}

ep = Episode(number=12, lesson=12, part="e", title="Un decor frumos",
             source="Limba care ne unește, nivelul I — Lecția 12 (partea E)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("elena", "Ce decor frumos!"),
    ("radu", "Da, și spectatorii aplaudă. Ce zici?"),
    ("elena", "Un spectacol interesant. Mergi în fiecare seară la teatru?"),
    ("radu", "Nu în fiecare seară. Dar eu și prietenul meu suntem amatori de teatru."),
    ("elena", "Eu nu cunosc bine orașul. Cum ajung acasă?"),
    ("radu", "Pe jos. Treci pe lângă școală și mergi înainte."),
    ("elena", "Mulțumesc! Îți scriu când ajung."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("The show is over. Elena is new in town, and she has to find her way "
        "home.", pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("decor", "the scenery — on a stage", "un decor", "m",
            teach_ro="Un decor frumos.", teach_en="Beautiful scenery.")
ep.new_item("cunosc", "I know — a place or a person", "cunosc", "f",
            teach_ro="Cunosc orașul.", teach_en="I know the city.")
ep.new_item("aplaudă", "they applaud", "aplaudă", "m",
            teach_ro="Spectatorii aplaudă.", teach_en="The spectators applaud.")
ep.new_item("prieten", "a friend", "un prieten", "f",
            teach_ro="Un prieten de la serviciu.", teach_en="A friend from work.")
ep.new_item("trec", "I go past", "trec", "m",
            teach_ro="Trec pe lângă școală.", teach_en="I go past the school.")
ep.new_item("amator", "a fan — of something", "un amator", "f",
            teach_ro="Un amator de teatru.", teach_en="A theatre fan.")
ep.narr("Mixed. Just the word.", pause=800)
for cue, ans, v in [("I go past", "trec", "f"), ("a friend", "un prieten", "m"),
                    ("they applaud", "aplaudă", "f"), ("a fan", "un amator", "m"),
                    ("I know — a place", "cunosc", "f"),
                    ("the scenery", "un decor", "m")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Know — the sound changes ═════════════════════════════════════════════
ep.narr("Know changes its sound to a friend. Listen:", pause=800,
        chapter="Know, by ear")
ep.ro("Cunoști orașul?", "f", SLOW, 1700)
ep.drill("you know — to a friend", "cunoști", "m")
ep.drill("Do you know the city? To a friend.", "Cunoști orașul?", "f")
ep.narr("And for she, it changes again. Listen:", pause=P_SHORT)
ep.ro("Cunoaște bine orașul.", "m", SLOW, 1900)
ep.drill("she knows", "cunoaște", "f")
ep.drill("He knows the city well.", "Cunoaște bine orașul.", "m",
         accept=["Cunoaște orașul bine."])
ep.narr("You can't work these out — learn them by ear. Polite is built from "
        "she, the way say went. Build it.", pause=P_SHORT)
ep.drill("Do you know the city? Politely.", "Cunoașteți orașul?", "f")
for cue, ans, v in [("I know — a place", "cunosc", "m"),
                    ("you know — to a friend", "cunoști", "f"),
                    ("she knows", "cunoaște", "m")]:
    ep.drill(cue, ans, v)
ep.narr("This know is for places and people. A fact is the other word, from "
        "I don't know. Listen to both:", pause=800)
ep.ro("Nu știu. Nu cunosc orașul.", "f", SLOW, 2200)
ep.drill("I don't know the city.", "Nu cunosc orașul.", "m")
ep.drill("I don't know.", "Nu știu.", "f")

# ═══ 3. Go past ══════════════════════════════════════════════════════════════
ep.narr("Go past goes like go. You haven't heard these — build them.",
        pause=800, chapter="Go past")
ep.drill("you go past — to a friend", "treci", "m")
ep.drill("she goes past", "trece", "f")
ep.drill("The bus goes past the theatre.", "Autobuzul trece pe lângă teatru.", "m")
ep.drill("Go past the school! To a friend.", "Treci pe lângă școală!", "f")
ep.drill("Do you go past the theatre? Politely.", "Treceți pe lângă teatru?", "m")

# ═══ 4. Fans and friends ═════════════════════════════════════════════════════
ep.narr("Fan goes like spectator: one, then many. Listen:", pause=800,
        chapter="Fans and friends")
ep.ro("Un amator. Mulți amatori.", "f", SLOW, 2000)
ep.drill("many fans", "mulți amatori", "m")
ep.drill("We're theatre fans.", "Suntem amatori de teatru.", "f")
ep.narr("Friend goes the same way. Build it.", pause=P_SHORT)
ep.drill("many friends", "mulți prieteni", "m")
ep.drill("my friend", "prietenul meu", "f")
ep.drill("I go to the theatre with friends.", "Merg la teatru cu prietenii.", "m",
         accept=["Merg cu prietenii la teatru."])

# ═══ 5. Applaud, scenery ═════════════════════════════════════════════════════
ep.narr("Applaud — they, and I. Listen to both:", pause=800,
        chapter="Applaud")
ep.ro("Ei aplaudă. Eu aplaud.", "m", SLOW, 2000)
ep.drill("I applaud", "aplaud", "f")
ep.drill("The spectators applaud.", "Spectatorii aplaudă.", "m")
ep.drill("The scenery is beautiful.", "Decorul e frumos.", "f")
ep.drill("an interesting set", "un decor interesant", "m")

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("What beautiful scenery!", "Ce decor frumos!", "f", {}),
    ("Do you go to the theatre every evening? To a friend.",
     "Mergi la teatru în fiecare seară?", "m",
     {"accept": ["Mergi în fiecare seară la teatru?"]}),
    ("My friend is a theatre fan.", "Prietenul meu e un amator de teatru.", "f", {}),
    ("I don't know the city well.", "Nu cunosc bine orașul.", "m",
     {"accept": ["Nu cunosc orașul bine."]}),
    ("How do I get home?", "Cum ajung acasă?", "f", {}),
    ("Go straight on! Politely.", "Mergeți înainte!", "m", {}),
    ("Go back! Politely.", "Mergeți înapoi!", "f", {}),
    ("Go past the school and go straight on. To a friend.",
     "Treci pe lângă școală și mergi înainte.", "m", {}),
    ("Everyone knows the city.", "Fiecare cunoaște orașul.", "f", {}),
    ("What do you think? To a friend.", "Ce zici?", "m", {"accept": ["Ce spui?"]}),
    ("I'll write to you when I get there.", "Îți scriu când ajung.", "f", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. Careful with my friend: from a woman, it often "
        "means my boyfriend. For just a friend, people say a friend of mine. "
        "Listen:", pause=800, chapter="How people really say it")
ep.ro("Un prieten de-al meu.", "m", SLOW, 1700)
ep.narr("And at the end of a show, spectators don't only applaud. Listen:",
        pause=P_SHORT)
ep.ro("Bravo! Bravo!", "f", NORMAL, 1400)
ep.narr("Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("The theatre again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("Beautiful scenery, a theatre fan, and the way home.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("12", []))
