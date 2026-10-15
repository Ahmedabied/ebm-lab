# 00 — Cold open
voice: eleven
length-target: ~1.5 min

## p01 | viz: the real world of seed 203 from tick 0: fields in colour (A red, B green, C blue, so food is yellow and poison is cyan), the creature with its two antennae, its path. Replays from life203.npz, slowed down. The on-screen tick counter shows the run's tick number.
This is a real life. Seed two hundred and three, from your lab, replayed tick by tick. Nothing on this screen is drawn by hand. The yellow glow is the smell of food, the cyan glow is the smell of poison, and the small dot with two feelers is the creature.

## p02 | viz: beside the world, three bars appear: Q for left, right, forward, moving every tick from the file; the chosen move lights up; a small legend under the bars: "Q, high wins". Below: the energy bar E and the toxin bar X.
Every tick, its brain gives each of its three moves a number, called Q. Nine times in ten it takes the move with the highest Q. Then its body tells it whether life just got a little better or a little worse. That is the whole loop. Sense, score, move, feel.

## p03 | viz: the weight heat map (3 moves × 12 readings) fades in, and the formula F(x,a) = −b_a − w_a·x − Σ_h softplus(c_h + u_h·x + v_{h,a}) fades in dim. Nothing is explained yet.
By the end of this lesson you will know what every number on this screen is, where it comes from, and why it is computed that way and not another way. Every number you will see is read from your own run files, and the one test I re-ran for this lesson is in the repo with its command.

## p04 | viz: the loop diagram that will grow one box per chapter: World → Senses → Brain → Move → Body → Lesson → Learning → Brain. The same seven boxes on every later screen; the policy lives inside the Move box.
We go almost in the order the data flows. The names first. Then the small maths everything is built from. Then the world, the senses, and the body, before the brain, because the brain's learning rule needs the body's number, so you must own that number first. Then the brain, the learning rule, the experiment, and finally the code. Each block plugs into the one before it. Let's start.
