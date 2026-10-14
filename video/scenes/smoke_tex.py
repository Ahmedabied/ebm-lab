from manim import *
class SmokeTex(Scene):
    def construct(self):
        eq = MathTex(r"F(x,a) = -b_a - w_a\cdot x - \sum_h \mathrm{softplus}(c_h + u_h\cdot x + v_{h,a})").scale(0.9)
        self.play(Write(eq)); self.wait(0.5)
