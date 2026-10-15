"""Chapter 08 — The code. Every code block is read from the repo file at render time; the formula sits
beside it and the symbol and the variable light up together, one pair per breath."""
import sys, os, re; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from manim import *
from lib import *
import numpy as np

MONO = "DejaVu Sans Mono"
CODE_SZ = 19
LAB_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def src_lines(relpath, name):
    """The code lines of `def name(` in relpath: docstring stripped, trailing comments cut, dedented.
    Returns (first_line_number, [lines])."""
    path = os.path.join(LAB_ROOT, relpath)
    raw = open(path).read().split("\n")
    start = next(i for i, l in enumerate(raw) if re.match(r"\s*def " + re.escape(name) + r"\(", l))
    indent = len(raw[start]) - len(raw[start].lstrip())
    body = [raw[start]]
    for l in raw[start + 1:]:
        if l.strip() and (len(l) - len(l.lstrip())) <= indent:
            break
        body.append(l)
    # strip the docstring (first statement starting with """)
    out, in_doc = [], False
    for l in body[1:]:
        s = l.strip()
        if not in_doc and s.startswith('"""'):
            if s.count('"""') >= 2 and len(s) > 3: continue
            in_doc = True; continue
        if in_doc:
            if '"""' in s: in_doc = False
            continue
        if not s or s.startswith("#"): continue
        # cut trailing comments (not inside strings; the lab's comments never contain quotes before #)
        if "#" in l and '"' not in l.split("#")[0][-1:]:
            l = l.split("#")[0].rstrip()
        out.append(l)
    sig = re.sub(r"\s*->\s*[^:]+:$", ":", body[0])                 # drop the return annotation
    sig = re.sub(r":\s*[A-Za-z_][\w\.\[\], |]*?(?=[,)])", "", sig)   # drop parameter annotations
    lines = [sig] + out
    split = []
    for l in lines:                                                # one statement per line
        ind = l[:len(l) - len(l.lstrip())]
        parts = [p.strip() for p in l.split("; ")] if "; " in l and '"' not in l else [l.strip()]
        split += [ind + p for p in parts]
    lines = split
    lines = [l[indent:] if l.startswith(" " * indent) else l for l in lines]
    note(f"code: {name}", path, f"line {start + 1}", f"{len(lines)} lines")
    return start + 1, lines


class CodeBlock(VGroup):
    """Monospace lines on a panel; span(i, substr) gives the character mobjects of a substring in line i."""
    def __init__(self, lines, caption=None, size=CODE_SZ, max_width=13.0, **kw):
        super().__init__(**kw)
        self.lines_str = lines
        self.rows = VGroup(*[Text(l if l else " ", font=MONO, font_size=size, color=FG) for l in lines])
        for r in self.rows: r.set_z_index(2)
        self.rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        # Text drops leading spaces: shift rows by their indent
        unit = Text("x", font=MONO, font_size=size).width
        for l, r in zip(lines, self.rows):
            ind = len(l) - len(l.lstrip(" "))
            r.shift(RIGHT * ind * unit)
        if self.rows.width > max_width: self.rows.scale_to_fit_width(max_width)
        self.panel = RoundedRectangle(corner_radius=0.15, width=self.rows.width + 0.6, height=self.rows.height + 0.5,
                                      fill_color=PANEL, fill_opacity=1, stroke_color=GRID, stroke_width=1.5).move_to(self.rows)
        self.add(self.panel, self.rows)
        if caption:
            self.cap = T(caption, SZ_TINY, DIM).next_to(self.panel, UP, buff=0.12).align_to(self.panel, LEFT)
            self.add(self.cap)

    def span(self, i, substr, occurrence=0):
        l = self.lines_str[i]; row = self.rows[i]
        pos = -1
        for _ in range(occurrence + 1):
            pos = l.find(substr, pos + 1)
        if pos < 0: return VGroup(row)
        before = sum(1 for ch in l[:pos] if not ch.isspace())
        n = sum(1 for ch in substr if not ch.isspace())
        return VGroup(*row[before:before + n])


class Ch08(Scene):
    def pair(self, n, pid, word, code_spans, formula_parts, color, occurrence=0):
        """On `word`, light the code substring(s) and the formula piece(s) together."""
        n.until(pid, word, occurrence)
        anims = [s.animate.set_color(color) for s in code_spans] + [f.animate.set_color(color) for f in formula_parts]
        self.play(*anims, run_time=0.45)
        self.play(*[Indicate(s, color=color, scale_factor=1.12) for s in code_spans + formula_parts], run_time=0.5)

    def swap(self, old, new, run_time=0.6):
        self.play(FadeOut(old), FadeIn(new), run_time=run_time)

    def construct(self):
        n = Narration(self, "08")
        hdr = header("The code", SZ_BIG)
        self.play(FadeIn(hdr), run_time=0.5)

        # ---------- p01: brain.F, first two terms
        d = n.say("p01")
        ln, lines = src_lines("creature/brain.py", "F")
        code = CodeBlock(lines, caption=f"creature/brain.py  ·  Brain.F  ·  line {ln}", max_width=12.5).move_to(DOWN * 1.3)
        f = formula_F(0.9).next_to(hdr, DOWN, buff=0.45)
        for p in f: p.set_color(FG)
        self.play(FadeIn(f), FadeIn(code), run_time=0.8)
        fl = next(i for i, l in enumerate(lines) if "F = -th" in l)
        self.pair(n, "p01", "resting", [code.span(fl, '-th["b"]')], [f[2]], C_BIAS)
        self.pair(n, "p01", "dot", [code.span(fl, 'X @ th["w"].T')], [f[3]], C_W)
        n.until("p01", "numpy")
        at = code.span(fl, "@"); self.play(Indicate(at, color=C_W, scale_factor=1.6), run_time=0.6)
        n.end()

        # ---------- p02: committee + centring
        d = n.say("p02")
        self.pair(n, "p02", "softplus", [code.span(fl, "_softplus(self.pre(X)).sum(axis=1)")], [f[5], f[6], f[7], f[8], f[9]], C_SP)
        self.pair(n, "p02", "axis", [code.span(fl, ".sum(axis=1)")], [f[4]], C_HID)
        n.until("p02", "centring")
        cl = next(i for i, l in enumerate(lines) if "np.log(2.0)" in l)
        hlog = MathTex(r"+\,H\log 2", color=C_SP).scale(0.9).next_to(f, RIGHT, buff=0.25)
        if hlog.get_right()[0] > 6.8: hlog.next_to(f, DOWN, buff=0.2).align_to(f, RIGHT)
        self.play(FadeIn(hlog), code.span(cl, "self.H * np.log(2.0)").animate.set_color(C_SP), run_time=0.6)
        self.play(Indicate(code.span(cl, "self.H * np.log(2.0)"), color=C_SP), run_time=0.5)
        n.end()

        # ---------- p03: pre, the z block
        d = n.say("p03")
        ln, lines = src_lines("creature/brain.py", "pre")
        code2 = CodeBlock(lines, caption=f"creature/brain.py  ·  Brain.pre  ·  line {ln}", max_width=13.0).move_to(DOWN * 0.4)
        fz = MathTex(r"z_{h,a}", r"=", r"c_h", r"+\,u_h\!\cdot\! x", r"+\,v_{h,a}").scale(0.95).next_to(hdr, DOWN, buff=0.45)
        self.swap(VGroup(f, hlog, code), VGroup(fz, code2))
        rl = next(i for i, l in enumerate(lines) if "return" in l)
        self.pair(n, "p03", "thresholds", [code2.span(rl, 'th["c"]')], [fz[2]], C_HID)
        self.pair(n, "p03", "weighted", [code2.span(rl, '(X @ th["u"].T)')], [fz[3]], C_HID)
        self.pair(n, "p03", "word", [code2.span(rl, 'th["v"]')], [fz[4]], C_HID)
        n.until("p03", "block")
        # the (N, H, A) block as a stack of H sheets, each A wide
        sheets = VGroup()
        for k in range(5):
            s = Rectangle(width=1.6, height=0.55, fill_color=C_HID, fill_opacity=0.25 + 0.1 * k, stroke_color=C_HID, stroke_width=1.5)
            s.shift(RIGHT * 0.18 * k + UP * 0.22 * k); sheets.add(s)
        labs = VGroup(T("A = 3 moves", SZ_TINY, C_HID).next_to(sheets[0], DOWN, buff=0.1),
                      T("H units", SZ_TINY, C_HID).next_to(sheets, RIGHT, buff=0.15),
                      T("N samples", SZ_TINY, DIM).next_to(sheets, UP, buff=0.1))
        block = VGroup(sheets, labs).next_to(code2, DOWN, buff=0.35)
        if block.get_bottom()[1] < -3.9: block.shift(UP * (-3.9 - block.get_bottom()[1]))
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in sheets], lag_ratio=0.15), FadeIn(labs), run_time=1.2)
        n.end()

        # ---------- p04: softplus = logaddexp
        d = n.say("p04")
        ln, lines = src_lines("creature/brain.py", "_softplus")
        code3 = CodeBlock(lines, caption=f"creature/brain.py  ·  _softplus  ·  line {ln}").move_to(DOWN * 0.6)
        fs = MathTex(r"\mathrm{softplus}(z)", r"=", r"\log\!\left(e^{0} + e^{z}\right)").scale(1.0).next_to(hdr, DOWN, buff=0.45)
        fs[2].set_color(C_SP)
        self.swap(VGroup(fz, code2, block), VGroup(fs, code3))
        rl = next(i for i, l in enumerate(lines) if "logaddexp" in l)
        self.pair(n, "p04", "exp", [code3.span(rl, "np.logaddexp(0.0, z)")], [fs[2]], C_SP)
        n.until("p04", "tickets")
        tix = VGroup(T("ticket off:  e⁰ = 1", SZ_SMALL, FG), T("ticket on:  eᶻ", SZ_SMALL, C_SP)).arrange(RIGHT, buff=1.0).next_to(code3, DOWN, buff=0.5)
        self.play(FadeIn(tix), run_time=0.6)
        n.end()

        # ---------- p05: act, egreedy branch
        d = n.say("p05")
        ln, lines = src_lines("creature/brain.py", "act")
        k0 = next(i for i, l in enumerate(lines) if '"egreedy"' in l)
        sl = lines[k0:k0 + 6]
        code4 = CodeBlock(sl, caption=f"creature/brain.py  ·  Brain.act  ·  the ε-greedy branch, line {ln + lines.index(sl[0])}", max_width=12.5).move_to(DOWN * 0.7)
        fa = MathTex(r"a", r"=", r"\arg\min_a F(x,a)", r"\;\text{ (9 in 10)},", r"\quad\text{random}", r"\;\text{ (1 in 10)}").scale(0.9).next_to(hdr, DOWN, buff=0.45)
        self.swap(VGroup(fs, code3, tix), VGroup(fa, code4))
        gl = next(i for i, l in enumerate(sl) if "argmin" in l); al = next(i for i, l in enumerate(sl) if "rng.random()" in l); pl = next(i for i, l in enumerate(sl) if "pb =" in l)
        self.pair(n, "p05", "arg", [code4.span(gl, "np.argmin(Fx)")], [fa[2]], C_Q)
        self.pair(n, "p05", "random", [code4.span(al, "rng.random() < eps")], [fa[5]], C_T)
        self.pair(n, "p05", "three", [code4.span(al, "rng.integers(A)")], [fa[4]], C_T)
        self.pair(n, "p05", "last", [code4.span(pl, "pb =")], [], DIM)
        n.end()

        # ---------- p06: grad_negF
        d = n.say("p06")
        ln, lines = src_lines("creature/brain.py", "grad_negF")
        code5 = CodeBlock(lines, caption=f"creature/brain.py  ·  Brain.grad_negF  ·  line {ln}", max_width=8.0).move_to(DOWN * 0.9 + LEFT * 2.6)
        fg = VGroup(MathTex(r"\frac{\partial Q}{\partial b_a} = \mathbb{1}[a]", color=C_BIAS),
                    MathTex(r"\frac{\partial Q}{\partial w_a} = \mathbb{1}[a]\, x", color=C_W),
                    MathTex(r"S = \sigma(z) = \frac{1}{1+e^{-z}}", color=C_HID),
                    MathTex(r"\frac{\partial Q}{\partial v_{h,a}} = S\,\mathbb{1}[a]", color=C_HID)).scale(0.75).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        fg.next_to(code5, RIGHT, buff=0.6).align_to(code5, UP)
        if fg.get_right()[0] > 6.9: fg.shift(LEFT * (fg.get_right()[0] - 6.9))
        for m in fg: m.set_color(FG)
        self.swap(VGroup(fa, code4), VGroup(code5, fg))
        li = lambda key: next(i for i, l in enumerate(lines) if key in l)
        self.pair(n, "p06", "Coef", [code5.span(li("coef = np.zeros"), "coef[np.arange(N), a] = 1.0")], [], C_Q)
        self.pair(n, "p06", "b", [code5.span(li('g["b"]'), 'g["b"] = coef')], [fg[0]], C_BIAS, occurrence=0)
        self.pair(n, "p06", "readings", [code5.span(li('g["w"]'), 'coef[:, :, None] * X[:, None, :]')], [fg[1]], C_W)
        self.pair(n, "p06", "sigmoid", [code5.span(li("_sigmoid"), "S = _sigmoid(self.pre(X))")], [fg[2]], C_HID)
        self.pair(n, "p06", "shared", [code5.span(li('g["c"]'), 'g["c"]'), code5.span(li('g["u"]'), 'g["u"]')], [fg[3]], C_HID)
        n.end()

        # ---------- p07: learn_q
        d = n.say("p07")
        ln, lines = src_lines("creature/brain.py", "learn_q")
        code6 = CodeBlock(lines, caption=f"creature/brain.py  ·  Brain.learn_q  ·  line {ln}", max_width=12.5).move_to(DOWN * 1.45)
        fq = MathTex(r"\theta", r"\;+\!=\;", r"\alpha", r"\,(y - Q)\,", r"\frac{\partial Q}{\partial\theta}").scale(0.95).next_to(hdr, DOWN, buff=0.45)
        fq_words = T("knob  +=  learning rate  ·  miss  ·  slope", SZ_SMALL, DIM).next_to(fq, RIGHT, buff=0.8)
        VGroup(fq, fq_words).move_to(fq.get_center()).set_x(0)
        self.swap(VGroup(code5, fg), VGroup(fq, fq_words, code6))
        tl = next(i for i, l in enumerate(lines) if "td = y" in l); ul = next(i for i, l in enumerate(lines) if "tensordot" in l)
        self.pair(n, "p07", "miss", [code6.span(tl, "td = y - self.Q(X)[np.arange(N), a]")], [fq[3]], C_SP)
        self.pair(n, "p07", "alpha", [code6.span(ul, "alpha * np.tensordot(td, g[k], axes=(0, 0)) / N")], [fq[2], fq[4]], C_W)
        n.end()

        # ---------- p08: q_targets
        d = n.say("p08")
        ln, lines = src_lines("creature/sim.py", "q_targets")
        code7 = CodeBlock(lines, caption=f"creature/sim.py  ·  q_targets  ·  line {ln}", max_width=12.5).move_to(DOWN * 1.0)
        fy = MathTex(r"y", r"=", r"r", r"+\,\gamma\,", r"(1-\mathrm{done})", r"\,\max_{a'} Q(x',a')").scale(0.95).next_to(hdr, DOWN, buff=0.45)
        self.swap(VGroup(fq, fq_words, code6), VGroup(fy, code7))
        bl = next(i for i, l in enumerate(lines) if "boot =" in l); rl = next(i for i, l in enumerate(lines) if "return r" in l)
        self.pair(n, "p08", "gamma", [code7.span(rl, "gamma * boot")], [fy[3]], C_T)
        self.pair(n, "p08", "best", [code7.span(bl, "brain.Q(np.atleast_2d(Xn)).max(axis=1)")], [fy[5]], C_Q)
        self.pair(n, "p08", "Done", [code7.span(bl, "done > 0, 0.0")], [fy[4]], C_BAD)
        n.until("p08", "night")
        nt = T("last tick of a day → done = 1 → y = r, no promise across the night", SZ_TINY, DIM).next_to(code7, DOWN, buff=0.4)
        self.play(FadeIn(nt), run_time=0.5)
        n.end()

        # ---------- p09: online vs replay
        d = n.say("p09")
        ln1, l1 = src_lines("creature/sim.py", "_online_q")
        ln2, l2 = src_lines("creature/sim.py", "_replay_td")
        # the replay slice: from the loop down to the learn_q call (skip the "ac" branch)
        s2 = [l for l in l2 if any(k in l for k in ("def _replay_td", "transitions(", "for _ in range", "permutation", "for i in range(0, n", "idx = order", "q_targets(", "learn_q("))]
        code8 = CodeBlock(l1, caption=f"creature/sim.py  ·  _online_q  ·  line {ln1}", size=17, max_width=13.2).move_to(UP * 1.3)
        code9 = CodeBlock(s2, caption=f"creature/sim.py  ·  _replay_td (the q branch)  ·  line {ln2}", size=17, max_width=13.2).next_to(code8, DOWN, buff=0.5)
        both = VGroup(code8, code9)
        if both.get_bottom()[1] < -3.9: both.shift(UP * (-3.9 - both.get_bottom()[1]))
        self.swap(VGroup(fy, code7, nt), both)
        self.pair(n, "p09", "Online", [code8.span(next(i for i, l in enumerate(l1) if "learn_q" in l), "learn_q")], [], C_SP)
        self.pair(n, "p09", "shuffled", [code9.span(next(i for i, l in enumerate(s2) if "permutation" in l), "self.rng.permutation(n)")], [], C_T)
        self.pair(n, "p09", "sixty", [code9.span(next(i for i, l in enumerate(s2) if "c.batch" in l), "c.batch")], [], C_W)
        self.pair(n, "p09", "three", [code9.span(next(i for i, l in enumerate(s2) if "sleep_epochs" in l), "c.sleep_epochs")], [], C_HID)
        self.pair(n, "p09", "Same", [code9.span(next(i for i, l in enumerate(s2) if "learn_q" in l), "learn_q")], [], C_SP)
        n.end()

        # ---------- p10: body.py
        d = n.say("p10")
        ln1, l1 = src_lines("creature/body.py", "drive")
        ln2, l2 = src_lines("creature/body.py", "tick")
        fd = MathTex(r"D", r"=", r"w_E\,|E_{set}-E|^{n}", r"+\,w_X\,|X_{set}-X|^{n}").scale(0.9).next_to(hdr, DOWN, buff=0.35)
        code10 = CodeBlock(l1, caption=f"creature/body.py  ·  Body.drive  ·  line {ln1}").next_to(fd, DOWN, buff=0.5)
        code11 = CodeBlock(l2, caption=f"creature/body.py  ·  Body.tick  ·  line {ln2}", size=17).move_to(DOWN * 0.9)
        if code11.get_bottom()[1] < -3.95: code11.shift(UP * (-3.95 - code11.get_bottom()[1]))
        self.swap(both, VGroup(fd, code10))
        dl = next(i for i, l in enumerate(l1) if "return" in l)
        self.pair(n, "p10", "bowl", [code10.span(dl, "abs(c.E_set - self.E) ** c.n")], [fd[2]], C_E)
        n.until("p10", "exactly")
        bowlnote = T("w 1, setpoints 1 and 0, n 2: the bowl of chapter four", SZ_SMALL, C_E).next_to(code10, DOWN, buff=0.4)
        self.play(FadeIn(bowlnote), run_time=0.5)
        n.until("p10", "Tick")
        self.play(FadeOut(code10), FadeOut(bowlnote), fd.animate.scale(0.7).to_corner(UR, buff=0.3).shift(DOWN * 1.05), FadeIn(code11), run_time=0.6)
        li = lambda key: next(i for i, l in enumerate(l2) if key in l)
        for word, key, sub, col in (("metabolism", "c.metabolic", "self.E -= c.metabolic", C_BAD), ("decays", "toxin_decay", "self.X *= c.toxin_decay", C_XT),
                                    ("drains", "toxin_drain", "self.E -= self.X * c.toxin_drain", C_XT), ("cap", "E_max", "min(c.E_max", C_E),
                                    ("poison", "c.toxicity", "self.X += c.toxicity * poison_mass", C_XT), ("kills", "alive = False", "self.alive = False", C_BAD),
                                    ("returns", "return D0", "return D0 - self.drive()", C_GOOD)):
            self.pair(n, "p10", word, [code11.span(li(key), sub)], [], col)
        n.end()

        # ---------- p11: the dictionary
        d = n.say("p11")
        rows = [(r"w", 'th["w"]', "w"), (r"b", 'th["b"]', "b"), (r"\mathrm{softplus}", "np.logaddexp", "Softplus"), (r"\sum_h", ".sum(axis=1)", "sum"),
                (r"T", "cfg.T", "T"), (r"\varepsilon", "cfg.eps", "epsilon"), (r"\gamma", "gamma", "gamma"), (r"\text{learning rate}", "alpha_q", "rate"),
                (r"\lambda", "lam", "lambda"), (r"\text{miss}", "td", "miss"), (r"D", "drive()", "drive"), (r"r", "tick() returns", "lesson")]
        self.play(FadeOut(VGroup(fd, code11)), run_time=0.5)
        left, right = rows[:6], rows[6:]
        def column(rs):
            g = VGroup()
            for sym, name, _ in rs:
                g.add(VGroup(MathTex(sym, color=C_Q).scale(0.85), T("↔", SZ_SMALL, DIM), Text(name, font=MONO, font_size=22, color=C_W)).arrange(RIGHT, buff=0.3))
            return g.arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        c1, c2 = column(left), column(right)
        cols = VGroup(c1, c2).arrange(RIGHT, buff=1.6, aligned_edge=UP).move_to(DOWN * 0.3)
        if cols.width > 13.2: cols.scale_to_fit_width(13.2)
        allrows = list(c1) + list(c2)
        for (sym, name, word), r in zip(rows, allrows):
            n.until("p11", word)
            self.play(FadeIn(r, shift=RIGHT * 0.15), run_time=0.35)
        n.until("p11", "Every")
        foot = T("every symbol in the formula has one name in one file", SZ_SMALL, C_SP).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(foot), run_time=0.5)
        n.finish(tail=1.2)
