"""
Episode 05R — "Recapitulare (1–5)" (consolidation after Lecția 5)

A generalization episode. No new vocabulary — every word and structure here has
been taught in episodes 1 to 5. The textbook does the same thing: after five
lessons it stops and lists what you now know (genders, plurals, both articles,
the pronouns, a fi, four-form adjectives) and what you can now do (greet, say
what you are, point at things, address people respectfully, ask where something
is). This episode turns that summary into retrieval.

It is built as one long drill, organised by grammar thread rather than by
lesson, so the same structure comes back cued from several angles. The cold-open
dialogue weaves all five lessons into a single visit; the closing monologue is a
full self-introduction using only what the block has taught.

Convention: a recap like this comes after every five lessons (see CLAUDE.md),
named with part="r" so it sorts after the block's last episode.
"""
from episode_kit import Episode, load, P_SECTION, NORMAL, SLOW

# Not a vocabulary list — a spread of anchor items, two or three per lesson, so
# the coverage check guarantees the recap actually touches all five lessons.
REQUIRED = [
    "sunt", "din", "moldovean",              # L1
    "inginer", "la", "ba da",                # L2
    "acesta", "cine", "pe", "lângă",         # L3
    "acasă", "niște", "dumnealui", "sub",    # L4
    "palton", "bluză", "fular", "alb",       # L5 — the wardrobe, now five parts
    "negru", "frumos", "cum", "unde",        # L5
]

GLUE = {
    "Și mie": "likewise — the reply to 'nice to meet you'",
    "Sanda / Mihai / Ana / Radu": "names",
}

ep = Episode(number=5, lesson=5, part="r", title="Recapitulare (1–5)",
             source="Limba care ne unește, nivelul I — Recapitulare, lecțiile 1–5",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana",  "Bună ziua, domnu' Radu! Poftiți. Îmi pare bine."),
    ("radu",  "Bună ziua, Sanda! Și mie. Ce mai faceți?"),
    ("dana",  "Bine, mulțumesc! Deci, acesta e apartamentul. Aici e salonul."),
    ("radu",  "Frumos! Cine e dumnealui?"),
    ("dana",  "Dumnealui e Mihai. E inginer. Iar dumneaei e Ana, e profesoară."),
    ("radu",  "Îmi pare bine. Cu ce vă ocupați, Sanda?"),
    ("dana",  "Sunt manager. Dar dumneavoastră?"),
    ("radu",  "Sunt contabil. Nu sunt din Chișinău — sunt din oraș."),
    ("dana",  "Nu sunteți moldovean?"),
    ("radu",  "Ba da, sunt moldovean. Deci, unde e paltonul?"),
    ("dana",  "Paltonul e în cuier. Pe scaun sunt niște cămăși albe."),
    ("radu",  "Un apartament modern și comod!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Everything in that visit came from the first five lessons — a "
        "greeting, who does what, whose home this is, where the coat is, what "
        "colour the shirts are. No new words today. Today you get it all back "
        "out.", pause=P_SECTION)

# ═══ 1. a fi ═════════════════════════════════════════════════════════════════
ep.narr("The verb everything runs on: a fi, to be. All the persons.",
        pause=800, chapter="a fi")
for cue, ans, v in [
    ("I am a teacher — a woman.", "Eu sunt profesoară.", "f"),
    ("You are an engineer. — tu.", "Tu ești inginer.", "m"),
    ("He is Moldovan.", "El e moldovean.", "m"),
    ("We are at home.", "Noi suntem acasă.", "m"),
    ("You are from the city. — voi.", "Voi sunteți din oraș.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 2. un / o / niște ═══════════════════════════════════════════════════════
ep.narr("A, an, and some — and the gender behind them.", pause=800,
        chapter="un, o, niște")
for cue, ans, v in [
    ("a coat, a shirt", "Un palton, o cămașă.", "m"),
    ("some coats, some shirts", "Niște paltoane, niște cămăși.", "m"),
    ("a chair, some chairs", "Un scaun, niște scaune.", "m"),
    ("a flower, some flowers", "O floare, niște flori.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 3. The definite article ═════════════════════════════════════════════════
ep.narr("And 'the', riding on the back of the word.", pause=800,
        chapter="the article")
for cue, ans, v in [
    ("the coat, the shirt", "Paltonul, cămașa.", "m"),
    ("the office, the school", "Biroul, școala.", "m"),
    ("Where is the dictionary?", "Unde e dicționarul?", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 4. Demonstratives and cine / ce ═════════════════════════════════════════
ep.narr("Pointing, and the two questions that go with it.", pause=800,
        chapter="acesta, cine, ce")
for cue, ans, v in [
    ("Who is this? — A course student.", "Cine e acesta? Un cursant.", "m"),
    ("What is this? — A mirror.", "Ce e aceasta? O oglindă.", "f"),
    ("These are some magazines.", "Acestea sunt niște reviste.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 5. Politeness ═══════════════════════════════════════════════════════════
ep.narr("Respect — for the person you speak to, and the person you speak "
        "about.", pause=800, chapter="politeness")
for cue, ans, v in [
    ("Are you a doctor? — respectfully.", "Dumneavoastră sunteți medic?", "m"),
    ("He is at home. — respectfully.", "Dumnealui e acasă.", "m"),
    ("She is a teacher. — respectfully.", "Dumneaei e profesoară.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 6. Prepositions ═════════════════════════════════════════════════════════
ep.narr("All the placing words at once — in, at, from, on, next to, under, "
        "behind, for.", pause=800, chapter="prepositions")
for cue, ans, v in [
    ("I am in Romania, in Bucharest.", "Sunt în România, la București.", "m"),
    ("On the table there is a newspaper.", "Pe masă e un ziar.", "m"),
    ("Next to the window there is an armchair.",
     "Lângă fereastră e un fotoliu.", "m"),
    ("Under the table there is a carpet.", "Sub masă e un covor.", "m"),
    ("Behind the door there is a coat rack.", "După ușă e un cuier.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 7. The wardrobe — all five parts of Lecția 5 ════════════════════════════
ep.narr("The whole wardrobe now, the thing Lecția 5 spent five parts on — name "
        "it, put the article on it, ask where it is.", pause=800,
        chapter="the wardrobe")
for cue, ans, v in [
    ("a coat, a blouse, a scarf", "Un palton, o bluză, un fular.", "m"),
    ("the coat, the blouse", "Paltonul, bluza.", "m"),
    ("Where is the dress? — In the wardrobe.", "Unde e rochia? În dulap.", "f"),
    ("Where are the gloves? — On the shelf.", "Unde sunt mănușile? Pe raft.", "f"),
    ("Here is the skirt, and here is the t-shirt.",
     "Iată fusta, iar iată tricoul.", "f"),
]:
    ep.drill(cue, ans, v)

# ═══ 8. Adjectives and agreement ═════════════════════════════════════════════
ep.narr("Describing things, endings matching.", pause=800, chapter="adjectives")
for cue, ans, v in [
    ("The shirt is white.", "Cămașa e albă.", "f"),
    ("The coat is black.", "Paltonul e negru.", "m"),
    ("The trousers are black.", "Pantalonii sunt negri.", "m"),
    ("some yellow dresses", "Niște rochii galbene.", "f"),
    ("a nice scarf, a nice shirt", "Un fular frumos, o cămașă frumoasă.", "m"),
    ("How is the coat? — It's elegant and modern.",
     "Cum e paltonul? E elegant și modern.", "m"),
    ("a good, comfortable apartment", "Un apartament bun și comod.", "m"),
]:
    ep.drill(cue, ans, v)

# ═══ 8. The things you can now say ═══════════════════════════════════════════
ep.narr("And the spoken turns from across the block — the ones the book does "
        "not give you. Still the ones that matter most.", pause=800,
        chapter="How people really say it")
for cue, ans, v in [
    ("What do you do for a living?", "Cu ce vă ocupați?", "f"),
    ("Aren't you from the city? — Yes I am.", "Nu sunteți din oraș? Ba da.", "m"),
    ("Where do you live? — casually.", "Unde stai?", "f"),
    ("Nice to meet you. — Likewise.", "Îmi pare bine. — Și mie.", "f"),
    ("What's this? — casually.", "Ce-i asta?", "f"),
]:
    ep.drill(cue, ans, v)
ep.narr("And keep the ear for e over este, and the dropped L — paltonu', "
        "apartamentu', domnu'. That is how all of it actually sounds.",
        pause=P_SECTION)

# ═══ 9. A full self-introduction ═════════════════════════════════════════════
ep.narr("Now all five lessons in one breath — a person introducing himself, "
        "his home, his day. Slowly first.", pause=800, chapter="Text")
TEXT = [
    "Bună ziua! Sunt Radu. Sunt moldovean, din oraș. Sunt contabil.",
    "Acum sunt acasă. Aceasta e o casă modernă.",
    "Aici e un salon și o bucătărie.",
    "În salon sunt o canapea, niște fotolii și un covor.",
    "Paltonul e în cuier. Pe scaun sunt niște cămăși albe.",
    "Dumnealui e Mihai. E inginer. Dumneaei e Ana, e profesoară.",
    "Îmbrăcămintea e comodă. Deci, e bine!",
]
for line in TEXT:
    ep.ro(line, "m", SLOW, 900)
ep.narr("And at speed.", pause=600)
for line in TEXT:
    ep.ro(line, "m", NORMAL, 300)

# ═══ 10. Cold open again ═════════════════════════════════════════════════════
ep.narr("The visit again. Same recording — five lessons, and you followed it.",
        pause=P_SECTION, chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 11. Close ═══════════════════════════════════════════════════════════════
ep.narr("Before the next lesson: introduce yourself out loud, the whole way "
        "through — who you are, where you're from, your job, your home, what "
        "you're wearing. Everything you need is now yours. Pe curând!",
        pause=1500, chapter="Close")

ep.emit(spoken_layer=[])
