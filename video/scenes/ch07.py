"""Chapter 07 — The experiment, step by step. Every bar is read from the lab's result files."""
import sys, os, re; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

REPORT = P("experiments", "results", "02_main_report.md")


def bar_chart(arms, labels, which, colors, width=11.0, height=3.4, vmax=5500, ceiling=None, title=None):
    """Bars with 95% whiskers from results(which)["stats"][arm]["ticks_alive"]. Returns (group, bars, whiskers, labs, vals)."""
    n = len(arms); slot = width / n; bw = slot * 0.62
    ax = Line(LEFT * width / 2, RIGHT * width / 2, color=DIM, stroke_width=2)
    bars, whisk, labs, vals = VGroup(), VGroup(), VGroup(), VGroup()
    for k, (arm, lab, col) in enumerate(zip(arms, labels, colors)):
        mean, lo, hi = arm_stats(arm, which)
        note(f"EXP-{which} {arm} ticks alive", RES02 if which == "02" else RES01, f"stats.{arm}.ticks_alive", f"{mean:.0f} [{lo:.0f}, {hi:.0f}]")
        xk = -width / 2 + slot * (k + 0.5)
        r = Rectangle(width=bw, height=height * mean / vmax, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to([xk, 0, 0], aligned_edge=DOWN)
        w = VGroup(Line([xk, height * lo / vmax, 0], [xk, height * hi / vmax, 0], color=FG, stroke_width=2),
                   Line([xk - 0.1, height * lo / vmax, 0], [xk + 0.1, height * lo / vmax, 0], color=FG, stroke_width=2),
                   Line([xk - 0.1, height * hi / vmax, 0], [xk + 0.1, height * hi / vmax, 0], color=FG, stroke_width=2))
        l = T(lab, 17, col).move_to([xk, -0.3, 0])
        if l.width > slot * 0.95: l.scale_to_fit_width(slot * 0.95)
        v = T(f"{mean:.0f}", 17, col).move_to([xk, height * hi / vmax + 0.22, 0])
        bars.add(r); whisk.add(w); labs.add(l); vals.add(v)
    g = VGroup(ax, bars, whisk, labs, vals)
    if ceiling:
        cl = DashedLine([-width / 2, height * ceiling / vmax, 0], [width / 2, height * ceiling / vmax, 0], color=DIM, dash_length=0.12)
        ct = T(f"ceiling {ceiling}", SZ_TINY, DIM).next_to(cl, UP, buff=0.05).align_to(cl, LEFT)
        g.add(cl, ct)
    if title:
        g.add(T(title, SZ_SMALL).next_to(ax, UP, buff=height + 0.75))
    return g, bars, whisk, labs, vals


def card(lines, color=FG, width=5.8, size=SZ_TINY):
    body = VGroup(*[T(l, size) for l in lines]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    for l in body:
        if l.width > width - 0.5: l.scale_to_fit_width(width - 0.5)
    box = RoundedRectangle(corner_radius=0.15, width=width, height=body.height + 0.6, stroke_color=color, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    body.move_to(box)
    return VGroup(box, body)


class Ch07(Scene):
    def construct(self):
        n = Narration(self, "07"); L = life()
        title_card(self, "7", "The experiment", hold=0.8)

        # ---------------- p01: tabular Q, the yardstick
        d = n.say("p01")
        hdr = header("The yardstick: tabular Q", SZ_BIG)
        self.play(FadeIn(hdr), run_time=0.5)
        rows, cols = 54, 3; ch = 0.085; cw = 0.42
        cells = VGroup(*[Square(side_length=ch, stroke_width=1.0, stroke_color=DIM, fill_color=GRID, fill_opacity=1)
                         .stretch_to_fit_width(cw).move_to([j * cw, -i * ch, 0]) for i in range(rows) for j in range(cols)])
        cells.move_to([-4.2, -0.3, 0])
        tlab = T("54 rows × 3 moves", SZ_TINY, DIM).next_to(cells, DOWN, buff=0.15)
        trows = T("27 sign patterns × hungry or not", 16, DIM).next_to(cells, LEFT, buff=0.2).rotate(PI / 2)
        note("tabular Q table", P("creature", "baselines.py"), "TabularQ._state: 3 signs^3 × 2 hunger = 54 states × 3 actions", "54x3")
        hm = Heatmap(nightly_w()[-1], cell=0.3, col_labels=L["input_names"]).scale(0.95).move_to([2.9, -0.2, 0])
        hlab = T("3 moves × 12 knobs, shared", SZ_TINY, DIM).next_to(hm, DOWN, buff=0.85)
        n.until("p01", "table")
        self.play(FadeIn(cells), FadeIn(tlab), FadeIn(trows), run_time=0.8)
        # sign feature: 0.52 collapses to +
        n.until("p01", "rounds")
        xA = float(L["x"][3193, 0]); note("sign feature example", LIFE_NPZ, "x[3193, contrast_A]", xA)
        sf = VGroup(T(f"contrast {xA:+.2f}", SZ_SMALL, C_X), T("→", SZ_SMALL, DIM), T("+", SZ_BIG, C_SP)).arrange(RIGHT, buff=0.3).move_to([2.9, 2.2, 0])
        self.play(FadeIn(sf[0]), run_time=0.4); self.play(FadeIn(sf[1]), FadeIn(sf[2]), run_time=0.5)
        n.until("p01", "fifty-four")
        self.play(Indicate(tlab, color=C_SP), run_time=0.6)
        n.until("p01", "cell")
        one = cells[20 * 3 + 1].copy().set_fill(C_SP, 1)
        self.play(FadeIn(one), run_time=0.3); self.play(FadeOut(one), run_time=0.4)
        n.until("p01", "shares")
        self.play(FadeOut(sf), FadeIn(hm), FadeIn(hlab), run_time=0.6)
        row = SurroundingRectangle(VGroup(*hm.cells[0:12]), color=C_SP, buff=0.02, stroke_width=3)
        self.play(Create(row), run_time=0.5); self.play(FadeOut(row), run_time=0.4)
        n.end()
        self.play(FadeOut(VGroup(hdr, cells, tlab, trows, hm, hlab)), run_time=0.5)

        # ---------------- p02: EXP-01 bars
        d = n.say("p02")
        arms1 = ["random", "ebm-nolearn", "ebm", "tabular_q", "oracle", "braitenberg"]
        labs1 = ["random", "learning off", "learning on", "tabular Q", "oracle", "hand-wired"]
        cols1 = [DIM, C_X, C_BAD, C_HID, FG, C_SP]
        g1, b1, w1, l1, v1 = bar_chart(arms1, labs1, "01", cols1, width=11, height=3.4)
        g1.move_to([0, -0.6, 0])
        t1 = header("EXP-01  ·  20 seeds  ·  15 days  ·  linear world", SZ_SMALL)
        self.play(FadeIn(t1), FadeIn(g1[0]), run_time=0.5)
        self.remove(b1, w1, l1, v1)
        order = [("Random", 0), ("off", 1), ("on", 2), ("Tabular", 3), ("hand-wired", 5)]
        for word, k in order:
            n.until("p02", word)
            self.play(GrowFromEdge(b1[k], DOWN), FadeIn(w1[k]), FadeIn(l1[k]), FadeIn(v1[k]), run_time=0.7)
        n.until("p02", "Everything")
        self.play(GrowFromEdge(b1[4], DOWN), FadeIn(w1[4]), FadeIn(l1[4]), FadeIn(v1[4]), run_time=0.6)
        n.end()
        self.play(FadeOut(g1), FadeOut(t1), run_time=0.5)

        # ---------------- p03: the lurch and the correction trail
        d = n.say("p03")
        M = m3(); lives = [x for x in M["lives"] if x["arm"] == "ebm"]
        s313 = [x for x in lives if x["seed"] == 313][0]["bias_after_night"]
        note("m3 bias seed 313", M3, "lives[seed=313].bias_after_night", s313)
        ax = Axes(x_range=[0, 5, 1], y_range=[-1, 1, 0.5], x_length=5.2, y_length=3.0,
                  axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([-3.6, 0.3, 0])
        xl = T("night", SZ_TINY, DIM).next_to(ax.x_axis, DOWN, buff=0.1)
        yl = T("resting turn bias  (+1 = always left, −1 = always right)", SZ_TINY, DIM).next_to(ax, UP, buff=0.35)
        ytk = VGroup(T("+1", 14, DIM).next_to(ax.c2p(0, 1), LEFT, buff=0.1), T("−1", 14, DIM).next_to(ax.c2p(0, -1), LEFT, buff=0.1))
        hh = header("Seed 313 flips overnight", SZ_BIG)
        self.play(FadeIn(hh), FadeIn(ax), FadeIn(xl), FadeIn(yl), FadeIn(ytk), run_time=0.6)
        others = VGroup()
        for x in lives[:6]:
            ba = x["bias_after_night"][:3]
            if len(ba) >= 2:
                pts_o = [ax.c2p(i + 1, b) for i, b in enumerate(ba)]
                others.add(VMobject(stroke_color=DIM, stroke_width=1.5, stroke_opacity=0.5, fill_opacity=0).set_points_as_corners(pts_o))
        self.play(FadeIn(others), run_time=0.6)
        n.until("p03", "three")
        pts = [ax.c2p(i + 1, b) for i, b in enumerate(s313)]
        line = VMobject(stroke_color=C_BAD, stroke_width=5).set_points_as_corners(pts)
        d1 = Dot(pts[0], color=C_BAD); d2 = Dot(pts[1], color=C_BAD)
        v1_ = T(f"{s313[0]:+.2f}", SZ_TINY, C_BAD).next_to(d1, UP); v2_ = T(f"{s313[1]:+.2f}", SZ_TINY, C_BAD).next_to(d2, DOWN)
        self.play(FadeIn(d1), FadeIn(v1_), run_time=0.4); self.play(Create(line), FadeIn(d2), FadeIn(v2_), run_time=0.9)
        # correction trail
        sents = ["1.  learned the right thing, too weakly to act on", "2.  a step 8–16× the weights; cannot unlearn", "3.  lurches between near-deterministic habits every night"]
        trail = VGroup(*[T(s, SZ_TINY) for s in sents]).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([3.4, 0.3, 0])
        for t in trail:
            if t.width > 6.4: t.scale_to_fit_width(6.4)
        note("findings/01 correction trail", P("findings", "01_exp01_within_life_learning.md"), "diagnosis + CORRECTION block", "3 sentences")
        n.until("p03", "first")
        self.play(FadeIn(trail[0]), run_time=0.5)
        n.until("p03", "second")
        strike0 = Line(trail[0].get_left(), trail[0].get_right(), color=C_BAD, stroke_width=3)
        self.play(Create(strike0), FadeIn(trail[1]), run_time=0.6)
        n.until("p03", "withdrawn")
        strike1 = Line(trail[1].get_left(), trail[1].get_right(), color=C_BAD, stroke_width=3)
        self.play(Create(strike1), run_time=0.5)
        n.until("p03", "lurches")
        self.play(FadeIn(trail[2]), run_time=0.5)
        n.until("p03", "still")
        self.play(Indicate(trail, color=C_SP, scale_factor=1.02), run_time=0.8)
        n.end()
        self.play(FadeOut(VGroup(hh, ax, xl, yl, ytk, others, line, d1, d2, v1_, v2_, trail, strike0, strike1)), run_time=0.5)

        # ---------------- p04: the referees
        d = n.say("p04")
        hh = header("Two hostile referees per claim", SZ_BIG)
        def silhouette(x):
            return VGroup(Circle(radius=0.35, color=FG, fill_color=PANEL, fill_opacity=1, stroke_width=2),
                          RoundedRectangle(corner_radius=0.2, width=1.2, height=1.0, color=FG, fill_color=PANEL, fill_opacity=1, stroke_width=2).shift(DOWN * 0.85)).move_to([x, 1.4, 0])
        s1, s2 = silhouette(-1.2), silhouette(1.2)
        brk = T("break this claim", SZ_SMALL, C_BAD).next_to(VGroup(s1, s2), DOWN, buff=0.25)
        self.play(FadeIn(hh), FadeIn(s1), FadeIn(s2), run_time=0.6)
        n.until("p04", "break")
        self.play(Write(brk), run_time=0.6)
        c16 = card(["A16  centring", "Q starts at 2.8, target ≈ 2.5", "greedy move loses its top spot 64–69%", "pilot: 627 → 3729 ticks"], C_SP, width=5.9)
        c17 = card(["A17  the table learner", "built s′ from the pre-move reading", "not textbook; tabular_q_next added", "pilot re-run on the fixed code"], C_HID, width=5.9)
        note("A16 numbers", P("DESIGN-AMENDMENTS.md"), "A16 row", "2.8 / 64-69% / 627 vs 3729"); note("A17", P("DESIGN-AMENDMENTS.md"), "A17 row", "tabular_q_next")
        VGroup(c16, c17).arrange(RIGHT, buff=0.5).move_to([0, -1.9, 0])
        n.until("p04", "One")
        self.play(FadeIn(c16, shift=UP * 0.2), run_time=0.6)
        n.until("p04", "Two")
        self.play(FadeIn(c17, shift=UP * 0.2), run_time=0.6)
        n.until("p04", "pilot")
        self.play(Indicate(c17[1][3], color=C_SP), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(hh, s1, s2, brk, c16, c17)), run_time=0.5)

        # ---------------- p05: the arms as characters
        d = n.say("p05")
        hh = header("EXP-02: which of tabular Q's four advantages?", SZ_SMALL)
        self.play(FadeIn(hh), run_time=0.4)
        adv = VGroup(*[T(s, SZ_SMALL) for s in ["1  sign features", "2  act on the highest Q", "3  the promise (bootstrapping)", "4  learn every tick"]]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-3.6, 1.2, 0])
        for t, w in zip(adv, ["sign", "highest", "promise", "every"]):
            n.until("p05", w); self.play(FadeIn(t, shift=RIGHT * 0.2), run_time=0.4)
        chars = [("ebm-dn", "B0", DIM, "online + night"), ("+sign", "1", C_X, "sign features"), ("+greedy", "2", C_X, "highest Q"),
                 ("+critic", "3", C_X, "a value helper"), ("ebm-td", "2+3+4", C_SP, "the value rule"), ("ebm-all", "1+2+3+4", C_HID, "everything")]
        row = VGroup()
        for name, which, col, what in chars:
            box = RoundedRectangle(corner_radius=0.12, width=1.85, height=1.5, stroke_color=col, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            g = VGroup(box, VGroup(T(name, 18, col), T(which, 16, DIM), T(what, 14, FG)).arrange(DOWN, buff=0.12).move_to(box))
            row.add(g)
        row.arrange(RIGHT, buff=0.25).move_to([0, -2.0, 0])
        n.until("p05", "alone")
        self.play(FadeIn(row[0]), run_time=0.4); self.play(LaggedStart(*[FadeIn(row[k], shift=UP * 0.2) for k in (1, 2, 3)], lag_ratio=0.3), run_time=1.0)
        n.until("p05", "value")
        self.play(FadeIn(row[4], shift=UP * 0.2), run_time=0.5)
        n.until("p05", "everything")
        self.play(FadeIn(row[5], shift=UP * 0.2), run_time=0.5)
        n.until("p05", "five")
        pre = T("five predictions, committed before the run", SZ_TINY, C_SP).move_to([3.0, 1.2, 0])
        self.play(FadeIn(pre), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(hh, adv, row, pre)), run_time=0.5)

        # ---------------- p06: EXP-02 bars
        d = n.say("p06")
        arms2 = ["random", "ebm-nolearn", "ebm-dn", "ebm-dn-greedy", "ebm-dn-critic", "ebm-dn-sign", "ebm-all", "tabular_q", "tabular_q_next", "ebm-td"]
        labs2 = ["random", "no learn", "B0", "+greedy", "+critic", "+sign", "all", "tabular Q", "textbook Q", "value rule"]
        cols2 = [DIM, DIM, DIM, C_X, C_X, C_X, C_HID, C_BIAS, C_BIAS, C_SP]
        g2, b2, w2, l2, v2 = bar_chart(arms2, labs2, "02", cols2, width=12.2, height=3.3, ceiling=5250)
        g2.move_to([0, -0.7, 0])
        t2 = header("EXP-02  ·  20 seeds  ·  15 days  ·  ticks alive", SZ_SMALL)
        R2 = results("02"); cens = {a: sum(1 for x in R2["lives"][a] if x["ticks_alive"] == 5250) for a in arms2}
        note("EXP-02 censored lives", RES02, "lives[arm] ticks_alive == 5250", cens)
        self.remove(b2, w2, l2, v2)
        self.play(FadeIn(t2), FadeIn(g2[0]), FadeIn(g2[5]), FadeIn(g2[6]), run_time=0.5)
        shown = [0, 1, 2, 7, 8]
        self.play(*[FadeIn(VGroup(b2[k], w2[k], l2[k], v2[k])) for k in shown], run_time=0.6)
        for word, k in [("Greedy", 3), ("helper", 4), ("Sign", 5), ("value", 9)]:
            n.until("p06", word)
            self.play(GrowFromEdge(b2[k], DOWN), FadeIn(w2[k]), FadeIn(l2[k]), FadeIn(v2[k]), run_time=0.7)
        n.until("p06", "fifteen")
        c15 = T(f"{cens['ebm-td']}/20 at the ceiling", SZ_TINY, C_SP).next_to(v2[9], UP, buff=0.1)
        self.play(FadeIn(c15), run_time=0.5)
        n.until("p06", "everything")
        self.play(GrowFromEdge(b2[6], DOWN), FadeIn(w2[6]), FadeIn(l2[6]), FadeIn(v2[6]), run_time=0.7)
        n.end()

        # ---------------- p07: ranges, paired difference, predictions
        d = n.say("p07")
        n.until("p07", "range")
        expl = T("20 seeds: the whisker is where the true mean most likely sits", SZ_TINY, FG).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(expl), Indicate(w2[9], color=C_SP, scale_factor=1.3), run_time=0.8)
        n.until("p07", "crosses")
        self.play(FadeOut(VGroup(g2, t2, c15, expl)), run_time=0.5)
        rep = open(REPORT).read()
        def paired(a, b):
            m = re.search(rf"\| {re.escape(a)} - {re.escape(b)} \| (-?\d+) \[(-?\d+), (-?\d+)\]", rep)
            vals = tuple(int(v) for v in m.groups()); note(f"paired {a} - {b}", REPORT, "Paired differences table, linear", vals); return vals
        pA = paired("ebm-td", "tabular_q"); pB = paired("ebm-td", "tabular_q_next")
        axp = Axes(x_range=[-1500, 3000, 500], y_range=[0, 2, 1], x_length=10, y_length=2.4,
                   axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}, y_axis_config={"stroke_opacity": 0}).move_to([0, 0.6, 0])
        zero = DashedLine(axp.c2p(0, 0), axp.c2p(0, 2), color=C_BAD, dash_length=0.1)
        zl = T("0", SZ_TINY, C_BAD).next_to(zero, DOWN, buff=0.1)
        hh = header("Paired difference in ticks alive (linear world)", SZ_SMALL)
        self.play(FadeIn(hh), FadeIn(axp), FadeIn(zero), FadeIn(zl), run_time=0.6)
        def interval(vals, y, label, col):
            m, lo, hi = vals
            ln = Line(axp.c2p(lo, y), axp.c2p(hi, y), color=col, stroke_width=5); dot = Dot(axp.c2p(m, y), color=col, radius=0.1)
            lab = T(f"{label}:  {m:+d}  [{lo}, {hi}]", SZ_TINY, col).next_to(ln, UP, buff=0.12)
            return VGroup(ln, dot, lab)
        iA = interval(pA, 1.4, "value rule − tabular Q", C_SP); iB = interval(pB, 0.6, "value rule − textbook Q", C_BIAS)
        n.until("p07", "twelve")
        self.play(FadeIn(iA), run_time=0.7)
        n.until("p07", "Superiority")
        sup = T("reaches its level; superiority not shown", SZ_SMALL, FG).move_to([0, -1.3, 0])
        self.play(FadeIn(sup), run_time=0.5)
        n.until("p07", "textbook")
        self.play(FadeIn(iB), run_time=0.7)
        n.until("p07", "five")
        preds = VGroup(*[T(s, SZ_TINY, c) for s, c in [("P1  failed", C_BAD), ("P2  failed", C_BAD), ("P3  held", C_GOOD), ("P4  not supported", DIM), ("P5  held", C_GOOD)]]).arrange(RIGHT, buff=0.6).move_to([0, -2.3, 0])
        note("P1-P5 verdicts", P("findings", "02_exp02_decomposition.md"), "Predictions, scored", "P1 failed, P2 failed, P3 held, P4 not supported, P5 held")
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.15) for p in preds], lag_ratio=0.2), run_time=1.2)
        n.end()
        self.play(FadeOut(VGroup(hh, axp, zero, zl, iA, iB, sup, preds)), run_time=0.5)

        # ---------------- p08: the weights night by night
        d = n.say("p08")
        W = nightly_w(); vmax = float(np.abs(W).max()); note("nightly w heat map", RUN_JSON, "brain[0..14].w", f"15 nights, |w|max {vmax:.3f}")
        hm = Heatmap(W[0], cell=0.3, vmax=vmax, col_labels=L["input_names"]).scale(0.95).move_to([-3.6, 0.3, 0])
        night = ValueTracker(0)
        nlab = T("after night 0", SZ_SMALL, C_SP).next_to(hm, UP, buff=0.9)
        hh = header("Seed 203: the weights, one picture per night", SZ_SMALL)
        self.play(FadeIn(hh), FadeIn(hm), FadeIn(nlab), run_time=0.6)
        # steering lines per day: w[LEFT,k] - w[RIGHT,k] day means for the three contrasts
        tw = L["theta_w"]; day = np.arange(tw.shape[0]) // 300
        pairs = {k: np.array([(tw[day == dd, 0, k] - tw[day == dd, 1, k]).mean() for dd in range(15)]) for k in range(3)}
        note("steering pairs per day", LIFE_NPZ, "theta_w[:,0,k]-theta_w[:,1,k] day means, k=contrast A/B/C", {k: np.round(v, 4).tolist() for k, v in pairs.items()})
        axs = Axes(x_range=[0, 14, 2], y_range=[-0.035, 0.035, 0.01], x_length=5.6, y_length=3.2,
                   axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([3.4, 0.2, 0])
        zl2 = DashedLine(axs.c2p(0, 0), axs.c2p(14, 0), color=DIM, dash_length=0.1)
        xl2 = T("day", SZ_TINY, DIM).next_to(axs.x_axis, DOWN, buff=0.1)
        yl2 = T("LEFT − RIGHT knob, per contrast", SZ_TINY, DIM).next_to(axs, UP, buff=0.1)
        self.play(FadeIn(axs), FadeIn(zl2), FadeIn(xl2), FadeIn(yl2), run_time=0.5)
        colors = {0: C_A, 1: C_B, 2: C_C}; names = {0: "A", 1: "B", 2: "C"}
        lines = {}; legend = VGroup()
        for k in range(3):
            lines[k] = VMobject(stroke_color=colors[k], stroke_width=4)
            legend.add(T(names[k], SZ_TINY, colors[k]))
        legend.arrange(RIGHT, buff=0.4).next_to(axs, DOWN, buff=0.45)
        def set_night(nn):
            nn = int(np.clip(nn, 0, 14)); hm.set_values(W[nn], vmax)
            nlab.become(T(f"after night {nn}", SZ_SMALL, C_SP).move_to(nlab))
            for k in range(3):
                pts = [axs.c2p(dd, pairs[k][dd]) for dd in range(nn + 1)]
                if len(pts) >= 2: lines[k].set_points_as_corners(pts)
                else: lines[k].set_points_as_corners([pts[0], pts[0]])
        self.add(*lines.values(), legend)
        # animate nights across the first part of the paragraph (until "B pair" is named)
        t_B = n.t_word("p08", "pair")
        self.play(UpdateFromFunc(hm, lambda m: set_night(night.get_value())), night.animate.set_value(14),
                  run_time=max(t_B - self.time - 0.3, 4), rate_func=linear)
        set_night(14)
        n.until("p08", "pair")
        self.play(Indicate(lines[1], color=C_B, scale_factor=1.05), run_time=0.8)
        n.until("p08", "A pair")
        self.play(Indicate(lines[0], color=C_A, scale_factor=1.05), run_time=0.8)
        n.until("p08", "C pair")
        self.play(Indicate(lines[2], color=C_C, scale_factor=1.05), run_time=0.8)
        n.until("p08", "twenty-four")
        mass = T("food mass 24  vs  poison mass 8", SZ_TINY, FOOD).to_edge(DOWN, buff=0.3)
        note("food vs poison mass", P("creature", "world.py"), "WorldConfig food_budget 24; n_poison 4 × poison_mass 2.0", "24 vs 8")
        self.play(FadeIn(mass), run_time=0.5)
        n.until("p08", "file")
        wf = T("world.py:  “B carries no information”   →   research/07 §2.2: wrong for the gradient", SZ_TINY, DIM).to_edge(DOWN, buff=0.3)
        self.play(FadeOut(mass), FadeIn(wf), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(hh, hm, nlab, axs, zl2, xl2, yl2, legend, wf, *lines.values())), run_time=0.5)

        # ---------------- p09: frozen / mirrored / birth
        d = n.say("p09")
        FZ = frozen(); arms = FZ["arms"]
        for k, v in arms.items(): note(f"frozen test {k}", FROZEN, f"arms.{k}", f"mean {v['mean']:.0f}, {v['at_ceiling']}/{len(v['ticks_alive'])} at ceiling")
        hh = header("Is it learned?  15 fresh seeds (500–514)", SZ_SMALL)
        self.play(FadeIn(hh), run_time=0.4)
        base = Line(LEFT * 5, RIGHT * 5, color=DIM, stroke_width=2).move_to([0, -2.2, 0])
        self.play(FadeIn(base), run_time=0.3)
        def fbar(k, key, lab, col):
            v = arms[key]; xk = -4.0 + k * 4.0; h = 3.4 * v["mean"] / 5500
            r = Rectangle(width=2.0, height=h, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to([xk, -2.2, 0], aligned_edge=DOWN)
            t = T(lab, SZ_TINY, col).move_to([xk, -2.5, 0])
            if t.width > 3.6: t.scale_to_fit_width(3.6)
            vv = T(f"{v['mean']:.0f}   {v['at_ceiling']}/{len(v['ticks_alive'])} at ceiling", SZ_TINY, col).next_to(r, UP, buff=0.1)
            return VGroup(r, t, vv)
        f1 = fbar(0, "frozen", "day-5 brain, frozen", C_SP); f2 = fbar(1, "frozen-mirrored", "same brain, mirrored antennae", C_BAD); f3 = fbar(2, "birth-brain", "the birth brain", DIM)
        n.until("p09", "survives")
        self.play(GrowFromEdge(f1[0], DOWN), FadeIn(f1[1]), FadeIn(f1[2]), run_time=0.8)
        n.until("p09", "Pause")
        pause_card(self, "Freeze the day-5 brain.\nSwap its antennae, left for right.\nWhat happens?", hold=max(n.t_word("p09", "dies") - self.time - 1.3, 1.0))
        n.until("p09", "dies")
        self.play(GrowFromEdge(f2[0], DOWN), FadeIn(f2[1]), FadeIn(f2[2]), run_time=0.8)
        n.until("p09", "born")
        self.play(GrowFromEdge(f3[0], DOWN), FadeIn(f3[1]), FadeIn(f3[2]), run_time=0.8)
        n.until("p09", "proof")
        self.play(Indicate(f2, color=C_BAD, scale_factor=1.04), run_time=0.8)
        n.end()
        self.play(FadeOut(VGroup(hh, base, f1, f2, f3)), run_time=0.5)

        # ---------------- p10: what it does on day 10
        d = n.say("p10")
        tick = ValueTracker(3000)
        wv = WorldView(size=5.4, trail=300).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        wv.set_tick(3000)
        hh = header("Day 10 of seed 203", SZ_SMALL)
        self.play(FadeIn(hh), FadeIn(wv), run_time=0.6)
        wv.add_updater(lambda m: m.set_tick(int(tick.get_value())))
        note("day-10 trajectory", LIFE_NPZ, "y, xpos, fields indices 3000-3300", "waking index = day 10")
        a = L["a"]; shares = {dd: np.bincount(a[day == dd], minlength=3) / 300 for dd in (0, 10)}
        note("action shares", LIFE_NPZ, "bincount(a) day 0 and day 10 / 300", {k: np.round(v, 2).tolist() for k, v in shares.items()})
        ca = L["x"][:, 0]; ratio = []
        for dd in range(15):
            m = day == dd; strong = np.abs(ca[m]) > 0.3; act = a[m]
            tw_ = (((ca[m] > 0.3) & (act == 0)) | ((ca[m] < -0.3) & (act == 1))).sum(); tu = ((act != 2) & strong).sum()
            ratio.append(tw_ / max(tu, 1))
        note("turn-toward-A ratio per day", LIFE_NPZ, "turns with |contrast_A|>0.3 toward the higher-A side / all such turns", np.round(ratio, 2).tolist())
        self.play(tick.animate.set_value(3120), run_time=max(n.t_word("p10", "half") - self.time - 0.2, 2), rate_func=linear)
        # stacked shares
        def stack(dd, x0, lab):
            g = VGroup(); y = 0
            for k in range(3):
                h = 2.6 * shares[dd][k]
                g.add(Rectangle(width=0.9, height=h, fill_color=MOVE[k], fill_opacity=0.9, stroke_width=0).move_to([x0, y, 0], aligned_edge=DOWN)); y += h
            g.add(T(lab, SZ_TINY).move_to([x0, -0.3, 0]))
            return g.shift(DOWN * 0.9)
        sA = stack(0, 1.6, "day 0"); sB = stack(10, 3.0, "day 10")
        leg = VGroup(*[T(MOVE_NAME[k], 14, MOVE[k]) for k in range(3)]).arrange(DOWN, buff=0.1).next_to(sB, RIGHT, buff=0.3)
        fwd = T(f"forward {shares[0][2]*100:.0f}% → {shares[10][2]*100:.0f}%", SZ_TINY, C_B).next_to(VGroup(sA, sB), UP, buff=0.2)
        n.until("p10", "half")
        self.play(FadeIn(sA), FadeIn(sB), FadeIn(leg), FadeIn(fwd), tick.animate.set_value(3180), run_time=1.2, rate_func=linear)
        n.until("p10", "four")
        self.play(FadeOut(VGroup(sA, sB, leg, fwd)), run_time=0.3)
        axr = Axes(x_range=[0, 14, 2], y_range=[0, 1, 0.25], x_length=5.0, y_length=2.4,
                   axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([3.4, 0.4, 0])
        rl = T("turns toward the higher-A side", SZ_TINY, DIM).next_to(axr, UP, buff=0.1)
        half = DashedLine(axr.c2p(0, 0.5), axr.c2p(14, 0.5), color=DIM, dash_length=0.1)
        lg = axr.plot_line_graph(list(range(15)), ratio, add_vertex_dots=True, vertex_dot_radius=0.05, line_color=C_A, stroke_width=3)
        xl3 = T("day", SZ_TINY, DIM).next_to(axr.x_axis, DOWN, buff=0.1)
        self.play(FadeIn(axr), FadeIn(rl), FadeIn(half), FadeIn(xl3), Create(lg), tick.animate.set_value(3230), run_time=1.5, rate_func=linear)
        n.until("p10", "coin")
        ct = T("day 1: coin toss", SZ_TINY, C_BAD).next_to(axr.c2p(1, ratio[1]), DOWN, buff=0.25).shift(RIGHT * 0.6)
        self.play(FadeIn(ct), tick.animate.set_value(3260), run_time=0.8, rate_func=linear)
        n.until("p10", "noisy")
        self.play(tick.animate.set_value(3299), run_time=max(n.remaining() - 0.2, 1.0), rate_func=linear)
        n.end()
        wv.clear_updaters()
        self.play(FadeOut(Group(hh, wv, axr, rl, half, lg, xl3, ct)), run_time=0.5)

        # ---------------- p11 + p12: limits
        d = n.say("p11")
        hh = header("What the referees would not let us say", SZ_SMALL)
        self.play(FadeIn(hh), run_time=0.4)
        note("poison rate vs random", P("findings", "02_exp02_decomposition.md"), "Limits 3", "ebm-td −0.011, p 0.84")
        note("v=0 frozen brains", P("findings", "02_exp02_decomposition.md"), "Limits 2", "5250 on 15/15")
        c1 = card(["1   no poison avoidance", "ebm-td poison rate vs random: −0.011, p = 0.84", "survivors simply eat more food"], C_BAD, width=6.2)
        c2 = card(["2   the committee did not carry the win", "frozen brains with v = 0 still reach 5250 on 15/15", "the twelve linear knobs did it"], C_HID, width=6.2)
        VGroup(c1, c2).arrange(RIGHT, buff=0.4).move_to([0, 0, 0])
        n.until("p11", "One")
        self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.6)
        n.until("p11", "Two")
        self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.6)
        n.end()
        d = n.say("p12")
        self.play(FadeOut(c1), FadeOut(c2), run_time=0.4)
        note("ebm-all at alpha 0.1", P("findings", "02_exp02_decomposition.md"), "Limits 1", "4806 on fresh seeds")
        c3 = card(["3   ebm-all: a step-size casualty", "15 inputs, same step: blew up on night 0", "at step 0.1 on fresh seeds: 4806"], C_X, width=6.2)
        c4 = card(["4   the ceiling", f"{cens['ebm-td']}/20 and {cens['tabular_q']}/20 lives at 5250", "means understate the differences"], DIM, width=6.2)
        c5 = card(["5   all or nothing", "ebm-td reaches the ceiling or starves", "its 5 failures ate ≤ 1 food"], C_BAD, width=6.2)
        VGroup(c3, c4).arrange(RIGHT, buff=0.4).move_to([0, 1.0, 0]); c5.move_to([0, -1.7, 0])
        n.until("p12", "Three")
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=0.6)
        n.until("p12", "Four")
        self.play(FadeIn(c4, shift=UP * 0.2), run_time=0.6)
        n.until("p12", "Five")
        self.play(FadeIn(c5, shift=UP * 0.2), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(hh, c3, c4, c5)), run_time=0.5)

        # ---------------- p13: the pivot
        d = n.say("p13")
        hh = header("The pivot: a creature made of brain-like cells", SZ_SMALL)
        self.play(FadeIn(hh), run_time=0.4)
        note("pivot verdicts", P("decisions", "0002_goal_pivot.md"), "Verdict on EXP-02 under the new goals", "learn yes; function yes; connect unused; born placeholder; die missing")
        items = [("learn", "yes:  the frozen test", C_GOOD), ("function", "yes:  three moves from smells", C_GOOD),
                 ("connect", "present, unused:  needs the xor world (A and B together is food; either alone is poison)", C_SP), ("born", "placeholder:  v = 0 units on eventful days", DIM), ("die", "missing", C_BAD)]
        rows_ = VGroup()
        for w, v, col in items:
            rows_.add(VGroup(T(w, SZ_BIG, col), T(v, SZ_SMALL)).arrange(RIGHT, buff=0.6, aligned_edge=DOWN))
        rows_.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, -0.3, 0])
        if rows_.width > 13: rows_.scale_to_fit_width(13)
        for rw, word in zip(rows_, ["learn,", "Function", "Connect", "Born", "Die"]):
            n.until("p13", word.strip(","))
            self.play(FadeIn(rw, shift=RIGHT * 0.2), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(hh, rows_)), run_time=0.5)

        # ---------------- p14: the loop, complete
        d = n.say("p14")
        loop = LoopDiagram(radius=2.6).set_done(LOOP_NODES).move_to([0, 0.6, 0])
        self.play(FadeIn(loop), run_time=0.6)
        for word, node in [("smells", "World"), ("numbers", "Senses"), ("highest", "Brain"), ("move", "Move"), ("bowl", "Body"), ("drop", "Lesson"), ("knobs", "Learning")]:
            n.until("p14", word)
            self.play(Indicate(loop.boxes[node], color=C_SP, scale_factor=1.08), run_time=0.5)
        n.until("p14", "Stripped")
        line = T("the body's number, through the promise, found the sign of three contrast knobs in five days", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.5)
        if line.width > 13.4: line.scale_to_fit_width(13.4)
        self.play(FadeIn(line), run_time=0.6)
        n.finish(tail=1.2)
