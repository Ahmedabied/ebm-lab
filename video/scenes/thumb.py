"""YouTube thumbnail: one frame, 1920x1080, saved with -s."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *


class Thumb(Scene):
    def construct(self):
        wv = WorldView(size=7.2, trail=200).set_tick(3200).to_edge(LEFT, buff=0.3)
        t1 = T("EBM lab", SZ_SMALL, DIM)
        t2 = T("lesson 01", SZ_TITLE, C_SP)
        t3 = T("every number\nin the creature's\nbrain, explained", 46, FG, line_spacing=1.0)
        f = formula_F(0.46).set_opacity(0.7)
        g = VGroup(t1, t2, t3).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(wv, RIGHT, buff=0.6).shift(UP * 0.5)
        f.next_to(g, DOWN, buff=0.6, aligned_edge=LEFT)
        if f.get_left()[0] < wv.get_right()[0] + 0.4: f.shift(RIGHT * (wv.get_right()[0] + 0.4 - f.get_left()[0]))
        self.add(wv, g, f)
