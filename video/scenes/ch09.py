"""Chapter 09 — Close. Returns to the cold-open screen with every element labelled."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np


class Ch09(Scene):
    def construct(self):
        n = Narration(self, "09"); L = life()
        tick = ValueTracker(3000)
        wv = WorldView(size=5.6).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        bars = Bars(vmax=0.05, height=1.8, title="Q(x, ·)").scale(0.8).move_to([3.3, 2.0, 0])
        body = BodyBars(width=2.2).scale(0.75).move_to([3.3, -0.6, 0])
        W = nightly_w()[-1]; note("close: weight heat map", RUN_JSON, "brain[14].w (after the last night)", "3x12")
        hm = Heatmap(W, cell=0.26, col_labels=L["input_names"]).scale(0.8).move_to([3.3, -2.6, 0])
        f = formula_F(0.55).set_opacity(0.6).to_edge(DOWN, buff=0.95).shift(LEFT * 1.6)
        def upd_bars(m):
            i = int(tick.get_value()); m.set_values(L["Q"][i]); m.highlight(int(L["a"][i]))
        def upd_body(m):
            i = int(tick.get_value()); m.set_state(float(L["E"][i]), float(L["X"][i]), float(L["D"][i]))
        wv.set_tick(3000); upd_bars(bars); upd_body(body)

        # p01: the first screen, now labelled
        d = n.say("p01")
        self.play(FadeIn(wv), FadeIn(bars), FadeIn(body), FadeIn(hm), FadeIn(f), run_time=1.0)
        wv.add_updater(lambda m: m.set_tick(int(tick.get_value()))); bars.add_updater(upd_bars); body.add_updater(upd_body)
        # one label at a time, in a banner, with the element it names flashing (one idea per screen)
        labels = [("smells", "the smells: three fields A, B, C that spread, fade and leak  (chapter 3)", wv.img, FOOD),
                  ("antennae", "two antennae, a log and a contrast: the twelve numbers x  (chapter 3)", VGroup(wv.antL, wv.antR), C_X),
                  ("weights", "the weights turn x into evidence; energy is its negative  (chapter 5)", hm, C_W),
                  ("highest", "the highest Q is taken, nine times in ten  (chapter 5)", bars, C_Q),
                  ("bowl", "the body's bowl: D from E and X  (chapter 4)", body, C_E),
                  ("lesson", "the drop in D is the lesson r  (chapter 4)", body.dlab, C_GOOD),
                  ("promise", "r corrects the promise Q made; the chain walks back from the bite  (chapter 6)", f, C_SP)]
        self.play(tick.animate.set_value(3000 + 40), run_time=1.5, rate_func=linear)
        banner = T("", SZ_SMALL).to_edge(DOWN, buff=0.35)
        self.add(banner); shown = VGroup(banner)
        for word, text, target, col in labels:
            n.until("p01", word)
            lab = T(text, SZ_SMALL, col).to_edge(DOWN, buff=0.35)
            if lab.width > 13.4: lab.scale_to_fit_width(13.4)
            f.set_opacity(0.6 if target is not f else 1.0)
            banner.become(lab)
            self.play(Indicate(target, color=col, scale_factor=1.06), tick.animate.increment_value(10), run_time=0.9, rate_func=linear)
        self.play(tick.animate.increment_value(max(n.remaining(), 0.5) * 8), run_time=max(n.remaining() - 0.1, 0.5), rate_func=linear)

        # p02: proved / measured / not shown
        d = n.say("p02")
        wv.clear_updaters(); bars.clear_updaters(); body.clear_updaters()
        self.play(FadeOut(wv), FadeOut(bars), FadeOut(body), FadeOut(hm), FadeOut(f), FadeOut(shown), run_time=0.7)
        cols = [("Proved", C_GOOD, ["the forager exists in the knob space", "two knobs, set by hand"]),
                ("Measured", C_SP, ["the lesson carries signal, ≈ 1.9 per day", "rule one's step: 8–16× too large", "rule two forages", "frozen + mirrored: it is learned"]),
                ("Not shown", C_BAD, ["beats tabular Q", "avoids poison", "the committee matters", "sign features help rule two"])]
        groups = VGroup()
        for name, col, items in cols:
            g = VGroup(T(name, SZ_BIG, col), *[T(it, SZ_TINY) for it in items]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            groups.add(g)
        groups.arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(ORIGIN)
        if groups.width > 13.4: groups.scale_to_fit_width(13.4)
        for g, w in zip(groups, ["proved", "measured", "not"]):
            n.until("p02", w); self.play(FadeIn(g, shift=UP * 0.2), run_time=0.6)
        n.end()

        # p03: five doors + the pivot's deliverable
        d = n.say("p03")
        self.play(FadeOut(groups), run_time=0.5)
        doors = ["fix the step, re-ask sign features", "rule one at a sane step + entropy bonus", "make the xor world bite",
                 "sleep on a learner that learns", "generations: inherit the priors"]
        dg = VGroup(*[T(f"{k+1}.  {t}", SZ_SMALL) for k, t in enumerate(doors)]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(UP * 0.6)
        hdr = T("Five open doors", SZ_BIG, C_SP).next_to(dg, UP, buff=0.5)
        self.play(FadeIn(hdr), run_time=0.4)
        for item, w in zip(dg, ["Fix", "Give", "Make", "test", "generations"]):
            n.until("p03", w); self.play(FadeIn(item, shift=RIGHT * 0.2), run_time=0.5)
        n.until("p03", "pivot")
        piv = T("first: the list of what a brain cell does, each with a source and a test", SZ_SMALL, C_HID).next_to(dg, DOWN, buff=0.6)
        self.play(FadeIn(piv), run_time=0.6)
        n.end()

        # p04: end card
        d = n.say("p04")
        self.play(FadeOut(dg), FadeOut(hdr), FadeOut(piv), run_time=0.5)
        loop = LoopDiagram(radius=2.4).set_done(LOOP_NODES).move_to(ORIGIN).shift(UP * 0.3)
        end = T("Next session we pick one.", SZ_BIG, C_SP).to_edge(UP, buff=0.6)
        prov = T("every number in this lesson: out/PROVENANCE.md", SZ_TINY, DIM).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(loop), Write(end), run_time=1.2)
        self.play(FadeIn(prov), run_time=0.6)
        for k, name in enumerate(LOOP_NODES):
            self.play(Indicate(loop.boxes[name], color=C_SP, scale_factor=1.05), run_time=max(n.remaining() / (len(LOOP_NODES) - k), 0.3))
        n.finish(tail=1.5)
