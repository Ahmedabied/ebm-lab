# 08 — The code
voice: kokoro
length-target: ~5 min
note: every code block is read from the repo file at render time (creature/brain.py, creature/sim.py, creature/body.py); the formula sits beside it and the symbol and the variable light up together, one pair per breath.

## p01 | viz: creature/brain.py, class Brain, method F: the first two terms beside F(x,a) = −b_a − w_a·x. Highlights in pairs: b_a ↔ th["b"]; w_a·x ↔ X @ th["w"].T.
The formula lives in brain dot py, in a method called F. Minus b: minus the resting preferences. Minus X at w transposed: the dot product for every move at once; the at sign is numpy's matrix product.

## p02 | viz: the same method, the committee and the centring: Σ_h softplus ↔ _softplus(self.pre(X)).sum(axis=1); H·log 2 ↔ self.H * np.log(2.0).
Minus softplus of pre, summed over axis one: the committee, and axis one is the h in the sigma. Then, if centring is on, plus H times log two.

## p03 | viz: method pre: c[None, :, None] + (X @ u.T)[:, :, None] + v[None, :, :]. A 3-D block (N, H, A) drawn as a stack of H sheets, each A wide.
The committee's input z is built in pre. Three terms, exactly as in chapter five: c, the thresholds; X at u transposed, each unit's weighted sum of the readings; and v, each unit's word about each move. The strange brackets with None are numpy's way of lining up three shapes into one block: samples by units by moves. That block is every z at once.

## p04 | viz: _softplus = np.logaddexp(0.0, z) beside log(e^0 + e^z).
Softplus is one call: log add exp of zero and z. It computes log of e to the zero plus e to the z, the two tickets from chapter five, without overflowing when z is large.

## p05 | viz: method act, the egreedy branch: greedy = argmin(Fx); a = rng.integers(A) if rng.random() < eps else greedy; the log β bookkeeping line.
Acting is in act. The greedy move is the arg min of F, the lowest energy, the highest Q. One random number; if it is below epsilon, a random move over all three; otherwise the greedy one. The last line records the chance the rule gave the chosen move, which the policy-gradient learners need and the Q learner ignores.

## p06 | viz: method grad_negF: coef = onehot(a); g["b"] = coef; g["w"] = coef[:, :, None] * X[:, None, :]; S = sigmoid(pre); g["v"] = S * coef; g["c"] = (S*coef).sum(axis=2); g["u"] = g["c"] * X.
The slope of Q is grad neg F. Coef is a one for the taken move and zeros for the other two: only the promise that was made gets corrected. The slope for b is that one. The slope for w is that one times the readings: the knob's slope is its reading, chapter two. For the committee, S is the sigmoid of z, the slope of softplus from chapter five; the slopes for v, c and u follow the same pattern through it, and c and u are shared, so they move on every step.

## p07 | viz: method learn_q: td = y − Q(X)[a]; for each k: theta[k] += alpha · tensordot(td, g[k]) / N. Beside: knob += learning rate · miss · slope.
And the step is learn q. The miss, td, is y minus Q of the taken move. Each block of knobs moves by alpha times the miss times its slope, averaged over the batch. That line is the whole of rule two.

## p08 | viz: sim.py, q_targets: r + gamma · (1 − done) · Q(Xn).max(axis=1). "done" at the last tick of a day: no promise across the night.
The target y is q targets in sim dot py: r plus gamma times one minus done times the best next Q. Done is one on the last tick of a day, so no promise is made across the night; the day ends with just the lesson.

## p09 | viz: _online_q (one transition, one learn_q) and _replay_td (permutation, batches of 64, sleep_epochs passes).
Online learning is one transition, one target, one step. Night replay is a shuffled order, cut into batches of sixty-four, walked three times, each batch a target and a step. Same two calls, different grouping.

## p10 | viz: body.py: drive() = w_E · |E_set − E|^n + w_X · |X_set − X|^n; tick(): the metabolic line, the toxin decay, the drain, the food cap, the toxin add, the death check, return D0 − drive(). A note: "w 1, setpoints 1 and 0, n 2: the bowl of chapter four".
The body is body dot py. Drive is the bowl: the absolute distance from each setpoint, to the power n, weighted and summed. With both weights one, setpoints one and zero and the power two, it is exactly the bowl from chapter four. Tick subtracts metabolism, decays toxin by two percent, drains energy by one percent of the toxin, adds the food up to the cap, adds half the poison, kills at zero energy, and returns drive before minus drive after. The lesson, in one return statement.

## p11 | viz: a dictionary card: w ↔ th["w"]; b ↔ th["b"]; softplus ↔ np.logaddexp; Σ_h ↔ .sum(axis=1); T ↔ cfg.T; ε ↔ cfg.eps; γ ↔ gamma; learning rate ↔ alpha_q; λ ↔ lam; D ↔ drive(); r ↔ the return of tick(); miss ↔ td.
Stripped down, the dictionary. w is theta w. Softplus is log add exp. The sum over h is dot sum axis one. T is cfg dot T, epsilon is cfg dot eps, gamma is gamma, the learning rate is alpha q, lambda is lam. The miss is td. The drive is drive, and the lesson is what tick returns. Every symbol in the formula has one name in one file.
