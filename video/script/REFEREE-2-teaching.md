# Referee 2: teaching quality, for one learner

Scope: every paragraph of 00_cold_open.md to 09_close.md, checked against the method in BRIEF.md ("The teaching method", items 1-7, plus the addendum "no sentence of explanation without a picture that moves"). Facts were cross-checked against FACTS.md only where an arithmetic or ordering problem depends on them; mathematical honesty is the other referee's job.

Severity: MAJOR = breaks the method (a why missing, a metaphor that does not map, a symbol used before it exists, an inconsistency the learner will trip on, a chapter without a prediction beat, arithmetic that does not reproduce). MINOR = polish.

Items are grouped: cross-chapter first, then chapter by chapter. Fixes are written for the ear, short, no em dashes.

---

## A. Cross-chapter (these break the "pattern and connections" promise)

**1. MAJOR. All chapters. The sign convention flips four times with five different words for the same quantity.**
Ch0 p02 shows Q bars where the highest is taken. Ch1 p02 says "the creature takes the lowest". Ch1 p06 says a positive weight "pushes the score up" (if score = energy, that makes the move worse; in the real formula it makes the move better). Ch2 p06 softmaxes "scores" where the highest wins. Ch5 p03 introduces "evidence" and says "from here I will say evidence, and you flip the sign". Ch5 p12 introduces Q. Ch8 p04 finally bridges "arg min of F, the lowest energy, the highest Q". Words used for one number or its negative: height, score, energy, evidence, value, Q. A learner who tracks patterns will stop at ch1 p06 and never trust the sign again.
Fix (two parts). (a) In ch1 p02, settle the vocabulary once and never drift: "Energy is a height, low wins. We will also talk about evidence, which is the same number with the sign flipped, high wins. Two words, one number, opposite sign. The code's name for evidence is Q." (b) A persistent small legend on every screen that shows bars: "F energy, low wins | Q = minus F, high wins". Every later paragraph uses "energy" or "Q", nothing else; "score" and "height" are deleted. Rewrite ch1 p06: "Positive: this reading adds evidence for the move, so its energy drops. Negative: it takes evidence away."

**2. MAJOR. Ch1 p10, ch6 p05, ch6 p13, ch9 p02. The length of a list (the norm) is used with numbers five times and never built.**
"The nightly step was eight to sixteen times bigger than the whole set of knobs", "the knobs at birth add up to a length of about 0.09", "total knob length slides from 0.096 to 0.078". How do you measure the size of a set of knobs? Square root of the sum of squares. Ahmed named "why are we doing square root" as exactly the kind of operation he wants reverse-engineered, and here it is used as a given.
Fix: add a seventh card to ch2, "length": "The need: one number for how big a whole list of knobs is. Square each knob so the sign does not matter and big knobs count more, add them up, then take the square root to undo the squaring, so the answer is in knob units again. A step of 0.68 on a brain of 0.09 is a step eight times the brain." Viz: twelve knobs as arrows, their squares as areas, the sum as one area, the square root as one arrow of that area's side length; slide one knob and the arrow grows. Then ch1 p10 says "we measure that in chapter two".

**3. MAJOR. Ch6 p05. "Entropy" is used with numbers (0.028 against a maximum of 1.099) and is never defined anywhere.**
Fix: either define it in the ch2 toolbox as an eighth card ("how spread the three chances are: zero when one move is certain, one point one when all three are equal; it is the average surprise") with a viz of three bars sliding and the number moving, or replace the sentence with one that needs no new word: "After that night the policy gave one move more than ninety-nine percent of the time." The second is cheaper and loses nothing for this lesson.

**4. MAJOR. Ch8 p05. "The slope of softplus is the sigmoid." Sigmoid is never defined.**
Fix in ch5 p08, where the softplus curve is already on screen: "Its slope is a number between zero and one: how switched on the unit is. At z minus three, five hundredths. At zero, one half. At plus three, ninety-five hundredths. That slope curve is called the sigmoid, and it comes back in the code." Viz: a tangent sliding along the softplus curve while its slope is plotted underneath as the S curve.

**5. MAJOR. Ch7 p01, p03, p04, p06; ch9 p02. "Tabular Q" is the yardstick of the whole experiment and is never explained.**
"The standard textbook learner" is a label, not a picture. The learner cannot judge "reaches tabular Q's level" without knowing what a table does differently from a formula.
Fix: one paragraph before ch7 p01: "Tabular Q keeps no knobs and no formula. It keeps a table: one row for each pattern the senses can show, three numbers in each row, one per move. It learns one cell at a time and never shares what it learned between rows. The energy brain shares twelve knobs per move across every sensation it will ever feel. That is the whole difference." Viz: a grid of cells with numbers beside the 3 by 12 heat map; a lesson updates one cell in the table and a whole row in the heat map. Check the exact row scheme against the lab's tabular_q code before recording (how the contrasts are binned), and say that number.

**6. MAJOR. Ch3 p02 and ch6 p09, ch8 p06. The letter alpha means two unrelated things and the script never says so.**
Alpha is the diffusion fraction (0.18) in ch3 and the learning step (0.3) in ch6. Ch1 called it "learning rate", ch6 p02 "learning rate" again for rule one, ch6 p09 "step size alpha", ch8 "alpha_q". Four names, one collision.
Fix in ch6 p09: "The step size, the learning rate from chapter one. The code calls it alpha q, a different alpha from the smell's alpha in chapter three; they share a letter and nothing else." Keep "learning rate" as the spoken name everywhere; show "alpha_q" only in the code chapter.

**7. MAJOR. Ch1 p03, ch6 p01. "One hundred and three knobs" is true at birth only; seed 203 grows a fifth unit (ch5 p10, ch6 p13) and then has one hundred and nineteen.**
3 b + 36 w + per unit (12 u + 1 c + 3 v = 16): four units 103, five units 119. The script says 103 in ch1 and again in ch6, after it has told the learner about the fifth unit. He will do this arithmetic.
Fix ch1 p03: "a hundred and three knobs at birth; every unit it grows adds sixteen more." Fix ch6 p01: "a hundred and nineteen knobs, in this brain, after it grew."

**8. MAJOR. Ch1 p03. "Learning means one thing: turning knobs. Nothing else ever changes inside the brain." Then ch6 p13 grows a unit.**
An absolute claim that is contradicted later is the fastest way to lose a learner who looks for the system.
Fix: "Learning means turning knobs. Once in a while, on an eventful day, the brain also adds a new unit, born with its output knobs at zero, so it changes nothing until learning turns them. That is the only other thing that ever changes."

**9. MAJOR. Ch4 p04 viz, ch6 p09. Numbers spoken at mixed precision do not reproduce when the learner redoes the subtraction.**
Ch4 p04 viz: 0.0492 minus 0.0300 is 0.0192, the screen says +0.0191 (the real values are 0.04916 and 0.03002). Ch6 p09: Q minus 0.00120, y minus 0.00125, miss stated as "one hundred-thousandth"; the subtraction on screen gives five hundred-thousandths. Eat tick 1231: 0.0077 minus 0.0073 is 0.0004, the script says 0.0003. Ahmed will redo these; the method says the same operation on the creature's real numbers must be visible and must work.
Fix: show every number in one subtraction at the same precision, enough digits that the screen arithmetic reproduces exactly (0.04916 minus 0.03002 is 0.01914; Q minus 0.001203, y minus 0.001254, miss minus 0.000051; or whatever the dump gives). Speak the rounded value, show the full one.

**10. MAJOR. Ch1 p05, ch1 p14, ch2 p06-p08. Temperature is taught as "how the creature picks" and only in ch5 p13 does the learner find out the brain that won never used it to act.**
Nine minutes of marble-on-a-shaking-table and softmax belong to the rule that failed. Nothing in ch1 or ch2 tells him that. He will carry T into the experiment chapter and be told it is not there.
Fix ch1 p05, last sentence: "One warning so the picture stays honest: the brain that won in your lab does not use the shaking table to act. It uses the dice from the policy word, coming next. You still need T, because the first rule used it, and because it explains why the first rule lurched." Also in ch1 p14, connect epsilon to T explicitly: "Epsilon and temperature are two answers to the same question, how often to try the other moves. Temperature ties it to the gaps between the heights; epsilon fixes it at one in ten whatever the gaps."

**11. MAJOR. Ch3 p01 versus ch7 p07. "B means food is a wrong lesson the creature can learn" is followed four chapters later by "toward B pays" and "the record now says B does carry information".**
Both are true in their own frame, but the script never reconciles them, and ch3 presents the first as the moral of the chemistry.
Fix ch3 p01: "Notice that B is in both. B alone cannot tell food from poison. But there is six times more food than poison in this world, so a creature that follows B still eats, and you will see in chapter seven that this is exactly what seed two hundred and three learned first."

**12. MAJOR. Ch5 p11. The centring paragraph uses "target", "learning step", "the learner compares Q to a target" and "TD step" one chapter before the update rule exists (ch6 p09).**
Half of this paragraph is a learning-rule story told inside the brain chapter. Two ideas in one block, one of them out of order.
Fix: keep in ch5 only: "Softplus of zero is log two. At birth every z is near zero, so four units hand every move two point seven seven of free evidence. Adding the same number to all three moves changes no choice, so for acting it is harmless. We subtract it anyway, H times log two, so Q starts near zero. Why that matters is a learning question, and it is the first thing in chapter six." Then open ch6 with the rotation story (the greedy move losing its top spot two times in three) right after the update rule in p09, where "target" and "step" exist.

**13. MAJOR. Ch2 p13 viz. Arithmetic error in the expectation example.**
0.5 times 10, plus 0.3 times 0, plus 0.2 times minus 5 is 4.0, not 3.5.
Fix: reorder the values to 10, minus 5, 0 with chances 0.5, 0.3, 0.2 (5 minus 1.5 plus 0 is 3.5), or keep the values and show 4.0.

**14. MAJOR. Ch3 p02 versus p03. "Each cell moves a fraction alpha of the way toward the average of its four neighbours" is wrong by a factor of four and contradicts the next paragraph.**
f plus alpha times (sum of four minus four f) equals f plus four alpha times (average minus f). So a cell moves four alpha of the way. p03 then says "at one quarter a cell takes exactly the neighbour average", which is only true with the factor four. The learner will do the algebra and find the two sentences disagree.
Fix p02: "Each cell moves four alpha of the way toward the average of its four neighbours. At alpha one quarter, four times a quarter is one, so the cell lands exactly on the average." Then p03 follows.

**15. MAJOR. Ch1, ch4, ch7, ch8 have no pause-and-predict beat. Ch1 is nine minutes without one.**
The brief makes prediction beats the in-video replacement for fiddling. Ch2, ch3, ch5, ch6 each have one; ch1 (the longest paid chapter), ch4 (the chapter with the operation he named, the square) and ch7 (the chapter with the best natural reveal, the mirrored antennae) have none.
Fixes:
- ch1 p05: "Pause. The table shakes as hard as it can. Where does the marble spend its time? ... Everywhere equally. Three moves, one chance each."
- ch1 p10: "Pause. The valley is one step wide and I take a step ten wide. Where do I land? ... On the far slope, every time, in a new place."
- ch4 p04, before the real bite: "Pause. The creature is at energy zero point seven eight and eats one bite. Then imagine it eats the same bite at zero point nine five. Which bite teaches more? ... The first, by far: the bowl is steep up the wall and flat at the bottom. That is the square at work." Viz: the ball at both positions, both drops marked.
- ch7 p08, before the mirrored result: "Pause. We swap the frozen brain's antennae, left for right. What happens? ... It dies every time." This is the single best prediction beat in the material and it is given away.

**16. MAJOR. Ch7 end and ch2 end have no loop diagram and no one-line strip-down; ch7 ends on the pivot list.**
The brief (item 4 and 5): the growing diagram is shown again at the end of every chapter, and every chapter collapses to one line. Ch3, ch4, ch5, ch6 do this well; ch2 ends on the six cards (acceptable as a toolbox, but the diagram should still appear to say "none of these is a box; all of them live inside Brain and Learning"), ch7 ends with no connection back to the loop at all.
Fix ch7, new p12: the complete loop, every box filled, one line: "Stripped down: the loop ran. The body's number, through the promise, found the sign of three contrast knobs in five days, and that is all the skill is." Fix ch2 p14: after the cards, the loop with Brain and Learning lit: "These six live inside two boxes: the brain uses the weighted sum, exponent, softmax and log; learning uses the slope and the average."

**17. MAJOR. Ch6 p02 viz is static symbols while the voice describes two movements.**
"Lower the energy of the move taken, raise the energy of every move in proportion to its chance" is the one place the contrastive rule can be seen, and the viz builds a formula.
Fix viz: the three energy bars from ch1 beside the formula. As "positive phase" is spoken, the taken bar sinks by lr times R. As "negative phase" is spoken, all three bars rise, each by its own chance times the same amount, the tallest-chance bar rising most. Then the net movement is shown as the difference. The formula terms light up in step with the bars.

---

## B. Chapter by chapter

### 00_cold_open.md

**18. MINOR. p04. "We go in the order the data flows" is false for body and brain.**
The diagram flows Senses to Brain to Move to Body; the chapters go body (4) then brain (5).
Fix: "We go almost in the order the data flows. The body comes before the brain, because the brain's learning rule needs the body's number, so you must own that number first."

**19. MINOR. p04 vs ch1 p15. The loop diagram's box set changes.**
Ch0 has World, Senses, Brain, Move, Body, Lesson, Learning. Ch1 p15 inserts Policy. Pick one set in ch0 (include Policy) so the diagram only ever fills, never changes shape.

### 01_names.md

**20. MINOR. p02. Two metaphors for one word, and the first one's break is not stated.**
Marble and price tag in one paragraph breaks "one idea per screen". The marble rolls over time; the brain compares three numbers in one instant, nothing rolls. The price tag maps exactly (three prices, buy the cheapest, a price change can switch shops).
Fix: lead with the price tag. Keep the marble only if T is kept (item 10), and say: "The marble is a picture for later, when the table shakes. One warning: a real marble takes time to roll. The brain compares three heights in one instant."

**21. MINOR. p03. The radio metaphor breaks and the break is not stated.**
A listener turns the radio's knobs. Nobody turns the brain's knobs; the lesson does. Add: "One difference: you turn the radio's knobs. Here the body's number turns them, and that is chapter six."

**22. MAJOR. p08. The dot product is called "how much two lists agree" and given a recipe example that does not map.**
Agreement is the cosine, which needs the lengths fixed; the dot product grows with either list's size. The recipe example (how much you have times how much is needed) breaks: ten eggs for a recipe that needs two scores higher than two eggs, which is not a better fit, and a fridge has no negative quantities, while knobs are negative half the time. Ch2 p02 then uses a different example (grocery bill) for the same operation.
Fix: use one example in both chapters, the grocery bill, and state its break here: "Quantity of each item times its price, added up, is the bill. Here the readings are the quantities and the knobs are the prices, and a price can be negative, a refund. We will do it on the real numbers in chapter two." Drop "agree"; say "a weighted total".

**23. MAJOR. p13. The train ticket metaphor contradicts the formula it prepares.**
"Costs you now and pays off at the station; its value is the trip, not the price" drops the now term. The promise taught in ch6 p07 is value equals the lesson now plus gamma times the best next. The metaphor says value is only the future.
Fix: "Value is what you get now plus what follows, with the far part counting less. A train ticket: you pay now, that is a small negative, and the trip is the positive that follows. Its value counts both." Viz: the now bar (negative) and the future bars stacked into one Q bar.

**24. MINOR. p07. Vector has no real-life example.**
Fix: "A till receipt is a vector: a fixed order of items, and the fifth price always belongs to the fifth item."

**25. MINOR. p12. The bowl's break is never stated (here or in ch4).**
A real ball rolls to the bottom by itself. This ball is pushed up the hunger wall by metabolism every tick and only eating pushes it down. Add one sentence here: "Unlike a real ball, it never rolls down on its own. Metabolism pushes it up every tick. Only eating brings it down."

**26. MINOR. p14. "One time in ten take a random move" overstates the exploration.**
The dice covers all three moves, so a third of the time it lands on the favourite anyway; FACTS gives 5-7% true explores. Say: "one time in ten, roll a dice over all three, so about one tick in fifteen it actually tries another move."

### 02_math.md

**27. MAJOR. p04. The exponent gets no alternative that fails and no real-life example, and its need is asserted rather than derived.**
"We want a fixed gap in height to mean a fixed ratio in odds" is stated as a want. Why want it? Show the alternative: "odds = height" fails because heights can be negative. "odds = height squared" fails because adding the same amount to all three heights changes the chances, and the brain's heights are only ever meaningful as differences. Exp passes both tests. This also plants the seed for ch5 p11 (adding a constant changes no choice), which the learner would then recognise instead of meeting cold.
Fix: insert a p04b with the two failures side by side on the real Q of tick 3693, then exp. Real-life example: "Compound interest. Each year multiplies by the same factor, so a fixed number of years is a fixed ratio of money, whichever year you start."

**28. MINOR. p05. "Every derivative we take later" uses derivative before slope is defined in p11.**
Say "every slope we take later".

**29. MINOR. p09. "Near a food source the smell is a hundred times stronger than two cells away" is a number with no source in FACTS.**
Either read it from the field at tick 3000 by the scene code or cut the number.

**30. MINOR. p09. One alternative is shown (raw concentration); the obvious second alternative, square root, is not.**
Ahmed named square root as a thing he wants reverse-engineered. Add: "Why not a square root, which also squashes? Because under a square root, doubling adds a different amount at every level. Under a log, every doubling adds the same zero point six nine. That is what makes near and far comparable." Viz: both curves, doubling steps marked, the log's steps equal, the root's shrinking.

**31. MINOR. p07. The conclusion "the second experiment stopped using softmax" skips the obvious alternative: just lower T.**
Add: "You could lower T to a thousandth instead. But then how often it explores depends on the gaps, which change all life. Epsilon fixes exploring at one in ten whatever the gaps, so it is one less thing to tune."

**32. MINOR. p12. The slope-equals-reading fact is asserted; the viz draws arrows but shows no nudge.**
Add viz: nudge the left knob on contrast A by 0.1; the total moves by 0.1 times 0.52, exactly 0.052; nudge the knob on body X (reading 0.001) by 0.1 and the total moves by 0.0001. The sentence "a knob can only matter through the reading it multiplies" then has a picture that moves.

**33. MINOR. p12 viz. "Q = w·x" writes Q before the letter is ever spoken (ch5 p12) and omits b and the committee.**
Write "evidence = w·x, the simplest brain" and say aloud "ignoring the committee for now".

**34. MINOR. p11, ch6 p09, ch8 p06. One quantity, three names: mistake (ch2), miss (ch6), td (ch8).**
Say in ch2 p11: "the mistake, which from chapter six we will call the miss, and the code calls td."

### 03_world_senses.md

**35. MINOR. p02. The need for diffusion is not stated and no alternative fails.**
Add first sentence: "Why spread at all? Without it the smell sits only on the food cell, and antennae one cell away feel nothing. Spreading is what gives the creature a slope to follow." Viz: the no-diffusion world, antennae reading zero everywhere but on the food.

**36. MINOR. p04. Three ideas in one paragraph: decay, emit, the ledger.**
Split: decay and emit (with the mass chart) on one screen; the ledger and the "created food out of nothing" aside on the next, or cut the aside.

**37. MINOR. p06. "Without noise steering is trivially easy" is a trust-me.**
Either show it (a noiseless run's steering) or say the honest version: "because real sensors are noisy, and a brain that only works on perfect readings has learned nothing about the world".

**38. MINOR. p07. Contrast has the best reverse-engineering in the script and no real-life example.**
Add: "Your ears do this. You turn toward the louder ear by how much louder it is compared to both together, not by the raw difference, so a whisper and a shout turn your head the same amount." Say where it breaks: "ears use a log ratio, the creature uses a plain ratio of logged readings; same idea, slightly different arithmetic."

**39. MINOR. p08. Four readings, four whys, one screen.**
Split at "Then the body's own energy and toxin": means and changes on one screen (the bacteria example), body and constant one on the next.

### 04_body.md

**40. MINOR. p02. The square has three whys and an alternative, but no real-life example, and the viz is static while the voice compares values.**
Example: "A car's stopping distance: twice the speed, four times the distance. Hunger works the same way here." Viz: a slider on E moving a dot along both curves at once, the two heights read out live, so the sixteen-to-four comparison is seen as E slides from 0.9 to 0.6.

**41. MINOR. p06. "We will come back to why that matters" is a promise with no pointer.**
Say "in chapter seven, when no brain learns to avoid poison".

### 05_brain.md

**42. MAJOR. p07. The hidden unit, the biggest new object in the formula, has no real-life example and three symbols arrive in one breath.**
Fix: a smoke alarm. "A hidden unit is a smoke alarm. It has its own sensitivity to each smell, that is u. It has a threshold before it speaks at all, that is c. And it is wired to say something about each move, that is v. Silent until its total crosses the threshold, then louder the more it is over." Then the three symbols, each pointed at. Say where it breaks: "a real alarm clicks on; this one fades in, which is the next paragraph."

**43. MINOR. p09. The tickets are e to the zero and e to the z, with no division by T, while softmax in ch2 divided by T.**
A pattern-tracker will ask where T went. Add: "inside the committee the temperature is fixed at one, so the tickets are plain e to the z".

**44. MINOR. p14. The honest note is good but dense: three claims in one block.**
Split: the symmetry argument (only contrasts know left from right) on one screen with the decomposition bars; the committee-as-bias and the findings file on the next.

### 06_learning.md

**45. MAJOR. p02. Rule one is six ideas in one paragraph, and "why the log" gets no alternative that fails.**
The log is asserted ("turns ratios into a sum"). The alternative, the slope of the chance itself, fails because it shrinks to nothing when a move's chance is small, so rare moves could never be learned about; the log divides by the chance and undoes that. Also the expansion into two phases is spoken as a done fact.
Fix: split into three screens. (a) The need and the rule's shape: lesson times slope of something about the move taken. (b) Why the log: show the slope of the chance going to zero for a rare move, then the log's slope staying usable. (c) The two phases, with the bars moving (item 17).

**46. MAJOR. p05. A wall: eight sentences carrying step size, entropy (undefined, item 3), the lurch, the corrected diagnosis, and "lr over T squared is one knob" (asserted).**
The learner with ADHD gets forty seconds of numbers with the screen showing two bars.
Fix: split into three screens, each with one moving picture. (a) Step versus brain: the two bars, nothing else. (b) The lurch: seed 313's bias flipping night to night, that line only. (c) The corrected diagnosis and the one knob. For the one knob, give the why in a sentence, not a claim: "One over T comes from the slope of the log chance. A second one over T comes from how sharply the chances react to a change in energy. Together the policy moves as lr over T squared, so halving T is the same as quadrupling the step."

**47. MINOR. p03. "The two phases cancel and nothing moves" is true on average, not on each step.**
Say "on average over many steps they cancel". Viz: single steps jitter, the running average stays flat.

**48. MINOR. p04. "The energy gaps need to be about one" is stated without the reason, which is already on screen in ch2 p07.**
Add: "about one, because at T zero point three the softmax only cares about gaps of that size; chapter two." Also: lambda (0.95) is spoken as a number and never named, then appears as "λ ↔ lam" in ch8 p10; and the learner now has two discounts, 0.95 and 0.9, with no word on why two. Add: "This shrink factor is called lambda, zero point nine five. It is a cousin of gamma from rule two, doing the same job, counting far lessons less, in a rule that has no promise to carry them."

**49. MINOR. p09. "Only the taken move's knobs move" is not exact.**
The committee's u and c are shared across moves and do move, through the taken move's v. Say: "only the taken move's row of w and b moves, and the committee moves only through what it said about that move."

**50. MINOR. p10. The chain is the clearest picture in the chapter and has no real-life example; also the word "bootstrapping" is first used in ch7 p04 as if it were taught here.**
Add: "This is called bootstrapping. Like news of a prize at the end of a corridor: the person next to it knows first, then tells the next, one handover per visit."

**51. MINOR. p11. "No correction factor is needed" names a thing that was never introduced.**
Cut, or: "the random moves need no special treatment".

**52. MINOR. p14. "Divided by the temperature, three point three" reads as if the temperature were 3.3.**
Say: "divided by the temperature, zero point three, which is the same as multiplying by three point three".

### 07_experiment.md

**53. MAJOR. p04. "Sign features" is one of the four borrowed advantages and is never defined.**
Fix: "A sign feature is the contrast rounded to minus, zero or plus: which side is stronger, with the amount thrown away. Tabular Q lives on these." Viz: the contrast 0.52 collapsing to a plus sign.

**54. MINOR. p06. "Interval" and "includes zero" use a confidence interval that was never introduced.**
One sentence: "Twenty seeds is not many, so each bar carries a range: where the true mean most likely sits. If the range of the difference crosses zero, we are not allowed to say which is better."

**55. MINOR. p10. Five limits, five ideas, one screen.**
Two screens: poison and committee (both "what did the work"), then step-size casualty, ceiling, all-or-nothing.

**56. MINOR. p11. "Connect: the knobs exist, the world never needed them" is the first time the pivot's five words appear; fine, but "xor world" in ch9 p03 will then be the first time that word appears anywhere.**
Add here or in ch9: "a world where food is A or B but not both, which no straight line of knobs can separate, so the committee must do it".

### 08_code.md

**57. MINOR. p09. New symbols (w_E, w_X, X_set, the power n) appear only in the code and not in ch4.**
Say: "with both weights one, setpoints one and zero and the power two, this is exactly the bowl from chapter four."

**58. MINOR. p01. "Four lines" and the formula is five terms with the centring; fine, but the screen should show the code line and formula term lighting together, and the voice should give one pair per breath.**
Split p01 into two screens: b and w on one, the committee and the centring on the next.

### 09_close.md

**59. MINOR. p02. "Signal about 1.9 per day" on screen is a signal-to-noise ratio that was never introduced.**
Say "about twice as much signal as noise, per day" and drop the raw number from the screen, or define it in ch6 p06 where "the daily gradient pointed the right way on 96 percent of days" already lives.

**60. MINOR. p03. "Entropy bonus" is undefined (and entropy itself, item 3).**
Say "a small push to keep trying all three moves".

---

## C. Other "trust me" or filler spots (all MINOR)

- Ch0 p03: "No trust me" is a promise; it is kept well in ch4, ch5, ch7, broken at items 3, 4, 5, 37, 46, 51.
- Ch2 p05: "Not a magic number, a convenient one." Good honesty; keep.
- Ch5 p08: "the committee would be nothing but thirty-six more linear knobs" asserts the count; say "nothing but more linear knobs" or show the collapse (u times v folds into w).
- Ch7 p02: the correction trail is a lesson about method, not about the creature; good, but it is a full minute without a creature number or picture. Put the m3 bias flip replay (which is in the viz) at the start, so the picture leads.

---

## D. ADHD thread-loss risks (longest stretches without a concrete number or moving picture)

- Ch1 p02-p04: three abstract words in a row (energy, model, EBM) with knob boxes and marbles but no creature number until p06's 0.52. Pull one real number forward: put the three real Q of tick 3693 under the marble in p02.
- Ch6 p02-p04: rule one, toy, credited lesson: about two minutes of formula before the real seed 313 number in p05. Item 17 and 45 fix part of it; also move one real r strip (p04's viz) to the top of p02.
- Ch6 p05: see item 46.
- Ch7 p02-p04: three paragraphs of method history before the result bars in p05. Consider showing the EXP-02 bars first (p05) and then the three paragraphs as "how we got there", so the picture anchors the story.

---

## What works (do not rewrite these)

- **The loop diagram as spine** (ch0 p04, ch1 p15, ch3 p09, ch4 p08, ch5 p15, ch6 p15, ch9 p01). It is the "pattern and connections" he asked for, made literal. Items 16 and 19 only ask that it never changes shape and appears at every chapter end.
- **Ch2 p02-p03, weighted sum with the two failing alternatives.** This is the method done exactly: need, why multiply, why add, grocery bill, real tick, then plain sum and max failing on screen. Use it as the template for items 27 and 45.
- **Ch2 p07, the softmax prediction beat on the real Q.** Real numbers, a guess, a surprise (almost equal), and a consequence that pays off in ch5 p13. Best single beat in the script.
- **Ch2 p12, "a knob can only matter through the reading it multiplies".** The one gradient fact the learner needs, stated as a cause, and it is reused correctly in ch6 p09 and ch8 p05.
- **Ch3 p07, the contrast.** Three whys (difference, divide by the sum, the small constant), each with the failure it prevents. Only a real-life example is missing (item 38).
- **Ch4 p02-p03, why square and why sum.** Three reasons for the square, all visible on the curves, and the sum as two walls of one bowl. Only the example and the moving slider are missing (item 40).
- **Ch4 p04-p06, the real bite, the real quiet tick, the real poison bite**, each as a ball movement with its number. The body chapter is the most coherent in the script.
- **Ch5 p03, "three minus signs, one meaning".** Right instinct; it just needs to happen in ch1 instead (item 1).
- **Ch5 p06, the pause-and-predict on the contrast A knob with the hand-set forager as the payoff.** Real knob, real reading, real jump (0.26), real consequence (20 of 20). Exactly "what each change does to the visualisation".
- **Ch5 p09, where softplus comes from and why "free".** Two tickets, stack, log. This is the kind of reverse-engineering he asked for and it demystifies the title of the field in forty seconds.
- **Ch6 p07-p08, the promise and the gamma prediction beat.** Each term has a why; 0.9^20 and 0.99^20 on a chain the learner can see.
- **Ch6 p10, the chain walking back from the bite.** The clearest explanation of bootstrapping I have seen for a non-specialist, and it is the honest answer to "why does chasing a moving target settle".
- **Ch6 p14, the two rules side by side with their step sizes in the same units.** Closes the loop on ch1 p10 and ch6 p05 with numbers.
- **Ch7 p07-p08, the weights night by night and the frozen/mirrored test.** The learning made visible, then falsifiable. The sentence "a brain that steers by contrast steers backwards when you mirror it" is the proof stated as a mechanism. Only the prediction beat is given away (item 15).
- **Ch7 p09 last sentence** ("this seed was a lucky starter, which is why the frozen test, not this ratio, is the proof"). Honesty that strengthens the claim rather than hedging it.
- **Ch8 p10, the symbol-to-variable dictionary**, and the pairwise highlighting throughout ch8. This is what "the code of the model itself" should look like for him.
- **Ch9 p02, three columns: proved, measured, not shown.** Keep exactly as is (modulo item 59).
- **Every strip-down line that exists** is a true reduction: "the senses turn a smell map into twelve numbers, and the one that steers is the contrast"; "the body is a bowl, and the lesson is how far the ball rolled"; "evidence is a weighted sum plus a committee, energy is its negative, and the choice is the sign of a difference"; "Q is a promise, and learning is keeping every promise consistent". Only ch2 and ch7 lack one (item 16).
