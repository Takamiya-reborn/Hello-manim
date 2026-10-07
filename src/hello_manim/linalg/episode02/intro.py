"""Episode02 片头：从行列式的局限引出矩阵。

对应 mindmap Episode02 Intro 的四条旁白。视觉任务：
    1. 剧集卡（片名）
    2. 行列式只留下一个数——"每个方向被带去了哪里？"
    3. 保存 / 复用 / 接起来——需要比行列式更丰富的记录
    4. 矩阵 = 线性变换在坐标系中的完整档案
    5. 本集路线图（Act01–Act07，双列排布）
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import C_DIM, C_HL, C_MAIN, FONT, STAGE_CENTER
from hello_manim.utils.widgets import chip


class EpisodeIntro(EpisodeScene):
    def construct(self) -> None:
        # ---- 剧集卡 ----------------------------------------------------
        series = Text("线性代数 · Episode 02", font=FONT, font_size=28, color=C_HL)
        title = Text("线性变换的本身——矩阵", font=FONT, font_size=46, weight=BOLD)
        card = VGroup(series, title).arrange(DOWN, buff=0.5).move_to(STAGE_CENTER)
        underline = Line(LEFT * 3, RIGHT * 3, color=C_HL, stroke_width=2).next_to(card, DOWN, buff=0.45)
        self.play(FadeIn(series, shift=DOWN * 0.3), run_time=0.7)
        self.play(Write(title), run_time=1.2)
        self.play(Create(underline), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(card), FadeOut(underline), run_time=0.6)

        # ---- 行列式只留下一个数 -----------------------------------------
        self.say(
            "行列式的描述只能告诉我们一个方阵最后留下了什么数："
            "它能不能让空间塌缩，方程组有没有唯一解。"
        )
        det = MathTex(r"\det(A)=ad-bc", font_size=48).move_to(STAGE_CENTER + UP * 0.3)
        self.play(Write(det), run_time=1.3)
        self.hold()

        self.say("可它不能完整告诉我们：一个变换究竟把每个方向带去了哪里。")
        q = Text("每个方向被带去了哪里？", font=FONT, font_size=36, color=C_HL)
        q.next_to(det, DOWN, buff=0.6)
        self.play(FadeIn(q, scale=1.15), run_time=0.6)
        self.play(Circumscribe(det, color=C_HL, run_time=0.9))
        self.hold()
        self.play(FadeOut(det), FadeOut(q), run_time=0.5)

        # ---- 想对变换做的三件事 -----------------------------------------
        self.say(
            "如果我们不再只关心消元过程中的“结果”，而是想把一个变换本身"
            "保存下来、重复使用、和另一个变换接起来，"
            "就需要一种比行列式更丰富的记录方式。"
        )
        wants = VGroup(
            chip("保存下来", C_MAIN),
            chip("重复使用", C_MAIN),
            chip("接起来", C_MAIN),
        ).arrange(RIGHT, buff=0.8).move_to(STAGE_CENTER)
        plus = VGroup(
            Text("＋", font=FONT, font_size=30, color=C_DIM),
            Text("＋", font=FONT, font_size=30, color=C_DIM),
        )
        plus[0].move_to((wants[0].get_right() + wants[1].get_left()) / 2)
        plus[1].move_to((wants[1].get_right() + wants[2].get_left()) / 2)
        self.play(LaggedStart(*[FadeIn(w, scale=1.1) for w in wants], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(plus), run_time=0.5)
        self.hold()
        self.play(FadeOut(wants), FadeOut(plus), run_time=0.5)

        # ---- 矩阵登场：完整档案 -----------------------------------------
        self.say(
            "矩阵正是在这个问题上出现的：它不是一张系数表的升级版，"
            "而是线性变换在某一组坐标系中的完整档案。"
        )
        matrix = MathTex(r"A=\begin{pmatrix}a&b\\c&d\end{pmatrix}", font_size=54)
        box = SurroundingRectangle(matrix, color=C_MAIN, buff=0.35, corner_radius=0.12)
        grp = VGroup(matrix, box).move_to(STAGE_CENTER + UP * 0.2)
        label = Text("线性变换的完整档案", font=FONT, font_size=28, color=C_HL)
        label.next_to(box, DOWN, buff=0.4)
        self.play(Write(matrix), Create(box), run_time=1.6)
        self.play(FadeIn(label, shift=UP * 0.3), run_time=0.6)
        self.hold()
        self.play(FadeOut(grp), FadeOut(label), run_time=0.5)

        # ---- 本集路线图 --------------------------------------------------
        self.say(
            "这一章要追踪的不是“矩阵怎么算”，而是一个方阵如何从一排数字，"
            "变成一个可以作用于空间、可以复合、可以撤销的对象。"
        )
        left_col = VGroup(
            chip("Act01 · 当作代数实体", C_MAIN),
            chip("Act02 · 矩阵是一台机器", C_MAIN),
            chip("Act03 · 两列见全貌", C_MAIN),
            chip("Act04 · 乘法就是复合", C_MAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right_col = VGroup(
            chip("Act05 · 换坐标换外观", C_MAIN),
            chip("Act06 · 逆矩阵与撤销", C_MAIN),
            chip("Act07 · 从表到变换语言", C_MAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        roadmap = VGroup(left_col, right_col).arrange(RIGHT, buff=1.0).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in roadmap], lag_ratio=0.15), run_time=2.0)
        self.hold()
        self.wait(0.8)
