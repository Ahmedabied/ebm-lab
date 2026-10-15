"""Reusable moving pictures. Every widget takes real values and has a set_* method so a scene can
animate 'what each change does to the picture' with ValueTracker/updaters or .animate."""
import numpy as np
from manim import *
from .theme import *
from . import data as D


# ---------------------------------------------------------------- world view (real fields + creature)
class WorldView(Group):
    """The 48x48 chemical fields as an image (A red, B green, C blue), the creature with two antennae
    and a fading trail, all read from the replay dump at tick index i (waking-tick index into life203)."""
    def __init__(self, size=6.0, trail=120, **kw):
        super().__init__(**kw)
        self.L = D.life(); self.size = size; self.trail = trail
        self.img = ImageMobject(D.field_rgb(self.L["fields"][0])).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        self.img.height = size
        self.frame = Square(side_length=size, color=GRID, stroke_width=2)
        self.path = VMobject(stroke_color=FG, stroke_width=2, stroke_opacity=0.8)
        self.body = Dot(radius=0.07, color=FG)
        self.antL = Line(ORIGIN, ORIGIN, stroke_color=FG, stroke_width=2)
        self.antR = Line(ORIGIN, ORIGIN, stroke_color=FG, stroke_width=2)
        self.add(self.img, self.frame, self.path, self.body, self.antL, self.antR)
        self.set_tick(0)

    def cell_to_point(self, y, x):
        s = self.size / 48.0; c = self.img.get_center()
        return c + np.array([(x - 24) * s, (24 - y) * s, 0])

    def set_tick(self, i):
        i = int(np.clip(i, 0, len(self.L["t"]) - 1)); self.i = i
        new = ImageMobject(D.field_rgb(self.L["fields"][i])).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        new.height = self.size; new.move_to(self.img.get_center()); self.img.become(new)
        y, x, h = self.L["y"][i], self.L["xpos"][i], self.L["h"][i]
        p = self.cell_to_point(y, x); self.body.move_to(p)
        for ant, sgn in ((self.antL, +1), (self.antR, -1)):
            a = h + sgn * np.deg2rad(45); ty, tx = y + 1.5 * np.sin(a), x + 1.5 * np.cos(a)
            # screen y is flipped relative to grid y; headings in the sim use (sin->y, cos->x)
            ant.put_start_and_end_on(p, self.cell_to_point(ty, tx))
        lo = max(0, i - self.trail); pts = []
        for j in range(lo, i + 1):           # break the trail where it wraps around the torus
            q = self.cell_to_point(self.L["y"][j], self.L["xpos"][j])
            if pts and np.linalg.norm(q - pts[-1]) > self.size / 4: pts = []
            pts.append(q)
        if len(pts) >= 2: self.path.set_points_as_corners(pts)
        else: self.path.set_points_as_corners([p, p])
        return self


# ---------------------------------------------------------------- three bars (Q or F or probabilities)
class Bars(VGroup):
    """Three labelled bars on a symmetric range [-vmax, vmax] (values are clipped to it), names fixed
    below the panel, the value printed at each bar's tip, an optional title above."""
    def __init__(self, labels=("LEFT", "RIGHT", "FORWARD"), colors=None, width=0.9, gap=0.6, height=2.4,
                 vmax=1.0, fmt="{:+.4f}", title=None, symmetric=True, **kw):
        super().__init__(**kw)
        colors = colors or [MOVE[0], MOVE[1], MOVE[2]]
        self.vmax, self.h, self.fmt, self.sym = float(vmax), height, fmt, symmetric
        half = 1.5 * (width + gap)
        self.base = Line(LEFT * half, RIGHT * half, color=DIM, stroke_width=2)
        self.panel = Rectangle(width=2 * half + 0.3, height=height + 0.3, stroke_width=0, fill_opacity=0).move_to(ORIGIN if symmetric else UP * height / 2)
        self.rects, self.vals, self.labs = VGroup(), VGroup(), VGroup()
        ylab = -(height / 2 + 0.45) if symmetric else -0.45
        for k, (lab, col) in enumerate(zip(labels, colors)):
            xk = (k - 1) * (width + gap)
            r = Rectangle(width=width, height=0.01, fill_color=col, fill_opacity=0.9, stroke_width=0).move_to([xk, 0, 0], aligned_edge=DOWN)
            self.rects.add(r)
            self.labs.add(T(lab, SZ_TINY, col).move_to([xk, ylab, 0]))
            self.vals.add(T("0", SZ_TINY, col).next_to(r, UP, buff=0.1))
        self.add(self.panel, self.base, self.rects, self.vals, self.labs)
        if title:
            self.title = T(title, SZ_SMALL).move_to([0, (height / 2 if symmetric else height) + 0.55, 0]); self.add(self.title)
        self.set_values([0, 0, 0])

    def y_of(self, v):
        v = float(np.clip(v, -self.vmax, self.vmax)) if self.sym else float(np.clip(v, 0, self.vmax))
        return self.h * v / (2 * self.vmax if self.sym else self.vmax)

    def set_values(self, vals, fmt=None):
        fmt = fmt or self.fmt; self.values = list(vals)
        base_y = self.base.get_center()[1]
        for r, lab, v in zip(self.rects, self.vals, self.values):
            hgt = max(abs(self.y_of(v)), 0.012); x = r.get_center()[0]
            new = Rectangle(width=r.width, height=hgt, fill_color=r.get_fill_color(), fill_opacity=r.get_fill_opacity(), stroke_width=0)
            new.move_to([x, base_y, 0], aligned_edge=DOWN if v >= 0 else UP); r.become(new)
            lab.become(T(fmt.format(v), SZ_TINY, r.get_fill_color()).next_to(r, UP if v >= 0 else DOWN, buff=0.08))
        return self

    def highlight(self, k):
        for j, r in enumerate(self.rects):
            r.set_fill(opacity=0.95 if j == k else 0.35)
        return self


# ---------------------------------------------------------------- body: E, X, D
class BodyBars(VGroup):
    def __init__(self, width=3.0, **kw):
        super().__init__(**kw)
        self.w = width
        self.rows = VGroup()
        for name, col in (("E", C_E), ("X", C_XT)):
            track = Rectangle(width=width, height=0.3, stroke_color=DIM, stroke_width=1.5)
            fill = Rectangle(width=0.001, height=0.3, fill_color=col, fill_opacity=0.9, stroke_width=0).align_to(track, LEFT)
            lab = T(name, SZ_SMALL, col).next_to(track, LEFT, buff=0.2)
            val = T("", SZ_TINY, col).next_to(track, RIGHT, buff=0.2)
            self.rows.add(VGroup(track, fill, lab, val))
        self.rows.arrange(DOWN, buff=0.35, aligned_edge=RIGHT)
        self.dlab = T("D = 0.0000", SZ_SMALL, C_D).next_to(self.rows, DOWN, buff=0.35)
        self.add(self.rows, self.dlab)

    def set_state(self, E, X, Dv=None, xmax=0.3):
        for row, v, vmax in zip(self.rows, (E, X), (1.0, xmax)):
            track, fill, lab, val = row
            new = Rectangle(width=max(track.width * min(v / vmax, 1.0), 0.001), height=track.height, fill_color=fill.get_fill_color(),
                            fill_opacity=0.9, stroke_width=0).align_to(track, LEFT).set_y(track.get_y())
            fill.become(new); val.become(T(f"{v:.3f}", SZ_TINY, fill.get_fill_color()).next_to(track, RIGHT, buff=0.2))
        if Dv is None: Dv = (1 - E) ** 2 + X ** 2
        self.dlab.become(T(f"D = {Dv:.4f}", SZ_SMALL, C_D).move_to(self.dlab))
        return self


# ---------------------------------------------------------------- the bowl D(E, X)
class Bowl(VGroup):
    """Side view of D = (1-E)^2 + X^2 along E (X fixed) with a ball; or a 2-D contour map."""
    def __init__(self, width=5.0, height=2.6, **kw):
        super().__init__(**kw)
        self.ax = Axes(x_range=[0, 1.05, 0.2], y_range=[0, 1.05, 0.25], x_length=width, y_length=height,
                       axis_config={"color": DIM, "include_numbers": False, "stroke_width": 2})
        self.xl = T("E  (energy)", SZ_TINY, C_E).next_to(self.ax.x_axis, DOWN, buff=0.1)
        self.yl = T("D", SZ_TINY, C_D).next_to(self.ax.y_axis, LEFT, buff=0.1)
        self.curve = self.ax.plot(lambda e: (1 - e) ** 2, x_range=[0, 1], color=FG, stroke_width=3)
        self.ball = Dot(color=C_E, radius=0.1)
        self.add(self.ax, self.xl, self.yl, self.curve, self.ball); self.set_state(0.8, 0.0)

    def set_state(self, E, X=0.0):
        self.ball.move_to(self.ax.c2p(E, (1 - E) ** 2 + X ** 2)); return self


# ---------------------------------------------------------------- weight heat map 3 x 12
class Heatmap(VGroup):
    def __init__(self, W, row_labels=("LEFT", "RIGHT", "FWD"), col_labels=None, cell=0.42, vmax=None, **kw):
        super().__init__(**kw)
        W = np.asarray(W); self.shape = W.shape; self.cell = cell
        self.vmax = vmax or max(float(np.abs(W).max()), 1e-6)
        self.cells = VGroup()
        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                sq = Square(side_length=cell, stroke_width=1, stroke_color=BG).move_to([j * cell, -i * cell, 0])
                self.cells.add(sq)
        self.add(self.cells)
        self.rl = VGroup(*[T(l, SZ_TINY, MOVE[i]).next_to(self.cells[i * W.shape[1]], LEFT, buff=0.15) for i, l in enumerate(row_labels)])
        self.add(self.rl)
        if col_labels:
            self.cl = VGroup(*[T(l, 22, FG).rotate(PI / 4).next_to(self.cells[(W.shape[0] - 1) * W.shape[1] + j], DOWN, buff=0.12)
                               for j, l in enumerate(col_labels)])
            self.add(self.cl)
        self.set_values(W)

    @staticmethod
    def color_of(v, vmax):
        t = float(np.clip(v / vmax, -1, 1))
        return interpolate_color(ManimColor(BG), ManimColor(C_W if t > 0 else C_X), abs(t) ** 0.7)

    def set_values(self, W, vmax=None):
        W = np.asarray(W); vmax = vmax or self.vmax
        for idx, sq in enumerate(self.cells):
            i, j = divmod(idx, self.shape[1]); sq.set_fill(self.color_of(W[i, j], vmax), opacity=1.0)
        return self


# ---------------------------------------------------------------- the growing loop diagram
LOOP_NODES = ["World", "Senses", "Brain", "Move", "Body", "Lesson", "Learning"]
class LoopDiagram(VGroup):
    """Seven boxes on a loop. lit(name) highlights, filled(name) marks a chapter done."""
    def __init__(self, radius=2.6, box_w=1.7, box_h=0.62, size=SZ_TINY + 2, **kw):
        super().__init__(**kw)
        self.boxes = {}; self.labels = {}
        n = len(LOOP_NODES)
        for k, name in enumerate(LOOP_NODES):
            ang = PI / 2 - 2 * PI * k / n
            p = radius * np.array([np.cos(ang), np.sin(ang) * 0.75, 0])
            b = RoundedRectangle(corner_radius=0.12, width=box_w, height=box_h, stroke_color=DIM, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1).move_to(p)
            l = T(name, size, DIM).move_to(p)
            self.boxes[name] = b; self.labels[name] = l; self.add(b, l)
        self.arrows = VGroup()
        for k in range(n):
            a, b = self.boxes[LOOP_NODES[k]], self.boxes[LOOP_NODES[(k + 1) % n]]
            d = b.get_center() - a.get_center(); d = d / np.linalg.norm(d)
            self.arrows.add(Arrow(a.get_boundary_point(d), b.get_boundary_point(-d), buff=0.08, color=DIM, stroke_width=2,
                                  max_tip_length_to_length_ratio=0.2, max_stroke_width_to_length_ratio=6))
        self.add(self.arrows)

    def lit(self, name, color=C_SP):
        return AnimationGroup(self.boxes[name].animate.set_stroke(color, 3), self.labels[name].animate.set_color(color))

    def filled(self, name, color=FG):
        return AnimationGroup(self.boxes[name].animate.set_stroke(color, 2).set_fill(GRID, 1), self.labels[name].animate.set_color(color))

    def set_done(self, names):
        for n in names:
            self.boxes[n].set_stroke(FG, 2).set_fill(GRID, 1); self.labels[n].set_color(FG)
        return self


# ---------------------------------------------------------------- the energy landscape (three dips + marble)
class Landscape(VGroup):
    """A smooth curve with three dips whose depths are the three energies; a marble sits in the lowest."""
    def __init__(self, width=6.0, height=2.2, **kw):
        super().__init__(**kw)
        self.lw, self.lh = width, height      # not .width/.height: those are Mobject properties
        self.curve = VMobject(stroke_color=FG, stroke_width=3)
        self.marble = Dot(radius=0.12, color=C_SP)
        self.labs = VGroup(*[T(MOVE_NAME[k], SZ_TINY, MOVE[k]) for k in range(3)])
        self.add(self.curve, self.marble, self.labs); self.set_energies([0, 0, 0])

    def set_energies(self, F, scale=1.0):
        F = np.asarray(F, dtype=float); centers = np.array([-2, 0, 2]) * self.lw / 6
        xs = np.linspace(-self.lw / 2, self.lw / 2, 160); ys = np.zeros_like(xs)
        for c, f in zip(centers, F):
            ys += -(0.9 - scale * f) * np.exp(-((xs - c) ** 2) / (2 * 0.35 ** 2)) * self.lh / 2
        ys += self.lh / 4
        pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
        self.curve.set_points_smoothly(pts)
        k = int(np.argmin(F)); j = int(np.argmin(np.abs(xs - centers[k])))
        self.marble.move_to(pts[j] + UP * 0.12)
        for k2, l in enumerate(self.labs):
            l.next_to([centers[k2], -self.lh / 2 - 0.1, 0], DOWN, buff=0.05)
        return self
