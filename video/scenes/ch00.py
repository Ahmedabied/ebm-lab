"""Chapter 00 — Cold open. Pattern scene: every other chapter follows this shape.
Render: PATH=$HOME/.TinyTeX/bin/x86_64-linux:$PATH .venv/bin/manim -qh --fps 60 scenes/ch00.py Ch00"""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np


class Ch00(Scene):
    def construct(self):
        n = Narration(self, "00"); L = life()
        tick = ValueTracker(0)
        wv = WorldView(size=6.2).to_edge(LEFT, buff=0.6)
        wv.add_updater(lambda m: m.set_tick(int(tick.get_value())))
        cap = caption("seed 203  ·  arm ebm-td  ·  linear world  ·  replayed from run.json", SZ_TINY)
        note("cold open replay", LIFE_NPZ, "fields, y, xpos, h, Q, a, E, X", "ticks 0-420")

        # p01: the world, replayed
        d = n.say("p01")
        self.play(FadeIn(wv), FadeIn(cap), run_time=0.8)
        self.play(tick.animate.set_value(140), run_time=d - 0.8, rate_func=linear)
        # labels land on their words
        food_lab = T("food smell", SZ_SMALL, FOOD).next_to(wv, UP, buff=0.25).shift(LEFT * 1.6)
        pois_lab = T("poison smell", SZ_SMALL, POISON).next_to(wv, UP, buff=0.25).shift(RIGHT * 1.6)
        # (labels appear during p01 at the words 'yellow' and 'cyan'; they were timed above by the
        #  linear run; to keep the replay continuous we add them with updaters keyed to time)
        self.add(food_lab, pois_lab)

        # p02: the three scores and the body
        d = n.say("p02")
        bars = Bars(vmax=0.05, height=2.2, title="Q(x, ·)  =  the score of each move").scale(0.9)
        bars.move_to([3.6, 1.3, 0])
        body = BodyBars(width=2.6).scale(0.8).move_to([3.6, -2.0, 0])
        def upd_bars(m):
            i = int(tick.get_value()); m.set_values(L["Q"][i]); m.highlight(int(L["a"][i]))
        def upd_body(m):
            i = int(tick.get_value()); m.set_state(float(L["E"][i]), float(L["X"][i]), float(L["D"][i]))
        # updaters that change text (digits) must not run during a FadeIn/FadeOut (family size changes)
        upd_bars(bars); self.play(FadeIn(bars), run_time=0.6); bars.add_updater(upd_bars)
        self.play(tick.animate.set_value(230), run_time=max(d * 0.45, 1), rate_func=linear)
        upd_body(body); self.play(FadeIn(body), run_time=0.6); body.add_updater(upd_body)
        self.play(tick.animate.set_value(300), run_time=max(n.remaining() - 0.2, 1), rate_func=linear)

        # p03: the weights and the formula, unexplained
        d = n.say("p03")
        W = nightly_w()[0]; note("weight heat map (cold open)", RUN_JSON, "brain[0].w (after night 0)", "3x12")
        hm = Heatmap(W, cell=0.3, col_labels=L["input_names"]).scale(0.85).move_to([3.6, -1.9, 0])
        f = formula_F(0.62).set_opacity(0.55).to_edge(DOWN, buff=0.25)
        body.clear_updaters(); self.play(FadeOut(body), run_time=0.4)
        self.play(FadeIn(hm), run_time=0.8)
        self.play(tick.animate.set_value(380), run_time=max(d * 0.45, 1), rate_func=linear)
        self.play(FadeOut(cap), FadeIn(f), run_time=0.8)
        self.play(tick.animate.set_value(440), run_time=max(n.remaining() - 0.2, 1), rate_func=linear)

        # p04: the loop, the order of the lesson
        d = n.say("p04")
        wv.clear_updaters(); bars.clear_updaters()
        self.play(FadeOut(wv), FadeOut(bars), FadeOut(hm), FadeOut(f), FadeOut(food_lab), FadeOut(pois_lab), run_time=0.7)
        loop = LoopDiagram(radius=2.9).move_to(ORIGIN)
        self.play(FadeIn(loop), run_time=0.8)
        order = ["World", "Senses", "Body", "Brain", "Learning", "Move", "Lesson"]
        words = ["names", "maths", "world", "senses", "body", "brain", "learning", "experiment", "code"]
        step = (d - 2.0) / len(words)
        chap = T("", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.5)
        self.add(chap)
        for k, w in enumerate(words):
            chap.become(T(f"chapter {k+1}:  {w}", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.5))
            node = {"names": None, "maths": None, "world": "World", "senses": "Senses", "body": "Body", "brain": "Brain",
                    "learning": "Learning", "experiment": "Move", "code": "Lesson"}[w]
            if node: self.play(loop.lit(node), run_time=min(step, 0.6))
            self.wait(max(step - 0.6, 0.05))
        n.finish(tail=1.2)
