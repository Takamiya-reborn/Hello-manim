"""Episode01 片头：抛出这一集要回答的问题。

对应 mindmap 的 Intro 五条旁白。视觉任务：
    1. 剧集卡（片名）
    2. "教材先给展开式"——展示 2x2 展开式，配一个问号
    3. "朴素的愿望"——方程组登场
    4. 行列式的三重身份（分母 → 开关 → 面积/体积/方向）
    5. 本集路线图（Act01–Act05）
    6. 三种答案（唯一 / 无解 / 无穷多解）
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
    C_TEXT,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import chip


class EpisodeIntro(EpisodeScene):
    def construct(self) -> None:
        # ---- 剧集卡 ----------------------------------------------------
        series = Text("线性代数 · Episode 01", font=FONT, font_size=28, color=C_HL)
        title = Text("从线性方程组生长出来的行列式", font=FONT, font_size=46, weight=BOLD)
        card = VGroup(series, title).arrange(DOWN, buff=0.5).move_to(STAGE_CENTER)
        underline = Line(LEFT * 3, RIGHT * 3, color=C_HL, stroke_width=2).next_to(card, DOWN, buff=0.45)
        self.play(FadeIn(series, shift=DOWN * 0.3), run_time=0.7)
        self.play(Write(title), run_time=1.2)
        self.play(Create(underline), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(card), FadeOut(underline), run_time=0.6)

        # ---- "为什么要发明它？" -----------------------------------------
        self.say(
            "教材往往先把行列式写成一个展开式，再告诉我们如何计算它；"
            "但展开式本身并没有回答最重要的问题：为什么要发明这样一个对象？"
        )
        formula = MathTex(
            r"\det\begin{pmatrix}a&b\\c&d\end{pmatrix}=ad-bc",
            font_size=48,
        ).move_to(STAGE_CENTER + UP * 0.4)
        qmark = Text("？", font=FONT, font_size=72, color=C_HL).next_to(formula, DOWN, buff=0.4)
        self.play(Write(formula), run_time=1.6)
        self.play(FadeIn(qmark, scale=1.6), run_time=0.5)
        self.play(Circumscribe(formula, color=C_HL, run_time=1.0))
        self.hold()
        self.play(FadeOut(formula), FadeOut(qmark), run_time=0.5)

        # ---- 朴素的愿望：方程组 ----------------------------------------
        self.say(
            "这一章不从公式出发，而从一个朴素的愿望出发："
            "当几个未知数被几条线性关系缠在一起时，"
            "我们能不能在真正消元之前，就判断它有没有唯一的解？"
        )
        system = MathTex(
            r"\begin{cases}ax+by=e\\cx+dy=f\end{cases}",
            font_size=52,
        ).move_to(STAGE_CENTER)
        self.play(Write(system), run_time=1.5)
        self.hold()
        self.play(FadeOut(system), run_time=0.5)

        # ---- 三重身份链 --------------------------------------------------
        self.say(
            "行列式并不是凭空降临的定义。它先是消元过程中反复出现的一个分母，"
            "后来变成判断方程组的“开关”，"
            "再后来才显露出它与面积、体积和空间方向之间的联系。"
        )
        chips = VGroup(
            chip("消元中反复出现的分母", C_MAIN),
            chip("判断唯一解的开关", C_HL),
            chip("面积 · 体积 · 方向", C_POS),
        ).arrange(RIGHT, buff=1.0).move_to(STAGE_CENTER)
        arrows = VGroup(
            Arrow(chips[0].get_right(), chips[1].get_left(), buff=0.12, stroke_width=3, color=C_DIM),
            Arrow(chips[1].get_right(), chips[2].get_left(), buff=0.12, stroke_width=3, color=C_DIM),
        )
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.4) for c in chips], lag_ratio=0.35), run_time=1.6)
        self.play(Create(arrows), run_time=0.8)
        self.hold()
        self.play(FadeOut(chips), FadeOut(arrows), run_time=0.5)

        # ---- 本集路线图 --------------------------------------------------
        self.say("所以这一章要追踪的不是“行列式怎么算”，而是一个问题如何一步步长成一个理论。")
        roadmap = VGroup(
            chip("Act01 · 行列式的诞生", C_MAIN),
            chip("Act02 · 独立理论的形成", C_MAIN),
            chip("Act03 · 行列式的几何意义", C_MAIN),
            chip("Act04 · 排列与奇偶性", C_MAIN),
            chip("Act05 · 行列式的身份证", C_MAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.25) for c in roadmap], lag_ratio=0.18), run_time=2.0)
        self.hold()
        self.play(FadeOut(roadmap), run_time=0.5)

        # ---- 三种答案 -----------------------------------------------------
        self.say(
            "但方程组不会只给出“唯一”或“不唯一”两个答案："
            "有时目标根本到不了，有时能到达却有无数条路。"
        )
        fates = VGroup(
            chip("唯一解", C_POS),
            chip("无解", C_NEG),
            chip("无穷多解", C_HL),
        ).arrange(RIGHT, buff=1.0).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(f, scale=1.15) for f in fates], lag_ratio=0.25), run_time=1.2)
        self.hold()

        self.say(
            "为了区分这三种情况，我们必须先允许方程组被消元反复改写，"
            "再追问：究竟有什么东西，在这些改写中没有消失？"
        )
        # 字幕停留在问题句上，画面让位：三种答案卡片闪烁后让位给"没有消失"。
        self.play(Circumscribe(fates, color=C_HL, run_time=1.2))
        self.hold()
        self.play(FadeOut(fates), run_time=0.6)
        self.wait(0.8)
