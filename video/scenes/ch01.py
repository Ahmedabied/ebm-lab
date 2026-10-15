"""Chapter 01 — The names. Thirteen words, one picture each, then where each lives in the creature."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

IDX = 3193          # waking index of tick 3693 (day 10), the worked example of the whole lesson


def tag(name, value, color, w=2.3, h=1.3):
    """A price tag: a rounded label with the move's name and its energy."""
    body = RoundedRectangle(corner_radius=0.18, width=w, height=h, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    hole = Dot(radius=0.07, color=DIM).move_to(body.get_top() + DOWN * 0.22)
    nm = T(name, SZ_TINY, color).move_to(body.get_center() + UP * 0.12)
    val = T(value, SZ_SMALL, FG).move_to(body.get_center() + DOWN * 0.3)
    g = VGroup(body, hole, nm, val); g.body, g.val, g.nm = body, val, nm
    return g


def legend():
    return T("F energy, low wins   |   Q = minus F, high wins", SZ_TINY, DIM).to_corner(DR, buff=0.3)


def knob(radius=0.22, angle=0.0, color=C_W):
    c = Circle(radius=radius, stroke_color=color, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    tick = Line(ORIGIN, UP * radius * 0.8, stroke_color=color, stroke_width=3).rotate(angle, about_point=ORIGIN)
    g = VGroup(c, tick); g.tick = tick; return g


def model_box(n_knobs=5):
    box = RoundedRectangle(corner_radius=0.2, width=4.2, height=2.6, stroke_color=FG, stroke_width=2.5, fill_color=PANEL, fill_opacity=1)
    knobs = VGroup(*[knob() for _ in range(n_knobs)]).arrange(RIGHT, buff=0.35).next_to(box.get_top(), DOWN, buff=0.25)
    ins = VGroup(*[Line(LEFT * 0.7, ORIGIN, stroke_color=C_X, stroke_width=2) for _ in range(12)]).arrange(DOWN, buff=0.08).next_to(box, LEFT, buff=0)
    outs = VGroup()
    for k in range(3):
        bar = Rectangle(width=0.8, height=0.35, fill_color=MOVE[k], fill_opacity=0.9, stroke_width=0)
        outs.add(bar)
    outs.arrange(DOWN, buff=0.25).next_to(box, RIGHT, buff=0.35)
    g = VGroup(box, knobs, ins, outs); g.box, g.knobs, g.ins, g.outs = box, knobs, ins, outs
    return g


class Land(VGroup):
    """Three dips + marble, sized by lw/lh (the lib Landscape's self.width collides with Mobject.width)."""
    def __init__(self, lw=6.0, lh=2.2, **kw):
        super().__init__(**kw)
        self.lw, self.lh = lw, lh; self.center = np.array([0.0, 0.0, 0.0])
        self.curve = VMobject(stroke_color=FG, stroke_width=3)
        self.marble = Dot(radius=0.12, color=C_SP)
        self.labs = VGroup(*[T(MOVE_NAME[k], SZ_TINY, MOVE[k]) for k in range(3)])
        self.add(self.curve, self.marble, self.labs)
        self.centers = np.array([-2, 0, 2]) * lw / 6
    def set_energies(self, F, scale=1.0):
        F = np.asarray(F, dtype=float); c0 = self.center
        xs = np.linspace(-self.lw / 2, self.lw / 2, 160); ys = np.zeros_like(xs)
        for c, f in zip(self.centers, F):
            ys += -(0.9 - scale * f) * np.exp(-((xs - c) ** 2) / (2 * 0.35 ** 2)) * self.lh / 2
        ys += self.lh / 4
        self.pts = [c0 + np.array([x, y, 0]) for x, y in zip(xs, ys)]
        self.curve.set_points_smoothly(self.pts)
        self.marble.move_to(self.dip_point(int(np.argmin(F))))
        for k2, l in enumerate(self.labs):
            l.move_to(c0 + np.array([self.centers[k2], -self.lh / 2 - 0.35, 0]))
        return self
    def dip_point(self, k):
        xs = np.array([p[0] for p in self.pts]) - self.center[0]
        j = int(np.argmin(np.abs(xs - self.centers[k]))); return self.pts[j] + UP * 0.12
    def at(self, center):
        self.center = np.array(center, dtype=float); return self


def bottom(text, size=SZ_SMALL, color=C_SP):
    """A caption above the legend line (the legend owns the bottom-right corner)."""
    m = T(text, size, color)
    if m.width > 7.0: m.scale_to_fit_width(7.0)
    return m.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.6)


def hill_curve(width=6.0, height=2.4, color=FG):
    """A valley: y = a x^2, as a VMobject centred at the origin (bottom at y = -height/2)."""
    xs = np.linspace(-width / 2, width / 2, 120)
    a = height / ((width / 2) ** 2)
    pts = [np.array([x, a * x * x - height / 2, 0]) for x in xs]
    c = VMobject(stroke_color=color, stroke_width=3); c.set_points_smoothly(pts)
    c.f = lambda x: a * x * x - height / 2; c.slope = lambda x: 2 * a * x
    return c


class Ch01(Scene):
    def construct(self):
        n = Narration(self, "01"); L = life()
        Q = L["Q"][IDX]; Fv = -Q; x = L["x"][IDX]; names = L["input_names"]
        note("chapter 1 worked tick", LIFE_NPZ, "Q[3193] (tick 3693)", [round(float(v), 6) for v in Q])
        note("chapter 1 worked tick", LIFE_NPZ, "x[3193] (tick 3693)", [round(float(v), 4) for v in x])
        self.leg = None

        # ---------------------------------------------------------------- p01 title + loop with empty slots
        d = n.say("p01")
        title_card(self, "1", "The names", hold=0.8)
        loop = LoopDiagram(radius=2.7).move_to(ORIGIN)
        slots = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.55, height=0.22, stroke_color=GRID, stroke_width=1.5)
                         for _ in range(13)]).arrange(RIGHT, buff=0.18).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(loop), run_time=0.8)
        n.until("p01", "Thirteen", lead=0.0)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in slots], lag_ratio=0.1), run_time=1.5)
        n.end()
        self.play(FadeOut(loop), FadeOut(slots), run_time=0.5)

        # ---------------------------------------------------------------- p02 ENERGY = a price
        d = n.say("p02")
        hdr = header("Energy")
        tags = VGroup(*[tag(MOVE_NAME[k], f"{Fv[k]:+.4f}", MOVE[k]) for k in range(3)]).arrange(RIGHT, buff=0.7).shift(UP * 0.6)
        cap = T("energy of each move, tick 3693", SZ_TINY, DIM).next_to(tags, DOWN, buff=0.35)
        self.play(FadeIn(hdr), run_time=0.4)
        n.until("p02", "price")
        self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tags], lag_ratio=0.2), FadeIn(cap), run_time=1.2)
        n.until("p02", "cheapest")
        self.play(tags[0].body.animate.set_fill(GRID).set_stroke(C_SP, 4), run_time=0.6)
        n.until("p02", "changes")
        # a price changes: RIGHT drops below LEFT, the cheapest switches
        new_val = T(f"{Fv[0]-0.002:+.4f}", SZ_SMALL, FG).move_to(tags[1].val)
        self.play(Transform(tags[1].val, new_val), run_time=0.5)
        self.play(tags[0].body.animate.set_fill(PANEL).set_stroke(MOVE[0], 2.5), tags[1].body.animate.set_fill(GRID).set_stroke(C_SP, 4), run_time=0.6)
        n.until("p02", "cheapest", occurrence=1)
        back_val = T(f"{Fv[1]:+.4f}", SZ_SMALL, FG).move_to(tags[1].val)
        self.play(Transform(tags[1].val, back_val), tags[1].body.animate.set_fill(PANEL).set_stroke(MOVE[1], 2.5),
                  tags[0].body.animate.set_fill(GRID).set_stroke(C_SP, 4), run_time=0.6)
        n.until("p02", "evidence")
        qrow = VGroup(*[T(f"Q = {Q[k]:+.4f}", SZ_SMALL, MOVE[k]).next_to(tags[k], DOWN, buff=0.9) for k in range(3)])
        flip = T("same number, sign flipped: high wins", SZ_TINY, DIM).next_to(qrow, DOWN, buff=0.3)
        self.play(FadeOut(cap), LaggedStart(*[FadeIn(q, shift=UP * 0.15) for q in qrow], lag_ratio=0.2), run_time=1.0)
        self.play(FadeIn(flip), run_time=0.5)
        n.until("p02", "legend") if "legend" in n.text("p02") else n.until("p02", "every")
        self.leg = legend()
        self.play(FadeIn(self.leg), run_time=0.6)
        n.end()
        self.play(FadeOut(hdr), FadeOut(tags), FadeOut(qrow), FadeOut(flip), run_time=0.5)

        # ---------------------------------------------------------------- p03 the marble, for later
        d = n.say("p03")
        land = Land(lw=7.0, lh=2.4).at(UP * 0.4)
        land.set_energies(Fv * 100)          # real energies, scaled so the dips are visible
        scale_cap = T("tick 3693 energies, ×100 so the dips show", SZ_TINY, DIM).next_to(land.labs, DOWN, buff=0.4)
        later = bottom("a picture for later, when the table shakes")
        land.marble.move_to(land.pts[0] + UP * 0.12)
        self.play(Create(land.curve), FadeIn(land.labs), FadeIn(scale_cap), run_time=1.0)
        n.until("p03", "rolls")
        # roll along the curve to the lowest dip
        k = int(np.argmin([p[1] for p in land.pts]))
        path = VMobject().set_points_as_corners([p + UP * 0.12 for p in land.pts[:k + 1:4]])
        self.add(land.marble); self.play(MoveAlongPath(land.marble, path), run_time=1.6, rate_func=rush_into)
        n.until("p03", "warning")
        self.play(FadeIn(later), run_time=0.5)
        n.end()
        self.play(FadeOut(land), FadeOut(scale_cap), FadeOut(later), run_time=0.5)

        # ---------------------------------------------------------------- p04 MODEL = a machine with knobs
        d = n.say("p04")
        hdr = header("Model")
        mb = model_box().move_to(ORIGIN + DOWN * 0.2)
        inl = T("12 readings in", SZ_TINY, C_X).next_to(mb.ins, LEFT, buff=0.15)
        outl = T("3 energies out", SZ_TINY, DIM).next_to(mb.outs, RIGHT, buff=0.15)
        counter = T("103 knobs at birth", SZ_SMALL, C_W).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(hdr), FadeIn(mb), FadeIn(inl), FadeIn(outl), run_time=0.8)
        rng = np.random.default_rng(1)
        def twist(k, ang, rt=0.7):
            # turning one knob changes the three outputs (illustrative: no numbers are shown)
            new_h = [0.35 + 0.35 * abs(np.sin(ang + 0.9 * j + 0.4 * k)) for j in range(3)]
            anims = [Rotate(mb.knobs[k].tick, angle=ang, about_point=mb.knobs[k][0].get_center())]
            for bar, h in zip(mb.outs, new_h):
                nb = Rectangle(width=0.3 + h, height=0.35, fill_color=bar.get_fill_color(), fill_opacity=0.9, stroke_width=0).move_to(bar, aligned_edge=LEFT)
                anims.append(Transform(bar, nb))
            self.play(*anims, run_time=rt)
        n.until("p04", "decide")
        twist(1, 1.2)
        n.until("p04", "radio")
        twist(3, -1.5)
        n.until("p04", "hundred")
        self.play(FadeIn(counter), run_time=0.5)
        n.until("p04", "grows")
        plus = T("+16 per new unit", SZ_TINY, C_HID).next_to(counter, RIGHT, buff=0.5)
        self.play(FadeIn(plus, shift=RIGHT * 0.2), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(inl), FadeOut(outl), FadeOut(counter), FadeOut(plus), run_time=0.4)

        # ---------------------------------------------------------------- p05 EBM = knobs feed the price tags
        d = n.say("p05")
        hdr = header("Energy-based model")
        self.play(FadeIn(hdr), mb.animate.scale(0.8).to_edge(LEFT, buff=0.6), run_time=0.7)
        tags = VGroup(*[tag(MOVE_NAME[k], f"{Fv[k]:+.4f}", MOVE[k], w=1.9, h=1.1) for k in range(3)]).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.9)
        wires = VGroup(*[Arrow(mb.outs[k].get_right(), tags[k].get_left(), buff=0.1, color=DIM, stroke_width=2, max_tip_length_to_length_ratio=0.1) for k in range(3)])
        self.play(FadeIn(tags), Create(wires), run_time=0.8)
        tags[0].body.set_fill(GRID).set_stroke(C_SP, 4)
        n.until("p05", "prefers")
        self.play(Indicate(tags[0], color=C_SP, scale_factor=1.05), run_time=0.6)
        n.until("p05", "comparing")
        twist(2, 1.4, rt=0.5)
        nv = T(f"{Fv[0]-0.004:+.4f}", SZ_SMALL, FG).move_to(tags[2].val)
        self.play(Transform(tags[2].val, nv), tags[0].body.animate.set_fill(PANEL).set_stroke(MOVE[0], 2.5), tags[2].body.animate.set_fill(GRID).set_stroke(C_SP, 4), run_time=0.7)
        n.until("p05", "raise")
        up = [T(f"{Fv[k]+0.006:+.4f}", SZ_SMALL, FG).move_to(tags[k].val) for k in (0, 1)]
        self.play(Transform(tags[0].val, up[0]), Transform(tags[1].val, up[1]), run_time=0.7)
        n.end()
        self.play(FadeOut(hdr), FadeOut(mb), FadeOut(tags), FadeOut(wires), run_time=0.5)

        # ---------------------------------------------------------------- p06 TEMPERATURE: the table shakes
        d = n.say("p06")
        hdr = header("Temperature")
        land_center = LEFT * 3.0 + DOWN * 0.3
        land = Land(lw=6.0, lh=2.2).at(land_center); land.set_energies(Fv * 100)
        Tt = ValueTracker(0.02)
        dial = VGroup(T("T", SZ_SMALL, C_T), NumberLine(x_range=[0, 2, 0.5], length=3.0, color=DIM, include_numbers=False, stroke_width=2)).arrange(RIGHT, buff=0.25).next_to(land.labs, DOWN, buff=0.55)
        pin = Triangle(color=C_T, fill_opacity=1).scale(0.12).rotate(PI)
        pin.add_updater(lambda m: m.move_to(dial[1].n2p(Tt.get_value()) + UP * 0.2))
        cold = T("cold", SZ_TINY, DIM).next_to(dial[1], LEFT, buff=0.15).shift(DOWN * 0.3); hot = T("hot", SZ_TINY, DIM).next_to(dial[1], RIGHT, buff=0.15).shift(DOWN * 0.3)
        pb = Bars(vmax=1.2, height=2.2, symmetric=False, fmt="{:.2f}", title="chance of each move").scale(0.85).move_to(RIGHT * 3.3 + DOWN * 0.5)
        pb.set_values(softmax(-Fv * 100, Tt.get_value()))
        rng = np.random.default_rng(7); state = {"k": int(np.argmin(Fv)), "t": 0.0}
        curve_home = land.curve.get_center().copy()
        def shake(m, dt):
            Tv = Tt.get_value(); state["t"] += dt
            # the table: jitter grows with T; the marble hops between dips with the softmax chances
            m.curve.move_to(curve_home + np.array([rng.normal(0, 0.02 * Tv), rng.normal(0, 0.02 * Tv), 0]))
            if state["t"] > 0.25:
                state["t"] = 0.0; p = softmax(-Fv * 100, Tv); state["k"] = int(rng.choice(3, p=p))
            m.marble.move_to(m.dip_point(state["k"]) + np.array([rng.normal(0, 0.03 * Tv), 0, 0]))
        self.play(FadeIn(hdr), Create(land.curve), FadeIn(land.labs), FadeIn(land.marble), FadeIn(dial), FadeIn(cold), FadeIn(hot), run_time=0.9)
        self.add(pin)
        pb.set_values(softmax(-Fv * 100, 0.02)); self.play(FadeIn(pb), run_time=0.5)
        pb.add_updater(lambda m: m.set_values(softmax(-Fv * 100, Tt.get_value())))
        land.add_updater(shake)
        n.until("p06", "shakes")
        self.play(Tt.animate.set_value(0.6), run_time=1.5)
        n.until("p06", "Pause")
        land.remove_updater(shake); pb.clear_updaters(); pin.clear_updaters()
        self.play(FadeOut(land), FadeOut(pb), FadeOut(dial), FadeOut(cold), FadeOut(hot), FadeOut(pin), FadeOut(hdr), run_time=0.3)
        pause_card(self, "The table shakes as hard as it can.\nWhere does the marble spend its time?", hold=max(0.5, n.t_word("p06", "Everywhere") - self.time - 1.2))
        self.play(FadeIn(land), FadeIn(pb), FadeIn(dial), FadeIn(cold), FadeIn(hot), FadeIn(pin), FadeIn(hdr), run_time=0.3)
        pin.add_updater(lambda m: m.move_to(dial[1].n2p(Tt.get_value()) + UP * 0.2))
        land.add_updater(shake); pb.add_updater(lambda m: m.set_values(softmax(-Fv * 100, Tt.get_value())))
        self.play(Tt.animate.set_value(2.0), run_time=1.2)
        n.until("p06", "Cold")
        self.play(Tt.animate.set_value(0.02), run_time=1.2)
        n.until("p06", "restless")
        self.play(Tt.animate.set_value(1.2), run_time=1.0)
        n.until("p06", "letter")
        self.play(Tt.animate.set_value(0.3), run_time=0.8)
        n.until("p06", "warning")
        warn = bottom("the brain that won does not act by T; it uses the dice (policy)", SZ_TINY)
        self.play(FadeIn(warn), run_time=0.5)
        n.end()
        land.clear_updaters(); pb.clear_updaters(); pin.clear_updaters()
        self.play(FadeOut(hdr), FadeOut(land), FadeOut(dial), FadeOut(cold), FadeOut(hot), FadeOut(pin), FadeOut(pb), FadeOut(warn), run_time=0.5)

        # ---------------------------------------------------------------- p07 WEIGHT = one knob
        d = n.say("p07")
        hdr = header("Weight")
        reading = T(f"reading  {x[0]:.3f}", SZ_BODY, C_X); times = T("×", SZ_BODY, DIM)
        kn = knob(radius=0.45); kval = T("knob  +0.00", SZ_BODY, C_W)
        eq = T("=", SZ_BODY, DIM); prod = T("product  +0.000", SZ_BODY, FG)
        row = VGroup(reading, times, VGroup(kn, kval).arrange(DOWN, buff=0.2), eq, prod).arrange(RIGHT, buff=0.5).shift(UP * 0.8)
        ebar = Bars(labels=("energy of LEFT",), colors=[MOVE[0]], vmax=0.4, height=2.0, fmt="{:+.3f}").scale(0.8).move_to(DOWN * 1.9)
        ebar.set_values([0.0])
        self.play(FadeIn(hdr), FadeIn(row), FadeIn(ebar), run_time=0.8)
        note("chapter 1 weight demo reading", LIFE_NPZ, "x[3193][contrast_A]", float(x[0]))
        def set_knob(wv, rt=0.9):
            p = wv * float(x[0])
            self.play(Rotate(kn.tick, angle=-wv * 2.0 - kn.tick.get_angle() + PI / 2, about_point=kn[0].get_center()),
                      Transform(kval, T(f"knob  {wv:+.2f}", SZ_BODY, C_W).move_to(kval)),
                      Transform(prod, T(f"product  {p:+.3f}", SZ_BODY, FG).move_to(prod)), run_time=rt)
            ebar.set_values([-p])
        n.until("p07", "Positive")
        set_knob(0.5)
        n.until("p07", "Negative")
        set_knob(-0.5)
        n.until("p07", "Zero")
        set_knob(0.0)
        n.until("p07", "thirty")
        c36 = bottom("12 readings × 3 moves = 36 knobs w", SZ_SMALL, C_W)
        self.play(FadeIn(c36), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(row), FadeOut(ebar), FadeOut(c36), run_time=0.5)

        # ---------------------------------------------------------------- p08 VECTOR = a fixed-order list
        d = n.say("p08")
        hdr = header("Vector")
        rec = VGroup(*[T(f"{i+1}.  {it}", SZ_TINY, FG) for i, it in enumerate(["bread   1.20", "milk    0.90", "eggs    2.40", "rice    1.10", "tea     3.00"])]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        paper = Rectangle(width=rec.width + 0.6, height=rec.height + 0.6, stroke_color=DIM, stroke_width=1.5).move_to(rec)
        receipt = VGroup(paper, rec).to_edge(LEFT, buff=1.2).shift(DOWN * 0.3)
        self.play(FadeIn(hdr), FadeIn(receipt), run_time=0.7)
        n.until("p08", "fifth")
        self.play(Indicate(rec[4], color=C_SP), run_time=0.6)
        n.until("p08", "twelve")
        col = VGroup()
        for i, (nm, v) in enumerate(zip(names, x)):
            box = Rectangle(width=3.6, height=0.42, stroke_color=GRID, stroke_width=1.5)
            lab = T(f"{i+1:2d}  {nm}", SZ_TINY, C_X).scale(0.85).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.12)
            val = T(f"{v:+.3f}", SZ_TINY, FG).scale(0.85).move_to(box).align_to(box, RIGHT).shift(LEFT * 0.12)
            col.add(VGroup(box, lab, val))
        col.arrange(DOWN, buff=0.0).scale(0.95).move_to(RIGHT * 2.8 + DOWN * 0.3)
        xlab = T("x, tick 3693", SZ_SMALL, C_X).next_to(col, UP, buff=0.2)
        groups = [(0, 3, "contrasts"), (3, 6, "levels"), (6, 9, "changes"), (9, 11, "body"), (11, 12, "one")]
        self.play(FadeIn(xlab), run_time=0.3)
        for a, b, word in groups:
            n.until("p08", word if word != "one" else "constant")
            self.play(LaggedStart(*[FadeIn(col[i], shift=LEFT * 0.1) for i in range(a, b)], lag_ratio=0.3), run_time=0.6)
        n.until("p08", "four")
        self.play(Indicate(col[3], color=C_SP), run_time=0.6)
        n.end()
        self.play(FadeOut(hdr), FadeOut(receipt), FadeOut(col), FadeOut(xlab), run_time=0.5)

        # ---------------------------------------------------------------- p09 DOT PRODUCT = the grocery bill
        d = n.say("p09")
        hdr = header("Dot product")
        items = [("bread", 2, 1.20), ("milk", 1, 0.90), ("eggs", 3, 2.40), ("refund", 1, -1.50)]
        rows = VGroup()
        for nm, q, p in items:
            rows.add(VGroup(T(nm, SZ_SMALL, FG), T(f"{q}", SZ_SMALL, C_X), T("×", SZ_TINY, DIM), T(f"{p:+.2f}", SZ_SMALL, C_W), T("=", SZ_TINY, DIM), T(f"{q*p:+.2f}", SZ_SMALL, FG)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(UP * 0.7)
        bill = T(f"bill  {sum(q*p for _, q, p in items):+.2f}", SZ_BODY, C_SP).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(hdr), run_time=0.3)
        n.until("p09", "Multiply")
        self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.3), run_time=1.0)
        n.until("p09", "add")
        self.play(FadeIn(bill), run_time=0.5)
        n.until("p09", "refund")
        self.play(FadeIn(rows[3]), Transform(bill, T(f"bill  {sum(q*p for _, q, p in items):+.2f}", SZ_BODY, C_SP).move_to(bill)), run_time=0.7)
        n.until("p09", "Readings")
        lab2 = VGroup(T("readings", SZ_TINY, C_X), T("× knobs", SZ_TINY, C_W), T("= one move's evidence", SZ_TINY, FG)).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(lab2), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(rows), FadeOut(bill), FadeOut(lab2), run_time=0.5)

        # ---------------------------------------------------------------- p10 GRADIENT = the arrow uphill
        d = n.say("p10")
        hdr = header("Gradient")
        hill = hill_curve(6.0, 2.4).shift(LEFT * 3.2 + DOWN * 0.2)
        hx = -2.1; dot = Dot(color=C_SP, radius=0.11).move_to(hill.get_center() + np.array([hx, hill.f(hx) + 1.2, 0]))
        def arrow_at(xv, length=1.2):
            s = hill.slope(xv); dirv = np.array([1, s, 0]) / np.hypot(1, s)
            if xv < 0: dirv = -dirv            # uphill
            p = hill.get_center() + np.array([xv, hill.f(xv) + 1.2, 0])
            return Arrow(p, p + dirv * length, buff=0.1, color=C_T, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        arr = arrow_at(hx)
        fog = T("fog: you only feel the slope under your feet", SZ_TINY, DIM).next_to(hill, DOWN, buff=0.5)
        xl = T("one knob", SZ_TINY, C_W).next_to(hill, DOWN, buff=0.15)
        self.play(FadeIn(hdr), Create(hill), FadeIn(dot), FadeIn(xl), run_time=0.8)
        n.until("p10", "arrow")
        self.play(GrowArrow(arr), FadeIn(fog), run_time=0.6)
        n.until("p10", "against")
        for xv in (-1.4, -0.8, -0.35, -0.1):
            self.play(dot.animate.move_to(hill.get_center() + np.array([xv, hill.f(xv) + 1.2, 0])), Transform(arr, arrow_at(xv, 0.5 + abs(xv) * 0.35)), run_time=0.4)
        n.until("p10", "knobs")
        rings = VGroup(*[Ellipse(width=1.4 * k, height=0.9 * k, stroke_color=GRID, stroke_width=1.5) for k in (1, 2, 3, 4)]).move_to(RIGHT * 3.3 + DOWN * 0.3)
        d2 = Dot(color=C_SP, radius=0.11).move_to(rings.get_center() + np.array([-2.2, 1.0, 0]))
        a2 = Arrow(d2.get_center(), d2.get_center() + np.array([-0.9, 0.5, 0]), buff=0.1, color=C_T, stroke_width=4, max_tip_length_to_length_ratio=0.25)
        tl = T("two knobs: one slope per knob", SZ_TINY, C_W).next_to(rings, DOWN, buff=0.15)
        self.play(FadeIn(rings), FadeIn(d2), GrowArrow(a2), FadeIn(tl), run_time=0.8)
        n.until("p10", "every")
        for f_ in (0.6, 0.35, 0.15):
            tgt = rings.get_center() + np.array([-2.2 * f_, 1.0 * f_, 0])
            self.play(d2.animate.move_to(tgt), Transform(a2, Arrow(tgt, tgt + np.array([-0.9 * f_ - 0.2, 0.5 * f_ + 0.1, 0]), buff=0.1, color=C_T, stroke_width=4, max_tip_length_to_length_ratio=0.3)), run_time=0.4)
        n.until("p10", "guitar")
        peg = VGroup(Line(LEFT * 0.6, RIGHT * 0.6, stroke_color=FG, stroke_width=4), Circle(radius=0.22, stroke_color=C_W, stroke_width=3)).arrange(RIGHT, buff=0.05).to_edge(DOWN, buff=0.95).shift(RIGHT * 4.0)
        pegl = T("one string, one peg", SZ_TINY, DIM).next_to(peg, LEFT, buff=0.3)
        self.play(FadeIn(peg), FadeIn(pegl), run_time=0.4)
        self.play(Rotate(peg[1], angle=PI / 2), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(rings), FadeOut(d2), FadeOut(a2), FadeOut(tl), FadeOut(peg), FadeOut(pegl), FadeOut(fog), FadeOut(arr), run_time=0.5)

        # ---------------------------------------------------------------- p11 LEARNING RATE = the step size
        d = n.say("p11")
        hdr = header("Learning rate")
        self.play(FadeIn(hdr), hill.animate.move_to(DOWN * 0.3), dot.animate.move_to(np.array([-2.4, hill.f(-2.4) + 1.2, 0]) + DOWN * 0.3 - hill.get_center() + DOWN * 0.3 + np.array([0, 0, 0])), FadeOut(xl), run_time=0.7)
        hc = hill.get_center()
        def hp(xv): return hc + np.array([xv, hill.f(xv) + 1.2, 0])
        dot.move_to(hp(-2.4))
        n.until("p11", "Pause")
        self.play(FadeOut(hill), FadeOut(dot), run_time=0.3)
        pause_card(self, "The valley is one step wide.\nI take a step ten wide. Where do I land?", hold=max(0.5, n.t_word("p11", "far") - self.time - 1.2))
        self.play(FadeIn(hill), FadeIn(dot), run_time=0.3)
        lab = T("step: ten valleys wide", SZ_SMALL, C_BAD).next_to(hill, DOWN, buff=0.4)
        self.play(FadeIn(lab), run_time=0.3)
        for xv in (2.3, -2.5, 2.1, -2.6):
            self.play(dot.animate.move_to(hp(xv)), run_time=0.45, rate_func=linear)
        n.until("p11", "small")
        self.play(Transform(lab, T("step: small", SZ_SMALL, C_GOOD).move_to(lab)), run_time=0.3)
        for xv in (-1.9, -1.4, -1.0, -0.65, -0.4, -0.22, -0.1, -0.03):
            self.play(dot.animate.move_to(hp(xv)), run_time=0.22, rate_func=linear)
        n.until("p11", "Too", occurrence=1)
        self.play(Transform(lab, T("step: too big", SZ_SMALL, C_BAD).move_to(lab)), run_time=0.3)
        for xv in (2.2, -2.4, 2.4, -2.2):
            self.play(dot.animate.move_to(hp(xv)), run_time=0.4, rate_func=linear)
        n.until("p11", "eight")
        nb = bottom("EXP-01: the nightly step was 8 to 16 × the whole brain")
        self.play(FadeIn(nb), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(hill), FadeOut(dot), FadeOut(lab), FadeOut(nb), run_time=0.5)

        # ---------------------------------------------------------------- p12 LESSON = the drop in D
        d = n.say("p12")
        hdr = header("Lesson")
        body = BodyBars(width=3.2).move_to(LEFT * 2.0 + DOWN * 0.3)
        E13, X13, D13 = float(L["E"][13]), float(L["X"][13]), float(L["D"][13])
        E14, X14, D14 = float(L["E"][14]), float(L["X"][14]), float(L["D"][14]); r14 = float(L["r"][14]); rq = float(L["r"][1])
        note("chapter 1 lesson demo", LIFE_NPZ, "E, D, r at ticks 13-14 and r at tick 1", [E13, D13, E14, D14, r14, rq])
        body.set_state(E13, X13, D13)
        self.play(FadeIn(hdr), FadeIn(body), run_time=0.7)
        rl = T("r  =  D before  −  D after", SZ_SMALL, DIM).move_to(RIGHT * 3.2 + UP * 1.2)
        n.until("p12", "dropped")
        self.play(FadeIn(rl), run_time=0.4)
        body.set_state(E14, X14, D14)
        g = T(f"r = {r14:+.5f}", SZ_BIG, C_GOOD).move_to(RIGHT * 3.2 + DOWN * 0.3)
        bite = T("a bite, tick 14", SZ_TINY, FOOD).next_to(g, DOWN, buff=0.2)
        self.play(FadeIn(g, shift=UP * 0.3), FadeIn(bite), run_time=0.6)
        n.until("p12", "Rose")
        body.set_state(E14 - 0.00155, X14, (1 - (E14 - 0.00155)) ** 2)
        q = T(f"r = {rq:+.5f}", SZ_BIG, C_BAD).move_to(g); quiet = T("a quiet tick", SZ_TINY, DIM).next_to(q, DOWN, buff=0.2)
        self.play(Transform(g, q), Transform(bite, quiet), run_time=0.6)
        n.until("p12", "letter")
        self.play(Indicate(rl, color=C_SP), run_time=0.6)
        n.end()
        self.play(FadeOut(hdr), FadeOut(body), FadeOut(rl), FadeOut(g), FadeOut(bite), run_time=0.5)

        # ---------------------------------------------------------------- p13 DRIVE = the bowl
        d = n.say("p13")
        hdr = header("Drive")
        bowl = Bowl(width=5.4, height=2.6).move_to(LEFT * 2.6 + DOWN * 0.4)
        bowl.set_state(0.8, 0.0)
        self.play(FadeIn(hdr), Create(bowl.ax), FadeIn(bowl.xl), FadeIn(bowl.yl), Create(bowl.curve), run_time=0.9)
        n.until("p13", "ball")
        self.play(FadeIn(bowl.ball, scale=0.5), run_time=0.4)
        dl = T("D = height of the ball", SZ_TINY, DIM).next_to(bowl, UP, buff=0.1)
        self.play(FadeIn(dl), run_time=0.3)
        # top view: contour map with axes E, X
        ax2 = Axes(x_range=[0, 1.05, 0.5], y_range=[0, 0.35, 0.1], x_length=3.6, y_length=2.4, axis_config={"color": DIM, "include_numbers": False, "stroke_width": 2}).move_to(RIGHT * 3.3 + DOWN * 0.4)
        conts = VGroup(*[ax2.plot_parametric_curve(lambda t, rr=rr: np.array([1 - rr * np.cos(t), rr * np.sin(t), 0]), t_range=[0, PI / 2], color=GRID, stroke_width=1.5) for rr in (0.1, 0.2, 0.3)])
        ball2 = Dot(color=C_E, radius=0.09).move_to(ax2.c2p(0.8, 0.0))
        xl2 = T("E", SZ_TINY, C_E).next_to(ax2.x_axis, DOWN, buff=0.1); yl2 = T("X", SZ_TINY, C_XT).next_to(ax2.y_axis, LEFT, buff=0.1)
        n.until("p13", "Hunger")
        self.play(Create(ax2), FadeIn(conts), FadeIn(xl2), FadeIn(yl2), FadeIn(ball2), run_time=0.8)
        self.play(bowl.ball.animate.move_to(bowl.ax.c2p(0.6, 0.16)), ball2.animate.move_to(ax2.c2p(0.6, 0.0)), run_time=0.7)
        n.until("p13", "poison")
        self.play(ball2.animate.move_to(ax2.c2p(0.6, 0.25)), run_time=0.6)
        n.until("p13", "Metabolism")
        self.play(ball2.animate.move_to(ax2.c2p(0.8, 0.0)), bowl.ball.animate.move_to(bowl.ax.c2p(0.8, 0.04)), run_time=0.4)
        for e in (0.76, 0.72, 0.68):
            self.play(bowl.ball.animate.move_to(bowl.ax.c2p(e, (1 - e) ** 2)), ball2.animate.move_to(ax2.c2p(e, 0.0)), run_time=0.35, rate_func=linear)
        n.until("p13", "eating")
        self.play(bowl.ball.animate.move_to(bowl.ax.c2p(0.9, 0.01)), ball2.animate.move_to(ax2.c2p(0.9, 0.0)), run_time=0.5)
        n.until("p13", "born")
        self.play(bowl.ball.animate.move_to(bowl.ax.c2p(0.8, 0.04)), ball2.animate.move_to(ax2.c2p(0.8, 0.0)), run_time=0.5)
        born = bottom("born at E = 0.8, D = 0.04", SZ_TINY, C_E)
        self.play(FadeIn(born), run_time=0.4)
        n.end()
        self.play(FadeOut(hdr), FadeOut(bowl), FadeOut(dl), FadeOut(ax2), FadeOut(conts), FadeOut(xl2), FadeOut(yl2), FadeOut(ball2), FadeOut(born), run_time=0.5)

        # ---------------------------------------------------------------- p14 VALUE = now plus what follows
        d = n.say("p14")
        hdr = header("Value")
        N = 24; gamma = 0.9
        dots = VGroup(*[Dot(radius=0.06, color=DIM) for _ in range(N)]).arrange(RIGHT, buff=0.22).shift(UP * 1.4)
        now = dots[0]; bite_dot = dots[20]
        now.set_color(C_BAD); bite_dot.set_color(FOOD).scale(1.6)
        nl = T("now: −0.0006", SZ_TINY, C_BAD).next_to(now, DOWN, buff=0.15)
        bl = T("a bite in 20 ticks: +0.019", SZ_TINY, FOOD).next_to(bite_dot, UP, buff=0.15)
        self.play(FadeIn(hdr), FadeIn(dots), run_time=0.7)
        n.until("p14", "now")
        self.play(FadeIn(nl), run_time=0.4)
        n.until("p14", "follows")
        self.play(FadeIn(bl), run_time=0.4)
        # the stack: each future lesson shrunk by gamma^k
        base_y = 0.5; x0 = -1.0
        lessons = [-0.0006] * N; lessons[20] = 0.019
        pieces = VGroup(); y = base_y
        for k, r_ in enumerate(lessons[:21]):
            h = r_ * gamma ** k * 150
            rect = Rectangle(width=0.9, height=max(abs(h), 0.004), fill_color=C_GOOD if h > 0 else C_BAD, fill_opacity=0.9, stroke_width=0)
            rect.move_to([x0, y, 0], aligned_edge=DOWN if h > 0 else UP); y += h; pieces.add(rect)
        ql = T("Q = now + what follows, each tick shrunk by 0.9", SZ_TINY, DIM).move_to([2.6, -1.3, 0])
        stack_lab = VGroup(T("20 quiet ticks (−)", SZ_TINY, C_BAD), T("the bite, shrunk 20 times (+)", SZ_TINY, C_GOOD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([2.6, -0.4, 0])
        n.until("p14", "train")
        tk = T("ticket: pay now (−), the trip follows (+)", SZ_TINY, DIM).move_to([2.6, 0.3, 0])
        self.play(FadeIn(tk), run_time=0.4)
        n.until("p14", "smell")
        self.play(LaggedStart(*[FadeIn(p) for p in pieces], lag_ratio=0.05), FadeIn(ql), FadeIn(stack_lab), run_time=1.6)
        qlab = T("Q", SZ_BODY, C_Q).next_to(pieces, LEFT, buff=0.3)
        self.play(FadeIn(qlab), run_time=0.3)
        n.until("p14", "learner")
        self.play(Indicate(qlab, color=C_SP), run_time=0.6)
        n.end()
        self.play(FadeOut(hdr), FadeOut(dots), FadeOut(nl), FadeOut(bl), FadeOut(pieces), FadeOut(ql), FadeOut(qlab), FadeOut(tk), FadeOut(stack_lab), run_time=0.5)

        # ---------------------------------------------------------------- p15 POLICY = the habit of choosing
        d = n.say("p15")
        hdr = header("Policy")
        qb = Bars(vmax=0.004, height=2.4, title="Q(x, ·), tick 3693").move_to(LEFT * 2.8 + DOWN * 0.4)
        qb.set_values(Q); qb.highlight(int(np.argmax(Q)))
        self.play(FadeIn(hdr), FadeIn(qb), run_time=0.7)
        nine = T("9 in 10: the highest Q", SZ_SMALL, C_Q).move_to(RIGHT * 3.0 + UP * 0.9)
        die = VGroup(Square(side_length=0.8, stroke_color=C_T, stroke_width=2.5, fill_color=PANEL, fill_opacity=1), *[Dot(radius=0.06, color=C_T).shift(p) for p in (UL * 0.2, ORIGIN, DR * 0.2)]).move_to(RIGHT * 1.2 + DOWN * 0.6)
        one = T("1 in 10: a dice over all three", SZ_SMALL, C_T).next_to(die, RIGHT, buff=0.3)
        eps = T("ε = 0.1", SZ_SMALL, C_T).next_to(die, DOWN, buff=0.3)
        n.until("p15", "highest")
        self.play(FadeIn(nine), Indicate(qb.rects[0], color=C_SP), run_time=0.7)
        n.until("p15", "dice")
        self.play(FadeIn(die), FadeIn(one), run_time=0.5)
        rng = np.random.default_rng(3)
        for _ in range(3):
            k = int(rng.integers(3)); self.play(Rotate(die, angle=PI / 2), run_time=0.3); qb.highlight(k); self.wait(0.15)
        qb.highlight(0)
        n.until("p15", "fifteen")
        fif = T("the dice lands on the favourite a third of the time: about 1 tick in 15 actually differs", SZ_TINY, DIM).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(fif), run_time=0.5)
        n.until("p15", "epsilon")
        self.play(FadeIn(eps), run_time=0.4)
        n.until("p15", "Temperature")
        tv = T("T: tries other moves by the gaps      ε: one in ten, whatever the gaps", SZ_TINY, C_T).to_edge(DOWN, buff=0.9)
        self.play(Transform(fif, tv), run_time=0.5)
        n.end()
        self.play(FadeOut(hdr), FadeOut(qb), FadeOut(nine), FadeOut(die), FadeOut(one), FadeOut(eps), FadeOut(fif), FadeOut(self.leg), run_time=0.5)

        # ---------------------------------------------------------------- p16 all the words on the loop
        d = n.say("p16")
        loop = LoopDiagram(radius=2.8).move_to(ORIGIN + DOWN * 0.1)
        self.play(FadeIn(loop), run_time=0.7)
        words = {"World": ("smells", "world"), "Senses": ("vector x", "senses"), "Brain": ("weights · dot product\nenergy, Q", "weights"),
                 "Move": ("policy: T or ε", "policy"), "Body": ("drive", "drive"), "Lesson": ("lesson r", "drop"), "Learning": ("gradient · learning rate\nvalue", "gradient")}
        placed = VGroup()
        for name, (txt, cue) in words.items():
            n.until("p16", cue)
            box = loop.boxes[name]; c = box.get_center()
            outward = c - loop.get_center(); outward = outward / max(np.linalg.norm(outward), 1e-6)
            lab = T(txt, SZ_TINY, C_SP, line_spacing=1.0).move_to(c + outward * (0.75 + 0.25 * (abs(outward[1]) > 0.7)))
            if abs(outward[0]) > 0.6: lab.next_to(box, RIGHT if outward[0] > 0 else LEFT, buff=0.2)
            else: lab.next_to(box, UP if outward[1] > 0 else DOWN, buff=0.15)
            placed.add(lab)
            self.play(loop.lit(name), FadeIn(lab, shift=outward * 0.15), run_time=0.5)
        n.until("p16", "Every")
        self.play(*[loop.filled(nm) for nm in LOOP_NODES], run_time=0.8)
        n.finish(tail=1.2)
