---
name: lesson-audio-script
description: "Write audio-lesson scripts for language learning from textbook chapters, as segment JSON ready for TTS rendering. Use when the user wants to turn a language textbook lesson, vocabulary list, or grammar point into a listening episode, drill track, or study podcast — including generating the next episode in a series they have already started. Covers scene design for pedagogical dialogue, retrieval-practice drills, bilingual sandwiching, L1/L2 balance, and spaced review across episodes. Do NOT use for translating text, general podcast or screenplay writing, or lesson plans meant to be read rather than heard."
---

# Language lesson audio scripts

Audio for language learning is not a podcast about a language. It is a
retrieval-practice instrument that happens to be delivered as audio. The
silence is as much a part of it as the speech.

## Non-negotiables

**Few new items per episode.** This is the one that decides whether anything is
retained. Six new items is the working cap; a couple of light function words
may push it to eight. A learner cannot produce a word heard once ten minutes
ago from inside a pile of fifteen similar words — that is not a prose problem,
it is a load problem, and no amount of good writing fixes it. Size the episode
to what a person can hold, *not* to the chapter: a chapter of thirty words is
five episodes, not one crammed one. New material is the scarce resource; the
majority of every episode is retrieval of items already introduced.

**The pause is the instrument, and it scales with the answer.** The learner must
produce the target language out loud, from memory, before hearing it. A script
with no silence teaches almost nothing regardless of how good the prose is. The
production pause is *proportional to the answer* — a single word needs a moment,
a whole sentence needs several seconds to assemble — so size it from the answer,
never a flat value (`recall_pause()` does this). Err long: a learner producing
aloud on the move who runs out of time before the answer forms gets nothing from
the drill. Anything the learner only repeats after gets a short 1200–1500 ms.

**The narrator never speaks the target language.** Every Romanian word or phrase
the learner hears comes from a target-language voice, never from the L1
narrator — a learner cannot parse L2 forms in an L1 accent, and hearing them
mangled is worse than not hearing them. The narrator explains and cues in L1;
grammar examples and paradigms are set up in L1 and then *spoken by the L2 voice*
(`example()`), not quoted inside a narration segment. Referring to a bare ending
in passing is fine; a word or phrase meant to be understood is not.

**Grade the recall.** Do not ask for a whole sentence the first time an item is
retrieved — when the word itself is not yet retrievable, the sentence is
impossible and the silence just fails. Introduce an item, retrieve the bare
word from an L1 cue seconds later, and only once the words are held ask for
them assembled into sentences. Reach the whole sentence; do not start there.

**Every new item must appear, and keep coming back.** The new set is small, so
cover it thoroughly: each item introduced, recalled bare on the spot, then used
in whole sentences. Then it belongs to the spacing schedule (below) and returns
across later episodes. Coverage of the small new set is checked mechanically;
retention comes from the return, not the first exposure.

**Ground the language in the source.** Do not introduce vocabulary or grammar
the chapter has not taught, beyond an explicit glue budget (below). If the
textbook supplies glosses, use them rather than translating afresh — a
mismatch between the book and the audio is worse than a clumsy gloss.

**Never let a target sentence be wrong.** For any language where you are less
than certain — agreement, articles, clitics, aspect, case — prefer sentences
lifted from or closely modelled on the chapter. A fluent-sounding error that
the learner rehearses twenty times is the worst possible outcome.

## Designing the dialogue

This is where most generated scripts fail. They come out as plausible
conversation, which is the wrong target. A textbook dialogue is an engineered
object that impersonates a conversation.

**Choose a scene where the target language is obligatory and repetition is
realistic.** This single choice does most of the work. Two strangers chatting
gives you no reason to use any particular structure and no reason to repeat it,
so every repetition sounds false. A registration desk, a roll call, a border
queue, a doctor's intake, a market stall — these have a participant whose job
is to ask everyone the same two questions. The learner hears the structure four
times and it sounds entirely natural, because it is.

Match the scene to the grammar:
- nationalities, origins, names → registration, roll call, border
- prices, numbers, quantities → market, ticket window
- times, days → booking, timetable enquiry
- likes, wants → ordering, shopping
- past events → someone recounting a day to someone who was absent

**Respect how the language actually behaves.** Textbooks over-produce forms to
make them visible — every pronoun spelled out, every subject stated. Copying
that into dialogue makes it sound like a conjugation table read aloud. In
pro-drop languages, drop the pronoun in dialogue and use it only for contrast;
then have the narrator point out the difference. The dialogue models real
speech, the drill practises the full forms. Both jobs get done.

**Glue budget: three or four items per episode.** A dialogue built strictly
from a 20-word list will be stilted. Allow a few extra items — a fixed
greeting, a title, a place name, a connector — and have the narrator deliver
them as whole chunks with no grammatical analysis. Keep them listed explicitly
so the budget stays a decision rather than a drift.

**Same recording twice.** The dialogue opens the episode at full speed, before
the learner can follow it, and closes the episode unchanged. Identical audio,
not a slower re-read: the learner's comprehension changed, and hearing the
identical file is what demonstrates that. Reuse the same segments so the
renderer's cache serves one synthesis for both positions.

## Episode shape

1. **Cold open** — the dialogue, full speed, no preamble.
2. **Anchor** — one sentence on what the learner will be able to do.
3. **Sounds** — only for early episodes, and only the sounds occurring in this
   chapter's words. Not the whole alphabet.
4. **Vocabulary** — the few new items, one at a time, interleaved with recall.
   Each item: bilingual sandwich (L2 → pause → L1 → L2 slowly → pause), then a
   bare-word retrieval seconds later, before the next item. Present items inside
   a short phrase, never bare, so the learner acquires a chunk. Do not stack all
   the items into one block and drill them ten minutes later — that is the
   failure mode. Introduce, retrieve, next.
5. **Grammar** — one point. Present the forms, then drill them immediately.
   Explanation without immediate practice does not survive to the next episode.
6. **Drill** — L1 cue, silence, correct L2, silence to repeat. The longest
   block, and now the words are held so the cues are whole sentences. Cover
   every new item and structure several ways.
7. **Review** — items from earlier episodes, pulled from the spacing state, not
   hand-picked. Usually the largest retrieval block after the drill.
8. **Text** — the chapter's own reading passage, slow then at speed.
9. **Cold open again** — the same segments as step 1.
10. **Close** — a short sign-off (the sign-off phrase spoken by the L2 voice). Do
    not end with homework or an instruction to go practise; the learner is
    listening on the move and will not do a between-episodes task. Any producing
    happens inside the episode, in the drills, not after it.

## Length

An episode is six or so new items plus a lot of retrieval, and lands around
10–14 minutes. The new material is a small fraction of that runtime; the rest
is recall of these items and review of earlier ones. If an episode is short,
that is fine — three passes over a tight 11-minute episode beat one pass over a
padded 20-minute one.

Do not lengthen an episode by adding new material — that is exactly what breaks
retention. Lengthen by adding retrieval: more drill items, the same content
cued a second way, more review from earlier episodes. Shorten by cutting
explanation, never by cutting drill. If a chapter will not fit six-at-a-time,
it becomes more episodes, never a fuller one.

Cap episodes near 20 minutes. Beyond that, active response becomes tiring and
the learner starts listening passively, which is the failure mode the whole
format exists to prevent. Split an over-long chapter into two episodes rather
than stretching one.

Design for re-listening. Three passes over a 13-minute episode beat one pass
over a 40-minute one.

## L1/L2 balance

Set the L1 share as an explicit parameter and decrease it across the course:
around 50–60% at the very beginning, under 20% by upper-beginner. Count it and
report it rather than judging by feel.

Choose the L1 the learner processes without effort. During a drill the silence
is for retrieving the L2, not for decoding the cue — a cue in a language that
costs even a moment of translation wastes the pause. If the textbook's glosses
are in a different language from the L1, carry both in the intermediate data
and use one in the script, so the mismatch stays visible.

## Spacing across episodes

This is the engine, not an afterthought. With only six new items per episode,
almost all retention comes from items returning on an expanding schedule, so the
spacing state does most of the teaching.

Keep a state file (`data/state.json`) mapping each item to the episode that
introduced it, plus a canonical L1→L2 pair reused verbatim when it comes due.
The play order lives in `sequence`; an item is due when the current episode's
position minus its introduction position is one of the intervals — +1, +3, +7,
+16. Because due-ness is a pure function of `sequence` and the intervals,
nothing is mutated on build except that each episode registers its own new
items. `Episode.review_auto()` pulls the due items, oldest gap first, capped
around seven. Build episodes in `sequence` order so an item is registered before
the later episode that reviews it.

## Output

Emit a flat ordered list of segments. One segment is one TTS call.

```json
{"id": "s042", "type": "prompt", "lang": "en", "voice": "en_narrator",
 "text": "She is not from Kyiv.", "rate": 1.0, "pause_after_ms": 3500}
```

- `type` — `narration`, `target`, `gloss`, `prompt`, `answer`, `line_a`/`line_b`
- `rate` — 1.0 normally, 0.8 for slow repetitions
- `chapter` — optional, marks the start of a chapter in the output file

Prefer generating the JSON from a small script with the content in plain lists
over writing the JSON by hand. It is shorter, it is editable, and it becomes
the template for the rest of the course.

Before returning, check: coverage of the item list, L1 share, total pause time
as a fraction of runtime (a third is healthy), and that no target sentence uses
grammar the chapter has not introduced.
