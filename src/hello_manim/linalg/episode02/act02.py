"""Act02 · 矩阵不是表格，而是一台机器。

对应 mindmap Episode02 Act02 的旁白。视觉主线：
    这张表对输入做了什么？ → Ax 的坐标公式 → 每行算一个输出
    → 两条线性纪律 → 纪律被编码进行乘列 → 一致生效的规则
    → 拉伸/压缩/剪切/翻转/升维 → 两个遗留问题（撞车与盲区）。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_MAIN,
    C_NEG,
    C_POS,
    C_SUB,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, chip, panel


class Act02Machine(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 02", "矩阵不是表格，而是一台机器")

        # ---- 1. 这张表到底做了什么？ ---------------------------------------
        self.say(
            "只看矩阵的数字排列，很容易把它误解成一张系数表。"
            "但一个更有解释力的问题是：这张表到底对一组输入坐标做了什么？"
        )
        mat = MathTex(r"A=\begin{pmatrix}a&b\\c&d\end{pmatrix}", font_size=48)
        mat.move_to(STAGE_CENTER + LEFT * 2.2)
        arrow = Arrow(mat.get_right() + RIGHT * 0.1, STAGE_CENTER + RIGHT * 1.4, buff=0.2, stroke_width=4, color=C_DIM)
        q = MathTex(r"?", font_size=64, color=C_HL).move_to(STAGE_CENTER + RIGHT * 2.4)
        xin = MathTex(r"\begin{pmatrix}x\\y\end{pmatrix}", font_size=36, color=C_DIM)
        xin.next_to(arrow, UP, buff=0.15)
        self.play(Write(mat), run_time=1.2)
        self.play(Create(arrow), Write(q), FadeIn(xin), run_time=1.0)
        self.hold()
        self.play(FadeOut(q), FadeOut(arrow), FadeOut(xin), run_time=0.5)

        # ---- 2. Ax：坐标公式 ------------------------------------------------
        self.say("对输入坐标施加矩阵 A，得到一组新的坐标。")
        ax = MathTex(
            r"A\begin{pmatrix}x\\y\end{pmatrix}=",
            r"\begin{pmatrix}",
            r"ax+by",
            r"\\",
            r"cx+dy",
            r"\end{pmatrix}",
            font_size=48,
        ).move_to(STAGE_CENTER)
        ax[2].set_color(C_MAIN)  # 第一行输出
        ax[4].set_color(C_POS)   # 第二行输出
        self.play(FadeOut(mat), run_time=0.5)
        self.play(Write(ax), run_time=1.6)
        self.hold()

        # ---- 3. 每行负责一个输出坐标 ------------------------------------------
        self.say(
            "矩阵的每一行都在计算一个输出坐标：第一行负责输出的第一维，"
            "第二行负责输出的第二维。矩阵把输入的坐标重新组织、混合，"
            "最后吐出一组新的坐标。"
        )
        row_tags = VGroup(
            Text("第一行 → 输出的第一维", font=FONT, font_size=26, color=C_MAIN),
            Text("第二行 → 输出的第二维", font=FONT, font_size=26, color=C_POS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(ax, RIGHT, buff=0.8)
        self.play(FadeIn(row_tags[0], shift=LEFT * 0.3), run_time=0.8)
        self.play(FadeIn(row_tags[1], shift=LEFT * 0.3), run_time=0.8)
        self.hold()
        self.play(FadeOut(row_tags), run_time=0.5)

        # ---- 4. 两条纪律 ------------------------------------------------------
        self.say(
            "但线性变换不应该只是“把一组数字送到另一组数字”。"
            "它必须同时满足两条纪律：加法能穿过变换，数乘也能穿过变换。"
        )
        d1 = card(
            "加法穿过",
            MathTex(r"T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v})", font_size=30),
            C_MAIN,
        )
        d2 = card(
            "数乘穿过",
            MathTex(r"T(k\,\mathbf{u})=k\,T(\mathbf{u})", font_size=30),
            C_POS,
        )
        disc = VGroup(d1, d2).arrange(RIGHT, buff=0.9).move_to(STAGE_CENTER)
        self.play(FadeOut(ax), run_time=0.5)
        self.play(FadeIn(d1, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(d2, shift=UP * 0.3), run_time=0.8)
        self.hold()

        # ---- 5. 纪律被编码进行乘列 --------------------------------------------
        self.say(
            "矩阵乘法之所以采用行乘列，正是为了把这两条纪律"
            "编码进每一个坐标公式里。"
        )
        check = MathTex(
            r"A(\mathbf{u}+\mathbf{v})=A\mathbf{u}+A\mathbf{v},\qquad A(k\,\mathbf{u})=k\,A\mathbf{u}",
            font_size=40,
        ).move_to(STAGE_CENTER + UP * 0.4)
        encode = panel("行乘列 ＝ 把纪律写进坐标公式", C_HL).next_to(check, DOWN, buff=0.6)
        self.play(FadeOut(disc), Write(check), run_time=1.6)
        self.play(FadeIn(encode, shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(check), FadeOut(encode), run_time=0.5)

        # ---- 6. 一致生效的规则 --------------------------------------------------
        self.say(
            "所以矩阵真正记录的不是“某几个输入的对应关系”，"
            "而是一条对整组坐标都一致生效的规则。"
        )
        rule = Text("对整组坐标一致生效的规则", font=FONT, font_size=34, color=C_HL)
        rule.move_to(STAGE_CENTER)
        self.play(FadeIn(rule, scale=1.08), run_time=0.8)
        self.play(Circumscribe(rule, color=C_HL, run_time=1.0))
        self.hold()
        self.play(FadeOut(rule), run_time=0.5)

        # ---- 7. 各种动作 ------------------------------------------------------
        self.say(
            "一个矩阵可以拉伸，可以压缩，可以剪切，可以翻转，"
            "也可以把二维坐标送进三维坐标。它的外形是数字，内核却是一个动作。"
        )
        moves = VGroup(
            chip("拉伸", C_MAIN),
            chip("压缩", C_MAIN),
            chip("剪切", C_MAIN),
            chip("翻转", C_MAIN),
            chip("升维", C_SUB),
        ).arrange(RIGHT, buff=0.55).move_to(STAGE_CENTER + UP * 0.5)
        core = card("外形是数字", "内核是一个动作", C_HL).next_to(moves, DOWN, buff=0.7)
        self.play(LaggedStart(*[FadeIn(m, scale=1.1) for m in moves], lag_ratio=0.2), run_time=1.6)
        self.play(FadeIn(core, shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(moves), FadeOut(core), run_time=0.5)

        # ---- 8. 两个遗留问题 ---------------------------------------------------
        self.say(
            "于是两个问题自然出现：有没有不同的输入会得到同一个输出？"
            "有没有某些输出无论怎样选择输入都得不到？"
            "这两个问题先留下来，等向量和空间的语言建立后再正式命名。"
        )
        q1 = card("问题一", "不同的输入 → 同一个输出？", C_HL)
        q2 = card("问题二", "某些输出 → 永远不可达？", C_NEG)
        qs = VGroup(q1, q2).arrange(RIGHT, buff=1.0).move_to(STAGE_CENTER)
        self.play(FadeIn(q1, shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(q2, shift=UP * 0.3), run_time=0.8)
        self.hold()
        self.wait(0.6)
