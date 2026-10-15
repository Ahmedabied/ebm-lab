"""Chapter 03 — The world and the senses."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

PHYS = os.path.join(LAB, "creature", "physics.py")
SENS = os.path.join(LAB, "creature", "senses.py")


def diffuse(f, alpha):
    """Same rule as creature/physics.diffuse (copied here so the demo is the code's rule)."""
    lap = (np.roll(f, 1, axis=-1) + np.roll(f, -1, axis=-1) + np.roll(f, 1, axis=-2) + np.roll(f, -1, axis=-2) - 4.0 * f)
    return f + alpha * lap


def bilinear(f, y, x):
    """Same as creature/physics.bilinear."""
    H, W = f.shape[-2], f.shape[-1]; y = y % H; x = x % W
    y0 = int(np.floor(y)); x0 = int(np.floor(x)); fy = y - y0; fx = x - x0; y1 = (y0 + 1) % H; x1 = (x0 + 1) % W
    return ((1 - fy) * (1 - fx) * f[..., y0, x0] + (1 - fy) * fx * f[..., y0, x1] + fy * (1 - fx) * f[..., y1, x0] + fy * fx * f[..., y1, x1])


def demo_rgb(arr, vmax, signed=False):
    """One chemical as an image: positive = food-yellow, negative (unstable demo) = red."""
    a = np.asarray(arr, dtype=np.float32)
    if signed:
        t = np.clip(a / vmax, -1, 1)
        pos = np.clip(t, 0, 1); neg = np.clip(-t, 0, 1)
        rgb = np.stack([pos * 250 + neg * 251, pos * 189 + neg * 73, pos * 47 + neg * 52], -1)
    else:
        t = np.clip(np.log1p(np.clip(a, 0, None) / (vmax * 0.03)) / np.log1p(1 / 0.03), 0, 1)
        rgb = np.stack([t * 250, t * 189, t * 47], -1)
    return rgb.astype(np.uint8)


def demo_img(arr, vmax, height=3.0, signed=False):
    im = ImageMobject(demo_rgb(arr, vmax, signed)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    im.height = height
    return im


def swap_img(mobj, arr, vmax, signed=False):
    new = ImageMobject(demo_rgb(arr, vmax, signed)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    new.height = mobj.height; new.move_to(mobj.get_center()); mobj.become(new)


def slot_column(names, values, colors, size=SZ_TINY, fmt="{:+.3f}", buff=0.12):
    rows = VGroup()
    for nm, v, col in zip(names, values, colors):
        box = Rectangle(width=1.45, height=0.36, stroke_color=DIM, stroke_width=1.2, fill_color=PANEL, fill_opacity=1)
        val = T(fmt.format(v) if v is not None else "", size - 2, col).move_to(box)
        lab = T(nm, size - 4, DIM).next_to(box, LEFT, buff=0.15)
        rows.add(VGroup(box, val, lab))
    rows.arrange(DOWN, buff=buff, aligned_edge=RIGHT)
    return rows


class Ch03(Scene):
    def construct(self):
        n = Narration(self, "03"); L = life(); cfgw = run()["meta"]["config"]["world"]
        I = 3193                                   # waking index of tick 3693 (sensed at the pre-move position of index 3192)

        # ---------------------------------------------------------------- p01: the world
        d = n.say("p01")
        loop = LoopDiagram(radius=2.6).move_to(ORIGIN)
        self.play(FadeIn(loop), run_time=0.6)
        self.play(loop.lit("World"), run_time=0.5)
        self.play(loop.lit("Senses"), run_time=0.5)
        n.until("p01", "forty")
        self.play(FadeOut(loop), run_time=0.4)
        fld = ImageMobject(field_rgb(L["fields"][3000])).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        fld.height = 6.0; fld.to_edge(LEFT, buff=0.7)
        note("real field, day 10 start", LIFE_NPZ, "fields[3000] (A,B,C)", "48x48")
        frame = Square(6.0, color=GRID, stroke_width=2).move_to(fld)
        cap = T(f"48 × 48, wraps at the edges  ·  tick {int(L['t'][3000])} (day {int(L['t'][3000]) // 350})", SZ_TINY, DIM).next_to(fld, DOWN, buff=0.2)
        self.play(FadeIn(fld), FadeIn(frame), FadeIn(cap), run_time=0.8)
        chem = VGroup(T("A", SZ_BIG, C_A), T("B", SZ_BIG, C_B), T("C", SZ_BIG, C_C)).arrange(RIGHT, buff=0.8).move_to([3.6, 2.6, 0])
        n.until("p01", "called")
        self.play(FadeIn(chem), run_time=0.5)
        food = VGroup(T("food = A + B", SZ_SMALL, FOOD), Square(0.35, fill_color=FOOD, fill_opacity=1, stroke_width=0)).arrange(RIGHT, buff=0.3)
        pois = VGroup(T("poison = B + C", SZ_SMALL, POISON), Square(0.35, fill_color=POISON, fill_opacity=1, stroke_width=0)).arrange(RIGHT, buff=0.3)
        food.move_to([3.6, 1.4, 0]); pois.move_to([3.6, 0.6, 0])
        n.until("p01", "yellow"); self.play(FadeIn(food), run_time=0.5)
        n.until("p01", "cyan"); self.play(FadeIn(pois), run_time=0.5)
        n.until("p01", "Notice")
        self.play(Indicate(food[0][7:], color=C_B), Indicate(pois[0][9:10], color=C_B), run_time=1.0)
        n.until("p01", "three")
        nf = int(cfgw["food_budget"] / cfgw["food_mass"])
        note("food/poison mass", RUN_JSON, "meta.config.world food_budget, food_mass, n_poison, poison_mass", f"{cfgw['food_budget']} vs {cfgw['n_poison']*cfgw['poison_mass']}")
        cnt = VGroup(T(f"{nf} food items × {cfgw['food_mass']:.1f} = {cfgw['food_budget']:.0f} mass", SZ_TINY, FOOD),
                     T(f"{cfgw['n_poison']} poison items × {cfgw['poison_mass']:.1f} = {cfgw['n_poison']*cfgw['poison_mass']:.0f} mass", SZ_TINY, POISON),
                     T(f"food mass ÷ poison mass = {cfgw['food_budget']/(cfgw['n_poison']*cfgw['poison_mass']):.0f}", SZ_SMALL, FG)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.6, -1.3, 0])
        self.play(FadeIn(cnt, shift=UP * 0.1), run_time=0.7)
        n.end()
        self.play(FadeOut(fld), FadeOut(frame), FadeOut(cap), FadeOut(chem), FadeOut(food), FadeOut(pois), FadeOut(cnt), run_time=0.5)

        # ---------------------------------------------------------------- p02: why spread
        d = n.say("p02")
        N = 16; src = (8, 8); emit = cfgw["emit_rate"] * cfgw["food_mass"]
        hdr = header("Why spread at all?")
        self.play(FadeIn(hdr), run_time=0.4)
        f_no = np.zeros((N, N), np.float32); f_yes = np.zeros((N, N), np.float32)
        for _ in range(60):
            f_no = f_no * cfgw["keep"]; f_no[src] += emit
            f_yes = diffuse(f_yes, cfgw["alpha"]) * cfgw["keep"]; f_yes[src] += emit
        vmax = float(max(f_no.max(), f_yes.max()))
        im_no = demo_img(f_no, vmax, 3.6).move_to([-3.4, -0.3, 0]); im_yes = demo_img(f_yes, vmax, 3.6).move_to([3.4, -0.3, 0])
        cell = 3.6 / N
        def ant_marks(center_img, cy, cx):
            c = center_img.get_center(); p = c + np.array([(cx - N / 2 + 0.5) * cell, (N / 2 - cy - 0.5) * cell, 0])
            a1 = p + np.array([-1.3 * cell, 1.0 * cell, 0]); a2 = p + np.array([1.3 * cell, 1.0 * cell, 0])
            return VGroup(Dot(p, radius=0.06, color=FG), Line(p, a1, stroke_width=2, color=FG), Line(p, a2, stroke_width=2, color=FG)), (cy - 1.0, cx - 1.3), (cy - 1.0, cx + 1.3)
        g1, t1, t2 = ant_marks(im_no, 9.5, 8.0); g2, _, _ = ant_marks(im_yes, 9.5, 8.0)
        rd_no = T(f"antenna reads  {bilinear(f_no, *t1):.3f}", SZ_TINY, C_BAD).next_to(im_no, DOWN, buff=0.2)
        rd_yes = T(f"antenna reads  {bilinear(f_yes, *t1):.3f}", SZ_TINY, C_GOOD).next_to(im_yes, DOWN, buff=0.2)
        l_no = T("no spreading", SZ_SMALL, DIM).next_to(im_no, UP, buff=0.2); l_yes = T("spreading, α = 0.18", SZ_SMALL, FG).next_to(im_yes, UP, buff=0.2)
        self.play(FadeIn(im_no), FadeIn(l_no), run_time=0.6)
        n.until("p02", "antennae")
        self.play(FadeIn(g1), FadeIn(rd_no), run_time=0.6)
        n.until("p02", "Spreading")
        self.play(FadeIn(im_yes), FadeIn(l_yes), FadeIn(g2), FadeIn(rd_yes), run_time=0.8)
        note("why-spread demo", PHYS, "diffuse rule, alpha 0.18, keep 0.95, emit 0.05 x 2.0 (computed live)", "16x16, 60 ticks")
        n.end()
        self.play(FadeOut(VGroup(l_no, l_yes, g1, g2, rd_no, rd_yes)), FadeOut(im_no), FadeOut(im_yes), FadeOut(hdr), run_time=0.5)

        # ---------------------------------------------------------------- p03: the rule
        d = n.say("p03")
        hdr = header("Diffusion: four neighbours")
        self.play(FadeIn(hdr), run_time=0.4)
        cs = 0.75
        cross = VGroup()
        pos = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0), "f": (0, 0)}
        for k, (dx, dy) in pos.items():
            sq = Square(cs, stroke_color=DIM, stroke_width=1.5, fill_color=PANEL, fill_opacity=1).move_to([dx * cs, dy * cs, 0])
            lab = T("f" if k == "f" else k, SZ_TINY, FG if k == "f" else C_X).move_to(sq)
            cross.add(VGroup(sq, lab))
        cross.move_to([-4.2, -0.4, 0])
        eq = MathTex(r"f_{\mathrm{new}}", "=", "f", "+", r"\alpha", r"\big(", r"\mathrm{up}+\mathrm{down}+\mathrm{left}+\mathrm{right}", "-", "4f", r"\big)").scale(0.8)
        eq.move_to([1.6, 1.0, 0])
        eq[4].set_color(C_T); eq[6].set_color(C_X); eq[8].set_color(FG)
        self.play(FadeIn(cross), run_time=0.5)
        n.until("p03", "Written")
        self.play(Write(eq[0:4]), run_time=0.6)
        n.until("p03", "alpha"); self.play(FadeIn(eq[4:6]), run_time=0.4)
        n.until("p03", "neighbours", 1); self.play(FadeIn(eq[6]), *[Indicate(cross[j][0], color=C_X) for j in range(4)], run_time=0.8)
        n.until("p03", "minus"); self.play(FadeIn(eq[7:10]), Indicate(cross[4][0], color=FG), run_time=0.6)
        eq2 = MathTex(r"=", "f", "+", r"4\alpha", r"\,\big(", r"\mathrm{average}", "-", "f", r"\big)").scale(0.8).next_to(eq, DOWN, buff=0.45).align_to(eq[1], LEFT)
        eq2[3].set_color(C_T); eq2[5].set_color(C_X)
        n.until("p03", "four", 2)
        self.play(Write(eq2), run_time=1.0)
        n.until("p03", "seventy")
        pct = T("4 × 0.18 = 0.72 of the way, every tick", SZ_SMALL, C_T).next_to(eq2, DOWN, buff=0.4).align_to(eq2, LEFT)
        note("alpha", RUN_JSON, "meta.config.world.alpha", cfgw["alpha"])
        self.play(FadeIn(pct), run_time=0.5)
        # a spike spreading over ten ticks
        f = np.zeros((N, N), np.float32); f[src] = 1.0
        im = demo_img(f, 1.0, 2.6).move_to([-4.2, -0.4, 0])
        tl = T("tick 0", SZ_TINY, DIM).next_to(im, DOWN, buff=0.15)
        self.play(FadeOut(cross), FadeIn(im), FadeIn(tl), run_time=0.5)
        step = max((n.remaining() - 0.3) / 10, 0.25)
        for k in range(1, 11):
            f = diffuse(f, cfgw["alpha"]); swap_img(im, f, 1.0); tl.become(T(f"tick {k}", SZ_TINY, DIM).next_to(im, DOWN, buff=0.15))
            self.wait(step)
        n.end()
        self.play(FadeOut(im), FadeOut(tl), FadeOut(eq), FadeOut(eq2), FadeOut(pct), FadeOut(hdr), run_time=0.5)

        # ---------------------------------------------------------------- p04: pause and predict, instability
        d = n.say("p04")
        pause_card(self, "α = 0.30.  What happens?", hold=2.2)
        fa = np.zeros((N, N), np.float32); fa[src] = 1.0; fb = fa.copy()
        ima = demo_img(fa, 1.0, 3.4, signed=True).move_to([-3.4, 0.1, 0]); imb = demo_img(fb, 1.0, 3.4, signed=True).move_to([3.4, 0.1, 0])
        la = T("α = 0.18", SZ_SMALL, C_GOOD).next_to(ima, UP, buff=0.2); lb = T("α = 0.30", SZ_SMALL, C_BAD).next_to(imb, UP, buff=0.2)
        ma = T("max 1.00", SZ_TINY, DIM).next_to(ima, DOWN, buff=0.15); mb = T("max 1.00", SZ_TINY, DIM).next_to(imb, DOWN, buff=0.15)
        self.play(FadeIn(ima), FadeIn(imb), FadeIn(la), FadeIn(lb), FadeIn(ma), FadeIn(mb), run_time=0.6)
        n.until("p04", "Watch")
        for k in range(1, 15):
            fa = diffuse(fa, 0.18); fb = diffuse(fb, 0.30)
            swap_img(ima, fa, max(float(fa.max()), 1e-6), True); swap_img(imb, fb, max(1.0, float(np.abs(fb).max()) * 0.5), True)
            ma.become(T(f"max {fa.max():.2f}", SZ_TINY, DIM).next_to(ima, DOWN, buff=0.15))
            mb.become(T(f"max |f| {np.abs(fb).max():.1f}", SZ_TINY, C_BAD).next_to(imb, DOWN, buff=0.15))
            self.wait(0.35)
        note("instability demo", PHYS, "diffuse rule at alpha 0.18 vs 0.30 (computed live); assert alpha <= 0.25", "checkerboard grows")
        n.until("p04", "refuses")
        axis = NumberLine(x_range=[0, 0.4, 0.1], length=5.0, color=DIM, include_numbers=True, font_size=18).to_edge(DOWN, buff=0.6)
        m18 = Dot(axis.n2p(0.18), color=C_GOOD); m25 = Line(axis.n2p(0.25) + DOWN * 0.25, axis.n2p(0.25) + UP * 0.25, color=C_SP, stroke_width=3); m30 = Dot(axis.n2p(0.30), color=C_BAD)
        lim = T("0.25: the code refuses anything above", SZ_TINY, C_SP).next_to(m25, UP, buff=0.1)
        self.play(FadeIn(axis), FadeIn(m18), FadeIn(m25), FadeIn(m30), FadeIn(lim), run_time=0.7)
        n.end()
        self.play(FadeOut(VGroup(la, lb, ma, mb, axis, m18, m25, m30, lim)), FadeOut(ima), FadeOut(imb), run_time=0.5)

        # ---------------------------------------------------------------- p05: decay and emit
        d = n.say("p05")
        hdr = header("Decay and emit")
        self.play(FadeIn(hdr), run_time=0.4)
        ax = Axes(x_range=[0, 300, 100], y_range=[0, 32, 10], x_length=6.0, y_length=3.2, axis_config={"color": DIM, "include_numbers": True, "font_size": 18}).move_to([-2.6, -0.5, 0])
        xl = T("ticks", SZ_TINY, DIM).next_to(ax.x_axis, DOWN, buff=0.1); yl = T("total smell mass", SZ_TINY, DIM).next_to(ax.y_axis, UP, buff=0.1)
        ts = np.arange(301); m_nodecay = emit * ts; m_decay = np.zeros(301)
        for t in range(1, 301): m_decay[t] = m_decay[t - 1] * cfgw["keep"] + emit
        c1 = ax.plot_line_graph(ts, m_nodecay, line_color=C_BAD, add_vertex_dots=False, stroke_width=3)
        c2 = ax.plot_line_graph(ts, m_decay, line_color=C_GOOD, add_vertex_dots=False, stroke_width=3)
        l1 = T("no decay: climbs forever", SZ_TINY, C_BAD).move_to([2.9, 1.2, 0]); l2 = T("keep 95%: settles at emit ÷ 0.05", SZ_TINY, C_GOOD).next_to(l1, DOWN, buff=0.3)
        self.play(FadeIn(ax), FadeIn(xl), FadeIn(yl), run_time=0.5)
        n.until("p05", "Without")
        self.play(Create(c1), FadeIn(l1), run_time=1.2)
        n.until("p05", "keeps")
        self.play(Create(c2), FadeIn(l2), run_time=1.2)
        note("decay/emit demo", PHYS, "decay keep 0.95; emit 0.05 per tick per unit mass (computed live)", "1 item, 300 ticks")
        n.until("p05", "Emit")
        cellsq = Square(1.0, stroke_color=DIM, stroke_width=1.5, fill_color=PANEL, fill_opacity=1).move_to([2.9, -1.5, 0])
        item = Dot(cellsq.get_center(), radius=0.12, color=FOOD)
        lab = MathTex(r"+\,\mathrm{blend}\times\mathrm{mass}\times 0.05", color=FOOD).scale(0.6).next_to(cellsq, DOWN, buff=0.15)
        self.play(FadeIn(cellsq), FadeIn(item), FadeIn(lab), run_time=0.5)
        for _ in range(4):
            self.play(cellsq.animate.set_fill(FOOD, 0.6), run_time=0.25); self.play(cellsq.animate.set_fill(PANEL, 1.0), run_time=0.35)
        n.end()
        self.play(FadeOut(VGroup(ax, xl, yl, c1, c2, l1, l2, cellsq, item, lab, hdr)), run_time=0.5)

        # ---------------------------------------------------------------- p06: the ledger
        d = n.say("p06")
        led = run()["meta"]["world_ledger"]; note("world ledger", RUN_JSON, "meta.world_ledger", led)
        hdr = header("The ledger")
        rows = VGroup()
        for name, key, col in (("emitted", "emitted", FOOD), ("decayed", "decayed", DIM), ("eaten", "eaten_food", C_GOOD)):
            rows.add(VGroup(T(name, SZ_BODY, col), T(f"{led[key]:.2f}", SZ_BODY, col)).arrange(RIGHT, buff=0.6, aligned_edge=DOWN))
        rows.arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to([-1.0, 0.2, 0])
        self.play(FadeIn(hdr), FadeIn(rows), run_time=0.6)
        chk = T("✓ books closed this tick", SZ_SMALL, C_GOOD).move_to([3.6, 0.2, 0])
        n.until("p06", "test")
        for _ in range(5):
            self.play(FadeIn(chk), run_time=0.2); self.wait(0.25); self.play(FadeOut(chk), run_time=0.15)
        self.play(FadeIn(chk), run_time=0.2)
        src_lab = T("seed 203, whole life (run.json world_ledger)", SZ_TINY, DIM).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(src_lab), run_time=0.3)
        n.end()
        self.play(FadeOut(VGroup(hdr, rows, chk, src_lab)), run_time=0.5)

        # ---------------------------------------------------------------- p07: the senses
        d = n.say("p07")
        hdr = header("The senses")
        self.play(FadeIn(hdr), run_time=0.4)
        f3 = L["fields"][I].astype(np.float32); y, x, h = float(L["y"][I - 1]), float(L["xpos"][I - 1]), float(L["h"][I - 1])
        note("tick 3693 field + pre-move pose", LIFE_NPZ, "fields[3193], y/xpos/h[3192]", f"({y:.2f},{x:.2f},{h:.2f})")
        # zoomed crop 12x12 around the creature
        R = 6; yy = (np.arange(int(y) - R, int(y) + R)) % 48; xx = (np.arange(int(x) - R, int(x) + R)) % 48
        crop = f3[:, yy][:, :, xx]
        zoom = ImageMobject(field_rgb(crop)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"]); zoom.height = 5.2; zoom.move_to([-3.6, -0.4, 0])
        zc = zoom.get_center(); cs2 = 5.2 / (2 * R)
        def pt(py, px): return zc + np.array([(px - int(x) + R - R + 0.0) * cs2, (-(py - int(y) + R - R)) * cs2, 0])
        # in the crop, cell (int(y)-R) is row 0 at the top; creature at (y - int(y) + R) rows down
        def pt(py, px):
            row = py - (int(y) - R); colx = px - (int(x) - R)
            return zc + np.array([(colx - R) * cs2, (R - row) * cs2, 0])
        body_dot = Dot(pt(y, x), radius=0.09, color=FG)
        aL = h + np.deg2rad(45); aR = h - np.deg2rad(45)
        tipL = (y + 1.5 * np.sin(aL), x + 1.5 * np.cos(aL)); tipR = (y + 1.5 * np.sin(aR), x + 1.5 * np.cos(aR))
        antL = Line(pt(y, x), pt(*tipL), stroke_width=3, color=FG); antR = Line(pt(y, x), pt(*tipR), stroke_width=3, color=FG)
        self.play(FadeIn(zoom), FadeIn(body_dot), run_time=0.6)
        n.until("p07", "antennae")
        self.play(Create(antL), Create(antR), run_time=0.8)
        spec = T("±45°, 1.5 cells", SZ_TINY, DIM).next_to(zoom, DOWN, buff=0.15)
        self.play(FadeIn(spec), run_time=0.3)
        rawL = bilinear(f3, *tipL); rawR = bilinear(f3, *tipR)
        note("raw antenna reads (recomputed, before noise)", LIFE_NPZ, "bilinear(fields[3193]) at the tips", f"L {np.round(rawL,4)} R {np.round(rawR,4)}")
        n.until("p07", "three")
        colL = slot_column(["A", "B", "C"], rawL, [C_A, C_B, C_C], fmt="{:.4f}"); colR = slot_column(["A", "B", "C"], rawR, [C_A, C_B, C_C], fmt="{:.4f}")
        hL = T("left tip", SZ_TINY, FG); hR = T("right tip", SZ_TINY, FG)
        gL = VGroup(hL, colL).arrange(DOWN, buff=0.2); gR = VGroup(hR, colR).arrange(DOWN, buff=0.2)
        six = VGroup(gL, gR).arrange(RIGHT, buff=1.0).move_to([3.2, 0.2, 0])
        self.play(FadeIn(gL), run_time=0.5); self.play(FadeIn(gR), run_time=0.5)
        n.until("p07", "Six")
        sixlab = T("six raw numbers: all the creature can know", SZ_SMALL, C_X).next_to(six, DOWN, buff=0.5)
        self.play(FadeIn(sixlab), run_time=0.5)
        n.until("p07", "No")
        nol = T("no positions · no labels · no map", SZ_TINY, DIM).next_to(sixlab, DOWN, buff=0.25)
        self.play(FadeIn(nol), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(sixlab, nol, hdr)), run_time=0.4)

        # ---------------------------------------------------------------- p08: log + noise
        d = n.say("p08")
        hdr = header("log, then noise")
        self.play(FadeIn(hdr), run_time=0.3)
        lgL = np.log1p(rawL / 0.05); lgR = np.log1p(rawR / 0.05)
        eqlog = MathTex(r"\log\!\left(1 + \frac{c}{0.05}\right)", color=C_X).scale(0.8).next_to(six, UP, buff=0.55)
        self.play(FadeIn(eqlog), run_time=0.4)
        n.until("p08", "log")
        newL = slot_column(["A", "B", "C"], lgL, [C_A, C_B, C_C], fmt="{:.4f}").move_to(colL); newR = slot_column(["A", "B", "C"], lgR, [C_A, C_B, C_C], fmt="{:.4f}").move_to(colR)
        self.play(Transform(colL, newL), Transform(colR, newR), run_time=1.0)
        n.until("p08", "noise")
        nz = T("+ noise, σ = 0.02", SZ_SMALL, C_T).next_to(six, DOWN, buff=0.4)
        self.play(FadeIn(nz), run_time=0.4)
        rng = np.random.default_rng(3)
        for _ in range(8):
            jL = lgL + rng.normal(0, 0.02, 3); jR = lgR + rng.normal(0, 0.02, 3)
            colL.become(slot_column(["A", "B", "C"], jL, [C_A, C_B, C_C], fmt="{:.4f}").move_to(colL))
            colR.become(slot_column(["A", "B", "C"], jR, [C_A, C_B, C_C], fmt="{:.4f}").move_to(colR))
            self.wait(0.22)
        note("noise", SENS, "SenseConfig.noise", 0.02)
        n.end()
        self.play(FadeOut(VGroup(nz, hdr, eqlog)), run_time=0.4)

        # ---------------------------------------------------------------- p09: contrast
        d = n.say("p09")
        hdr = header("Contrast")
        self.play(FadeIn(hdr), FadeOut(zoom), FadeOut(body_dot), FadeOut(antL), FadeOut(antR), FadeOut(spec), FadeOut(six), run_time=0.6)
        Lv, Rv = float(lgL[0]), float(lgR[0])
        num = MathTex("L", "-", "R", color=FG).scale(1.0)
        frac = MathTex(r"\mathrm{contrast}", "=", r"\frac{L - R}{|L| + |R| + \varepsilon}").scale(1.0)
        frac.move_to([-3.6, 1.9, 0]); num.move_to(frac[2].get_center() + UP * 0.35)
        self.play(Write(frac[0:2]), FadeIn(num), run_time=0.8)
        n.until("p09", "divided")
        self.play(FadeOut(num), FadeIn(frac[2]), run_time=0.6)
        n.until("p09", "difference", 1)
        why1 = T("the difference: which side is stronger", SZ_SMALL, C_X).move_to([-6.6, 0.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(why1), run_time=0.4)
        n.until("p09", "fifteen")
        why2 = VGroup(T("raw log difference ≈ 0.15  →  a decisive turn would need knobs ≈ 13", SZ_SMALL, C_BAD),
                      T("÷ the total  →  order one  →  knobs of order one are enough", SZ_SMALL, C_GOOD)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(why1, DOWN, buff=0.35).align_to(why1, LEFT)
        self.play(FadeIn(why2), run_time=0.6)
        note("A9 reason for contrast", SENS, "module comment (raw L-R ~0.15 log units, weights ~13)", "")
        real = T(f"this tick, A:  ({Lv:.3f} − {Rv:.3f}) ÷ ({Lv:.3f} + {Rv:.3f} + 0.05) = {(Lv - Rv)/(abs(Lv)+abs(Rv)+0.05):.2f}   (before noise; the brain got {L['x'][I][0]:.2f})", SZ_TINY, FG)
        real.scale_to_fit_width(min(real.width, 12.8)).next_to(why2, DOWN, buff=0.35).align_to(why2, LEFT)
        note("contrast_A at tick 3693", LIFE_NPZ, "x[3193][0] (with noise) vs recomputed from fields", f"{L['x'][I][0]:.3f} vs {(Lv - Rv)/(abs(Lv)+abs(Rv)+0.05):.3f}")
        self.play(FadeIn(real), run_time=0.5)
        n.until("p09", "constant", 1)
        eps_card = VGroup(T("far from everything:  L = 0.02, R = −0.01  (just noise)", SZ_SMALL, DIM),
                          T("without ε:  0.03 ÷ 0.03 = 1.00   a random number", SZ_SMALL, C_BAD),
                          T("with ε = 0.05:  0.03 ÷ 0.08 = 0.38   pinned toward zero", SZ_SMALL, C_GOOD)).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(real, DOWN, buff=0.35).align_to(why2, LEFT)
        if eps_card.get_bottom()[1] < -3.1: eps_card.shift(UP * (-3.1 - eps_card.get_bottom()[1]))
        self.play(FadeIn(eps_card), run_time=0.6)
        n.until("p09", "ears")
        ears = T("your ears: louder side ÷ both together (a log ratio; the creature divides logged readings)", SZ_TINY, C_HID).to_edge(DOWN, buff=0.4)
        ears.scale_to_fit_width(min(ears.width, 13.2))
        self.play(FadeIn(ears), run_time=0.5)
        n.end()
        self.play(FadeOut(VGroup(hdr, frac, why1, why2, real, eps_card, ears)), run_time=0.5)

        # ---------------------------------------------------------------- p10: mean and change
        d = n.say("p10")
        hdr = header("Mean and change")
        self.play(FadeIn(hdr), run_time=0.3)
        mean = 0.5 * (lgL + lgR)
        colM = slot_column(["mean A", "mean B", "mean C"], mean, [C_A, C_B, C_C], fmt="{:.4f}").move_to([-3.8, 0.9, 0])
        self.play(FadeIn(colM), run_time=0.6)
        n.until("p10", "change")
        ch = L["x"][I][6:9]; note("change at tick 3693", LIFE_NPZ, "x[3193][6:9]", np.round(ch, 4))
        colC = slot_column(["change A", "change B", "change C"], ch, [C_A, C_B, C_C], fmt="{:+.4f}").next_to(colM, DOWN, buff=0.5).align_to(colM, RIGHT)
        arrows = VGroup(*[Arrow(ORIGIN, UP * 0.35 if v > 0 else DOWN * 0.35, color=C_GOOD if v > 0 else C_BAD, stroke_width=3, max_tip_length_to_length_ratio=0.4).next_to(row, RIGHT, buff=0.15) for row, v in zip(colC, ch)])
        self.play(FadeIn(colC), FadeIn(arrows), run_time=0.6)
        n.until("p10", "bacterium")
        # one-nose steering: a dot on a 1-D gradient
        ax2 = NumberLine(x_range=[0, 10, 1], length=5.5, color=DIM).move_to([3.2, -0.6, 0])
        grad = ax2.copy().set_stroke(width=14, color=FOOD, opacity=0.35)
        src = Dot(ax2.n2p(9), color=FOOD, radius=0.14); bug = Dot(ax2.n2p(2), color=FG, radius=0.1)
        lbl = T("one nose: run while it rises, turn when it falls", SZ_TINY, DIM).next_to(ax2, DOWN, buff=0.3)
        self.play(FadeIn(grad), FadeIn(ax2), FadeIn(src), FadeIn(bug), FadeIn(lbl), run_time=0.5)
        self.play(bug.animate.move_to(ax2.n2p(4.5)), run_time=0.9, rate_func=linear)
        self.play(bug.animate.move_to(ax2.n2p(3.6)), run_time=0.5, rate_func=linear)   # drifted away: smell fell
        tumble = T("falls → turn", SZ_TINY, C_BAD).next_to(bug, UP, buff=0.15)
        self.play(FadeIn(tumble), Rotate(bug, PI), run_time=0.4)
        self.play(FadeOut(tumble), bug.animate.move_to(ax2.n2p(8.4)), run_time=max(n.remaining() - 0.2, 0.8), rate_func=linear)
        n.end()
        self.play(FadeOut(VGroup(hdr, grad, ax2, src, bug, lbl, arrows)), run_time=0.4)

        # ---------------------------------------------------------------- p11: body, one, the full x
        d = n.say("p11")
        hdr = header("x, twelve numbers")
        self.play(FadeIn(hdr), FadeOut(six), run_time=0.3)
        xv = L["x"][I]; names = L["input_names"]
        note("x at tick 3693", LIFE_NPZ, "x[3193]", np.round(xv, 4))
        cols = [C_A, C_B, C_C] * 3 + [C_E, C_XT, FG]
        full = slot_column(names, xv, cols, size=SZ_SMALL, fmt="{:+.3f}", buff=0.07).move_to([1.6, -0.25, 0])
        if full.height > 6.2: full.scale_to_fit_height(6.2)
        # bring the existing mean/change columns to their slots, then add body and one
        self.play(FadeOut(colM), FadeOut(colC), FadeIn(full[0:3]), FadeIn(full[3:9]), run_time=0.7)
        n.until("p11", "energy")
        self.play(FadeIn(full[9:11]), run_time=0.5)
        n.until("p11", "constant")
        self.play(FadeIn(full[11]), run_time=0.5)
        n.until("p11", "Twelve")
        brace = Brace(full, LEFT, color=DIM); xl = MathTex("x", color=C_X).scale(1.4).next_to(brace, LEFT, buff=0.2)
        tk = T("tick 3693, day 10  (with the noise the brain actually got)", SZ_TINY, DIM).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(brace), FadeIn(xl), FadeIn(tk), run_time=0.6)
        n.end()
        self.play(FadeOut(VGroup(hdr, full, brace, xl, tk)), run_time=0.5)

        # ---------------------------------------------------------------- p12: connections
        d = n.say("p12")
        loop2 = LoopDiagram(radius=2.6).set_done(["World", "Senses"]).move_to(ORIGIN)
        self.play(FadeIn(loop2), run_time=0.6)
        arr_lab = T("x, 12 numbers, every tick", SZ_TINY, C_X).next_to(loop2.boxes["Senses"], RIGHT, buff=0.25).shift(DOWN * 0.45)
        self.play(FadeIn(arr_lab), run_time=0.4)
        n.until("p12", "body")
        self.play(Indicate(loop2.boxes["Body"], color=FG, scale_factor=1.04), run_time=0.5)
        n.until("p12", "brain")
        self.play(loop2.lit("Brain"), run_time=0.5)
        n.until("p12", "Stripped")
        line = T("the senses turn a smell map into twelve numbers; the one that steers is the contrast", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.5)
        line.scale_to_fit_width(min(line.width, 13.2))
        self.play(FadeIn(line), run_time=0.6)
        n.finish(tail=1.0)
