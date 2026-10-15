"""Chapter 06 — Energy-based training: why it works, and why it first did not.
Render: ./build.sh render ql 06 && ./build.sh qc ql 06"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

LEGEND = "F energy, low wins   |   Q = minus F, high wins"


def lesson_strip(r, width=11.0, height=1.6, scale=None, colors=True):
    """60 small bars for a lesson strip: red below zero, green above."""
    n = len(r); bw = width / n * 0.8; step = width / n
    scale = scale or (height / 2) / max(float(np.abs(r).max()), 1e-9)
    g = VGroup()
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=DIM, stroke_width=1.5)
    for k, v in enumerate(r):
        h = max(abs(float(v)) * scale, 0.01)
        col = (C_GOOD if v >= 0 else C_BAD) if colors else FG
        rect = Rectangle(width=bw, height=h, fill_color=col, fill_opacity=0.9, stroke_width=0)
        rect.move_to([-width / 2 + step * (k + 0.5), 0, 0], aligned_edge=DOWN if v >= 0 else UP)
        g.add(rect)
    return VGroup(base, g)


def credit(r, lam=0.95):
    """Exactly creature/sim.py Cache.close_day: credited, mean-subtracted, standardised lesson."""
    r = np.asarray(r, dtype=np.float64)
    R = np.zeros_like(r); acc = r.mean() / (1.0 - lam)
    for t in range(len(r) - 1, -1, -1):
        acc = r[t] + lam * acc; R[t] = acc
    R0 = R.copy()
    R1 = R - R.mean()
    sd = R1.std()
    R2 = R1 / max(sd, 1e-3) if sd >= 1e-6 else np.zeros_like(R1)
    return R0, R1, R2


def bottom(mobj, maxw=8.8):
    """A bottom line that stays clear of the legend in the bottom-right corner."""
    if mobj.width > maxw: mobj.scale_to_fit_width(maxw)
    return mobj.to_edge(DOWN, buff=0.45).shift(LEFT * 2.4)


def softmax_(q, T=1.0):
    z = np.asarray(q, float) / T; z = z - z.max(); p = np.exp(z); return p / p.sum()


class Ch06(Scene):
    def construct(self):
        n = Narration(self, "06"); L = life(); R = run()
        legend = T(LEGEND, SZ_TINY, DIM).to_corner(DR, buff=0.25)

        # ------------------------------------------------------------ p01: the need
        d = n.say("p01")
        loop = LoopDiagram(radius=2.2).scale(0.85).move_to([-3.6, 0.6, 0])
        hdr = header("119 knobs in this brain,  one number per tick", SZ_BODY)
        self.play(FadeIn(loop), FadeIn(hdr), run_time=0.8)
        self.play(loop.lit("Learning"), run_time=0.6)
        a_in = Arrow(loop.boxes["Lesson"].get_right(), loop.boxes["Learning"].get_left(), buff=0.1, color=C_GOOD, stroke_width=3)
        l_in = T("r", SZ_SMALL, C_GOOD).next_to(a_in, DOWN, buff=0.05)
        n.until("p01", "hundred")
        self.play(GrowArrow(a_in), FadeIn(l_in), run_time=0.6)
        r60 = L["r"][:60]; note("day-0 lesson strip", LIFE_NPZ, "r[0:60] (waking ticks 0-59)", f"min {r60.min():.5f} max {r60.max():.5f}")
        strip = lesson_strip(r60, width=6.0, height=2.2).move_to([3.3, 0.4, 0])
        slab = T("the first 60 lessons r of seed 203, day 0", SZ_TINY, DIM).next_to(strip, DOWN, buff=0.4)
        n.until("p01", "stream")
        self.play(FadeIn(strip[0]), FadeIn(slab), run_time=0.3)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN if b.get_center()[1] >= strip[0].get_y() else UP) for b in strip[1]], lag_ratio=0.03), run_time=3.0)
        n.until("p01", "Two")
        rules = VGroup(T("rule one: contrastive policy gradient  (failed)", SZ_SMALL, C_BAD),
                       T("rule two: the value rule  (worked)", SZ_SMALL, C_GOOD)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(rules[0]), run_time=0.5); n.until("p01", "second"); self.play(FadeIn(rules[1]), run_time=0.5)
        n.end()
        self.play(FadeOut(loop), FadeOut(hdr), FadeOut(a_in), FadeOut(l_in), FadeOut(strip), FadeOut(slab), FadeOut(rules), run_time=0.5)

        # ------------------------------------------------------------ p02: rule one, the shape
        d = n.say("p02")
        self.add(legend)
        h2 = header("Rule one", SZ_BIG)
        shape = MathTex(r"\Delta\theta", r"=", r"\mathrm{lr}", r"\cdot", r"R", r"\cdot", r"\text{slope of (something about the move taken)}").scale(0.85)
        shape[2].set_color(C_T); shape[4].set_color(C_GOOD); shape[6].set_color(C_SP)
        shape.next_to(h2, DOWN, buff=0.7)
        i0 = 3193; Fx = -L["Q"][i0]; note("price tags, tick 3693", LIFE_NPZ, "Q[3193] (negated)", np.round(Fx, 6).tolist())
        tags = Bars(vmax=0.004, height=2.0, title="energy F of each move", fmt="{:+.4f}").move_to([0, -1.3, 0])
        tags.set_values(Fx); tags.highlight(int(L["a"][i0]))
        taken = T("taken", SZ_TINY, C_SP).next_to(tags.rects[int(L["a"][i0])], UP, buff=0.4)
        self.play(FadeIn(h2), run_time=0.4)
        n.until("p02", "learning"); self.play(Write(shape[0:2]), FadeIn(shape[2]), run_time=0.8)
        n.until("p02", "lesson"); self.play(FadeIn(shape[3:5]), run_time=0.5)
        n.until("p02", "slope"); self.play(FadeIn(shape[5:7]), run_time=0.6)
        n.until("p02", "taken"); self.play(FadeIn(tags), FadeIn(taken), run_time=0.7)
        n.until("p02", "good"); self.play(tags.rects[0].animate.shift(DOWN * 0.3), run_time=0.6)
        n.until("p02", "bad"); self.play(tags.rects[0].animate.shift(UP * 0.6), run_time=0.6)
        self.play(tags.rects[0].animate.shift(DOWN * 0.3), run_time=0.4)
        n.until("p02", "what"); self.play(Indicate(shape[6], color=C_SP), run_time=1.0)
        n.end()
        self.play(FadeOut(tags), FadeOut(taken), FadeOut(shape), FadeOut(h2), run_time=0.5)

        # ------------------------------------------------------------ p03: why the log
        d = n.say("p03")
        h3 = header("Why the slope of the log of the chance", SZ_BODY)
        ax = Axes(x_range=[-5, 2, 1], y_range=[-5, 1.2, 1], x_length=7.5, y_length=4.2,
                  axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([-1.2, -0.6, 0])
        xl = T("Q of the move taken (others fixed at 0)", SZ_TINY, DIM).next_to(ax.x_axis, DOWN, buff=0.1)
        pi = lambda q: np.exp(q) / (np.exp(q) + 2.0)
        c_pi = ax.plot(pi, x_range=[-5, 2], color=C_X, stroke_width=3)
        c_log = ax.plot(lambda q: np.log(pi(q)), x_range=[-5, 2], color=C_SP, stroke_width=3)
        l_pi = T("chance  π", SZ_SMALL, C_X).next_to(ax.c2p(2, pi(2)), RIGHT, buff=0.15)
        l_log = T("log π", SZ_SMALL, C_SP).next_to(ax.c2p(2, np.log(pi(2))), RIGHT, buff=0.15)
        q0 = float(np.log(2 * 0.02 / 0.98))           # where π = 0.02
        dot1 = Dot(ax.c2p(q0, pi(q0)), color=C_X, radius=0.08); dot2 = Dot(ax.c2p(q0, np.log(pi(q0))), color=C_SP, radius=0.08)
        s1 = pi(q0) * (1 - pi(q0)); s2 = 1 - pi(q0)
        def tangent(x0, y0, slope, color, half=0.9):
            p0 = ax.c2p(x0 - half, y0 - slope * half); p1 = ax.c2p(x0 + half, y0 + slope * half)
            return Line(p0, p1, color=color, stroke_width=4)
        t1 = tangent(q0, pi(q0), s1, C_X); t2 = tangent(q0, np.log(pi(q0)), s2, C_SP)
        lab1 = T(f"slope {s1:.3f}", SZ_TINY, C_X).next_to(t1, UP, buff=0.1)
        lab2 = T(f"slope {s2:.2f}", SZ_TINY, C_SP).next_to(t2, DOWN, buff=0.1)
        rare = T("a rare move: chance 0.02", SZ_SMALL, FG).move_to([4.2, 2.2, 0])
        eq = MathTex(r"\text{slope of }\log\pi", r"=", r"\frac{\text{slope of }\pi}{\pi}").scale(0.8).move_to([4.2, -1.8, 0])
        eq[0].set_color(C_SP); eq[2].set_color(C_X)
        self.play(FadeIn(h3), Create(ax), FadeIn(xl), run_time=0.8)
        self.play(Create(c_pi), FadeIn(l_pi), run_time=1.0)
        n.until("p03", "rarely"); self.play(FadeIn(rare), FadeIn(dot1), run_time=0.5)
        n.until("p03", "tiny", 1); self.play(Create(t1), FadeIn(lab1), run_time=0.8)
        n.until("p03", "log"); self.play(Create(c_log), FadeIn(l_log), FadeIn(dot2), run_time=1.0)
        n.until("p03", "divides"); self.play(Create(t2), FadeIn(lab2), Write(eq), run_time=1.0)
        n.until("p03", "usable"); self.play(Indicate(t2, color=C_SP), run_time=0.8)
        n.end()
        self.play(FadeOut(VGroup(h3, ax, xl, c_pi, c_log, l_pi, l_log, dot1, dot2, t1, t2, lab1, lab2, rare, eq)), run_time=0.5)

        # ------------------------------------------------------------ p04: the two phases, moving
        d = n.say("p04")
        f4 = MathTex(r"\log\pi(a|x)", r"=", r"\frac{Q(x,a)}{T}", r"-", r"\log\sum_{a'} e^{Q(x,a')/T}").scale(0.8).to_edge(UP, buff=0.4)
        f4[2].set_color(C_GOOD); f4[4].set_color(C_BAD)
        g4 = MathTex(r"\Delta\theta \propto", r"\underbrace{-\,\partial F(x,a)}_{\text{positive phase}}", r"+", r"\underbrace{\sum_{a'}\pi(a'|x)\,\partial F(x,a')}_{\text{negative phase}}").scale(0.75).next_to(f4, DOWN, buff=0.35)
        g4[1].set_color(C_GOOD); g4[3].set_color(C_BAD)
        F0 = np.array([0.5, 0.7, 0.9]); pis = softmax_(-F0 / 0.3)
        bars4 = Bars(vmax=1.5, height=2.3, title="energy F", fmt="{:+.2f}", symmetric=False).move_to([-2.5, -2.3, 0]).scale(0.9)
        bars4.set_values(F0); bars4.highlight(0)
        tk = T("taken: LEFT", SZ_TINY, C_SP).next_to(bars4.rects[0], UP, buff=0.45)
        chances = VGroup(*[T(f"chance {p:.2f}", SZ_TINY, MOVE[k]).next_to(bars4.labs[k], DOWN, buff=0.1) for k, p in enumerate(pis)])
        self.play(Write(f4), run_time=1.2)
        n.until("p04", "splits"); self.play(FadeIn(g4), run_time=0.8)
        n.until("p04", "first"); self.play(FadeIn(bars4), FadeIn(tk), run_time=0.6)
        amt = 0.3
        n.until("p04", "sink")
        F1 = F0.copy(); F1[0] -= amt; self.play(Indicate(g4[1], color=C_GOOD), run_time=0.4)
        self.play(UpdateFromAlphaFunc(bars4, lambda m, al: m.set_values(F0 + (F1 - F0) * al)), run_time=1.2)
        n.until("p04", "second"); self.play(FadeIn(chances), run_time=0.5)
        n.until("p04", "rise")
        F2 = F1 + amt * pis; self.play(Indicate(g4[3], color=C_BAD), run_time=0.4)
        self.play(UpdateFromAlphaFunc(bars4, lambda m, al: m.set_values(F1 + (F2 - F1) * al)), run_time=1.2)
        net = VGroup(T("net change", SZ_SMALL, FG), *[T(f"{MOVE_NAME[k]}: {F2[k]-F0[k]:+.2f}", SZ_TINY, MOVE[k]) for k in range(3)]).arrange(DOWN, buff=0.2).move_to([3.3, -2.0, 0])
        n.until("p04", "difference"); self.play(FadeIn(net), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(f4, g4, bars4, tk, chances, net)), run_time=0.5)

        # ------------------------------------------------------------ p05: the toy
        d = n.say("p05")
        h5 = header("toy, not lab data:  three moves, lesson = +1 whatever you do", SZ_SMALL)
        rng = np.random.default_rng(7); steps = 160; lr = 0.08
        Fa = np.zeros(3); Fb = np.zeros(3); trajA = [Fa.copy()]; trajB = [Fb.copy()]
        for _ in range(steps):
            pa = softmax_(-Fa); a = rng.choice(3, p=pa); Fa = Fa.copy(); Fa[a] -= lr; trajA.append(Fa.copy())
            pb = softmax_(-Fb); b = rng.choice(3, p=pb); onehot = np.eye(3)[b]; Fb = Fb - lr * (onehot - pb); trajB.append(Fb.copy())
        trajA = np.array(trajA); trajB = np.array(trajB)
        bA = Bars(vmax=6, height=2.6, title="positive phase only", fmt="{:+.1f}", symmetric=True).scale(0.85).move_to([-3.4, -0.6, 0])
        bB = Bars(vmax=6, height=2.6, title="both phases", fmt="{:+.1f}", symmetric=True).scale(0.85).move_to([3.4, -0.6, 0])
        tr = ValueTracker(0)
        self.play(FadeIn(h5), FadeIn(bA), run_time=0.6)
        bA.add_updater(lambda m: m.set_values(trajA[int(tr.get_value())]))
        n.until("p05", "lowered")
        self.play(tr.animate.set_value(steps), run_time=max(min(n.t_word("p05", "comparison") - self.time - 0.3, 9.0), 3.0), rate_func=linear)
        bA.clear_updaters()
        col = T("collapsed onto a favourite", SZ_TINY, C_BAD).next_to(bA, DOWN, buff=0.35)
        self.play(FadeIn(col), run_time=0.4)
        n.until("p05", "Add"); tr.set_value(0); bB.set_values(trajB[0]); self.play(FadeIn(bB), run_time=0.5)
        bB.add_updater(lambda m: m.set_values(trajB[int(tr.get_value())]))
        self.play(tr.animate.set_value(steps), run_time=max(n.remaining() - 1.5, 3.0), rate_func=linear)
        bB.clear_updaters()
        lvl = T("jitters, stays level on average", SZ_TINY, C_GOOD).next_to(bB, DOWN, buff=0.35)
        self.play(FadeIn(lvl), run_time=0.4)
        n.end()
        self.play(FadeOut(VGroup(h5, bA, bB, col, lvl)), run_time=0.5)

        # ------------------------------------------------------------ p06: the credited lesson
        d = n.say("p06")
        r_day = L["r"][:300]; R0, R1, R2 = credit(r_day, 0.95)
        note("credited lesson, day 0", LIFE_NPZ, "r[0:300] -> Cache.close_day(lam=0.95)", f"R std before scaling {R1.std():.5f}")
        h6 = header("the lesson that enters rule one", SZ_BODY)
        stage = T("raw lessons r, first 60 ticks", SZ_SMALL, FG).next_to(h6, DOWN, buff=0.35)
        sc = (1.0) / max(float(np.abs(R0[:60]).max()), 1e-9)
        s_raw = lesson_strip(r_day[:60], width=11.0, height=2.0).move_to([0, -0.8, 0])
        s_R0 = lesson_strip(R0[:60], width=11.0, height=2.0).move_to([0, -0.8, 0])
        s_R1 = lesson_strip(R1[:60], width=11.0, height=2.0).move_to([0, -0.8, 0])
        s_R2 = lesson_strip(R2[:60], width=11.0, height=2.0).move_to([0, -0.8, 0])
        axl = T("size: hundredths", SZ_TINY, DIM).next_to(s_raw, DOWN, buff=0.4)
        self.play(FadeIn(h6), FadeIn(stage), FadeIn(s_raw), FadeIn(axl), run_time=0.8)
        n.until("p06", "credited")
        self.play(Transform(s_raw, s_R0), stage.animate.become(T("credited: each tick inherits what followed, × 0.95 per tick (λ)", SZ_SMALL, FG).next_to(h6, DOWN, buff=0.35)), run_time=1.5)
        n.until("p06", "Second")
        self.play(Transform(s_raw, s_R1), stage.animate.become(T("minus the day's average", SZ_SMALL, FG).next_to(h6, DOWN, buff=0.35)), run_time=1.5)
        n.until("p06", "Third")
        self.play(Transform(s_raw, s_R2), stage.animate.become(T("divided by the day's spread", SZ_SMALL, FG).next_to(h6, DOWN, buff=0.35)),
                  axl.animate.become(T("size: about one", SZ_TINY, C_SP).next_to(s_raw, DOWN, buff=0.4)), run_time=1.5)
        n.until("p06", "trouble")
        warn = bottom(T("size one  ×  lr 1  ÷  T 0.3", SZ_SMALL, C_BAD))
        self.play(FadeIn(warn), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(h6, stage, s_raw, axl, warn)), run_time=0.5)

        # ------------------------------------------------------------ p07: step versus brain
        d = n.say("p07")
        note("step vs brain", P("research", "07-proof-of-possibility.md"), "§2.2: |θ₀| 0.087–0.093, night-1 |Δθ| 0.68–1.39", "8–16×")
        k = 7.0
        brain_bar = Rectangle(width=0.09 * k, height=0.5, fill_color=C_W, fill_opacity=0.9, stroke_width=0).move_to([-6.3 + 0.09 * k / 2, 0.9, 0])
        step_bar = Rectangle(width=0.68 * k, height=0.5, fill_color=C_BAD, fill_opacity=0.9, stroke_width=0).move_to([-6.3 + 0.68 * k / 2, -0.6, 0])
        step_ext = Rectangle(width=(1.39 - 0.68) * k, height=0.5, fill_color=C_BAD, fill_opacity=0.35, stroke_width=0).next_to(step_bar, RIGHT, buff=0)
        lb = T("the knobs at birth: length 0.09", SZ_SMALL, C_W).next_to(brain_bar, UP, buff=0.2, aligned_edge=LEFT)
        ls = T("the first night's step: 0.68 to 1.39", SZ_SMALL, C_BAD).next_to(step_bar, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(lb), GrowFromEdge(brain_bar, LEFT), run_time=1.0)
        n.until("p07", "step"); self.play(FadeIn(ls), GrowFromEdge(step_bar, LEFT), run_time=1.2); self.play(GrowFromEdge(step_ext, LEFT), run_time=0.8)
        n.until("p07", "Eight")
        ratio = T("8 to 16 times the whole brain, in one night", SZ_BIG, FG).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(ratio), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(brain_bar, step_bar, step_ext, lb, ls, ratio)), run_time=0.5)

        # ------------------------------------------------------------ p08: the lurch
        d = n.say("p08")
        m = m3(); lives = [l for l in m["lives"] if l["arm"] == "ebm"]
        note("lurch", M3, "lives[seed 313].bias_after_night", [round(v, 2) for v in next(l for l in lives if l["seed"] == 313)["bias_after_night"]])
        h8 = header("resting turn bias after each night (research 07, m3)", SZ_SMALL)
        ax8 = Axes(x_range=[1, 6, 1], y_range=[-1, 1, 0.5], x_length=8, y_length=4.2,
                   axis_config={"color": DIM, "stroke_width": 2, "include_numbers": True, "font_size": 20}).move_to([-0.5, -0.4, 0])
        yl = T("π(LEFT) − π(RIGHT) at rest", SZ_TINY, DIM).rotate(PI / 2).next_to(ax8.y_axis, LEFT, buff=0.15)
        xl8 = T("night", SZ_TINY, DIM).next_to(ax8.x_axis, DOWN, buff=0.1)
        self.play(FadeIn(h8), Create(ax8), FadeIn(yl), FadeIn(xl8), run_time=0.8)
        def line_for(seed, color, width):
            b = next(l for l in lives if l["seed"] == seed)["bias_after_night"]
            pts = [ax8.c2p(i + 1, v) for i, v in enumerate(b)]
            if len(pts) == 1: pts = pts * 2
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts), b
        l313, b313 = line_for(313, C_BAD, 6)
        d1 = Dot(ax8.c2p(1, b313[0]), color=C_BAD); d2 = Dot(ax8.c2p(2, b313[1]), color=C_BAD)
        t1 = T("+0.99", SZ_TINY, C_BAD).next_to(d1, UP, buff=0.1); t2 = T("−1.00", SZ_TINY, C_BAD).next_to(d2, DOWN, buff=0.1)
        s313 = T("seed 313", SZ_SMALL, C_BAD).move_to([4.6, 1.8, 0])
        n.until("p08", "deterministic")
        self.play(FadeIn(d1), FadeIn(t1), FadeIn(s313), run_time=0.6)
        n.until("p08", "overnight")
        self.play(Create(l313), FadeIn(d2), FadeIn(t2), run_time=1.0)
        others = VGroup(*[line_for(s, DIM, 2.5)[0] for s in (318, 316, 307, 300)])
        n.until("p08", "stall")
        self.play(LaggedStart(*[Create(o) for o in others], lag_ratio=0.3), run_time=1.5)
        lurch = T("not a stall, a lurch", SZ_BIG, FG).move_to([4.6, -2.6, 0])
        if lurch.get_right()[0] > 6.9: lurch.shift(LEFT * (lurch.get_right()[0] - 6.9))
        self.play(FadeIn(lurch), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(h8, ax8, yl, xl8, l313, d1, d2, t1, t2, s313, others, lurch)), run_time=0.5)

        # ------------------------------------------------------------ p09: one knob
        d = n.say("p09")
        corr = VGroup(T("first write-up:  learned too weakly to act", SZ_SMALL, DIM),
                      T("measured:  a step 8 to 16 times the brain, lurching nightly", SZ_SMALL, FG)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(UP, buff=0.5)
        strike = Line(corr[0].get_left(), corr[0].get_right(), color=C_BAD, stroke_width=3)
        self.play(FadeIn(corr[0]), run_time=0.5)
        n.until("p09", "opposite"); self.play(Create(strike), FadeIn(corr[1]), run_time=0.8)
        f9 = MathTex(r"\Delta\theta", r"\;=\;\mathrm{lr}\cdot R\cdot", r"\frac{1}{T}", r"\big[\dots\big]", r"\qquad \text{chances react as}\;", r"\frac{1}{T}", r"\;\Rightarrow\;\text{policy moves as}\;", r"\frac{\mathrm{lr}}{T^{2}}").scale(0.8).move_to([0, 0.1, 0])
        f9[2].set_color(C_T); f9[5].set_color(C_T); f9[7].set_color(C_T)
        if f9.width > 13.2: f9.scale_to_fit_width(13.2)
        n.until("p09", "one"); self.play(Write(f9[0:4]), run_time=1.0)
        n.until("p09", "second"); self.play(FadeIn(f9[4:6]), run_time=0.8)
        n.until("p09", "Together"); self.play(FadeIn(f9[6:8]), run_time=0.8)
        dial = VGroup(T("T = 0.3   →   lr / T² = 11.1", SZ_BODY, FG), T("T = 0.15  →   lr / T² = 44.4", SZ_BODY, C_T),
                      T("halve T  =  quadruple the step", SZ_SMALL, DIM)).arrange(DOWN, buff=0.3).move_to([0, -2.2, 0])
        n.until("p09", "halving"); self.play(FadeIn(dial[0]), run_time=0.4); self.play(FadeIn(dial[1]), FadeIn(dial[2]), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(corr, strike, f9, dial)), run_time=0.5)

        # ------------------------------------------------------------ p10: the hill
        d = n.say("p10")
        axh = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=6.5, y_length=3.8, axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([-3.2, -0.3, 0])
        hill = axh.plot(lambda x: x * x, x_range=[-3, 3], color=FG, stroke_width=3)
        axs = Axes(x_range=[-3, 3, 1], y_range=[0, 9, 3], x_length=5.0, y_length=3.8, axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([3.6, -0.3, 0])
        hill2 = axs.plot(lambda x: x * x, x_range=[-3, 3], color=FG, stroke_width=3)
        lbig = T("a step 10× the valley", SZ_SMALL, C_BAD).next_to(axh, UP, buff=0.2); lsm = T("a small step", SZ_SMALL, C_GOOD).next_to(axs, UP, buff=0.2)
        self.play(Create(axh), Create(hill), FadeIn(lbig), Create(axs), Create(hill2), FadeIn(lsm), run_time=1.0)
        xs = [2.5, -2.3, 2.1, -2.4, 2.2, -2.2]; dot = Dot(axh.c2p(xs[0], xs[0] ** 2), color=C_BAD, radius=0.1)
        self.add(dot)
        for x in xs[1:]:
            self.play(dot.animate.move_to(axh.c2p(x, x * x)), run_time=0.45, rate_func=there_and_back_with_pause if False else smooth)
        sd = Dot(axs.c2p(2.6, 2.6 ** 2), color=C_GOOD, radius=0.1); self.add(sd)
        xs2 = [2.6 * (0.78 ** i) for i in range(1, 9)]
        n.until("p10", "signal")
        for x in xs2:
            self.play(sd.animate.move_to(axs.c2p(x, x * x)), run_time=0.3)
        sig = bottom(T("the daily gradient pointed the right way on 96% of creature-days", SZ_SMALL, C_GOOD))
        self.play(FadeIn(sig), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(axh, hill, axs, hill2, lbig, lsm, dot, sd, sig)), run_time=0.5)

        # ------------------------------------------------------------ p11: rule two, the promise
        d = n.say("p11")
        h11 = header("Rule two: the promise", SZ_BIG)
        prom = MathTex(r"Q(x,a)", r"\;\approx\;", r"r_{\text{now}}", r"\;+\;", r"\gamma", r"\cdot", r"\max_{a'} Q(x',a')").scale(0.95).next_to(h11, DOWN, buff=0.5)
        prom[0].set_color(C_Q); prom[2].set_color(C_GOOD); prom[4].set_color(C_T); prom[6].set_color(C_SP)
        self.play(FadeIn(h11), Write(prom[0:2]), run_time=0.8)
        n.until("p11", "lesson"); self.play(FadeIn(prom[2:4]), run_time=0.6)
        n.until("p11", "max"); self.play(FadeIn(prom[6]), run_time=0.6)
        n.until("p11", "gamma"); self.play(FadeIn(prom[4:6]), run_time=0.6)
        # path with shrinking weights
        K = 60; w11 = 11.0; base_y = -1.6
        gbars = VGroup()
        for k in range(K):
            h = 2.2 * 0.9 ** k
            rect = Rectangle(width=w11 / K * 0.75, height=max(h, 0.015), fill_color=C_T, fill_opacity=0.85, stroke_width=0)
            rect.move_to([-w11 / 2 + w11 / K * (k + 0.5), base_y, 0], aligned_edge=DOWN); gbars.add(rect)
        bite = Dot([-w11 / 2 + w11 / K * (K - 0.5), base_y - 0.3, 0], color=FOOD, radius=0.1)
        bl = T("a bite, 60 ticks away", SZ_TINY, FOOD).next_to(bite, DOWN, buff=0.1)
        gl = T("how much a tick k away counts: 0.9^k", SZ_TINY, DIM).move_to([0, base_y - 0.55, 0]).shift(LEFT * 2.5)
        m20 = T("0.9^20 = 0.12", SZ_SMALL, C_T).move_to([-w11 / 2 + w11 / K * 20.5, base_y + 1.0, 0])
        m50 = T("0.9^50 = 0.005", SZ_SMALL, C_T).move_to([-w11 / 2 + w11 / K * 50.5, base_y + 1.0, 0])
        n.until("p11", "Why", 2)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in gbars], lag_ratio=0.01), FadeIn(bite), FadeIn(bl), FadeIn(gl), run_time=1.5)
        n.until("p11", "twelve"); self.play(FadeIn(m20), run_time=0.5)
        n.until("p11", "half"); self.play(FadeIn(m50), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(h11, m20, m50, bl, gl)), run_time=0.4)

        # ------------------------------------------------------------ p12: pause and predict γ
        d = n.say("p12")
        pause_card(self, "γ → 0.99.  How far does the promise reach?", hold=2.5)
        gam_lab = T("γ = 0.9", SZ_BIG, C_T).move_to([4.0, 1.0, 0])
        self.play(FadeIn(gam_lab), run_time=0.3)
        def set_gamma(g, lab):
            anims = []
            for k, b in enumerate(gbars):
                h = max(2.2 * g ** k, 0.015); x = b.get_center()[0]
                new = Rectangle(width=b.width, height=h, fill_color=C_T, fill_opacity=0.85, stroke_width=0).move_to([x, base_y, 0], aligned_edge=DOWN)
                anims.append(Transform(b, new))
            anims.append(gam_lab.animate.become(T(lab, SZ_BIG, C_T).move_to([4.0, 1.0, 0])))
            return anims
        n.until("p12", "Raise"); self.play(*set_gamma(0.99, "γ = 0.99"), run_time=1.5)
        m99 = T("0.99^20 = 0.82", SZ_SMALL, C_T).move_to([-w11 / 2 + w11 / K * 20.5, base_y + 2.6, 0])
        n.until("p12", "eighty"); self.play(FadeIn(m99), run_time=0.5)
        n.until("p12", "Lower"); self.play(FadeOut(m99), *set_gamma(0.5, "γ = 0.5"), run_time=1.5)
        m5 = T("0.5^3 = 0.125", SZ_SMALL, C_T).move_to([-w11 / 2 + w11 / K * 3.5 + 1.2, base_y + 1.6, 0])
        n.until("p12", "three"); self.play(FadeIn(m5), run_time=0.5)
        n.until("p12", "Gamma")
        far = bottom(T("gamma is how far ahead the creature lives", SZ_BODY, FG))
        self.play(FadeIn(far), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(prom, gbars, bite, gam_lab, m5, far)), run_time=0.5)

        # ------------------------------------------------------------ p13: the update, real tick 3693
        d = n.say("p13")
        up = MathTex(r"y = r + \gamma\,\max_{a'}Q(x',a')", r"\qquad \text{miss} = y - Q(x,a)", r"\qquad \text{knob} \mathrel{+}= \text{lr}\cdot\text{miss}\cdot\text{reading}").scale(0.72).to_edge(UP, buff=0.4)
        up[0].set_color(C_SP); up[1].set_color(C_BAD); up[2].set_color(C_W)
        if up.width > 13.2: up.scale_to_fit_width(13.2)
        self.play(Write(up[0]), run_time=0.8)
        n.until("p13", "miss"); self.play(FadeIn(up[1]), run_time=0.5)
        n.until("p13", "Turn"); self.play(FadeIn(up[2]), run_time=0.5)
        alpha_note = T("learning rate 0.3 = alpha_q  (not the smell's alpha)", SZ_TINY, DIM).next_to(up, DOWN, buff=0.2)
        n.until("p13", "alpha"); self.play(FadeIn(alpha_note), run_time=0.5)
        i = 3193; Qi = float(L["Q"][i][int(L["a"][i])]); ri = float(L["r"][i]); yi = float(L["y_target"][i + 1]); tdi = float(L["td"][i + 1]); xi = L["x"][i]
        note("TD example tick 3693", LIFE_NPZ, "Q[3193][LEFT], r[3193], y_target[3194], td[3194]", [Qi, ri, yi, tdi])
        rows = [("Q(x, LEFT)", f"{Qi:+.7f}", C_Q), ("r", f"{ri:+.7f}", C_GOOD), ("y", f"{yi:+.7f}", C_SP), ("miss = y − Q", f"{tdi:+.7f}", C_BAD)]
        tbl = VGroup(*[VGroup(T(a, SZ_SMALL, c), T(b, SZ_SMALL, c)).arrange(RIGHT, buff=0.5) for a, b, c in rows]).arrange(DOWN, buff=0.22, aligned_edge=RIGHT).move_to([-3.4, -0.5, 0])
        ttl = T("tick 3693, day 10", SZ_SMALL, FG).next_to(tbl, UP, buff=0.3)
        W = theta_at(i)["w"]; hm = Heatmap(W, cell=0.3, col_labels=L["input_names"]).scale(0.85).move_to([3.6, 0.0, 0])
        box = SurroundingRectangle(VGroup(*hm.cells[0:12]), color=C_SP, buff=0.02, stroke_width=3)
        shared = T("+ the committee's shared c and u", SZ_TINY, C_HID).next_to(hm, DOWN, buff=0.75)
        n.until("p13", "Only"); self.play(FadeIn(hm), Create(box), run_time=0.8); self.play(FadeIn(shared), run_time=0.4)
        n.until("p13", "Real"); self.play(FadeIn(ttl), run_time=0.3)
        for row, wd in zip(tbl, ["Q", "lesson", "y", "miss"]):
            n.until("p13", wd, 0 if wd != "miss" else 1); self.play(FadeIn(row), run_time=0.4)
        dws = [("contrast A", 0.3 * tdi * float(xi[0])), ("energy", 0.3 * tdi * float(xi[9])), ("constant", 0.3 * tdi * float(xi[11]))]
        dtbl = VGroup(*[T(f"Δw[LEFT, {nm}] = 0.3 × miss × {float(v / (0.3 * tdi)):.3f} = {v:+.7f}", SZ_TINY, C_W) for nm, v in dws]).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.4)
        if dtbl.width > 8.6: dtbl.scale_to_fit_width(8.6)
        n.until("p13", "Each"); self.play(FadeIn(dtbl), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(tbl, ttl, hm, box, shared, dtbl)), run_time=0.5)

        # ------------------------------------------------------------ p14: tick 1231, a bite with a full tank
        d = n.say("p14")
        j = 1081; Qj = float(L["Q"][j][int(L["a"][j])]); rj = float(L["r"][j]); yj = float(L["y_target"][j + 1]); tdj = float(L["td"][j + 1])
        note("TD example tick 1231", LIFE_NPZ, "Q[1081][LEFT], r[1081], y_target[1082], td[1082], E[1081]", [Qj, rj, yj, tdj, float(L["E"][j])])
        ttl2 = T("tick 1231, day 3:  a bite with a full tank  (E = 1.0, r = 0)", SZ_SMALL, FG).move_to([0, 1.3, 0])
        sub = VGroup(T(f"y     {yj:+.7f}", SZ_BIG, C_SP), T(f"Q     {Qj:+.7f}", SZ_BIG, C_Q), Line(LEFT * 3.2, RIGHT * 3.2, color=DIM),
                     T(f"miss  {tdj:+.7f}", SZ_BIG, C_BAD)).arrange(DOWN, buff=0.25, aligned_edge=RIGHT).move_to([0, -0.9, 0])
        self.play(FadeIn(ttl2), run_time=0.5)
        n.until("p14", "Q"); self.play(FadeIn(sub[1]), run_time=0.4)
        n.until("p14", "y"); self.play(FadeIn(sub[0]), run_time=0.4)
        n.until("p14", "miss"); self.play(Create(sub[2]), FadeIn(sub[3]), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(up, alpha_note, ttl2, sub)), run_time=0.5)

        # ------------------------------------------------------------ p15: why centring mattered
        d = n.say("p15")
        h15 = header("without centring  (A16)", SZ_BODY)
        note("A16 centring", P("DESIGN-AMENDMENTS.md"), "A16: 64–69%; pilot 627 → 3729", "")
        cb = Bars(vmax=3.2, height=3.0, title="Q of each move", fmt="{:.2f}", symmetric=False).move_to([-3.0, -1.6, 0])
        Qc = np.array([2.80, 2.80, 2.80]); cb.set_values(Qc); cb.highlight(0)
        tgt = DashedLine(cb.base.get_left() + UP * cb.y_of(2.5), cb.base.get_right() + UP * cb.y_of(2.5), color=C_SP, stroke_width=3)
        tl = T("target y ≈ r + 0.9 × 2.8 ≈ 2.5", SZ_TINY, C_SP).next_to(tgt, RIGHT, buff=0.2)
        self.play(FadeIn(h15), FadeIn(cb), run_time=0.6)
        n.until("p15", "target"); self.play(Create(tgt), FadeIn(tl), run_time=0.7)
        n.until("p15", "pulled")
        log = T("", SZ_TINY, DIM).move_to([3.6, -2.6, 0]); self.add(log)
        rot = VGroup();
        for s in range(6):
            kk = int(np.argmax(Qc + np.array([0, -1e-6, -2e-6]))); Qn = Qc.copy(); Qn[kk] += 0.3 * (2.5 - Qc[kk])
            cb.highlight(kk)
            self.play(UpdateFromAlphaFunc(cb, lambda m, al, a0=Qc.copy(), a1=Qn.copy(): m.set_values(a0 + (a1 - a0) * al)), run_time=0.55)
            Qc = Qn
        lost = T("the top move loses its spot after its own update\n(64–69% of the time in the pilot)", SZ_SMALL, FG, line_spacing=1.0).move_to([3.6, 0.2, 0])
        if lost.width > 6.4: lost.scale_to_fit_width(6.4)
        n.until("p15", "lost"); self.play(FadeIn(lost), run_time=0.5)
        fix = T("with centring: all three near 0, target near 0, tiny steps\npilot: 627 → 3729 ticks", SZ_SMALL, C_GOOD, line_spacing=1.0).move_to([3.6, -1.6, 0])
        if fix.width > 6.4: fix.scale_to_fit_width(6.4)
        n.until("p15", "referee"); self.play(FadeIn(fix), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(h15, cb, tgt, tl, lost, fix, log)), run_time=0.5)

        # ------------------------------------------------------------ p16: consistency / bootstrapping
        d = n.say("p16")
        h16 = header("the chain walks back from the bite", SZ_BODY)
        nS = 5; Qs = np.zeros(nS); rs = np.zeros(nS); rs[-1] = 1.0
        chain = Bars(labels=[f"spot {k+1}" for k in range(nS)], colors=[C_Q] * nS, width=1.1, gap=0.6, vmax=1.0, height=2.4, fmt="{:.2f}", symmetric=False).move_to([-1.0, -1.0, 0])
        chain.set_values(Qs)
        food = Dot(chain.rects[-1].get_center() + RIGHT * 1.25 + UP * 1.3, color=FOOD, radius=0.12); fl = T("bite r = 1", SZ_TINY, FOOD).next_to(food, RIGHT, buff=0.12)
        pl = T("pass 0", SZ_SMALL, C_SP).move_to([5.2, 1.4, 0])
        self.play(FadeIn(h16), FadeIn(chain), FadeIn(food), FadeIn(fl), FadeIn(pl), run_time=0.8)
        n.until("p16", "First")
        for p in range(1, 6):
            Qn = rs + 0.9 * np.r_[Qs[1:], 0.0]
            self.play(UpdateFromAlphaFunc(chain, lambda m, al, a0=Qs.copy(), a1=Qn.copy(): m.set_values(a0 + (a1 - a0) * al)),
                      pl.animate.become(T(f"pass {p}", SZ_SMALL, C_SP).move_to([5.2, 1.4, 0])), run_time=0.9)
            Qs = Qn
            if p == 1: n.until("p16", "Second")
            elif p == 2: n.until("p16", "Each")
        boot = bottom(T("bootstrapping: one handover per visit", SZ_BODY, FG))
        n.until("p16", "bootstrapping"); self.play(FadeIn(boot), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(h16, chain, food, fl, pl, boot)), run_time=0.5)

        # ------------------------------------------------------------ p17: epsilon-greedy and the sign
        d = n.say("p17")
        h17 = header("compared, not scaled", SZ_BODY)
        qb = Bars(vmax=0.004, height=2.4, title="Q, high wins", fmt="{:+.4f}").move_to([-2.8, -0.8, 0])
        qb.set_values(L["Q"][3193]); qb.highlight(0)
        gap = T("gap LEFT − RIGHT: +0.0034", SZ_TINY, FG).next_to(qb, DOWN, buff=0.5)
        dice = T("dice: 1 in 10", SZ_SMALL, C_T).move_to([3.4, 0.8, 0]); dice_box = SurroundingRectangle(dice, color=C_T, buff=0.2)
        self.play(FadeIn(h17), FadeIn(qb), FadeIn(gap), run_time=0.7)
        # replay the real explore events over 40 ticks from 3193
        ticks = range(3193, 3233); expl = [k for k in ticks if L["a"][k] != L["greedy"][k]]
        note("explore events", LIFE_NPZ, "a != greedy on indices 3193-3232", expl)
        n.until("p17", "dice"); self.play(FadeIn(dice), Create(dice_box), run_time=0.5)
        counter = T("", SZ_TINY, DIM).next_to(dice_box, DOWN, buff=0.25); self.add(counter)
        for k in ticks:
            counter.become(T(f"tick {int(L['t'][k])}:  " + ("explore!" if k in expl else "greedy"), SZ_TINY, C_T if k in expl else DIM).next_to(dice_box, DOWN, buff=0.25))
            qb.set_values(L["Q"][k]); qb.highlight(int(L["a"][k]))
            if k in expl: self.play(Indicate(dice_box, color=C_T), run_time=0.3)
            else: self.wait(0.12)
        off = T("the target uses max:\nit learns about the best move\neven while doing a random one", SZ_SMALL, FG, line_spacing=1.0).move_to([3.4, -1.8, 0])
        n.until("p17", "target"); self.play(FadeIn(off), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(h17, qb, gap, dice, dice_box, counter, off)), run_time=0.5)

        # ------------------------------------------------------------ p18: online + night
        d = n.say("p18")
        h18 = header("every tick, and every night", SZ_BODY)
        day = Rectangle(width=11, height=0.45, stroke_color=DIM, stroke_width=2).move_to([0, 1.4, 0])
        dl = T("day: 300 ticks, one step each", SZ_TINY, FG).next_to(day, UP, buff=0.15)
        cursor = Rectangle(width=0.05, height=0.6, fill_color=C_SP, fill_opacity=1, stroke_width=0).move_to(day.get_left())
        self.play(FadeIn(h18), FadeIn(day), FadeIn(dl), FadeIn(cursor), run_time=0.6)
        self.play(cursor.animate.move_to(day.get_right()), run_time=2.0, rate_func=linear)
        n.until("p18", "night")
        nl = T("night: the last 3 days, ~900 transitions, shuffled", SZ_TINY, FG).move_to([0, 0.2, 0])
        cells = VGroup(*[Square(side_length=0.11, fill_color=DIM, fill_opacity=1, stroke_width=0) for _ in range(90)]).arrange_in_grid(rows=3, cols=30, buff=0.05).move_to([0, -0.6, 0])
        bite_i = 40; cells[bite_i].set_fill(FOOD)
        self.play(FadeIn(nl), FadeIn(cells), run_time=0.8)
        n.until("p18", "shuffled")
        perm = np.random.default_rng(3).permutation(90)
        targets = [cells[k].get_center().copy() for k in range(90)]
        self.play(*[cells[k].animate.move_to(targets[perm[k]]) for k in range(90)], run_time=1.2)
        bl18 = T("batches of 64, three passes", SZ_TINY, FG).next_to(cells, DOWN, buff=0.3)
        self.play(FadeIn(bl18), run_time=0.4)
        cnt = bottom(T("the bite's transition used: 0×", SZ_SMALL, FOOD))
        n.until("p18", "replay", 1); self.add(cnt)
        for u in range(1, 10):
            cnt.become(bottom(T(f"the bite's transition used: {u}×", SZ_SMALL, FOOD)))
            self.play(Indicate(cells[bite_i], color=FOOD, scale_factor=1.6), run_time=0.25)
        n.end()
        self.play(FadeOut(VGroup(h18, day, dl, cursor, nl, cells, bl18, cnt)), run_time=0.5)

        # ------------------------------------------------------------ p19: downscale and growth
        d = n.say("p19")
        wn = [s["w_norm"] for s in R["brain"]]; note("w_norm per night", RUN_JSON, "brain[i].w_norm, i=0..14", wn)
        h19 = header("at night: shrink by 1%, and sometimes grow", SZ_BODY)
        ax19 = Axes(x_range=[0, 14, 2], y_range=[0.07, 0.1, 0.01], x_length=7, y_length=3.6,
                    axis_config={"color": DIM, "stroke_width": 2, "include_numbers": True, "font_size": 20, "decimal_number_config": {"num_decimal_places": 2}}).move_to([-2.6, -0.8, 0])
        xl19 = T("night", SZ_TINY, DIM).next_to(ax19.x_axis, DOWN, buff=0.1); yl19 = T("knob length (w, u, v)", SZ_TINY, DIM).next_to(ax19.y_axis, UP, buff=0.1, aligned_edge=LEFT)
        curve = VMobject(stroke_color=C_W, stroke_width=4).set_points_as_corners([ax19.c2p(i, v) for i, v in enumerate(wn)])
        e0 = T("0.096", SZ_TINY, C_W).next_to(ax19.c2p(0, wn[0]), UP, buff=0.1); e1 = T("0.078", SZ_TINY, C_W).next_to(ax19.c2p(14, wn[-1]), UP, buff=0.1)
        self.play(FadeIn(h19), Create(ax19), FadeIn(xl19), FadeIn(yl19), run_time=0.8)
        n.until("p19", "see"); self.play(Create(curve), FadeIn(e0), FadeIn(e1), run_time=1.5)
        unit = VGroup(RoundedRectangle(corner_radius=0.1, width=2.2, height=1.2, stroke_color=C_HID, stroke_width=2),
                      T("unit 5, night 1", SZ_TINY, C_HID)).move_to([3.8, 0.9, 0]); unit[1].next_to(unit[0], UP, buff=0.1)
        vb = Bars(labels=("v L", "v R", "v F"), colors=[MOVE[0], MOVE[1], MOVE[2]], width=0.45, gap=0.3, vmax=0.05, height=1.4, fmt="{:.2f}").move_to([3.8, -1.3, 0])
        vb.set_values([0, 0, 0]); vl = T("output knobs born at zero", SZ_TINY, C_HID).next_to(vb, DOWN, buff=0.45)
        note("grow event", RUN_JSON, "events kind=grow", "night 1, H 4 -> 5")
        n.until("p19", "grows"); self.play(FadeIn(unit), FadeIn(vb), FadeIn(vl), run_time=0.8)
        n.end()
        self.play(FadeOut(VGroup(h19, ax19, xl19, yl19, curve, e0, e1, unit, vb, vl)), run_time=0.5)

        # ------------------------------------------------------------ p20: the two rules side by side
        d = n.say("p20")
        h20 = header("same brain, same world, two step sizes", SZ_BODY)
        colA = VGroup(T("rule one", SZ_BODY, C_BAD), T("lesson scaled to size 1", SZ_TINY), T("× lr 1  ÷ T 0.3  (× 3.3)", SZ_TINY),
                      T("night 1: ~300 samples, ~15 batch steps", SZ_TINY), T("each step 0.08 to 0.19", SZ_TINY), T("on knobs of total length 0.09", SZ_TINY, C_W)).arrange(DOWN, buff=0.22).move_to([-3.4, -0.2, 0])
        colB = VGroup(T("rule two", SZ_BODY, C_GOOD), T("raw lesson, hundredths", SZ_TINY), T("× learning rate 0.3", SZ_TINY),
                      T("one step per tick + replay", SZ_TINY), T("quiet tick: hundred-thousandths; bite tick: a few hundredths", SZ_TINY), T("on knob differences of thousandths", SZ_TINY, C_W)).arrange(DOWN, buff=0.22).move_to([3.4, -0.2, 0])
        sf = min(1.0, 6.3 / max(colA.width, colB.width))
        colA.scale(sf); colB.scale(sf)
        self.play(FadeIn(h20), FadeIn(colA[0]), FadeIn(colB[0]), run_time=0.6)
        n.until("p20", "Rule", 0)
        for it in colA[1:]: self.play(FadeIn(it), run_time=0.35)
        n.until("p20", "Rule", 1)
        for it in colB[1:]: self.play(FadeIn(it), run_time=0.35)
        n.until("p20", "caution")
        caution = bottom(T("caution: the Q step is itself at the edge of stability (15 inputs blew up on night 0)", SZ_TINY, C_SP))
        self.play(FadeIn(caution), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(h20, colA, colB, caution)), run_time=0.5)

        # ------------------------------------------------------------ p21: connections and the one line
        d = n.say("p21")
        loop2 = LoopDiagram(radius=2.2).scale(0.85).set_done(["World", "Senses", "Body", "Brain", "Learning"]).move_to([-3.6, 0.3, 0])
        arr = Arrow(loop2.boxes["Learning"].get_top(), loop2.boxes["Brain"].get_left(), buff=0.1, color=C_W, stroke_width=3)
        al = T("learning rate · miss · reading", SZ_TINY, C_W).next_to(arr.get_center(), UP, buff=0.1)
        self.play(FadeIn(loop2), run_time=0.7)
        n.until("p21", "slope"); self.play(GrowArrow(arr), FadeIn(al), run_time=0.7)
        n.until("p21", "Stripped")
        one = VGroup(T("Q is a promise.", SZ_BIG, C_Q),
                     T("Learning keeps every promise consistent\nwith what the body said and with the next promise.", SZ_SMALL, FG, line_spacing=1.0),
                     T("The bite is the only anchor;\nthe chain walks back from it, one step per visit.", SZ_SMALL, DIM, line_spacing=1.0)).arrange(DOWN, buff=0.35).move_to([3.3, 0.3, 0])
        for g in one:
            if g.width > 6.6: g.scale_to_fit_width(6.6)
        self.play(FadeIn(one[0]), run_time=0.5); self.play(FadeIn(one[1]), run_time=0.6)
        n.until("p21", "anchor"); self.play(FadeIn(one[2]), run_time=0.6)
        n.finish(tail=1.2)
