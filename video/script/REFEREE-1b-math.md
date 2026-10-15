# Referee 1b (mathematics and numbers): re-check of the rewritten script and FACTS v2

Date: 2026-10-15. Scope: BLOCKER and MAJOR only. Every chapter 00–09 and FACTS.md re-read from disk;
every spoken number re-verified against life203.npz (weights at the same index as the tick), run.json,
results.json, frozen_brain_test.json, findings/01, findings/02, research/07, DESIGN-AMENDMENTS, prereg,
decisions/0002 and creature/*.py. Nothing in the script was modified.

## The 17 BLOCKER/MAJOR items from REFEREE-1-math.md

1. TD worked example labelled tick 3693 but taken from tick 4293 — **resolved.** 06 p13 and FACTS now use
   the real tick 3693 (index 3193): Q(x, LEFT) +0.001089, r −0.00026, y +0.000892 (recorded y_target at
   index 3194), miss −0.000197, implied best next Q +0.00128, Δw −0.000031 / −0.000054 / −0.000059. All
   reproduce exactly. FACTS now says day 10.
2. Diffusion "fraction alpha" — **resolved.** 03 p03 says four alpha, 72% at 0.18; 03 p04 explains the
   quarter correctly.
3. Two knobs credited with 20/20 — **resolved.** 05 p06 and FACTS: 10/10 fresh seeds for the A pair,
   20/20 for the five-number construct.
4. "A hundred times stronger two cells away" — **resolved.** 02 p10 now says five times at two cells,
   twenty at four (measured 5.6 and 18). See new item 21 on "well over a thousandfold".
5. Dot product "about a thousandth" — **resolved.** 02 p02, 05 p05, 05 p12: fourteen thousandths, with
   the b and committee terms shown summing to +0.001089.
6. Tabular Q "the standard textbook learner" — **resolved.** 07 p02: "the table learner as it was then
   written"; the phrase is on the forbidden list in FACTS.
7. Uncentred Q "target near zero" — **resolved.** 05 p11 defers the why; 06 p15 says the target is about a
   quarter below 2.8 (2.5), each step lowers only the taken move, 64–69%, pilot 627 → 3729. Matches A16
   and the learn_q docstring.
8. Turn-toward-A ratios hiding day 1 — **resolved.** 07 p10 speaks 0.81, coin toss on day 1, back above
   three quarters from day 2; FACTS lists all fifteen days and every value reproduces (0.81, 0.51, 0.79,
   0.73, 0.77, 0.80, 0.76, 0.73, 0.77, 0.82, 0.83, 0.86, 0.74, 0.86, 0.82).
9. Tick 1231 "the bite landed the tick before" — **resolved.** 04 p09 and 06 p14: a bite with a full tank
   (E 1.0 before and after), r = 0; Q 0.007341, y 0.007669, miss +0.000327 reproduce.
10. B as "a wrong lesson" vs "toward B pays" — **resolved.** 03 p01 now says three times as much food mass
    as poison mass, B points mostly to food; consistent with 07 p08.
11. "Divided by the temperature, three point three" and "900 samples" — **resolved.** 06 p20: 0.3, a factor
    of 3.3; ~300 samples on night 1 in ~15 batch steps.
12. Committee "bias because the fifth unit has v = 0" — **resolved.** 05 p15 gives the sigmoid ≈ 0.5
    reason (measured 0.493–0.508 on the worked tick), mean share 0.0018, slowly drifting constant.
13. "103 knobs, nothing else ever changes" — **resolved.** 01 p04: 103 at birth, a grown unit adds sixteen
    knobs; 06 p01: 119 in this brain after it grew.
14. "Only the taken move's knobs move" — **resolved.** 06 p13 and 08 p06: plus the shared c and u.
15. "Across all twenty seeds" — **resolved.** 07 p10: "in the lives the referee traced for the findings".
16. "Nothing had to be redone" — **resolved.** 07 p04: the step-size pilot was re-run; the main run was not.
17. "Your world file once said" — **resolved.** 07 p08: "still says", correction recorded in research seven.

## New statements introduced by the rewrite

18. **BLOCKER. 07 p13.** Spoken: "that needs the xor world, where food is A or B but not both, which no
    straight line of knobs can separate, so the committee must do it." Viz: "needs the xor world, 'A or B
    but not both'".
    Truth: `creature/world.py` line 17 and BLENDS: xor **food = A and B together** (blend 1,1,0); **poison =
    A alone or B alone**. The script states the world backwards. The "no straight line" point survives
    either way; the labels do not.
    Corrected sentence: "that needs the xor world, where food is A and B together and either note alone is
    poison, which no straight line of knobs can separate, so the committee must do it." Fix the viz card
    to "A and B together = food; A alone or B alone = poison".

19. **MAJOR. 06 p08.** Spoken: "After that night the policy was almost deterministic: on most seeds it gave
    one move more than ninety-nine percent of the time."
    Truth: the only per-seed numbers are the four night-1 entropies on seeds 300–303 (research/07 §2.2:
    0.028, 0.092, 0.004, 0.139 nats). The highest top-move probability consistent with each is 0.996,
    0.981, 0.9995 and 0.969. So two of the four seeds are above 99% and two are at 97–98%; "most seeds"
    is not in the source, and the 20-seed bias statistic (0.533) does not give a top-move probability at
    all. FACTS line 41 carries the same unsupported sentence.
    Corrected sentence: "After that night the policy was almost deterministic: on the four proof seeds
    measured it gave one move between ninety-seven and ninety-nine point nine percent of the time."

## Minor notes found on the way (not blocking; fix if convenient)

20. 05 p11 viz: "Five units × 0.693 = 3.466 of free evidence for every move at birth." At birth H = 4
    (2.773); five only from night 1. The spoken text is fine. Viz should read four units, 2.773, or drop
    "at birth".
21. 02 p10 and FACTS: "across the map it spans well over a thousandfold." At index 3000 the A field spans
    1007× (max 0.214, min 0.00021) and B 840×. "About a thousandfold" is the honest reading of the two
    fields that matter; only C, which nothing emits here, spans more.
22. 01 p02 viz: "energy +0.0023, −0.0011, +0.0016" for tick 3693. In LEFT, RIGHT, FORWARD order the
    energies are −0.0011, +0.0023, +0.0016; the first two are swapped.
23. 06 p20: "each step moves the knobs by hundred-thousandths." True for the quiet example tick; across the
    life the online step on w has median norm 0.0004 (ten-thousandths) and reaches 0.01–0.025 on bite
    ticks. "A few hundred-thousandths on a quiet tick, up to hundredths on a bite" is the measured range.

## Verdict

**NOT CLEAR.** All seventeen earlier items are fixed and every re-derived number in the rewrite reproduces
from the dump, but 07 p13 states the xor world backwards (food is A and B together, not "A or B but not
both"), and 06 p08's "more than ninety-nine percent on most seeds" is not supported by the four
entropies it rests on. Fix those two sentences (and the matching FACTS line 41 and the two viz cards) and
it is clear to record.
