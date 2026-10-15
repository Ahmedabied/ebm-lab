"""Chapter 04 — The body is the only teacher."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

I14, I192, I1231 = 14, 192, 1081          # waking indices: tick 14, tick 192, tick 1231 (day 3)


def two_curves(width=6.4, height=3.2, x_range=(0, 1.05, 0.2), y_range=(0, 1.05, 0.25)):
    ax = Axes(x_range=list(x_range), y_range=list(y_range), x_length=width, y_length=height,
              axis_config={"color": DIM, "include_numbers": False, "stroke_width": 2})
    lin = ax.plot(lambda e: abs(1 - e), x_range=[x_range[0], 1], color=DIM, stroke_width=3)
    sq = ax.plot(lambda e: (1 - e) ** 2, x_range=[x_range[0], 1], color=C_D, stroke_width=4)
    return ax, lin, sq


class BowlTop(VGroup):
    """The bowl seen from above: contours of D = (1-E)^2 + X^2 are circles centred at (1, 0)."""
    def __init__(self, width=5.2, height=3.4, **kw):
        super().__init__(**kw)
        self.ax = Axes(x_range=[0.4, 1.02, 0.2], y_range=[0, 0.42, 0.1], x_length=width, y_length=height,
                       axis_config={"color": DIM, "include_numbers": False, "stroke_width": 2})
        self.xl = T("E  energy", SZ_TINY, C_E).next_to(self.ax.x_axis, DOWN, buff=0.1)
        self.yl = T("X  toxin", SZ_TINY, C_XT).next_to(self.ax.y_axis, UP, buff=0.1)
        self.rings = VGroup()
        for d in (0.01, 0.04, 0.09, 0.16, 0.25, 0.36):
            r = np.sqrt(d)
            pts = [self.ax.c2p(1 - r * np.cos(a), r * np.sin(a)) for a in np.linspace(0, np.pi / 2, 40)]
            ring = VMobject(stroke_color=GRID, stroke_width=2).set_points_smoothly(pts)
            lab = T(f"{d:.2f}", 17, DIM).move_to(self.ax.c2p(1 - r * np.cos(0.7), r * np.sin(0.7) + 0.012))
            self.rings.add(ring, lab)
        self.bottom = Dot(self.ax.c2p(1, 0), radius=0.05, color=FG)
        self.ball = Dot(radius=0.11, color=C_E)
        self.add(self.ax, self.xl, self.yl, self.rings, self.bottom, self.ball); self.set_state(0.8, 0.0)

    def set_state(self, E, X):
        self.ball.move_to(self.ax.c2p(E, X)); return self


class Ch04(Scene):
    def construct(self):
        n = Narration(self, "04"); L = life()
        E, X, Dv, R = L["E"], L["X"], L["D"], L["r"]
        legend = None

        # ---------------- p01: the body box, the bowl, the formula ----------------
        d = n.say("p01")
        loop = LoopDiagram(radius=2.6).set_done(["World", "Senses"]).move_to(ORIGIN)
        self.play(FadeIn(loop), run_time=0.6)
        self.play(loop.lit("Body"), run_time=0.6)
        self.play(loop.animate.scale(0.32).to_corner(UR, buff=0.25), run_time=0.8)
        bowl = Bowl(width=6.4, height=3.2).shift(LEFT * 3.2 + DOWN * 0.6)
        bb = BodyBars(width=2.0).move_to([3.6, 0.9, 0]); bb.set_state(0.8, 0.0, 0.04)
        n.until("p01", "energy")
        self.play(FadeIn(bowl), FadeIn(bb), run_time=0.8)
        formula = MathTex(r"D", r"=", r"(1-E)^2", r"+", r"X^2").scale(1.2).move_to([3.6, -1.6, 0])
        formula[0].set_color(C_D); formula[2].set_color(C_E); formula[4].set_color(C_XT)
        n.until("p01", "formula")
        self.play(FadeIn(formula[0]), FadeIn(formula[1]), run_time=0.4)
        n.until("p01", "squared"); self.play(Write(formula[2]), run_time=0.7)
        n.until("p01", "plus"); self.play(Write(formula[3]), Write(formula[4]), run_time=0.7)
        note("drive formula", P("creature", "body.py"), "Body.drive (w 1, setpoints 1/0, n 2)", "D = (1-E)^2 + X^2")
        n.end()

        # ---------------- p02: why square (E slider on two curves) ----------------
        d = n.say("p02")
        self.play(FadeOut(bowl), FadeOut(bb), formula.animate.scale(0.7).to_edge(UP, buff=0.35).shift(LEFT * 3.5), run_time=0.7)
        ax, lin, sq = two_curves(width=6.6, height=3.4)
        g = VGroup(ax, lin, sq).move_to([-2.6, -0.6, 0])
        xl = T("E  energy", SZ_TINY, C_E).next_to(ax.x_axis, DOWN, buff=0.1)
        lab_lin = VGroup(Line(ORIGIN, RIGHT * 0.5, color=DIM, stroke_width=3), T("plain distance  |1 − E|", SZ_TINY, DIM)).arrange(RIGHT, buff=0.15)
        lab_sq = VGroup(Line(ORIGIN, RIGHT * 0.5, color=C_D, stroke_width=4), T("square  (1 − E)²", SZ_TINY, C_D)).arrange(RIGHT, buff=0.15)
        VGroup(lab_lin, lab_sq).arrange(RIGHT, buff=0.6).next_to(xl, DOWN, buff=0.25)
        self.play(Create(ax), FadeIn(xl), run_time=0.6)
        self.play(Create(lin), FadeIn(lab_lin), Create(sq), FadeIn(lab_sq), run_time=1.0)
        e = ValueTracker(0.9)
        dot_l = Dot(color=DIM, radius=0.08); dot_s = Dot(color=C_D, radius=0.09)
        dot_l.add_updater(lambda m: m.move_to(ax.c2p(e.get_value(), abs(1 - e.get_value()))))
        dot_s.add_updater(lambda m: m.move_to(ax.c2p(e.get_value(), (1 - e.get_value()) ** 2)))
        panel = VGroup(T("E = 0.90", SZ_BODY, C_E), T("|1 − E| = 0.10", SZ_BODY, DIM), T("(1 − E)² = 0.01", SZ_BODY, C_D)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.7, 0.2, 0])
        self.add(dot_l, dot_s); self.play(FadeIn(panel), run_time=0.4)
        def upd_panel(m):
            ev = e.get_value()
            m[0].become(T(f"E = {ev:.2f}", SZ_BODY, C_E).move_to(m[0], aligned_edge=LEFT))
            m[1].become(T(f"|1 − E| = {abs(1-ev):.2f}", SZ_BODY, DIM).move_to(m[1], aligned_edge=LEFT))
            m[2].become(T(f"(1 − E)² = {(1-ev)**2:.2f}", SZ_BODY, C_D).move_to(m[2], aligned_edge=LEFT))
        panel.add_updater(upd_panel)
        n.until("p02", "slides")
        self.play(e.animate.set_value(0.6), run_time=max(n.t_word("p02", "sixteen") - self.time - 0.5, 3.0), rate_func=linear)
        panel.clear_updaters()
        n.until("p02", "car")
        car = T("twice the speed, four times the stopping distance", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(car), run_time=0.5)
        n.end()

        # ---------------- p03: abs first; flat bottom ----------------
        d = n.say("p03")
        self.play(FadeOut(car), FadeOut(panel), run_time=0.4)
        self.play(e.animate.set_value(0.97), run_time=1.5)
        absnote = T("the code takes |1 − E| first, then squares it", SZ_SMALL, FG).move_to([3.7, 0.9, 0])
        if absnote.width > 6: absnote.scale_to_fit_width(6)
        n.until("p03", "absolute"); self.play(FadeIn(absnote), run_time=0.5)
        n.until("p03", "bottom")
        flat = T("flat at the bottom", SZ_SMALL, C_D).next_to(ax.c2p(0.97, 0.02), UP, buff=0.5).shift(LEFT * 0.8)
        steep = T("steep up the wall", SZ_SMALL, C_D).next_to(ax.c2p(0.25, 0.56), UP, buff=0.15).shift(RIGHT * 0.9)
        self.play(FadeIn(flat), run_time=0.4)
        self.play(e.animate.set_value(0.99), run_time=0.8); self.play(e.animate.set_value(0.95), run_time=0.8)
        n.until("p03", "steep"); self.play(FadeIn(steep), e.animate.set_value(0.3), run_time=1.2)
        n.end()

        # ---------------- p04: why a sum: two walls ----------------
        d = n.say("p04")
        dot_l.clear_updaters(); dot_s.clear_updaters()
        self.play(FadeOut(VGroup(g, xl, lab_lin, lab_sq, dot_l, dot_s, absnote, flat, steep)), run_time=0.5)
        top = BowlTop(width=6.0, height=3.6).move_to([-2.4, -0.5, 0])
        self.play(FadeIn(top), run_time=0.8)
        wall1 = T("the hunger wall: (1 − E)²", SZ_SMALL, C_E).move_to([3.7, 0.9, 0])
        wall2 = T("the poison wall: X²", SZ_SMALL, C_XT).next_to(wall1, DOWN, buff=0.4, aligned_edge=LEFT)
        both = T("hungry and poisoned: the sum", SZ_SMALL, C_D).next_to(wall2, DOWN, buff=0.4, aligned_edge=LEFT)
        dlab = T("D = 0.04", SZ_BODY, C_D).next_to(both, DOWN, buff=0.6)
        self.add(dlab)
        def set_top(Ev, Xv):
            top.set_state(Ev, Xv); dlab.become(T(f"D = {(1-Ev)**2 + Xv**2:.3f}", SZ_BODY, C_D).move_to(dlab))
        n.until("p04", "Hungry")
        self.play(FadeIn(wall1), run_time=0.3)
        for Ev in np.linspace(0.8, 0.5, 12): set_top(Ev, 0.0); self.wait(0.07)
        n.until("p04", "poisoned")
        self.play(FadeIn(wall2), run_time=0.3)
        for k, Xv in enumerate(np.linspace(0.0, 0.3, 12)): set_top(0.5, Xv); self.wait(0.07)
        n.until("p04", "sum")
        self.play(FadeIn(both), run_time=0.3)
        for k in range(12): set_top(0.5 + 0.3 * k / 11, 0.3 - 0.3 * k / 11); self.wait(0.06)
        set_top(0.8, 0.0)
        n.end()

        # ---------------- p05: pause and predict: which bite teaches more ----------------
        d = n.say("p05")
        self.play(FadeOut(VGroup(top, wall1, wall2, both, dlab)), run_time=0.4)
        pause_card(self, "One bite of 0.05 at energy 0.78,\nor the same bite at energy 0.95.\nWhich teaches more?", hold=max(n.t_word("p05", "first") - self.time - 1.2, 2.0))
        bowl2 = Bowl(width=7.0, height=3.4).move_to([-2.3, -0.5, 0])
        self.play(FadeIn(bowl2), run_time=0.5)
        ballA = Dot(bowl2.ax.c2p(0.78, 0.22 ** 2), radius=0.11, color=C_E); ballB = Dot(bowl2.ax.c2p(0.95, 0.05 ** 2), radius=0.11, color=C_SP)
        bowl2.ball.set_opacity(0)
        self.play(FadeIn(ballA), FadeIn(ballB), run_time=0.4)
        resA = VGroup(T("from E = 0.78", SZ_SMALL, C_E), T("0.0484 → 0.0289", SZ_SMALL, FG), T("drop 0.0195", SZ_BODY, C_GOOD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.9, 1.2, 0])
        resB = VGroup(T("from E = 0.95", SZ_SMALL, C_SP), T("0.0025 → 0.0000", SZ_SMALL, FG), T("drop 0.0025", SZ_BODY, DIM)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.9, -1.3, 0])
        n.until("p05", "first")
        self.play(ballA.animate.move_to(bowl2.ax.c2p(0.83, 0.17 ** 2)), ballB.animate.move_to(bowl2.ax.c2p(1.0, 0.0)), run_time=1.2)
        self.play(FadeIn(resA), run_time=0.4)
        n.until("p05", "against"); self.play(FadeIn(resB), run_time=0.4)
        n.until("p05", "steep")
        self.play(Indicate(bowl2.curve, color=C_SP, scale_factor=1.02), run_time=1.0)
        n.end()

        # ---------------- p06: the real tick 14 ----------------
        d = n.say("p06")
        self.play(FadeOut(VGroup(ballA, ballB, resA, resB)), run_time=0.4)
        bowl2.ball.set_opacity(1); bowl2.set_state(float(E[I14 - 1]), float(X[I14 - 1]))
        bb2 = BodyBars(width=1.9).move_to([3.9, 1.6, 0]); bb2.set_state(float(E[I14 - 1]), float(X[I14 - 1]), float(Dv[I14 - 1]))
        self.play(FadeIn(bb2), run_time=0.4)
        hdr = T("seed 203, tick 14: the first bite", SZ_SMALL, FOOD).to_edge(UP, buff=0.4).shift(RIGHT * 2.2)
        self.play(FadeOut(formula), run_time=0.3)
        self.play(FadeIn(hdr), run_time=0.3)
        note("tick 14 D before", LIFE_NPZ, "D[13]", f"{Dv[I14-1]:.5f}"); note("tick 14 D after", LIFE_NPZ, "D[14]", f"{Dv[I14]:.5f}"); note("tick 14 r", LIFE_NPZ, "r[14]", f"{R[I14]:.5f}")
        n.until("p06", "fourteen")
        l1 = T(f"D before   {Dv[I14-1]:.5f}", SZ_BODY, C_D).move_to([3.9, -0.3, 0])
        self.play(FadeIn(l1), run_time=0.3)
        n.until("p06", "Energy")
        self.play(bowl2.ball.animate.move_to(bowl2.ax.c2p(float(E[I14]), float(Dv[I14]))), run_time=1.0)
        bb2.set_state(float(E[I14]), float(X[I14]), float(Dv[I14]))
        l2 = T(f"D after     {Dv[I14]:.5f}", SZ_BODY, C_D).next_to(l1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(l2), run_time=0.3)
        n.until("p06", "lesson")
        Db, Da = round(float(Dv[I14-1]), 5), round(float(Dv[I14]), 5)
        l3 = T(f"r  =  {Db:.5f} − {Da:.5f}  =  +{Db-Da:.5f}", SZ_SMALL, C_GOOD).next_to(l2, DOWN, buff=0.35)
        l3.shift(RIGHT * (3.9 - l3.get_center()[0]))
        if l3.get_right()[0] > 6.9: l3.shift(LEFT * (l3.get_right()[0] - 6.9))
        cap = T(f"(the file keeps r = {R[I14]:+.5f}, from unrounded values)", SZ_TINY, DIM).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(l3), run_time=0.4); self.play(FadeIn(cap), run_time=0.3)
        n.until("p06", "positive", occurrence=1)
        self.play(Indicate(l3, color=C_GOOD, scale_factor=1.05), run_time=0.8)
        n.end()

        # ---------------- p07: metabolism ----------------
        d = n.say("p07")
        self.play(FadeOut(VGroup(l1, l2, l3, cap, hdr, bb2, bowl2)), run_time=0.4)
        cost = MathTex(r"0.0005", r"+", r"0.001", r"+", r"4 \times 0.0000125", r"=", r"0.00155").scale(1.05).to_edge(UP, buff=0.7).shift(LEFT * 1.0)
        cl = VGroup(T("resting", SZ_TINY, DIM), T("moving", SZ_TINY, DIM), T("4 units of brain", SZ_TINY, DIM), T("per tick", SZ_TINY, C_E))
        for k, (piece, lab) in enumerate(zip((cost[0], cost[2], cost[4], cost[6]), cl)): lab.next_to(piece, DOWN, buff=0.15)
        note("metabolic cost", P("creature", "body.py"), "BodyConfig.metabolic, move_cost, unit_cost", "0.0005 + 0.001 + 4 x 1.25e-5")
        n.until("p07", "Resting"); self.play(FadeIn(cost[0]), FadeIn(cl[0]), run_time=0.4)
        n.until("p07", "Moving"); self.play(FadeIn(cost[1]), FadeIn(cost[2]), FadeIn(cl[1]), run_time=0.4)
        n.until("p07", "unit"); self.play(FadeIn(cost[3]), FadeIn(cost[4]), FadeIn(cl[2]), run_time=0.4)
        n.until("p07", "Together"); self.play(FadeIn(cost[5]), FadeIn(cost[6]), FadeIn(cl[3]), run_time=0.4)
        # the ball creeping up, and the strip of real quiet ticks
        bowl3 = Bowl(width=5.2, height=2.6).move_to([-3.3, -1.5, 0]); bowl3.set_state(0.8, 0)
        quiet = np.where((L["food"] == 0) & (L["poison"] == 0))[0][:50]
        note("quiet-tick lessons", LIFE_NPZ, "r on the first 50 ticks without a bite", f"mean {R[quiet].mean():+.5f}")
        strip = VGroup()
        for k, i in enumerate(quiet):
            h = min(abs(float(R[i])) * 900, 1.2)
            bar = Rectangle(width=0.09, height=max(h, 0.02), fill_color=C_BAD if R[i] < 0 else C_GOOD, fill_opacity=0.9, stroke_width=0)
            bar.move_to([1.2 + k * 0.11, -0.9, 0], aligned_edge=UP if R[i] < 0 else DOWN); strip.add(bar)
        base = Line([1.1, -0.9, 0], [1.2 + 50 * 0.11, -0.9, 0], color=DIM, stroke_width=2)
        slab = T("50 quiet ticks, real r", SZ_TINY, DIM).next_to(base, UP, buff=0.15).shift(RIGHT * 0.3)
        rlab = T(f"each one about r = {R[quiet].mean():+.4f}", SZ_SMALL, C_BAD).next_to(base, DOWN, buff=0.85)
        n.until("p07", "pushes")
        self.play(FadeIn(bowl3), run_time=0.4)
        Ev = 0.8
        for k in range(12):
            Ev -= 0.00155 * 8; bowl3.set_state(Ev, 0); self.wait(0.08)
        n.until("p07", "negative")
        self.play(FadeIn(base), FadeIn(slab), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(b) for b in strip], lag_ratio=0.04), run_time=1.5)
        self.play(FadeIn(rlab), run_time=0.3)
        n.until("p07", "Ninety")
        pct = T(f"{np.mean(R < 0) * 100:.0f}% of waking ticks: r < 0", SZ_BODY, C_BAD).to_edge(DOWN, buff=0.4)
        note("fraction of negative lessons", LIFE_NPZ, "mean(r < 0)", f"{np.mean(R < 0):.4f}")
        self.play(FadeIn(pct), run_time=0.4)
        n.end()

        # ---------------- p08: poison ----------------
        d = n.say("p08")
        self.play(FadeOut(VGroup(cost, cl, bowl3, strip, base, slab, rlab, pct)), run_time=0.4)
        top2 = BowlTop(width=6.0, height=3.6).move_to([-2.4, -0.3, 0]); top2.set_state(float(E[I192 - 1]), float(X[I192 - 1]))
        bb3 = BodyBars(width=1.9).move_to([3.9, 1.5, 0]); bb3.set_state(float(E[I192 - 1]), float(X[I192 - 1]), float(Dv[I192 - 1]), xmax=0.1)
        hdr = T("seed 203, tick 192: the first poison bite", SZ_SMALL, POISON).to_edge(UP, buff=0.4).shift(LEFT * 1.0)
        self.play(FadeIn(top2), FadeIn(bb3), FadeIn(hdr), run_time=0.5)
        note("tick 192 X", LIFE_NPZ, "X[192]", f"{X[I192]:.4f}"); note("tick 192 r", LIFE_NPZ, "r[192]", f"{R[I192]:.5f}")
        n.until("p08", "adds")
        xj = MathTex(r"X \mathrel{+}= 0.5 \times 0.05 = 0.025").scale(0.9).set_color(C_XT).move_to([3.9, -0.4, 0])
        self.play(top2.ball.animate.move_to(top2.ax.c2p(float(E[I192]), float(X[I192]))), FadeIn(xj), run_time=0.8)
        bb3.set_state(float(E[I192]), float(X[I192]), float(Dv[I192]), xmax=0.1)
        n.until("p08", "negative")
        rl = T(f"r = {R[I192]:+.5f}", SZ_BODY, C_BAD).next_to(xj, DOWN, buff=0.4)
        self.play(FadeIn(rl), run_time=0.4)
        n.until("p08", "fades")
        fade = T("X × 0.98 each tick;  E − 0.01 × X each tick", SZ_TINY, DIM).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(fade), run_time=0.3)
        t_end = n.t_word("p08", "survivable") - 0.3
        idxs = list(range(I192 + 1, I192 + 90, 2)); per = max((t_end - self.time) / len(idxs), 0.03)
        for i in idxs:
            top2.set_state(float(E[i]), float(X[i])); bb3.set_state(float(E[i]), float(X[i]), float(Dv[i]), xmax=0.1); self.wait(per)
        n.end()

        # ---------------- p09: death and the cap ----------------
        d = n.say("p09")
        self.play(FadeOut(VGroup(top2, xj, rl, fade, hdr)), run_time=0.4)
        rule = T("alive while  E > 0", SZ_BIG, FG).move_to([-2.8, 1.6, 0])
        self.play(FadeIn(rule), run_time=0.4)
        bb3.clear_updaters()
        creature = Dot(radius=0.25, color=FG).move_to([-2.8, -0.6, 0])
        self.play(FadeIn(creature), run_time=0.3)
        n.until("p09", "zero")
        for Ev in np.linspace(float(E[I192]), 0.0, 20):
            bb3.set_state(Ev, 0.0, (1 - Ev) ** 2); self.wait(0.05)
        self.play(creature.animate.set_color(GRID), run_time=0.5)
        n.until("p09", "capped")
        cap2 = T("E is capped at 1.0", SZ_BIG, C_E).move_to([-2.8, 1.6, 0])
        self.play(Transform(rule, cap2), creature.animate.set_color(FG), run_time=0.5)
        note("tick 1231 E", LIFE_NPZ, "E[1080], E[1081]", f"{E[I1231-1]:.3f}, {E[I1231]:.3f}"); note("tick 1231 r", LIFE_NPZ, "r[1081]", f"{R[I1231]:.5f}")
        n.until("p09", "one")
        bb3.set_state(float(E[I1231 - 1]), float(X[I1231 - 1]), float(Dv[I1231 - 1]), xmax=0.1)
        full = VGroup(T("tick 1231: a bite with a full tank", SZ_SMALL, FOOD), T(f"E  {E[I1231-1]:.3f} → {E[I1231]:.3f}", SZ_BODY, C_E), T(f"r = {R[I1231]:.5f}", SZ_BODY, DIM)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-2.8, -0.9, 0])
        self.play(FadeOut(creature), FadeIn(full), run_time=0.5)
        n.end()

        # ---------------- p10: connections ----------------
        d = n.say("p10")
        self.play(FadeOut(VGroup(rule, full, bb3)), run_time=0.4)
        loop2 = LoopDiagram(radius=2.6).set_done(["World", "Senses", "Body"]).move_to(ORIGIN)
        self.play(FadeOut(loop), FadeIn(loop2), run_time=0.6)
        a1 = T("r, one number, every tick", SZ_TINY, C_GOOD).next_to(loop2.boxes["Lesson"], DOWN, buff=0.2)
        a2 = T("E, X back into the senses", SZ_TINY, C_E).next_to(loop2.boxes["Senses"], RIGHT, buff=0.25)
        n.until("p10", "energy"); self.play(FadeIn(a2), run_time=0.4)
        n.until("p10", "lesson"); self.play(FadeIn(a1), loop2.lit("Lesson", C_GOOD), run_time=0.5)
        n.until("p10", "Stripped")
        strip_line = T("the body is a bowl; the lesson is how far the ball rolled toward the bottom", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.4)
        if strip_line.width > 13.4: strip_line.scale_to_fit_width(13.4)
        self.play(FadeIn(strip_line), run_time=0.5)
        n.finish(tail=1.0)
