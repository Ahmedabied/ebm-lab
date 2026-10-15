"""Chapter 02 — Maths from the beginning. Seven operations, each: need, why this one, example, real numbers."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

IDX = 3193          # waking index of tick 3693 (day 10) in life203.npz
CARDS = ["weighted sum", "exponent", "softmax", "log", "slope", "average", "length"]
SHORT = {"contrast_A": "contrast A", "contrast_B": "contrast B", "contrast_C": "contrast C", "mean_A": "mean A", "mean_B": "mean B",
         "mean_C": "mean C", "change_A": "change A", "change_B": "change B", "change_C": "change C", "body_E": "energy", "body_X": "toxin", "bias": "one"}


def fmt(v, d=5):
    return f"{v:+.{d}f}"


class Ch02(Scene):
    def clear_all(self, *keep, run_time=0.5):
        mobs = [m for m in self.mobjects if m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def construct(self):
        n = Narration(self, "02"); L = life()
        x = L["x"][IDX].astype(float); th = theta_at(IDX); names = L["input_names"]
        Q = L["Q"][IDX].astype(float); wL = th["w"][0]
        note("worked tick", LIFE_NPZ, "t[3193]", int(L["t"][IDX]))
        note("x at tick 3693", LIFE_NPZ, "x[3193]", [round(float(v), 4) for v in x])
        note("w[LEFT] used at tick 3693", LIFE_NPZ, "theta_w[3193][0]", [round(float(v), 5) for v in wL])
        note("Q at tick 3693", LIFE_NPZ, "Q[3193]", [round(float(v), 6) for v in Q])

        # ------------------------------------------------------------------ p01: title + seven cards
        n.say("p01")
        title = T("Maths from the beginning", SZ_TITLE).to_edge(UP, buff=0.8)
        cards = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.12, width=1.75, height=0.9, stroke_color=DIM, stroke_width=2, fill_color=PANEL, fill_opacity=1),
                                T(c, 18)) for c in CARDS]).arrange(RIGHT, buff=0.18).move_to(ORIGIN)
        cap = caption("voice from here: Kokoro (local)  ·  the paid minutes went to chapters 0 and 1", SZ_TINY)
        self.play(Write(title), FadeIn(cap), run_time=1.2)
        n.until("p01", "Seven")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.15), run_time=1.6)
        need = VGroup(T("the need", SZ_SMALL, C_SP), T("why this one", SZ_SMALL, C_SP), T("one example", SZ_SMALL, C_SP), T("the real numbers", SZ_SMALL, C_SP)).arrange(RIGHT, buff=0.7).next_to(cards, DOWN, buff=0.8)
        for w, m in zip(["need", "why", "example", "real"], need):
            n.until("p01", w); self.play(FadeIn(m, shift=UP * 0.1), run_time=0.4)
        n.end()

        # ------------------------------------------------------------------ p02: weighted sum on the real tick
        n.say("p02")
        self.clear_all()
        hdr = T("weighted sum", SZ_BIG).move_to([-4.6, 3.55, 0])
        rows = VGroup()
        for k in range(12):
            r = VGroup(T(SHORT[names[k]], SZ_TINY, DIM), T(f"{x[k]:+.4f}", SZ_TINY, C_X), T("×", SZ_TINY, DIM),
                       T(f"{wL[k]:+.5f}", SZ_TINY, C_W), T("=", SZ_TINY, DIM), T(fmt(wL[k] * x[k]), SZ_TINY, FG))
            rows.add(r)
        # align columns
        colx = [-5.6, -3.4, -2.2, -1.0, 0.5, 1.7]
        for k, r in enumerate(rows):
            y = 2.35 - k * 0.45
            for m, cx in zip(r, colx):
                m.move_to([cx, y, 0], aligned_edge=LEFT)
        heads = VGroup(T("reading", SZ_TINY, C_X).move_to([colx[1], 2.85, 0], aligned_edge=LEFT), T("knob (left)", SZ_TINY, C_W).move_to([colx[3], 2.85, 0], aligned_edge=LEFT),
                       T("product", SZ_TINY, FG).move_to([colx[5], 2.85, 0], aligned_edge=LEFT))
        tick_lab = T("tick 3693, day 10", SZ_TINY, DIM).move_to([-1.2, 3.55, 0])
        self.play(FadeIn(hdr), run_time=0.4)
        n.until("p02", "twelve")
        self.play(FadeIn(heads[0]), LaggedStart(*[FadeIn(VGroup(r[0], r[1])) for r in rows], lag_ratio=0.05), run_time=1.2)
        n.until("p02", "multiply")
        self.play(FadeIn(heads[1]), LaggedStart(*[FadeIn(VGroup(r[2], r[3])) for r in rows], lag_ratio=0.05), run_time=1.2)
        n.until("p02", "add")
        self.play(FadeIn(heads[2]), LaggedStart(*[FadeIn(VGroup(r[4], r[5])) for r in rows], lag_ratio=0.05), run_time=1.2)
        # grocery bill aside, on the right
        bill = VGroup(T("grocery bill", SZ_SMALL, C_SP), T("quantity × price, added up", SZ_TINY), T("readings × knobs, added up", SZ_TINY)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bill.scale_to_fit_width(3.1).move_to([5.35, 2.2, 0])
        n.until("p02", "grocery"); self.play(FadeIn(bill), run_time=0.5)
        n.until("p02", "real"); self.play(FadeIn(tick_lab), run_time=0.4)
        total_line = Line([colx[5] - 0.1, 2.35 - 11 * 0.45 - 0.25, 0], [colx[5] + 1.6, 2.35 - 11 * 0.45 - 0.25, 0], color=DIM)
        total = T(fmt(float((wL * x).sum()), 6), SZ_SMALL, C_SP).next_to(total_line, DOWN, buff=0.1).align_to(rows[0][5], LEFT)
        tot_lab = T("total", SZ_TINY, C_SP).next_to(total, LEFT, buff=0.3)
        n.until("p02", "total"); self.play(Create(total_line), FadeIn(total), FadeIn(tot_lab), run_time=0.6)
        note("w[LEFT]·x at tick 3693", LIFE_NPZ, "sum(theta_w[3193][0] * x[3193])", round(float((wL * x).sum()), 6))
        n.until("p02", "energy"); self.play(Indicate(rows[9][5], color=C_SP, scale_factor=1.3), run_time=0.7)
        n.until("p02", "constant"); self.play(Indicate(rows[11][5], color=C_SP, scale_factor=1.3), run_time=0.7)
        # the committee and b bring it down to Q (chapter five)
        qv = L["Q"][IDX][0]; b0 = th["b"][0]; comm = qv - b0 - float((wL * x).sum())
        side = VGroup(T("chapter five:", SZ_TINY, DIM), T(f"+ b  {b0:+.6f}", SZ_TINY, C_BIAS), T(f"+ committee  {comm:+.6f}", SZ_TINY, C_HID),
                      T(f"= Q for left  {qv:+.6f}", SZ_TINY, C_Q)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([5.3, -0.6, 0])
        note("b[LEFT] at tick 3693", LIFE_NPZ, "theta_b[3193][0]", round(float(b0), 6))
        n.until("p02", "committee"); self.play(FadeIn(side), run_time=0.6)
        n.until("p02", "sign"); self.play(Indicate(side[3], color=C_SP), run_time=0.7)
        n.end()

        # ------------------------------------------------------------------ p03: the alternatives failing
        n.say("p03")
        self.play(FadeOut(bill), FadeOut(side), FadeOut(heads[1]), FadeOut(heads[2]), *[FadeOut(VGroup(r[2], r[3], r[4], r[5])) for r in rows],
                  FadeOut(total_line), FadeOut(total), FadeOut(tot_lab), run_time=0.5)
        alt1 = VGroup(T("plain sum, no knobs", SZ_SMALL, C_BAD), T(f"all twelve added:  {x.sum():+.3f}", SZ_TINY), T("A counts the same as C", SZ_TINY, DIM)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.4, 2.0, 0])
        n.until("p03", "add"); self.play(FadeIn(alt1), run_time=0.5)
        # swap A and C readings: the total does not move
        swap = T("swap A and C: same total", SZ_TINY, C_BAD).next_to(alt1, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(Swap(rows[0][1], rows[2][1]), FadeIn(swap), run_time=1.0)
        alt2 = VGroup(T("biggest reading only", SZ_SMALL, C_BAD), T("the constant one, 1.000", SZ_TINY), T("eleven readings thrown away", SZ_TINY, DIM)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.4, -1.2, 0])
        n.until("p03", "biggest"); self.play(FadeIn(alt2), *[r[1].animate.set_opacity(0.25) for r in rows[:11]], run_time=0.8)
        n.until("p03", "smallest")
        self.play(*[r[1].animate.set_opacity(1.0) for r in rows[:11]], FadeOut(alt1), FadeOut(alt2), FadeOut(swap), run_time=0.6)
        ok = T("weighted sum: weigh every reading differently, one number out", SZ_SMALL, C_GOOD).move_to([4.2, 0.3, 0])
        if ok.width > 5.4: ok.scale_to_fit_width(5.4)
        self.play(FadeIn(ok), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p04: exponent, the need
        n.say("p04")
        self.clear_all()
        hdr = header("exponent: the need", SZ_BIG)
        qbars = Bars(vmax=0.004, height=2.2, fmt="{:+.4f}", title="Q at tick 3693").scale(0.9).move_to([-3.8, 0.3, 0])
        qbars.set_values(Q)
        self.play(FadeIn(hdr), FadeIn(qbars), run_time=0.6)
        # odds = Q: tickets
        t1 = T("odds = Q ?", SZ_SMALL, C_BAD).move_to([2.8, 2.6, 0])
        tickets = VGroup()
        for k in range(3):
            tk = VGroup(RoundedRectangle(corner_radius=0.08, width=1.5, height=0.7, stroke_color=MOVE[k], stroke_width=2),
                        T(f"{Q[k]:+.4f}", SZ_TINY, MOVE[k])).move_to([1.4 + k * 1.7, 1.6, 0])
            tickets.add(tk)
        n.until("p04", "Odds"); self.play(FadeIn(t1), FadeIn(tickets), run_time=0.6)
        n.until("p04", "negative")
        crosses = VGroup(*[Cross(tickets[k], stroke_color=C_BAD, stroke_width=4) for k in (1, 2)])
        self.play(Create(crosses), run_time=0.6)
        # odds = Q squared: shares before / after a shared shift
        sq = Q ** 2; sh1 = sq / sq.sum(); Q2 = Q + 0.01; sh2 = Q2 ** 2 / (Q2 ** 2).sum()
        t2 = T("odds = Q² ?", SZ_SMALL, C_BAD).move_to([2.8, 0.3, 0])
        shares = Bars(vmax=1.0, height=1.5, fmt="{:.2f}", symmetric=False, title=None).scale(0.8).move_to([2.8, -1.8, 0])
        shares.set_values(sh1)
        lab_sh = T("shares", SZ_TINY, DIM).next_to(shares, UP, buff=0.1)
        n.until("p04", "squared"); self.play(FadeIn(t2), FadeIn(shares), FadeIn(lab_sh), run_time=0.6)
        n.until("p04", "shared")
        shift_lab = T("add +0.01 to all three Q", SZ_TINY, C_SP).next_to(t2, DOWN, buff=0.15)
        self.play(FadeIn(shift_lab), run_time=0.3)
        self.play(UpdateFromAlphaFunc(shares, lambda m, a: m.set_values(sh1 + a * (sh2 - sh1))),
                  UpdateFromAlphaFunc(qbars, lambda m, a: m.set_values(Q + a * 0.01)), run_time=1.6)
        n.until("p04", "wrong")
        bad = T("the shares moved, the gaps did not", SZ_TINY, C_BAD).next_to(shares, DOWN, buff=0.5)
        self.play(FadeIn(bad), run_time=0.4)
        n.end()

        # ------------------------------------------------------------------ p05: exp passes both
        n.say("p05")
        self.clear_all()
        hdr = header("exponent: gaps become ratios", SZ_BIG)
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 8, 2], x_length=7, y_length=4.2, axis_config={"color": DIM, "include_numbers": True, "font_size": 20}).move_to([-1.5, -0.3, 0])
        xl = T("Q", SZ_TINY, C_Q).next_to(ax.x_axis, RIGHT, buff=0.1); yl = T("odds = e^Q", SZ_TINY, C_SP).next_to(ax.y_axis, UP, buff=0.1)
        curve = ax.plot(lambda v: np.exp(v), x_range=[-2.5, 2.08], color=C_SP, stroke_width=3)
        self.play(FadeIn(hdr), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.8)
        n.until("p05", "positive"); self.play(Create(curve), run_time=1.0)
        a = ValueTracker(-1.5)
        d1 = always_redraw(lambda: Dot(ax.c2p(a.get_value(), np.exp(a.get_value())), color=MOVE[0], radius=0.08))
        d2 = always_redraw(lambda: Dot(ax.c2p(a.get_value() + 1, np.exp(a.get_value() + 1)), color=MOVE[1], radius=0.08))
        brace = always_redraw(lambda: VGroup(DashedLine(ax.c2p(a.get_value(), 0), ax.c2p(a.get_value(), np.exp(a.get_value())), color=DIM),
                                             DashedLine(ax.c2p(a.get_value() + 1, 0), ax.c2p(a.get_value() + 1, np.exp(a.get_value() + 1)), color=DIM)))
        ratio = always_redraw(lambda: T(f"gap 1  →  ratio {np.exp(a.get_value()+1)/np.exp(a.get_value()):.3f}", SZ_SMALL, C_SP).move_to([4.2, 2.0, 0]))
        n.until("p05", "ratio"); self.play(FadeIn(d1), FadeIn(d2), FadeIn(brace), FadeIn(ratio), run_time=0.6)
        n.until("p05", "shift"); self.play(a.animate.set_value(0.9), run_time=2.5, rate_func=there_and_back)
        n.until("p05", "Compound")
        ci = VGroup(T("compound interest", SZ_SMALL, C_SP), T("each year × the same factor", SZ_TINY), T("n years = a fixed ratio", SZ_TINY), T("whichever year you start", SZ_TINY, DIM)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.4, -0.8, 0])
        self.play(FadeIn(ci), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p06: why e
        n.say("p06")
        self.play(FadeOut(ci), FadeOut(ratio), FadeOut(d1), FadeOut(d2), FadeOut(brace), FadeOut(hdr), run_time=0.4)
        hdr = header("why e", SZ_BIG); self.play(FadeIn(hdr), run_time=0.3)
        p = ValueTracker(-1.0)
        dot = always_redraw(lambda: Dot(ax.c2p(p.get_value(), np.exp(p.get_value())), color=C_SP, radius=0.09))
        tang = always_redraw(lambda: Line(ax.c2p(p.get_value() - 0.8, np.exp(p.get_value()) * (1 - 0.8)), ax.c2p(p.get_value() + 0.8, np.exp(p.get_value()) * (1 + 0.8)), color=MOVE[1], stroke_width=3))
        hgt = always_redraw(lambda: DashedLine(ax.c2p(p.get_value(), 0), ax.c2p(p.get_value(), np.exp(p.get_value())), color=DIM))
        lab = always_redraw(lambda: VGroup(T(f"height  {np.exp(p.get_value()):.2f}", SZ_SMALL, C_SP), T(f"slope   {np.exp(p.get_value()):.2f}", SZ_SMALL, MOVE[1])).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.4, 1.8, 0]))
        n.until("p06", "slope"); self.play(FadeIn(dot), FadeIn(tang), FadeIn(hgt), FadeIn(lab), run_time=0.5)
        self.play(p.animate.set_value(1.6), run_time=3.0, rate_func=there_and_back)
        n.until("p06", "lowering")
        e1 = T("energy down by 1 at T = 1  →  odds × 2.718", SZ_SMALL, C_SP).move_to([4.2, -1.0, 0])
        if e1.width > 5.5: e1.scale_to_fit_width(5.5)
        self.play(FadeIn(e1), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p07: softmax in four steps
        n.say("p07")
        self.clear_all()
        hdr = header("softmax, four steps", SZ_BIG)
        Tval = ValueTracker(0.3)
        def cols_for(Tv):
            z = Q / Tv; ex = np.exp(z - z.max()); pr = ex / ex.sum(); exs = np.exp(z)
            return z, exs, pr
        titles = ["1  Q", "2  Q / T", "3  e^(Q/T)", "4  ÷ total"]
        cx = [-5.0, -1.7, 1.6, 4.9]
        colbars = [Bars(vmax=0.004, height=2.0, fmt="{:+.4f}"), Bars(vmax=0.012, height=2.0, fmt="{:+.4f}"),
                   Bars(vmax=1.1, height=2.0, fmt="{:.4f}", symmetric=False), Bars(vmax=1.0, height=2.0, fmt="{:.3f}", symmetric=False)]
        z, exs, pr = cols_for(0.3)
        vals = [Q, z, exs, pr]
        heads2 = VGroup()
        for k, (bb, tt, vv) in enumerate(zip(colbars, titles, vals)):
            bb.scale(0.72).move_to([cx[k], -0.3, 0]); bb.set_values(vv)
            heads2.add(T(tt, SZ_SMALL, C_SP).move_to([cx[k], 2.4, 0]))
        tlab = T("T = 0.3", SZ_SMALL, C_T).move_to([0.0, 2.95, 0])
        self.play(FadeIn(hdr), run_time=0.3)
        n.until("p07", "Take"); self.play(FadeIn(heads2[0]), FadeIn(colbars[0]), run_time=0.6)
        n.until("p07", "Divide"); self.play(FadeIn(heads2[1]), FadeIn(colbars[1]), FadeIn(tlab), run_time=0.6)
        n.until("p07", "power"); self.play(FadeIn(heads2[2]), FadeIn(colbars[2]), run_time=0.6)
        qmark = T("?", SZ_TITLE, DIM).move_to([cx[3], -0.3, 0])
        n.until("p07", "divide"); self.play(FadeIn(heads2[3]), FadeIn(qmark), run_time=0.6)
        raffle = T("my tickets ÷ all tickets", SZ_TINY, DIM).next_to(heads2[3], DOWN, buff=0.15)
        n.until("p07", "raffle"); self.play(FadeIn(raffle), run_time=0.4)
        n.until("p07", "three"); self.play(Indicate(colbars[0], color=C_SP, scale_factor=1.05), run_time=1.0)
        n.end()

        # ------------------------------------------------------------------ p08: pause and predict
        n.say("p08")
        pause_card(self, "T = 0.3.  What are the three chances?", hold=max(n.t_word("p08", "Here") - self.time - 1.2, 2.0))
        n.until("p08", "Here")
        self.play(FadeOut(qmark), FadeIn(colbars[3]), run_time=0.6)
        note("softmax at tick 3693, T=0.3", LIFE_NPZ, "softmax(Q[3193], 0.3)", [round(float(v), 3) for v in pr])
        def set_T(Tv):
            z, exs, pr = cols_for(Tv)
            colbars[1].vmax = max(float(np.abs(z).max()) * 1.8, 0.012); colbars[2].vmax = max(float(exs.max()) * 1.1, 1.1)
            colbars[1].set_values(z); colbars[2].set_values(exs); colbars[3].set_values(pr)
            tlab.become(T(f"T = {Tv:.3g}", SZ_SMALL, C_T).move_to(tlab))
        n.until("p08", "Even")
        self.play(UpdateFromAlphaFunc(VGroup(colbars[1], colbars[2], colbars[3], tlab), lambda m, a: set_T(0.3 + a * (0.05 - 0.3))), run_time=1.5)
        note("softmax at T=0.05", LIFE_NPZ, "softmax(Q[3193], 0.05)", [round(float(v), 3) for v in cols_for(0.05)[2]])
        n.until("p08", "thousandth")
        self.play(UpdateFromAlphaFunc(VGroup(colbars[1], colbars[2], colbars[3], tlab), lambda m, a: set_T(0.05 * (0.001 / 0.05) ** a)), run_time=1.5)
        note("softmax at T=0.001", LIFE_NPZ, "softmax(Q[3193], 0.001)", [round(float(v), 3) for v in cols_for(0.001)[2]])
        n.end()

        # ------------------------------------------------------------------ p09: T as a dial, then the dice
        n.say("p09")
        self.play(FadeOut(colbars[0]), FadeOut(colbars[1]), FadeOut(colbars[2]), FadeOut(heads2), FadeOut(raffle), FadeOut(hdr), run_time=0.4)
        hdr = header("what T does", SZ_BIG)
        probs = colbars[3]; self.play(FadeIn(hdr), probs.animate.scale(1.3).move_to([-2.5, -0.3, 0]), tlab.animate.move_to([-2.5, 2.6, 0]), run_time=0.6)
        # dial
        dial = VGroup(Arc(radius=1.0, start_angle=PI, angle=-PI, color=DIM, stroke_width=3), T("cold", SZ_TINY, C_C).move_to([-1.2, -0.1, 0]), T("hot", SZ_TINY, C_A).move_to([1.2, -0.1, 0])).move_to([3.2, 1.6, 0])
        needle = always_redraw(lambda: Line(dial[0].get_arc_center(), dial[0].get_arc_center() + 0.9 * np.array([np.cos(PI - PI * (np.log10(Tval.get_value()) + 3) / 3), np.sin(PI - PI * (np.log10(Tval.get_value()) + 3) / 3), 0]), color=C_T, stroke_width=4))
        Tval.set_value(0.001)
        self.play(FadeIn(dial), FadeIn(needle), run_time=0.4)
        n.until("p09", "Small")
        self.play(UpdateFromAlphaFunc(VGroup(probs, tlab), lambda m, a: (set_T(0.001 * 1000 ** a), Tval.set_value(0.001 * 1000 ** a))), run_time=4.0, rate_func=linear)
        n.until("p09", "marble")
        self.play(UpdateFromAlphaFunc(VGroup(probs, tlab), lambda m, a: (set_T(1.0 * 0.001 ** a), Tval.set_value(1.0 * 0.001 ** a))), run_time=3.0, rate_func=linear)
        n.until("p09", "dice")
        eps = Bars(vmax=1.0, height=2.0, fmt="{:.3f}", symmetric=False, title="epsilon dice: 1 in 10").scale(0.9).move_to([3.2, -1.3, 0])
        eps.set_values([0.9 + 0.1 / 3, 0.1 / 3, 0.1 / 3])
        self.play(FadeOut(dial), FadeOut(needle), FadeIn(eps), run_time=0.6)
        n.until("p09", "winning")
        win = T("whatever the gaps", SZ_TINY, C_GOOD).next_to(eps, DOWN, buff=0.45)
        self.play(FadeIn(win), run_time=0.4)
        n.end()

        # ------------------------------------------------------------------ p10: log
        n.say("p10")
        self.clear_all()
        hdr = header("log", SZ_BIG)
        # real falloff from the field at index 3000
        f = L["fields"][3000][0].astype(float); yy, xx2 = np.unravel_index(f.argmax(), f.shape)
        prof = [float(f[yy, (xx2 + k) % 48]) for k in range(5)]
        note("A smell falloff from a peak", LIFE_NPZ, "fields[3000][0] along a row from argmax", [round(v, 4) for v in prof])
        pb = VGroup()
        for k, v in enumerate(prof):
            bar = Rectangle(width=0.5, height=max(v / prof[0] * 2.0, 0.02), fill_color=C_A, fill_opacity=0.9, stroke_width=0).move_to([-5.6 + k * 0.7, 1.2, 0], aligned_edge=DOWN)
            pb.add(VGroup(bar, T(f"{prof[0]/v:.0f}×" if k else "peak", 16, DIM).next_to(bar, UP, buff=0.08), T(f"{k}", 16, DIM).next_to(bar, DOWN, buff=0.08)))
        plab = T("cells from the source", 16, DIM).next_to(pb, DOWN, buff=0.3)
        self.play(FadeIn(hdr), run_time=0.3)
        n.until("p10", "Two"); self.play(FadeIn(pb), FadeIn(plab), run_time=0.8)
        ax = Axes(x_range=[0, 5.2, 1], y_range=[0, 5.5, 1], x_length=6.2, y_length=4.2, axis_config={"color": DIM, "include_numbers": True, "font_size": 18}).move_to([2.6, -0.4, 0])
        xl = T("smell c", SZ_TINY, C_A).next_to(ax.x_axis, DOWN, buff=0.05).shift(RIGHT * 2.3); yl = T("reading", SZ_TINY, C_X).next_to(ax.y_axis, UP, buff=0.05)
        raw = ax.plot(lambda c: c, x_range=[0, 5], color=C_BAD, stroke_width=2)
        rawl = T("raw: far ≈ 0, near blows out", SZ_TINY, C_BAD).move_to([5.0, 3.0, 0])
        logc = ax.plot(lambda c: np.log1p(c / 0.05), x_range=[0.0, 5], color=C_X, stroke_width=3)
        n.until("p10", "raw"); self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(raw), FadeIn(rawl), run_time=1.0)
        n.until("p10", "fixes"); self.play(Create(logc), raw.animate.set_opacity(0.3), rawl.animate.set_opacity(0.4), run_time=1.0)
        # doubling steps on the log curve
        steps = VGroup()
        for c in (1.25, 2.5, 5.0):
            steps.add(Dot(ax.c2p(c, np.log1p(c / 0.05)), color=C_X, radius=0.06))
        incs = [np.log1p(2.5 / 0.05) - np.log1p(1.25 / 0.05), np.log1p(5 / 0.05) - np.log1p(2.5 / 0.05)]
        inc_l = VGroup(T(f"+{incs[0]:.2f}", 16, C_X).move_to(ax.c2p(1.9, 4.2)), T(f"+{incs[1]:.2f}", 16, C_X).move_to(ax.c2p(3.75, 4.9)))
        n.until("p10", "doubling"); self.play(FadeIn(steps), FadeIn(inc_l), run_time=0.6)
        sq = ax.plot(lambda c: np.sqrt(c / 0.05) / 2, x_range=[0, 5], color=C_W, stroke_width=2)
        sqs = VGroup(*[Dot(ax.c2p(c, np.sqrt(c / 0.05) / 2), color=C_W, radius=0.06) for c in (1.25, 2.5, 5.0)])
        sqi = [np.sqrt(2.5 / 0.05) / 2 - np.sqrt(1.25 / 0.05) / 2, np.sqrt(5 / 0.05) / 2 - np.sqrt(2.5 / 0.05) / 2]
        sq_l = VGroup(T(f"+{sqi[0]:.2f}", 16, C_W).move_to(ax.c2p(1.9, 2.4)), T(f"+{sqi[1]:.2f}", 16, C_W).move_to(ax.c2p(3.75, 3.6)), T("square root (÷2 to fit): steps grow", 16, C_W).move_to([4.3, -2.9, 0]))
        n.until("p10", "square"); self.play(Create(sq), FadeIn(sqs), FadeIn(sq_l), run_time=1.0)
        pts = VGroup(*[VGroup(Dot(ax.c2p(c, np.log1p(c / 0.05)), color=C_SP, radius=0.07), T(f"{c:g} → {np.log1p(c/0.05):.2f}", 16, C_SP).next_to(ax.c2p(c, np.log1p(c / 0.05)), UL if c < 1 else UP, buff=0.1)) for c in (0.05, 0.5, 5.0)])
        n.until("p10", "smell"); self.play(FadeOut(sq), FadeOut(sqs), FadeOut(sq_l), FadeOut(steps), FadeOut(inc_l), FadeIn(pts[0]), run_time=0.6)
        n.until("p10", "Ten"); self.play(FadeIn(pts[1]), run_time=0.4)
        n.until("p10", "hundred"); self.play(FadeIn(pts[2]), run_time=0.4)
        n.end()

        # ------------------------------------------------------------------ p11: log1p detail
        n.say("p11")
        self.play(FadeOut(pb), FadeOut(plab), FadeOut(pts), FadeOut(raw), FadeOut(rawl), FadeOut(hdr), run_time=0.4)
        hdr = header("log of one plus", SZ_BIG); self.play(FadeIn(hdr), run_time=0.3)
        plain = ax.plot(lambda c: np.log(c), x_range=[0.01, 5], color=C_BAD, stroke_width=2)
        pl = T("log c: dives to minus infinity at zero", SZ_TINY, C_BAD).move_to([-3.6, -2.6, 0])
        n.until("p11", "plain"); self.play(Create(plain), FadeIn(pl), run_time=1.0)
        c0 = ValueTracker(0.05)
        lp = always_redraw(lambda: ax.plot(lambda c: np.log1p(c / c0.get_value()), x_range=[0, 5], color=C_X, stroke_width=3))
        lpl = always_redraw(lambda: T(f"log(1 + c / {c0.get_value():.2f})", SZ_SMALL, C_X).move_to([-3.6, 1.2, 0]))
        n.until("p11", "code"); self.play(FadeOut(logc), FadeIn(lp), FadeIn(lpl), run_time=0.6)
        n.until("p11", "constant"); self.play(c0.animate.set_value(0.4), run_time=2.0); self.play(c0.animate.set_value(0.02), run_time=2.0); self.play(c0.animate.set_value(0.05), run_time=1.0)
        n.end()

        # ------------------------------------------------------------------ p12: slope, one knob
        n.say("p12")
        self.clear_all()
        hdr = header("slope: one knob", SZ_BIG)
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[0, 4.5, 1], x_length=7.5, y_length=4.3, axis_config={"color": DIM, "include_numbers": False}).move_to([-1.5, -0.4, 0])
        xl = T("knob value", SZ_TINY, C_W).next_to(ax.x_axis, DOWN, buff=0.1); yl = T("mistake", SZ_TINY, C_BAD).next_to(ax.y_axis, UP, buff=0.1)
        fcur = lambda k: 0.9 * (k - 0.6) ** 2 + 0.3
        bowl = ax.plot(fcur, x_range=[-1.6, 2.2], color=FG, stroke_width=3)
        self.play(FadeIn(hdr), Create(ax), FadeIn(xl), FadeIn(yl), run_time=0.6)
        n.until("p12", "Draw"); self.play(Create(bowl), run_time=1.0)
        kv = ValueTracker(-1.3)
        dot = always_redraw(lambda: Dot(ax.c2p(kv.get_value(), fcur(kv.get_value())), color=C_SP, radius=0.09))
        def tri():
            k = kv.get_value(); s = 1.8 * (k - 0.6); p0 = ax.c2p(k, fcur(k)); p1 = ax.c2p(k + 0.5, fcur(k)); p2 = ax.c2p(k + 0.5, fcur(k) + 0.5 * s)
            return VGroup(Line(p0, p1, color=MOVE[1], stroke_width=2), Line(p1, p2, color=MOVE[1], stroke_width=2), Line(p0, p2, color=MOVE[1], stroke_width=3),
                          T("run", 14, MOVE[1]).next_to(Line(p0, p1), DOWN, buff=0.05), T("rise", 14, MOVE[1]).next_to(Line(p1, p2), RIGHT, buff=0.05))
        tr = always_redraw(tri)
        slab = always_redraw(lambda: T(f"slope  {1.8*(kv.get_value()-0.6):+.2f}", SZ_SMALL, MOVE[1]).move_to([4.3, 2.0, 0]))
        n.until("p12", "slope"); self.play(FadeIn(dot), FadeIn(tr), FadeIn(slab), run_time=0.5)
        n.until("p12", "Move")
        for step in range(5):
            k = kv.get_value(); s = 1.8 * (k - 0.6)
            self.play(kv.animate.set_value(k - 0.35 * s), run_time=0.6)
        n.until("p12", "shower")
        tap = VGroup(T("shower tap", SZ_SMALL, C_SP), T("too hot → toward cold, a bit, feel again", SZ_TINY)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([4.3, 0.3, 0])
        if tap.width > 5.4: tap.scale_to_fit_width(5.4)
        self.play(FadeIn(tap), run_time=0.5)
        n.until("p12", "miss")
        nm = T("mistake  =  miss  =  td", SZ_SMALL, C_BAD).move_to([4.3, -1.6, 0])
        self.play(FadeIn(nm), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p13: gradient, many knobs
        n.say("p13")
        self.clear_all()
        hdr = header("gradient: one slope per knob", SZ_BIG)
        ev = MathTex(r"\text{evidence}", r"=", r"w", r"\cdot", r"x", r"= \sum_k w_k\, x_k").scale(0.9).move_to([-3.6, 2.2, 0]); ev[2].set_color(C_W); ev[4].set_color(C_X)
        evl = T("the simplest brain, committee ignored", SZ_TINY, DIM).next_to(ev, DOWN, buff=0.15)
        sl = MathTex(r"\frac{\partial\,\text{evidence}}{\partial w_k}", r"=", r"x_k").scale(0.9).move_to([-3.6, 0.3, 0]); sl[2].set_color(C_X)
        sll = T("the slope for knob k is its reading", SZ_TINY, C_X).next_to(sl, DOWN, buff=0.15)
        self.play(FadeIn(hdr), run_time=0.3)
        n.until("p13", "weighted"); self.play(FadeIn(ev), FadeIn(evl), run_time=0.6)
        n.until("p13", "slope"); self.play(FadeIn(sl), FadeIn(sll), run_time=0.6)
        # twelve arrows with length = reading
        arrows = VGroup()
        for k in range(12):
            y0 = 2.5 - k * 0.45
            arrows.add(VGroup(T(SHORT[names[k]], 16, DIM).move_to([2.0, y0, 0], aligned_edge=RIGHT),
                              Arrow([2.2, y0, 0], [2.2 + 3.2 * x[k], y0, 0], buff=0, color=C_X, stroke_width=3, max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=10)))
        self.play(LaggedStart(*[FadeIn(a_) for a_ in arrows], lag_ratio=0.05), run_time=1.2)
        # the nudges, computed with the real weights
        def Qn(k, d):
            th2 = {kk: v.copy() for kk, v in th.items()}; th2["w"][0, k] += d; return float(-F_of(th2, x)[0])
        q0 = float(-F_of(th, x)[0]); dA = Qn(0, 0.1) - q0; dX = Qn(10, 0.1) - q0
        note("nudge w[LEFT,contrast_A] +0.1", LIFE_NPZ, "F_of(theta_at(3193)) recomputed", round(dA, 6))
        note("nudge w[LEFT,body_X] +0.1", LIFE_NPZ, "F_of(theta_at(3193)) recomputed", round(dX, 6))
        n1 = VGroup(T("knob on contrast A  +0.1", SZ_TINY, C_W), T(f"Q for left moves  {dA:+.4f}", SZ_TINY, C_SP), T("= 0.1 × 0.521", 16, DIM)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-3.6, -1.6, 0])
        n2 = VGroup(T("knob on toxin  +0.1", SZ_TINY, C_W), T(f"Q for left moves  {dX:+.5f}", SZ_TINY, C_SP), T("= 0.1 × 0.0014", 16, DIM)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([-3.6, -3.2, 0])
        n.until("p13", "Nudge"); self.play(FadeIn(n1), Indicate(arrows[0][1], color=C_SP, scale_factor=1.2), run_time=0.8)
        n.until("p13", "toxin"); self.play(FadeIn(n2), Indicate(arrows[10][1], color=C_SP, scale_factor=1.6), run_time=0.8)
        n.until("p13", "smelled")
        fin = T("a knob only matters through the reading it multiplies", SZ_TINY, C_GOOD).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(fin), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p14: average over chances
        n.say("p14")
        self.clear_all()
        hdr = header("average over chances", SZ_BIG)
        vals_ = [10, -5, 0]; ch = [0.5, 0.3, 0.2]; cols = [MOVE[0], MOVE[1], MOVE[2]]
        items = VGroup()
        for k in range(3):
            items.add(VGroup(T(f"value {vals_[k]:+d}", SZ_SMALL, cols[k]), T(f"chance {ch[k]:.1f}", SZ_TINY, DIM)).arrange(DOWN, buff=0.1).move_to([-4.5 + k * 2.6, 1.6, 0]))
        self.play(FadeIn(hdr), run_time=0.3)
        n.until("p14", "operation"); self.play(FadeIn(items), run_time=0.6)
        lot = VGroup(T("lottery ticket", SZ_SMALL, C_SP), T("prize × chance, summed", SZ_TINY)).arrange(DOWN, buff=0.1).move_to([4.3, 1.6, 0])
        n.until("p14", "lottery"); self.play(FadeIn(lot), run_time=0.5)
        pieces = VGroup(); base = -1.6; scale_ = 0.35
        parts = [vals_[k] * ch[k] for k in range(3)]
        for k in range(3):
            h = parts[k] * scale_
            rect = Rectangle(width=0.9, height=max(abs(h), 0.04), fill_color=cols[k], fill_opacity=0.9, stroke_width=0)
            rect.move_to([1.3 + k * 1.2, base, 0], aligned_edge=DOWN if h >= 0 else UP)
            lab_ = T(f"{parts[k]:+.1f}", SZ_TINY, cols[k]).next_to(rect, UP if h >= 0 else DOWN, buff=0.1)
            eq = T(f"{vals_[k]:+d} × {ch[k]:.1f}", 16, DIM).move_to([1.3 + k * 1.2, base - 1.1, 0])
            pieces.add(VGroup(rect, lab_, eq))
        baseline = Line([0.6, base, 0], [6.2, base, 0], color=DIM, stroke_width=2)
        self.add(baseline)
        n.until("p14", "Ten")
        for k in range(3):
            self.play(Transform(items[k].copy(), pieces[k]), run_time=0.6); self.add(pieces[k])
        n.until("p14", "three")
        tbar = Rectangle(width=0.9, height=sum(parts) * scale_, fill_color=C_SP, fill_opacity=0.9, stroke_width=0).move_to([5.4, base, 0], aligned_edge=DOWN)
        total = VGroup(tbar, T(f"= {sum(parts):.1f}", SZ_SMALL, C_SP).next_to(tbar, UP, buff=0.1), T("sum", 16, DIM).move_to([5.4, base - 1.1, 0]))
        self.play(FadeIn(total), run_time=0.5)
        n.end()

        # ------------------------------------------------------------------ p15: length
        n.say("p15")
        self.clear_all()
        hdr = header("length of a list", SZ_BIG)
        kn = VGroup()
        W = wL.copy()
        for k in range(12):
            y0 = 2.3 - k * 0.42
            kn.add(Arrow([-4.6, y0, 0], [-4.6 + 90 * W[k], y0, 0], buff=0, color=C_W, stroke_width=3, max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=10))
        knl = T("twelve knobs (left row, tick 3693)", SZ_TINY, DIM).move_to([-4.6, 2.85, 0])
        self.play(FadeIn(hdr), FadeIn(knl), FadeIn(kn), run_time=0.6)
        sqv = W ** 2; tot = float(np.sqrt(sqv.sum()))
        squares = VGroup(*[Square(side_length=max(abs(W[k]) * 60, 0.03), fill_color=C_W, fill_opacity=0.7, stroke_width=0).move_to([-1.6 + (k % 4) * 0.5, 1.9 - (k // 4) * 0.5, 0]) for k in range(12)])
        sql = T("square each", SZ_TINY, DIM).move_to([-0.9, 2.85, 0])
        n.until("p15", "square"); self.play(FadeIn(sql), LaggedStart(*[FadeIn(s_) for s_ in squares], lag_ratio=0.05), run_time=1.0)
        big = Square(side_length=tot * 60, fill_color=C_SP, fill_opacity=0.7, stroke_width=0).move_to([1.6, 1.4, 0])
        bigl = T("add the areas", SZ_TINY, DIM).move_to([1.6, 2.85, 0])
        n.until("p15", "add"); self.play(FadeIn(bigl), Transform(squares.copy(), big), run_time=1.0)
        root = Arrow([3.2, 1.4, 0], [3.2 + 90 * tot, 1.4, 0], buff=0, color=C_SP, stroke_width=4, max_tip_length_to_length_ratio=0.2)
        rootl = VGroup(T("square root: back to knob units", SZ_TINY, DIM), T(f"length = {tot:.4f}", SZ_SMALL, C_SP)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([4.8, 2.6, 0])
        note("length of w[LEFT] at tick 3693", LIFE_NPZ, "sqrt(sum(theta_w[3193][0]**2))", round(tot, 5))
        n.until("p15", "root"); self.play(GrowArrow(root), FadeIn(rootl), run_time=0.8)
        n.until("p15", "room")
        room = VGroup(T("a room: sides 3 and 4", SZ_TINY, DIM), T("corner to corner  √(9 + 16) = 5", SZ_TINY, C_SP)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([4.2, 0.0, 0])
        self.play(FadeIn(room), run_time=0.5)
        n.until("p15", "step")
        bars2 = VGroup(Rectangle(width=0.09 * 6, height=0.4, fill_color=C_W, fill_opacity=0.9, stroke_width=0), Rectangle(width=0.68 * 6, height=0.4, fill_color=C_BAD, fill_opacity=0.9, stroke_width=0)).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([0.3, -2.3, 0], aligned_edge=LEFT)
        bl = VGroup(T("brain at birth  0.09", SZ_TINY, C_W).next_to(bars2[0], UP, buff=0.08, aligned_edge=LEFT), T("one night's step  0.68 to 1.39", SZ_TINY, C_BAD).next_to(bars2[1], DOWN, buff=0.08, aligned_edge=LEFT))
        self.play(FadeOut(room), FadeIn(bars2), FadeIn(bl), run_time=0.6)
        n.until("p15", "eight")
        e8 = T("8× the brain", SZ_SMALL, C_BAD).next_to(bars2[1], RIGHT, buff=0.3)
        self.play(FadeIn(e8), run_time=0.4)
        n.end()

        # ------------------------------------------------------------------ p16: strip it down
        n.say("p16")
        self.clear_all()
        lines = ["weighted sum = a total vote", "exponent = gaps become ratios", "softmax = my tickets ÷ all tickets", "log = every doubling adds the same",
                 "slope of a weighted sum = the knob's reading", "average = value × chance, summed", "length = square, add, root"]
        lg = VGroup(*[T(s, SZ_SMALL) for s in lines]).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([-3.2, 0.2, 0])
        words = ["weighted", "exponent", "Softmax", "log", "slope", "average", "Length"]
        for w, m in zip(words, lg):
            n.until("p16", w); self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.4)
        loop = LoopDiagram(radius=1.9, box_w=1.4, box_h=0.52, size=16).move_to([4.3, 0.2, 0])
        n.until("p16", "None"); self.play(FadeIn(loop), run_time=0.6)
        n.until("p16", "first"); self.play(loop.lit("Brain"), loop.lit("Senses"), *[m.animate.set_color(C_SP) for m in lg[:4]], run_time=0.8)
        n.until("p16", "last"); self.play(loop.lit("Learning", color=C_GOOD), *[m.animate.set_color(C_GOOD) for m in lg[4:]], run_time=0.8)
        n.finish(tail=1.0)
