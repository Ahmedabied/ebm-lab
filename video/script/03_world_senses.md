# 03 — The world and the senses
voice: kokoro
length-target: ~6 min

## p01 | viz: the loop diagram with the World and Senses boxes lit. Then the real 48×48 field at tick 3000, A in red, B in green, C in blue, so food is yellow and poison is cyan. Counters: "12 food items × 2.0 = 24 mass; 4 poison items × 2.0 = 8 mass".
First box: the world. It is a forty-eight by forty-eight grid that wraps around at the edges, like an old arcade screen. Three chemicals live on it, called A, B and C. Food leaks A and B, so it glows yellow. Poison leaks B and C, so it glows cyan. Notice that B is in both. B alone cannot tell food from poison. But there is three times as much food mass as poison mass in this world, so B still points mostly to food. Hold that; it comes back in chapter seven.

## p02 | viz: WHY SPREAD. A no-diffusion world: the smell sits only on the food cell; antennae one cell away read zero. Then diffusion on: a gradient the antennae can feel.
Why does the smell spread at all? Without spreading, the smell sits only on the food's own cell, and antennae one cell away feel nothing. Spreading is what gives the creature a slope to follow.

## p03 | viz: DIFFUSION. One cell and its four neighbours. The rule f + α·(up + down + left + right − 4f) built term by term, then rewritten as f + 4α·(average − f). A spike of smell spreading over ten ticks at α = 0.18.
The rule is four neighbours. Written out: the new value is the old value plus alpha times, the four neighbours added, minus four times the cell. Why minus four times the cell? Because the four neighbours added, minus four copies of the cell, is four times the difference between the neighbour average and the cell. So each cell moves four alpha of the way toward the average of its neighbours. At alpha zero point one eight, that is seventy-two percent of the way, every tick. Heat on a metal plate does the same thing.

## p04 | viz: PAUSE AND PREDICT: "α = 0.30. What happens?" Then two spreads side by side, α = 0.18 and α = 0.30: the second grows a checkerboard and blows up. A mark at α = 0.25.
Pause and predict. What if we set alpha to zero point three? Watch. At one quarter, four times a quarter is one, so a cell lands exactly on the neighbour average. Above that it overshoots, the neighbours overshoot back, and you get a checkerboard that grows every tick until the numbers explode. The code refuses any alpha above zero point two five for this reason. Not a style choice; a stability limit.

## p05 | viz: DECAY and EMIT. The total field mass over 300 ticks: without decay it climbs forever; with keep = 0.95 it settles. Food items pulse their blend into their cell every tick.
Two more rules. Decay: every tick, each cell keeps ninety-five percent. Without it the smell would fill the world and nothing would stand out. Emit: each food or poison item adds its blend, times its mass, times zero point zero five, into its own cell, every tick.

## p06 | viz: THE LEDGER. Three counters: emitted, decayed, eaten; a test ticks green each tick as the books close.
Every unit of smell that appears or vanishes is written in a ledger, and a test closes the books each tick. Your old project once created food out of nothing without noticing; this one cannot.

## p07 | viz: SENSES. The creature with two antennae at ±45°, length 1.5 cells. Each antenna reads three numbers (A, B, C) by blending the four nearest cells. Six raw numbers appear.
Second box: the senses. The creature has two antennae, forty-five degrees left and right, one and a half cells long. Each antenna reads the three chemicals at its tip. Six raw numbers. That is everything the creature can ever know about the world. No positions, no labels, no map. The words food and poison exist only in the world's bookkeeping.

## p08 | viz: the six raw numbers go through log1p(c/0.05) then get a small noise jitter (σ 0.02), shown as the values wobbling.
Each of the six goes through the log from chapter two, so a whisper and a shout both fit. Then a little noise is added, two hundredths in log units, because real sensors are noisy, and a brain that only works on perfect readings has learned nothing about the world.

## p09 | viz: CONTRAST. Left and right A readings. The formula (L − R)/(|L| + |R| + ε) built term by term. The raw difference in log units ≈ 0.15 beside the knob size it would need, ≈ 13; then the contrast, order one. Far from any source: noise over noise, pinned to zero by ε.
Now the first clever step. For each chemical, the brain is not handed left and right separately. It is handed the contrast: left minus right, divided by left plus right plus a small constant. Why the difference? Because which side is stronger is the steering question. Why divide by the sum? In log units the left-right difference is only about fifteen hundredths, so a decisive turn would need knobs of thirteen. Dividing by the total stretches it to order one, and knobs of order one are enough. Why the small constant? Far from everything, both readings are noise, and noise divided by noise is a random number. The constant pins it to zero instead. Your ears do something like this: you turn toward the louder ear by how much louder it is compared with both together, not by the raw difference. Ears use a log ratio; the creature divides logged readings. Same idea, slightly different arithmetic.

## p10 | viz: MEAN and CHANGE. The mean of left and right per chemical; the change since last tick as a small arrow up or down. A bacterium steering with one nose: run while it rises, tumble when it falls.
Then the mean of left and right per chemical, so the brain knows how strong the smell is overall. Then the change in that mean since last tick, so it can tell rising from falling. That is how a bacterium steers with one nose: keep going while the smell rises, turn when it falls.

## p11 | viz: BODY and ONE. The body's E and X as two more slots; the constant one as a slot that is always lit. The full vector x assembles for tick 3693, every slot with its real value.
Then the body's own energy and toxin, so the brain can act differently when hungry or poisoned. And a constant one, so one knob can act as a resting preference that does not depend on any smell. Twelve numbers. This is x, the vector from chapter one, with the real values from tick three six nine three.

## p12 | viz: the loop diagram: World → Senses now filled; the arrow out of Senses is labelled "x, 12 numbers, every tick".
Connections. The world's three fields come in through two antennae, pass through a log and a contrast, and leave this box as twelve numbers. The next box, the body, does not read x at all. The brain does. Stripped down: the senses turn a smell map into twelve numbers, and the one that steers is the contrast.
