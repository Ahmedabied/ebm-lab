"""Chapter 05 — The brain, symbol by symbol. Every number is read from the lab files (see note() calls)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

I_TICK = 3193            # waking index of tick 3693 (day 10)


class Ch05(Scene):
    def construct(self):
        n = Narration(self, "05"); L = life(); names = L["input_names"]
        th = theta_at(I_TICK); x = L["x"][I_TICK].astype(float); tick = int(L["t"][I_TICK])
        Q = -F_of(th, x)
        note("tick 3693 x", LIFE_NPZ, f"x[{I_TICK}] (t={tick})", np.round(x, 4).tolist())
        note("tick 3693 Q", LIFE_NPZ, f"-F_of(theta_at({I_TICK}), x)", np.round(Q, 6).tolist())
        legend = T("F = energy, low wins   |   Q = minus F, high wins", SZ_TINY, DIM).to_corner(DR, buff=0.25)

        # ---------- p01: the need
        d = n.say("p01")
        loop = LoopDiagram(radius=2.5).shift(UP * 0.2)
        self.play(FadeIn(loop), run_time=0.8)
        self.play(loop.lit("Brain"), run_time=0.6)
        need = T("x  (12 numbers)   →   one energy per move", SZ_BODY, C_SP).to_edge(DOWN, buff=0.8)
        n.until("p01", "twelve"); self.play(FadeIn(need), run_time=0.6)
        n.until("p01", "formula"); self.play(FadeOut(loop), FadeIn(legend), run_time=0.6)
        n.end()

        # ---------- p02: the formula, whole and dim
        d = n.say("p02")
        f = formula_F(0.72).to_edge(UP, buff=0.5)
        self.play(FadeOut(need), run_time=0.3)
        self.play(FadeIn(f), run_time=1.0); f.set_opacity(0.45)
        n.end()

        # ---------- p03: evidence and the sign
        d = n.say("p03")
        qf = MathTex(r"Q(x,a)", r"=", r"b_a", r"+\,w_a\!\cdot\! x", r"+\sum_h \mathrm{softplus}(\cdots)").scale(0.8)
        qf[2].set_color(C_BIAS); qf[3].set_color(C_W); qf[4].set_color(C_HID)
        qlab = T("evidence for move a", SZ_SMALL, C_SP)
        g = VGroup(qf, qlab).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        n.until("p03", "evidence"); self.play(FadeIn(g), run_time=0.7)
        fq = MathTex(r"F(x,a) = -\,Q(x,a)").scale(0.9).next_to(g, DOWN, buff=0.6)
        n.until("p03", "Energy"); self.play(Write(fq), run_time=0.8)
        # price tags: F of the real tick
        tags = VGroup()
        for k in range(3):
            box = RoundedRectangle(corner_radius=0.1, width=2.0, height=1.1, stroke_color=MOVE[k], stroke_width=2)
            lab = VGroup(T(MOVE_NAME[k], SZ_TINY, MOVE[k]), T(f"F = {-Q[k]:+.4f}", SZ_TINY)).arrange(DOWN, buff=0.1).move_to(box)
            tags.add(VGroup(box, lab))
        tags.arrange(RIGHT, buff=0.5).next_to(fq, DOWN, buff=0.6)
        n.until("p03", "price"); self.play(FadeIn(tags), run_time=0.6)
        k = int(np.argmin(-Q)); n.until("p03", "cheap")
        self.play(tags[k][0].animate.set_fill(MOVE[k], 0.25), Indicate(tags[k], color=MOVE[k]), run_time=0.8)
        n.end()
        self.play(FadeOut(g), FadeOut(fq), FadeOut(tags), run_time=0.4)

        # ---------- p04: b_a
        d = n.say("p04")
        self.play(f[2].animate.set_opacity(1.0), Indicate(f[2], color=C_BIAS), run_time=0.8)
        b14 = np.array(run()["brain"][14]["b"]); note("b after night 14", RUN_JSON, "brain[14].b", b14.tolist())
        bb = Bars(vmax=0.01, height=2.2, title="b after the last night  (resting preference)").shift(DOWN * 0.5)
        bb.set_values(b14); n.until("p04", "two hundred")
        self.play(FadeIn(bb), run_time=0.7)
        for w_, k in (("five", 0), ("two", 1), ("six", 2)):
            n.until("p04", w_, occurrence=1 if w_ == "two" else 0); self.play(Indicate(bb.rects[k], color=MOVE[k]), run_time=0.5)
        n.end(); self.play(FadeOut(bb), run_time=0.4)

        # ---------- p05: w_a·x, the heat map and the LEFT row dot product
        d = n.say("p05")
        self.play(f[3].animate.set_opacity(1.0), Indicate(f[3], color=C_W), run_time=0.8)
        W14 = nightly_w()[14]; note("w after night 14", RUN_JSON, "brain[14].w", "3x12")
        hm = Heatmap(W14, cell=0.42, col_labels=names).move_to([0, 0.4, 0])
        n.until("p05", "block"); self.play(FadeIn(hm), run_time=0.8)
        n.until("p05", "Pull")
        wl = th["w"][0]; prods = wl * x; note("w[LEFT]·x at tick 3693", LIFE_NPZ, f"theta_w[{I_TICK}][0]·x", float(prods.sum()))
        rowbox = SurroundingRectangle(VGroup(*hm.cells[0:12]), color=C_W, buff=0.02)
        self.play(Create(rowbox), run_time=0.5)
        # products under the columns, as bars aligned with the heat map columns
        pb = VGroup(); vmaxp = 0.01
        for j in range(12):
            cx = hm.cells[j].get_center()[0]; h = max(abs(prods[j]) / vmaxp * 0.9, 0.02)
            r = Rectangle(width=0.3, height=h, fill_color=C_W if prods[j] >= 0 else C_X, fill_opacity=0.9, stroke_width=0)
            r.move_to([cx, -1.9, 0], aligned_edge=DOWN if prods[j] >= 0 else UP); pb.add(r)
        base = Line([hm.cells[0].get_center()[0] - 0.3, -1.9, 0], [hm.cells[11].get_center()[0] + 0.3, -1.9, 0], color=DIM)
        xrow = T("×  x of tick 3693", SZ_TINY, C_X).next_to(base, UP, buff=0.9).to_edge(LEFT, buff=0.4)
        n.until("p05", "multiply"); self.play(Create(base), FadeIn(xrow), LaggedStart(*[GrowFromEdge(r, DOWN) for r in pb], lag_ratio=0.05), run_time=1.4)
        total = T(f"sum = {prods.sum():+.6f}", SZ_SMALL, C_W).next_to(base, DOWN, buff=0.9)
        n.until("p05", "add"); self.play(FadeIn(total), run_time=0.5)
        jE, jB = names.index("body_E"), names.index("bias")
        n.until("p05", "energy"); self.play(Indicate(pb[jE], color=C_SP), Indicate(pb[jB], color=C_SP), run_time=0.8)
        n.end(); self.play(FadeOut(VGroup(hm, rowbox, pb, base, xrow, total)), run_time=0.4)

        # ---------- p06: pause and predict on the contrast-A knob
        d = n.say("p06")
        pause_card(self, "Turn the LEFT knob on contrast A\nfrom 0.00 up to +0.50.\nWhat happens to Q when A is stronger on the left?", hold=3.0)
        qb = Bars(vmax=0.3, height=2.0, title="Q(x, ·) at tick 3693").move_to([-3.2, 0.1, 0])
        qb.set_values(Q); qb.highlight(int(np.argmax(Q)))
        wv = WorldView(size=3.4).move_to([3.4, 0.1, 0]); wv.set_tick(I_TICK)
        knob = T("w[LEFT, contrast A] = " + f"{th['w'][0,0]:+.3f}", SZ_SMALL, C_W).move_to([-3.2, 2.1, 0])
        self.play(FadeIn(qb), FadeIn(wv), FadeIn(knob), run_time=0.7)
        th2 = {k_: v_.copy() for k_, v_ in th.items()}; th2["w"][0, 0] += 0.5; Q2 = -F_of(th2, x)
        note("Q with w[LEFT,contrast_A]+0.5", LIFE_NPZ, "F_of(theta+0.5)", np.round(Q2, 4).tolist())
        n.until("p06", "jumps")
        tr = ValueTracker(0.0)
        def upd_q(m):
            a = tr.get_value(); thq = {k_: v_.copy() for k_, v_ in th.items()}; thq["w"][0, 0] += a
            m.set_values(-F_of(thq, x)); m.highlight(int(np.argmax(-F_of(thq, x))))
        qb.add_updater(upd_q)
        knob2 = T("w[LEFT, contrast A] = " + f"{th['w'][0,0]+0.5:+.3f}", SZ_SMALL, C_W).move_to(knob)
        self.play(tr.animate.set_value(0.5), Transform(knob, knob2), run_time=1.5)
        qb.clear_updaters()
        jump = T(f"Q LEFT: {Q[0]:+.4f}  →  {Q2[0]:+.4f}   (+{Q2[0]-Q[0]:.4f})", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(jump), run_time=0.5)
        n.until("p06", "turns"); self.play(*[AnimationGroup(*[ApplyMethod(wv.set_tick, I_TICK + s) for s in range(1, 8)], lag_ratio=1.0)], run_time=2.0)
        n.until("p06", "checked")
        hand = VGroup(T("hand-set forager (research/07 §1.1)", SZ_SMALL, C_SP),
                      T("two knobs:  +3 on LEFT·contrast A,  −3 on RIGHT·contrast A", SZ_TINY),
                      T("5250 ticks on 10 of 10 fresh seeds;  with the C pair: 20 of 20", SZ_TINY)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3).shift(LEFT * 2.2)
        note("hand-set forager", "research/07-proof-of-possibility.md", "§1.1 claim 1.1", "10/10 (A pair), 20/20 (five numbers)")
        self.play(FadeOut(jump), FadeOut(legend), FadeIn(hand), run_time=0.6)
        n.end(); self.play(FadeOut(Group(qb, wv, knob, hand)), FadeIn(legend), run_time=0.4)

        # ---------- p07: the committee
        d = n.say("p07")
        self.play(f[4].animate.set_opacity(1.0), f[5].animate.set_opacity(1.0), f[9].animate.set_opacity(1.0),
                  f[6].animate.set_opacity(1.0), f[7].animate.set_opacity(1.0), f[8].animate.set_opacity(1.0), run_time=0.6)
        alarm = VGroup(Circle(radius=0.6, color=C_HID, stroke_width=3), Circle(radius=0.25, color=C_HID, stroke_width=3), Dot(color=C_HID, radius=0.06))
        alabel = T("a hidden unit = a smoke alarm", SZ_SMALL, C_HID)
        ag = VGroup(alarm, alabel).arrange(DOWN, buff=0.3).move_to([-3.6, -0.3, 0])
        n.until("p07", "smoke"); self.play(FadeIn(ag), run_time=0.6)
        unit = VGroup()
        box = RoundedRectangle(corner_radius=0.15, width=3.4, height=2.6, stroke_color=C_HID, stroke_width=2)
        lu = T("u: 12 input knobs  (sensitivity)", SZ_TINY, C_HID); lc = T("c: threshold", SZ_TINY, C_HID); lv = T("v: 3 output knobs  (what it says per move)", SZ_TINY, C_HID)
        inner = VGroup(lu, lc, lv).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(box)
        unit.add(box, inner); unit.move_to([2.6, -0.3, 0])
        self.play(FadeIn(box), run_time=0.4)
        for w_, lab, piece in (("u", lu, f[7]), ("c", lc, f[6]), ("v", lv, f[8])):
            n.until("p07", w_); self.play(FadeIn(lab), Indicate(piece, color=C_HID), run_time=0.6)
        zeq = MathTex(r"z_{h,a} = c_h + u_h\!\cdot\! x + v_{h,a}", color=C_HID).scale(0.8).to_edge(DOWN, buff=0.7)
        n.until("p07", "z"); self.play(Write(zeq), run_time=0.8)
        n.until("p07", "sigma"); self.play(Indicate(f[4], color=C_HID), run_time=0.6)
        n.end(); self.play(FadeOut(ag), FadeOut(unit), FadeOut(zeq), run_time=0.4)

        # ---------- p08: softplus and its slope (sigmoid)
        d = n.say("p08")
        ax = Axes(x_range=[-4, 4, 1], y_range=[0, 4, 1], x_length=6.0, y_length=2.6, axis_config={"color": DIM, "stroke_width": 2}).move_to([-2.8, 0.3, 0])
        relu = ax.plot(lambda z: max(0.0, z), x_range=[-4, 4], color=DIM, stroke_width=3)
        sp = ax.plot(lambda z: float(np.logaddexp(0, z)), x_range=[-4, 4], color=C_SP, stroke_width=3)
        lab_sp = MathTex(r"\mathrm{softplus}(z)=\log(1+e^{z})", color=C_SP).scale(0.7).next_to(ax, UP, buff=0.15)
        self.play(FadeIn(ax), Create(relu), run_time=0.8)
        n.until("p08", "Log"); self.play(Transform(relu, sp), FadeIn(lab_sp), run_time=1.0)
        zt = ValueTracker(-3.0)
        dot = always_redraw(lambda: Dot(ax.c2p(zt.get_value(), float(np.logaddexp(0, zt.get_value()))), color=C_SP, radius=0.08))
        read = always_redraw(lambda: T(f"z = {zt.get_value():+.1f}   softplus = {float(np.logaddexp(0, zt.get_value())):.3f}", SZ_TINY, C_SP).next_to(ax, DOWN, buff=0.15))
        self.add(dot, read)
        n.until("p08", "shape"); self.play(zt.animate.set_value(3.0), run_time=2.0); self.play(zt.animate.set_value(-3.0), run_time=1.5)
        n.until("p08", "hinge"); self.play(Indicate(relu, color=FG), run_time=0.6)
        # sigmoid panel
        ax2 = Axes(x_range=[-4, 4, 1], y_range=[0, 1, 0.5], x_length=6.0, y_length=2.0, axis_config={"color": DIM, "stroke_width": 2}).move_to([3.0, -0.2, 0])
        sig = ax2.plot(lambda z: 1 / (1 + np.exp(-z)), x_range=[-4, 4], color=C_HID, stroke_width=3)
        lab_sig = T("slope of softplus = sigmoid, 0 to 1", SZ_TINY, C_HID).next_to(ax2, UP, buff=0.15)
        tangent = always_redraw(lambda: Line(ax.c2p(zt.get_value() - 0.8, float(np.logaddexp(0, zt.get_value())) - 0.8 / (1 + np.exp(-zt.get_value()))),
                                             ax.c2p(zt.get_value() + 0.8, float(np.logaddexp(0, zt.get_value())) + 0.8 / (1 + np.exp(-zt.get_value()))), color=C_HID, stroke_width=3))
        sdot = always_redraw(lambda: Dot(ax2.c2p(zt.get_value(), 1 / (1 + np.exp(-zt.get_value()))), color=C_HID, radius=0.08))
        sread = always_redraw(lambda: T(f"slope = {1/(1+np.exp(-zt.get_value())):.3f}", SZ_TINY, C_HID).next_to(ax2, DOWN, buff=0.15))
        n.until("p08", "slope"); self.play(FadeIn(ax2), Create(sig), FadeIn(lab_sig), run_time=0.8); self.add(tangent, sdot, sread)
        for w_, zv, occ in (("minus", -3.0, 0), ("zero", 0.0, 1), ("plus", 3.0, 0)):
            n.until("p08", w_, occurrence=occ); self.play(zt.animate.set_value(zv), run_time=0.8)
        note("softplus/sigmoid samples", "creature/brain.py", "_softplus, _sigmoid at z=-3,0,3", [0.0486, 0.693, 3.049, 0.047, 0.5, 0.953])
        n.end()
        self.remove(dot, read, tangent, sdot, sread)
        self.play(FadeOut(VGroup(ax, relu, lab_sp, ax2, sig, lab_sig)), run_time=0.4)

        # ---------- p09: where softplus comes from (free energy)
        d = n.say("p09")
        zval = 1.0
        off = Rectangle(width=1.2, height=1.0 * 0.6, fill_color=DIM, fill_opacity=0.8, stroke_width=0)
        on = Rectangle(width=1.2, height=np.exp(zval) * 0.6, fill_color=C_HID, fill_opacity=0.8, stroke_width=0)
        offl = VGroup(T("off", SZ_TINY), MathTex(r"e^{0}=1").scale(0.7)).arrange(DOWN, buff=0.1)
        onl = VGroup(T("on", SZ_TINY, C_HID), MathTex(r"e^{z}").scale(0.7).set_color(C_HID)).arrange(DOWN, buff=0.1)
        goff = VGroup(off, offl).arrange(DOWN, buff=0.2); gon = VGroup(on, onl).arrange(DOWN, buff=0.2)
        tickets = VGroup(goff, gon).arrange(RIGHT, buff=0.8, aligned_edge=DOWN).move_to([-4.2, -0.8, 0])
        n.until("p09", "off"); self.play(FadeIn(goff), run_time=0.5)
        n.until("p09", "On"); self.play(FadeIn(gon), run_time=0.5)
        stack_off = off.copy(); stack_on = on.copy()
        n.until("p09", "count")
        stack_on.move_to([-0.3, -1.6, 0], aligned_edge=DOWN); stack_off.next_to(stack_on, UP, buff=0)
        stl = MathTex(r"1+e^{z}").scale(0.8).next_to(stack_off, UP, buff=0.15)
        self.play(TransformFromCopy(off, stack_off), TransformFromCopy(on, stack_on), FadeIn(stl), run_time=1.2)
        logl = MathTex(r"\log(1+e^{z}) = \mathrm{softplus}(z)", color=C_SP).scale(0.8).move_to([3.6, 0.9, 0])
        n.until("p09", "log"); self.play(Write(logl), run_time=0.8)
        free = T("“free”: the on-or-off was summed out", SZ_SMALL, C_SP).move_to([3.6, -0.2, 0])
        n.until("p09", "Free"); self.play(FadeIn(free), run_time=0.6)
        tnote = T("inside the committee, T is fixed at 1", SZ_TINY, DIM).move_to([3.6, -1.0, 0])
        self.play(FadeIn(tnote), run_time=0.4)
        n.end(); self.play(FadeOut(VGroup(tickets, stack_off, stack_on, stl, logl, free, tnote)), run_time=0.4)

        # ---------- p10: the five units stack
        d = n.say("p10")
        pre = th["c"][:, None] + (th["u"] @ x)[:, None] + th["v"]; spL = np.logaddexp(0, pre[:, 0]); H = len(th["c"])
        note("committee softplus outputs for LEFT at tick 3693", LIFE_NPZ, "softplus(c + u·x + v[:,LEFT])", np.round(spL, 4).tolist())
        units = VGroup()
        for h in range(H):
            bx = RoundedRectangle(corner_radius=0.1, width=1.5, height=0.9, stroke_color=C_HID, stroke_width=2)
            lb = VGroup(T(f"unit {h+1}", SZ_TINY, C_HID), T(f"{spL[h]:.3f}", SZ_TINY)).arrange(DOWN, buff=0.08).move_to(bx)
            units.add(VGroup(bx, lb))
        units.arrange(RIGHT, buff=0.3).move_to([-2.0, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(u) for u in units[:4]], lag_ratio=0.2), run_time=1.0)
        n.until("p10", "fifth"); self.play(FadeIn(units[4]), Indicate(units[4], color=C_SP), run_time=0.7)
        stack = VGroup(); y0 = -2.6
        for h in range(H):
            r = Rectangle(width=1.0, height=spL[h] * 0.8, fill_color=C_HID, fill_opacity=0.5 + 0.1 * h, stroke_color=BG, stroke_width=1)
            r.move_to([4.0, y0, 0], aligned_edge=DOWN); y0 += spL[h] * 0.8; stack.add(r)
        slab = T(f"stack = {spL.sum():.3f}", SZ_SMALL, C_HID).next_to(stack, UP, buff=0.15)
        n.until("p10", "stacked"); self.play(LaggedStart(*[TransformFromCopy(units[h][0], stack[h]) for h in range(H)], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(slab), run_time=0.4)
        n.until("p10", "log"); l2 = T("each ≈ log 2 = 0.693", SZ_TINY, DIM).next_to(units, DOWN, buff=0.3); self.play(FadeIn(l2), run_time=0.5)
        n.end(); self.play(FadeOut(VGroup(units, stack, slab, l2)), run_time=0.4)

        # ---------- p11: centring
        d = n.say("p11")
        c1 = MathTex(r"\mathrm{softplus}(0)=\log 2 = 0.693", color=C_SP).scale(0.8).move_to([-3.3, 0.9, 0])
        c2 = VGroup(MathTex(r"4\times 0.693 = 2.773", color=C_SP).scale(0.8), T("at birth: 4 units", SZ_TINY, DIM)).arrange(DOWN, buff=0.15).next_to(c1, DOWN, buff=0.4)
        n.until("p11", "Softplus"); self.play(Write(c1), run_time=0.8)
        n.until("p11", "free"); self.play(Write(c2), run_time=0.7)
        Q0 = L["Q"][0]; note("birth Q", LIFE_NPZ, "Q[0]", np.round(Q0, 4).tolist())
        cb = Bars(vmax=4.0, height=2.4, fmt="{:+.3f}", title="Q at birth").move_to([3.0, -0.4, 0])
        H0 = 4; note("units at birth", RUN_JSON, "meta.config.brain.H0", H0)
        cb.set_values(Q0 + H0 * np.log(2)); self.play(FadeIn(cb), run_time=0.6)
        sub = MathTex(r"-\,H\log 2", color=C_SP).scale(0.9).next_to(c2, DOWN, buff=0.6)
        n.until("p11", "subtract"); self.play(Write(sub), run_time=0.6)
        tr2 = ValueTracker(0.0); cb.add_updater(lambda m: m.set_values(Q0 + (1 - tr2.get_value()) * H0 * np.log(2)))
        self.play(tr2.animate.set_value(1.0), run_time=1.5); cb.clear_updaters()
        n.end(); self.play(FadeOut(VGroup(c1, c2, sub, cb)), run_time=0.4)

        # ---------- p12: the three parts of Q LEFT
        d = n.say("p12")
        parts = [("b  (resting)", th["b"][0], C_BIAS), ("w · x  (readings)", float(prods.sum()), C_W), ("committee − H log 2", float(spL.sum() - H * np.log(2)), C_HID)]
        note("Q LEFT parts at tick 3693", LIFE_NPZ, "b, w·x, committee share", [round(p[1], 6) for p in parts])
        scale = 120.0; cur = 0.0; blocks = VGroup(); labs = VGroup(); words = ["resting", "weighted", "committee"]
        for (nm, val, col), w_ in zip(parts, words):
            r = Rectangle(width=1.4, height=max(abs(val) * scale, 0.02), fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([-2.4, -1.5 + cur * scale, 0], aligned_edge=DOWN if val >= 0 else UP)
            lab = T(f"{nm}   {val:+.6f}", SZ_TINY, col).move_to([1.6, 1.2 - 0.5 * len(labs), 0], aligned_edge=LEFT)
            cur += val; blocks.add(r); labs.add(lab)
            n.until("p12", w_); self.play(GrowFromEdge(r, DOWN if val >= 0 else UP), FadeIn(lab), run_time=0.7)
        net = Line([-3.6, -1.5 + cur * scale, 0], [-1.2, -1.5 + cur * scale, 0], color=C_SP, stroke_width=3)
        netl = T(f"Q LEFT = {cur:+.6f}", SZ_SMALL, C_SP).move_to([1.6, -0.6, 0], aligned_edge=LEFT)
        n.until("p12", "Add"); self.play(Create(net), FadeIn(netl), run_time=0.7)
        bq = Bars(vmax=0.03, height=1.6, title="Q at birth").scale(0.7).move_to([2.9, -2.3, 0]); bq.set_values(Q0)
        n.until("p12", "birth"); self.play(FadeIn(bq), run_time=0.6)
        n.end(); self.play(FadeOut(VGroup(blocks, labs, net, netl, bq)), run_time=0.4)

        # ---------- p13: two ways to act
        d = n.say("p13")
        pi = softmax(Q, 0.3); note("softmax of tick-3693 Q at T=0.3", LIFE_NPZ, "softmax(Q, 0.3)", np.round(pi, 3).tolist())
        left = Bars(vmax=1.0, height=2.0, fmt="{:.3f}", title="EXP-01:  softmax(Q / T),  T = 0.3", symmetric=False).scale(0.85).move_to([-3.4, -0.9, 0])
        left.set_values(pi)
        right = Bars(vmax=0.004, height=2.0, title="EXP-02:  highest Q, 9 times in 10").scale(0.85).move_to([3.4, -0.9, 0])
        right.set_values(Q); right.highlight(int(np.argmax(Q)))
        n.until("p13", "softmax"); self.play(FadeIn(left), run_time=0.6)
        n.until("p13", "second"); self.play(FadeIn(right), run_time=0.6)
        dice = T("1 in 10: a dice over all three", SZ_TINY, C_T).next_to(right, DOWN, buff=0.5)
        n.until("p13", "dice"); self.play(FadeIn(dice), run_time=0.5)
        gap = T(f"LEFT − RIGHT = {Q[0]-Q[1]:+.4f}", SZ_TINY, C_SP).next_to(dice, DOWN, buff=0.2)
        n.until("p13", "three thousandths"); self.play(FadeIn(gap), Indicate(right.rects[0], color=MOVE[0]), run_time=0.7)
        n.end(); self.play(FadeOut(VGroup(left, right, dice, gap)), run_time=0.4)

        # ---------- p14: symmetry: only contrasts know left from right
        d = n.say("p14")
        con = VGroup(*[T(nm, SZ_TINY, C_X) for nm in names[:3]]).arrange(DOWN, buff=0.2)
        oth = VGroup(*[T(nm, SZ_TINY, DIM) for nm in names[3:]]).arrange(DOWN, buff=0.15)
        ctitle = T("flip sign if antennae swap", SZ_TINY, C_X); otitle = T("same for both antennae", SZ_TINY, DIM)
        gcon = VGroup(ctitle, con).arrange(DOWN, buff=0.25); goth = VGroup(otitle, oth).arrange(DOWN, buff=0.25)
        groups = VGroup(gcon, goth).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([-3.6, -0.5, 0])
        n.until("p14", "contrast"); self.play(FadeIn(gcon), run_time=0.6)
        n.until("p14", "Every"); self.play(FadeIn(goth), run_time=0.6)
        # the split of Q_LEFT - Q_RIGHT over day 10
        X = L["x"]; Wt = L["theta_w"]; Bt = L["theta_b"]; QQ = L["Q"]
        dwv = Wt[:, 0, :] - Wt[:, 1, :]; anti = (dwv[:, :3] * X[:, :3]).sum(1); dLR = QQ[:, 0] - QQ[:, 1]; rest = dLR - anti
        note("Q_LEFT−Q_RIGHT split, day 10", LIFE_NPZ, "contrast part vs rest, mean |.| over indices 3000-3299", [float(np.abs(anti[3000:3300]).mean()), float(np.abs(rest[3000:3300]).mean())])
        sb = Bars(labels=("contrast part", "the rest"), colors=[C_X, DIM], vmax=0.01, height=2.0, width=1.1, title="Q LEFT − Q RIGHT, day 10, tick by tick").scale(0.85).move_to([3.3, -0.6, 0])
        it = ValueTracker(3000); sb.set_values([anti[3000], rest[3000]])
        n.until("p14", "knobs"); self.play(FadeIn(sb), run_time=0.5)
        sb.add_updater(lambda m: m.set_values([anti[int(it.get_value())], rest[int(it.get_value())]]))
        self.play(it.animate.set_value(3120), run_time=max(n.remaining() - 0.6, 2.0), rate_func=linear)
        sb.clear_updaters(); n.end()
        self.play(FadeOut(VGroup(groups, sb)), run_time=0.4)

        # ---------- p15: the committee's share over the life
        d = n.say("p15")
        Ct, Ut, Vt = L["theta_c"], L["theta_u"], L["theta_v"]
        hid = np.zeros(len(X))
        for i in range(len(X)):
            m = ~np.isnan(Ct[i]); z = Ct[i][m][:, None] + (Ut[i][m] @ X[i].astype(float))[:, None] + Vt[i][m]
            spv = np.logaddexp(0, z); hid[i] = spv[:, 0].sum() - spv[:, 1].sum()
        note("committee share of Q_LEFT−Q_RIGHT over the life", LIFE_NPZ, "sum softplus(z_L) − sum softplus(z_R); mean/std", [float(hid.mean()), float(hid.std())])
        ax3 = Axes(x_range=[0, 4500, 900], y_range=[-0.03, 0.02, 0.01], x_length=8.0, y_length=2.8,
                   axis_config={"color": DIM, "stroke_width": 2, "include_numbers": False}).move_to([-1.2, -0.4, 0])
        step = 5; pts = [ax3.c2p(i, hid[i]) for i in range(0, len(hid), step)]
        line = VMobject(stroke_color=C_HID, stroke_width=1.5).set_points_as_corners(pts)
        meanl = DashedLine(ax3.c2p(0, hid.mean()), ax3.c2p(4500, hid.mean()), color=C_SP, stroke_width=2)
        xl = T("waking ticks of the life", SZ_TINY, DIM).next_to(ax3, DOWN, buff=0.1)
        yl = T("committee's share of  Q LEFT − Q RIGHT", SZ_TINY, C_HID).next_to(ax3, UP, buff=0.1)
        self.play(FadeIn(ax3), FadeIn(xl), FadeIn(yl), run_time=0.5)
        self.play(Create(line), run_time=2.5)
        sigs = 1 / (1 + np.exp(-pre[:, 0]))
        sg = VGroup(T("sigmoids at tick 3693", SZ_TINY, C_HID), *[T(f"{s:.3f}", SZ_TINY) for s in sigs]).arrange(DOWN, buff=0.12).move_to([5.2, -0.4, 0])
        n.until("p15", "halfway"); self.play(FadeIn(sg), run_time=0.6)
        ml = T(f"mean {hid.mean():+.4f}", SZ_TINY, C_SP).next_to(meanl, UP, buff=0.05).shift(RIGHT * 2.5)
        n.until("p15", "constant", occurrence=1); self.play(Create(meanl), FadeIn(ml), run_time=0.6)
        n.end(); self.play(FadeOut(VGroup(ax3, line, meanl, xl, yl, sg, ml)), run_time=0.4)

        # ---------- p16: one breath, then the loop
        d = n.say("p16")
        f.set_opacity(0.45)
        big = f.copy().scale(1.3).move_to([0, 0.8, 0]); big.set_opacity(0.45)
        self.play(FadeOut(legend), Transform(f, big), run_time=0.6)
        for w_, idxs in (("resting", [2]), ("weighted", [3]), ("committee", [4, 5, 6, 7, 8, 9])):
            n.until("p16", w_); self.play(*[f[j].animate.set_opacity(1.0) for j in idxs], *[Indicate(f[j], color=C_SP) for j in idxs], run_time=0.8)
        n.until("p16", "Q"); qline = VGroup(MathTex(r"Q = -F", color=C_SP).scale(0.9), T("act on the highest Q", SZ_SMALL, C_SP)).arrange(RIGHT, buff=0.8).next_to(f, DOWN, buff=0.6)
        self.play(Write(qline), run_time=0.8)
        n.until("p16", "Stripped")
        self.play(FadeOut(f), FadeOut(qline), run_time=0.4)
        loop2 = LoopDiagram(radius=2.3).set_done(["World", "Senses", "Body", "Brain"]).shift(UP * 0.4)
        strip = T("evidence = weighted sum + committee;  energy = its negative;  the choice = the sign of a difference", SZ_TINY, C_SP).to_edge(DOWN, buff=0.5)
        if strip.width > 13.4: strip.scale_to_fit_width(13.4)
        self.play(FadeIn(loop2), FadeIn(strip), run_time=0.8)
        out = T("Brain:  x  →  F(x, ·),  three numbers", SZ_SMALL, FG).next_to(strip, UP, buff=0.35)
        self.play(Indicate(loop2.boxes["Brain"], color=C_SP), FadeIn(out), run_time=0.8)
        n.finish(tail=1.0)
