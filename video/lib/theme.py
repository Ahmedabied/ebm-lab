"""Design tokens. Warm dark palette (Ahmed's terminal: visibility over contrast, no pure white),
Lexend for all on-screen words, one idea per screen, big sparse text."""
from manim import config, Text, MathTex, Tex, TexTemplate
BG = "#1D2021"; FG = "#EBDBB2"; DIM = "#7C6F64"; GRID = "#3C3836"; PANEL = "#282828"
# chemicals (viewer convention: A red, B green, C blue -> food yellow, poison cyan)
C_A = "#FB4934"; C_B = "#B8BB26"; C_C = "#83A598"; FOOD = "#FABD2F"; POISON = "#8EC07C"
# symbols, used consistently through every chapter
C_X = "#83A598"      # readings x
C_W = "#FE8019"      # weights/knobs w
C_BIAS = "#D3869B"   # b
C_HID = "#8EC07C"    # committee c, u, v
C_SP = "#FABD2F"     # softplus
C_T = "#FB4934"      # temperature / epsilon / gamma dials
C_Q = "#EBDBB2"      # F / Q
C_GOOD = "#B8BB26"; C_BAD = "#FB4934"
C_E = "#FABD2F"; C_XT = "#D3869B"; C_D = "#EBDBB2"
MOVE = {0: "#83A598", 1: "#FE8019", 2: "#B8BB26"}; MOVE_NAME = {0: "LEFT", 1: "RIGHT", 2: "FORWARD"}
FONT = "Lexend"
config.background_color = BG
Text.set_default(font=FONT, color=FG)
MathTex.set_default(color=FG)
Tex.set_default(color=FG)
SZ_TITLE = 56; SZ_BIG = 44; SZ_BODY = 34; SZ_SMALL = 26; SZ_TINY = 20


def T(s, size=SZ_BODY, color=FG, **kw):
    """Lexend text with the lesson's defaults."""
    return Text(s, font=FONT, font_size=size, color=color, **kw)
