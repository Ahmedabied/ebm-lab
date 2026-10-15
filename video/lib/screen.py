"""Screen furniture: titles, captions, pause-and-predict cards, formula helper."""
from manim import *
from .theme import *


def title_card(scene, number, name, hold=1.2):
    num = T(f"{number}", SZ_TITLE, DIM); nm = T(name, SZ_TITLE)
    g = VGroup(num, nm).arrange(RIGHT, buff=0.6).move_to(ORIGIN)
    scene.play(FadeIn(num, shift=UP * 0.2), Write(nm), run_time=1.0)
    scene.wait(hold)
    scene.play(FadeOut(g), run_time=0.5)


def caption(text, size=SZ_SMALL, color=DIM, edge=DOWN, buff=0.35):
    return T(text, size, color).to_edge(edge, buff=buff)


def header(text, size=SZ_BIG):
    return T(text, size).to_edge(UP, buff=0.4)


def pause_card(scene, question, hold=2.5):
    """A 'pause and predict' beat: dim everything, ask, hold, clear."""
    veil = Rectangle(width=20, height=12, fill_color=BG, fill_opacity=0.82, stroke_width=0)
    tag = T("PAUSE AND PREDICT", SZ_SMALL, C_SP)
    q = T(question, SZ_BIG, FG, line_spacing=1.1)
    if q.width > 12: q.scale_to_fit_width(12)
    g = VGroup(tag, q).arrange(DOWN, buff=0.5)
    scene.play(FadeIn(veil), FadeIn(g), run_time=0.6)
    scene.wait(hold)
    scene.play(FadeOut(veil), FadeOut(g), run_time=0.5)


def formula_F(scale=0.9):
    """The whole F(x,a) formula split into addressable pieces, with the lesson's symbol colours."""
    f = MathTex(r"F(x,a)", r"=", r"-\,b_a", r"-\,w_a\!\cdot\! x",
                r"-\sum_h", r"\mathrm{softplus}\!\left(", r"c_h", r"+\,u_h\!\cdot\! x", r"+\,v_{h,a}", r"\right)").scale(scale)
    f[2].set_color(C_BIAS); f[3].set_color(C_W); f[4].set_color(C_HID); f[5].set_color(C_SP); f[9].set_color(C_SP)
    f[6].set_color(C_HID); f[7].set_color(C_HID); f[8].set_color(C_HID)
    return f


def flash(scene, mobj, color=C_SP, run_time=0.6):
    scene.play(Indicate(mobj, color=color, scale_factor=1.15), run_time=run_time)
