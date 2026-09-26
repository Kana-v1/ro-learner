"""
Episode 04A — "Sunt acasă" (Lecția 4, first half)

Lecția 4 is 36 items — the largest chapter yet — so it splits along its two
grammar points. This half is the home and its rooms, the words for being at,
near, or far from home, and the politeness pronouns dumnealui / dumneaei /
dumnealor (how to speak respectfully about a third person). The plural, the
furniture, and niște go to 4B.

Scene: Sanda shows Radu round her apartment — the book's own role-play, "Dvs.
sunteți în vizită. Sanda vă arată apartamentul." A person walking a visitor
through the rooms says "here's the hall, the kitchen's there, the bedroom's
near" as a matter of course, so the repetition is what a host actually does.

Continuity: episode 3's spoken layer is ordinary speech now — dropped -l
(apartamentu', dormitoru') and Ce-i asta? are used unremarked. Episode 1-2 forms
continue (e, domnu', Poftiți, Mulțumesc, Îmi pare bine). The politeness pronouns
build straight on episode 1's dumneavoastră / dumneata.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# The home-and-rooms half of Lecția 4's VOCABULAR block, plus the place adverbs
# and the third-person politeness pronouns this half is built on.
REQUIRED = [
    "casă", "bloc", "apartament", "antreu", "cameră", "baie", "bucătărie",
    "dormitor", "salon", "covor", "podea", "tavan",
    "acasă", "acum", "aproape", "departe",
    "dumnealui", "dumneaei", "dumnealor",
]

GLUE = {
    "frumos / frumoasă": "nice, lovely",
    "bun": "good",
    "Sanda / Mihai / Ana": "names",
}

ep = Episode(number=4, lesson=4, part="a", title="Sunt acasă",
             source="Limba care ne unește, nivelul I — Lecția 4 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună ziua, domnu' Radu! Poftiți."),
    ("radu",  "Bună ziua, Sanda! Mulțumesc."),
    ("dana",  "Deci, acesta e apartamentul. Aici e antreul, iar acolo e "
              "bucătăria."),
    ("radu",  "Frumos! Camera e aproape?"),
    ("dana",  "Da, dormitorul e aici, aproape. Salonul e acolo, iar baia e "
              "departe."),
    ("radu",  "Dar acum? Cine e acasă?"),
    ("dana",  "Dumnealui e Mihai. E inginer. Dumneaei e Ana."),
    ("radu",  "Îmi pare bine."),
    ("dana",  "Poftiți în salon. E o casă frumoasă, nu?"),
    ("radu",  "Da! Un bloc bun."),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("A visit. Sanda is showing Radu round her apartment — the hall, the "
        "kitchen, which room is near and which is far — and mentioning, "
        "politely, who is home. By the end you will do the same walk.",
        pause=P_SECTION)

# ═══ 1. Vocabulary — the rooms ═══════════════════════════════════════════════
ep.narr("A home, room by room. Each inside a sentence — say it out loud in the "
        "gap.", pause=800, chapter="The rooms")
for r, e, v in [
    ("Aceasta e o casă.", "This is a house.", "f"),
    ("Acesta e un bloc.", "This is an apartment block.", "m"),
    ("Acesta e un apartament.", "This is an apartment.", "m"),
    ("Acesta e un antreu.", "This is an entrance hall.", "m"),
    ("Aceasta e o cameră.", "This is a room.", "f"),
    ("Aceasta e o baie.", "This is a bathroom.", "f"),
    ("Aceasta e o bucătărie.", "This is a kitchen.", "f"),
    ("Acesta e un dormitor.", "This is a bedroom.", "m"),
    ("Acesta e un salon.", "This is a living room.", "m"),
]:
    ep.teach(r, e, v)

ep.narr("And the surfaces of a room.", pause=600)
for r, e, v in [
    ("Acesta e un covor.", "This is a carpet.", "m"),
    ("Aceasta e o podea.", "This is a floor.", "f"),
    ("Acesta e un tavan.", "This is a ceiling.", "m"),
]:
    ep.teach(r, e, v)

# ═══ 2. At home, near and far ════════════════════════════════════════════════
ep.narr("Now where things are, and where you are. Home, near, far, now.",
        pause=800, chapter="acasă, aproape, departe")
for r, e in [
    ("Sunt acasă.", "I am at home."),
    ("Acum sunt în bucătărie.", "Now I am in the kitchen."),
    ("Dormitorul e aproape.", "The bedroom is near."),
    ("Baia e departe.", "The bathroom is far."),
    ("Salonul e aproape, iar baia e departe.",
     "The living room is near, and the bathroom is far."),
]:
    ep.teach(r, e, "m")

# ═══ 3. Grammar — the politeness pronouns ════════════════════════════════════
ep.narr("Now people. In episode one you met dumneavoastră and dumneata — the "
        "respectful ways to say you. Romanian does the same for he, she and "
        "they: a polite set for speaking about someone with respect.",
        pause=800, chapter="dumnealui, dumneaei, dumnealor")
for r, e in [("Dumnealui e acasă.", "He is at home. — respectfully."),
             ("Dumnealui e inginer.", "He is an engineer."),
             ("Dumneaei e în bucătărie.", "She is in the kitchen."),
             ("Dumneaei e profesoară.", "She is a teacher."),
             ("Dumnealor sunt acasă.", "They are at home.")]:
    ep.teach(r, e, "m" if "Dumnealui" in r or "Dumnealor" in r else "f")
ep.narr("Dumnealui, he. Dumneaei, she. Dumnealor, they — and dumnealor takes "
        "sunt, the plural, like dumneavoastră did. They point back at a "
        "person you are treating with respect.", pause=600)
ep.teach("Cine e dumnealui? Dumnealui e domnu' Radu.",
         "Who is he? He is Mr Radu.", "m")

# ═══ 4. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes in Bucharest — and the question the chapter "
        "forgot.", pause=800, chapter="How people really say it")

ep.narr("The whole lesson is about the home, yet it never teaches you to ask "
        "where someone lives. Here it is:")
ep.teach("Unde locuiești?", "Where do you live?", "f")
ep.narr("Locuiești is the book's verb. In speech, unde stai — where do you "
        "stay — is just as common. Answer with what you have: la bloc, "
        "într-un apartament.", pause=600)

ep.narr("And those polite pronouns. Dumnealui and dumneaei are correct and "
        "genuinely respectful — but formal. You would use them about someone "
        "older, a superior, in an office. Among people your own age, el and "
        "ea are perfectly neutral.")
for r in ["el", "ea"]:
    ep.ro(r, "m", SLOW, 900)
ep.narr("With a stranger, though, dumnealui is never wrong. Keep both.",
        pause=P_SECTION)

# ═══ 5. Drill ════════════════════════════════════════════════════════════════
ep.narr("The work. English in, a whole Romanian sentence out loud, then the "
        "answer. Take your time — the gap is long on purpose.",
        pause=P_SECTION, chapter="Drill")
for cue, ans, v in [
    ("This is a house.", "Aceasta e o casă.", "f"),
    ("This is an apartment.", "Acesta e un apartament.", "m"),
    ("This is an apartment block.", "Acesta e un bloc.", "m"),
    ("Here is a hall, there is a kitchen.",
     "Aici e un antreu, acolo e o bucătărie.", "m"),
    ("This is a room.", "Aceasta e o cameră.", "f"),
    ("This is a bedroom, and this is a living room.",
     "Acesta e un dormitor, iar acesta e un salon.", "m"),
    ("This is a bathroom.", "Aceasta e o baie.", "f"),
    ("This is a carpet.", "Acesta e un covor.", "m"),
    ("This is a floor, and this is a ceiling.",
     "Aceasta e o podea, iar acesta e un tavan.", "f"),
    ("I am at home.", "Sunt acasă.", "m"),
    ("The apartment is near.", "Apartamentul e aproape.", "m"),
    ("The house is far.", "Casa e departe.", "f"),
    ("Now I am in the kitchen.", "Acum sunt în bucătărie.", "m"),
    ("He is at home. — respectfully.", "Dumnealui e acasă.", "m"),
    ("She is in the kitchen. — respectfully.", "Dumneaei e în bucătărie.", "f"),
    ("They are at home. — respectfully.", "Dumnealor sunt acasă.", "m"),
    ("Who is he? — He is Mr Radu.", "Cine e dumnealui? Dumnealui e domnu' Radu.", "m"),
    ("Where do you live?", "Unde locuiești?", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 6. Review of episodes 2-3 ═══════════════════════════════════════════════
ep.review([
    ("What is this? — A dictionary.", "Ce e acesta? Un dicționar.", "m"),
    ("On the table there is a flower.", "Pe masă e o floare.", "f"),
    ("Next to the window there is a bench.", "Lângă fereastră e o bancă.", "f"),
    ("Who is this? — A course student.", "Cine e acesta? Un cursant.", "m"),
    ("What do you do for a living?", "Cu ce vă ocupați?", "f"),
    ("He is a lawyer, she is a teacher.", "El e jurist, ea e profesoară.", "m"),
])

# ═══ 7. A short passage, and the proverb ═════════════════════════════════════
ep.narr("A few sentences run together. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Sunt acasă. Acesta e apartamentul.",
    "Aici e un antreu și o bucătărie.",
    "Acolo e un dormitor, un salon și o baie. Camera e aproape.",
    "Dumnealui e Mihai. E inginer. Dumneaei e Ana.",
    "Acum, dumnealor sunt acasă. E o casă frumoasă.",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

ep.narr("The chapter's proverb, and it fits the lesson's name. Acasă este ca "
        "în rai — home is like paradise. There's no place like home.",
        pause=800)
ep.ro("Acasă este ca în rai.", "m", SLOW, 1400)

# ═══ 8. Cold open again ══════════════════════════════════════════════════════
ep.narr("The visit again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)
ep.narr("Next time, the other half — the furniture in these rooms, and how one "
        "chair becomes some chairs.", pause=600)

# ═══ 9. Close ════════════════════════════════════════════════════════════════
ep.narr("Before next time: walk through your own home out loud. Aici e..., "
        "acolo e..., camera e aproape. And say where you live — unde stai. "
        "Pe curând!", pause=1500, chapter="Close")

ep.emit(spoken_layer=load("spoken.json").get("4", []))
