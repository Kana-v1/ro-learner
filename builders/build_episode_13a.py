"""
Episode 13A — "Vii la noi?" (Lecția 13 "În vizită la prieteni", memory-first, part 1)

Lecția 13 is about 32 items plus the numbers to a thousand, so it runs to six
parts:
  13A  guests are coming — vin, vizită, oaspete, invit, luați loc, poftă bună
  13B  laying the table — mâncare, farfurie, pahar, lingură, cald, rece
  13C  at the table — ciorbă, sarmale, gustos, furculiță, cuțit, tacâm
  13D  going out — ies, afară, cobor, scară, de obicei, zgomot
  13E  what you hear and know — aud, dorm, știu, nimic, cuvânt, devin
  13F  numbers and age, the text — douăzeci… o sută, o mie, the book's
       "Astăzi avem oaspeți" and its proverb
(13C onward are built after the next results, so they can use them; items may
move between parts.)

The chapter's grammar is the fourth group of verbs, and every one of them
changes its sound (vin, vii, vine; dorm, doarme; aud, auzi). So, as in 11A
and 12D, each form is heard alone in a short sentence before it is asked —
here come gets I, friend, she and we. Invite is not from that group: it goes
like listen from 8A (ascult, asculți, ascultă), which the learner still
misses ("Asculți mult?" in struggles), so the friend-form is heard first too.

Luați loc and Poftă bună are chunks, as the book gives them; "Ia loc", the
friend-form, is heard once beside the polite one — two side by side.

12E's spoken layer (un prieten de-al meu) is ordinary speech in the dialogue.
12F's (ăla, aia) is informal and stays recognise-only.

12E and 12F results: first recalls of the new words often failed and came
right on the retry, and dialogue-length sentences fell apart — so the drill
sentences here stay at four or five words.

Scene: Dana has guests tonight. She rings Elena, then opens the door to Radu
and a friend — so come, invite, sit down and enjoy your meal come round for
each guest, the way a host really says them.
"""
from episode_kit import Episode, load, P_SECTION, P_SHORT, NORMAL, SLOW

REQUIRED = ["vin", "vizită", "oaspete", "invit", "luați loc", "poftă bună"]
GLUE = {"la noi": "to our place — a chunk"}

ep = Episode(number=13, lesson=13, part="a", title="Vii la noi?",
             source="Limba care ne unește, nivelul I — Lecția 13 (partea A)",
             required=REQUIRED, glue=GLUE)

DIALOGUE = [
    ("dana", "Alo, Elena? Astăzi avem oaspeți. Vii la noi?"),
    ("elena", "Da, vin! La ce oră?"),
    ("dana", "La ora șapte. Invit și prietenii."),
    ("radu", "Bună seara! Vin cu un prieten de-al meu."),
    ("dana", "Bine ați venit! Luați loc, vă rog."),
    ("elena", "Mulțumesc! Ce frumos e aici!"),
    ("dana", "Poftă bună!"),
    ("radu", "Mulțumim!"),
]

# ═══ 0. Cold open ════════════════════════════════════════════════════════════
ep.add("target", "Ascultați!", "ro", "dana", NORMAL, 900, chapter="Cold open")
ep.dialogue(DIALOGUE)
ep.narr("Lesson 13: visiting friends. Dana has guests tonight.",
        pause=P_SECTION)

# ═══ 1. Six words — introduced then recalled at once ═════════════════════════
ep.narr("Six words, one at a time.", pause=800, chapter="Six words")
ep.new_item("vin", "I come", "vin", "m",
            teach_ro="Vin la ora șapte.", teach_en="I'm coming at seven.")
ep.new_item("oaspete", "a guest", "un oaspete", "f",
            teach_ro="Astăzi avem oaspeți.", teach_en="Today we have guests.")
ep.new_item("invit", "I invite", "invit", "m",
            teach_ro="Invit prietenii.", teach_en="I'm inviting friends.")
ep.new_item("vizită", "on a visit", "în vizită", "f",
            teach_ro="Venim în vizită.", teach_en="We're coming on a visit.")
ep.new_item("luați loc", "Please sit down — politely", "Luați loc, vă rog.", "m",
            teach_ro="Luați loc, vă rog.", teach_en="Please sit down.")
ep.new_item("poftă bună", "Enjoy your meal!", "Poftă bună!", "f")
ep.narr("Mixed. Just the words.", pause=800)
for cue, ans, v in [("a guest", "un oaspete", "m"), ("I come", "vin", "f"),
                    ("Enjoy your meal!", "Poftă bună!", "m"),
                    ("on a visit", "în vizită", "f"), ("I invite", "invit", "m"),
                    ("Please sit down — politely", "Luați loc, vă rog.", "f")]:
    ep.recall_word(cue, ans, v)

# ═══ 2. Come — the sound changes ═════════════════════════════════════════════
ep.narr("Come changes its sound to a friend — a long sound at the end. And to "
        "our place is a chunk. Listen:", pause=800, chapter="Come, by ear")
ep.ro("Vii la noi?", "f", SLOW, 1700)
ep.drill("you come — to a friend", "vii", "m")
ep.drill("Are you coming to our place? To a friend.", "Vii la noi?", "f")
ep.narr("She comes — listen:", pause=P_SHORT)
ep.ro("Vine și Radu.", "m", SLOW, 1700)
ep.drill("she comes", "vine", "f")
ep.drill("Radu's coming too.", "Vine și Radu.", "m",
         accept=["Și Radu vine."])
ep.narr("And we come — listen:", pause=P_SHORT)
ep.ro("Venim în vizită.", "f", SLOW, 1700)
ep.drill("we come", "venim", "m")
ep.narr("You can't work these out — learn each by ear. Mixed.", pause=800)
for cue, ans, v in [("I come", "vin", "f"), ("she comes", "vine", "m"),
                    ("you come — to a friend", "vii", "f"), ("we come", "venim", "m"),
                    ("I'm coming at seven.", "Vin la ora șapte.", "f")]:
    ep.drill(cue, ans, v)

# ═══ 3. Invite — like listen ═════════════════════════════════════════════════
ep.narr("Invite goes like listen: to a friend, the last sound softens. Listen "
        "to both:", pause=800, chapter="Invite, like listen")
ep.ro("Asculți. Inviți.", "m", SLOW, 1800)
ep.drill("you invite — to a friend", "inviți", "f")
ep.drill("you listen — to a friend", "asculți", "m")
ep.narr("She invites is plain, like she listens. Build it.", pause=P_SHORT)
ep.drill("she invites", "invită", "f")
ep.drill("She's inviting friends.", "Invită prietenii.", "m")
ep.drill("Are you inviting friends? To a friend.", "Inviți prietenii?", "f")

# ═══ 4. Guests, a visit ══════════════════════════════════════════════════════
ep.narr("One guest, many guests — the end changes. Listen to both:",
        pause=800, chapter="Guests")
ep.ro("Un oaspete. Doi oaspeți.", "f", SLOW, 2000)
ep.drill("We have guests.", "Avem oaspeți.", "m")
ep.drill("two guests", "doi oaspeți", "f")
ep.drill("I'm coming on a visit.", "Vin în vizită.", "m")
ep.drill("We're going on a visit to friends.", "Mergem în vizită la prieteni.", "f")

# ═══ 5. Sit down — politely, and to a friend ═════════════════════════════════
ep.narr("Sit down, politely — and to a friend. Listen to both:", pause=800,
        chapter="Sit down")
ep.ro("Luați loc. Ia loc.", "m", SLOW, 1900)
ep.drill("Sit down — to a friend.", "Ia loc.", "f")
ep.drill("Please sit down — politely.", "Luați loc, vă rog.", "m")
ep.drill("Welcome! Politely.", "Bine ați venit!", "f")
ep.drill("Enjoy your meal!", "Poftă bună!", "m")

# ═══ 6. Drill ════════════════════════════════════════════════════════════════
ep.narr("Short sentences — take your time.", pause=P_SECTION, chapter="Drill")
for cue, ans, v, extra in [
    ("Today we have guests.", "Astăzi avem oaspeți.", "f",
     {"accept": ["Azi avem oaspeți.", "Avem oaspeți astăzi."]}),
    ("Are you coming to our place? To a friend.", "Vii la noi?", "m", {}),
    ("Yes, I'm coming!", "Da, vin!", "f", {}),
    ("At what time?", "La ce oră?", "m", {}),
    ("I'm inviting friends too.", "Invit și prietenii.", "f", {}),
    ("I'm coming with a friend of mine.", "Vin cu un prieten de-al meu.", "m", {}),
    ("Welcome! Please sit down.", "Bine ați venit! Luați loc, vă rog.", "f", {}),
    ("How beautiful it is here!", "Ce frumos e aici!", "m", {}),
    ("Enjoy your meal! — Thank you!", "Poftă bună! — Mulțumesc!", "f",
     {"accept": ["Poftă bună! — Mulțumim!"]}),
    ("When are you coming? To a friend.", "Când vii?", "m", {}),
]:
    ep.drill(cue, ans, v, **extra)

# ═══ 7. Spoken layer ═════════════════════════════════════════════════════════
ep.narr("How this really goes. When someone says enjoy your meal, the usual "
        "answer is thanks — and the same to you. Listen:", pause=800,
        chapter="How people really say it")
ep.ro("Mersi, la fel!", "f", SLOW, 1600)
ep.narr("That thanks is the everyday one, between friends and at the table. "
        "Just to recognise for now.", pause=P_SECTION)

# ═══ 8. Review — your misses first, then the schedule ════════════════════════
ep.review_auto(cap=8)

# ═══ 9. Cold open again ══════════════════════════════════════════════════════
ep.narr("Dana's guests again. Same recording.", pause=P_SECTION,
        chapter="Cold open again")
ep.dialogue(DIALOGUE)

# ═══ 10. Close ═══════════════════════════════════════════════════════════════
ep.narr("Guests at the door, a seat, and enjoy your meal.",
        pause=P_SHORT, chapter="Close")
ep.ro("Pe curând!", "f", NORMAL, 1200)

ep.emit(spoken_layer=load("spoken.json").get("13", []))
