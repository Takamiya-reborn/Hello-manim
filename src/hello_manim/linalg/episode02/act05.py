"""Act05 · 同一个变换，为什么会有不同的矩阵。

对应 mindmap Episode02 Act05 的旁白。视觉主线：
    换坐标系矩阵就变，变换也变了吗？ → 动作=对象 / 坐标=语言
    → 坐标尺演示（同一支箭头：标准坐标 (2,1) vs 交换两轴后的 (1,2)）
    → 换语言要重新翻译 → 过渡矩阵 C 与 C⁻¹AC → 两面性 → 留尾
    （哪些量不随坐标改变？——特征值章节的钩子）。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_MAIN,
    C_POS,
    C_SUB,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, chip, panel


class Act05Coordinates(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 05", "同一个变换，为什么会有不同的矩阵")

        # ---- 1. 疑问 -------------------------------------------------------
        self.say(
            "如果矩阵记录的是变换本身，为什么换一套坐标系，"
            "矩阵里的数字就会改变？难道变换也跟着改变了吗？"
        )
        mats = MathTex(r"A", r"\neq", r"A'", font_size=56).move_to(STAGE_CENTER)
        mats[0].set_color(C_MAIN)
        mats[2].set_color(C_HL)
        sub = Text("数字变了——动作也变了吗？", font=FONT, font_size=28, color=C_DIM)
        sub.next_to(mats, DOWN, buff=0.5)
        self.play(Write(mats), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.25), run_time=0.7)
        self.hold()
        self.play(FadeOut(mats), FadeOut(sub), run_time=0.5)

        # ---- 2. 动作是对象，坐标是语言 ---------------------------------------
        self.say(
            "这里必须把两件事分开：空间中的动作是对象，坐标表述是语言。"
            "换坐标，就像换一种语言描述同一个动作，数字会变，但动作未必改变。"
        )
        pair = VGroup(
            chip("动作 ＝ 对象", C_MAIN),
            chip("坐标 ＝ 语言", C_HL),
        ).arrange(RIGHT, buff=1.2).move_to(STAGE_CENTER)
        self.play(FadeIn(pair[0], scale=1.1), run_time=0.8)
        self.play(FadeIn(pair[1], scale=1.1), run_time=0.8)
        self.hold()
        self.play(FadeOut(pair), run_time=0.5)

        # ---- 3. 坐标尺演示：箭头没动，尺换了 -----------------------------------
        self.say(
            "选择一套坐标描述，就等于给空间安装了一把坐标尺。"
            "数字依赖这把尺，矩阵中的行和列也随之改变，"
            "因为同一个动作可以用不同的坐标语言记录。"
        )
        plane = NumberPlane(
            x_range=[-2.4, 2.4, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=4.6,
            y_length=3.4,
            background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.5},
            axis_config={"stroke_width": 2},
        ).move_to(STAGE_CENTER)
        o = np.array(plane.c2p(0, 0))
        vec = Arrow(o, plane.c2p(2, 1), buff=0, color=C_MAIN, stroke_width=6)
        vlabel = MathTex(r"(2,\,1)", font_size=40, color=C_MAIN)
        vlabel.next_to(vec.get_end(), UR, buff=0.15)
        self.play(Create(plane), run_time=1.2)
        self.play(GrowArrow(vec), FadeIn(vlabel), run_time=0.9)
        self.hold()

        # 换一把坐标尺：新轴 1 = 旧 y 轴，新轴 2 = 旧 x 轴（交换两轴）。
        new1 = Line(o, plane.c2p(0, 1.6), stroke_color=C_SUB, stroke_width=3)
        new2 = Line(o, plane.c2p(2.2, 0), stroke_color=C_SUB, stroke_width=3)
        n1tag = Text("新轴 1", font=FONT, font_size=20, color=C_SUB)
        n2tag = Text("新轴 2", font=FONT, font_size=20, color=C_SUB)
        n1tag.next_to(new1.get_end(), UP, buff=0.1)
        n2tag.next_to(new2.get_end(), DOWN, buff=0.1)
        old1 = Text("旧坐标 (2, 1)", font=FONT, font_size=24, color=C_DIM)
        old1.to_corner(UL, buff=0.5).shift(DOWN * 1.1)
        old2 = Text("新坐标 (1, 2)", font=FONT, font_size=24, color=C_HL)
        old2.next_to(old1, DOWN, buff=0.3)
        note = Text("箭头没动，尺换了", font=FONT, font_size=28, color=C_HL)
        note.next_to(old2, DOWN, buff=0.4)
        self.play(Create(new1), Create(new2), FadeIn(n1tag), FadeIn(n2tag), run_time=0.9)
        self.play(FadeIn(old1), run_time=0.6)
        self.play(Transform(vlabel, MathTex(r"(1,\,2)", font_size=40, color=C_HL).move_to(vlabel)), FadeIn(old2), run_time=0.9)
        self.play(FadeIn(note, shift=UP * 0.25), run_time=0.7)
        self.hold()
        self.play(
            FadeOut(plane), FadeOut(vec), FadeOut(vlabel),
            FadeOut(new1), FadeOut(new2), FadeOut(n1tag), FadeOut(n2tag),
            FadeOut(old1), FadeOut(old2), FadeOut(note),
            run_time=0.6,
        )

        # ---- 4. 换语言：输入输出都要翻译 --------------------------------------
        self.say(
            "如果从一套坐标语言换到另一套，输入和输出都要被重新翻译。"
            "此时矩阵里的数字会变化，但它所描述的动作未必变化。"
        )
        bridge = VGroup(
            panel("新语言输入", C_SUB),
            MathTex(r"\Rightarrow", font_size=40, color=C_DIM),
            panel("旧语言计算", C_MAIN),
            MathTex(r"\Rightarrow", font_size=40, color=C_DIM),
            panel("翻回新语言", C_SUB),
        ).arrange(RIGHT, buff=0.45).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(b, scale=1.05) for b in bridge], lag_ratio=0.25), run_time=1.5)
        self.hold()
        self.play(FadeOut(bridge), run_time=0.5)

        # ---- 5. 过渡矩阵与 C⁻¹AC --------------------------------------------
        self.say(
            "把新基写成旧基的线性组合，组合系数排成的可逆矩阵 C 称为过渡矩阵："
            "同一个向量的新旧坐标满足 x = Cy，"
            "同一个变换在新坐标下的矩阵则变成 C⁻¹AC。"
        )
        change = MathTex(
            r"\mathbf{x}=C\mathbf{y}",
            r",\qquad",
            r"A'=",
            r"C^{-1}AC",
            font_size=48,
        ).move_to(STAGE_CENTER + UP * 0.4)
        change[3].set_color(C_HL)
        chain = MathTex(
            r"\mathbf{y}",
            r"\xrightarrow{\;C\;}",
            r"\mathbf{x}",
            r"\xrightarrow{\;A\;}",
            r"A\mathbf{x}",
            r"\xrightarrow{\;C^{-1}\;}",
            r"A'\mathbf{y}",
            font_size=38,
        ).next_to(change, DOWN, buff=0.65)
        if chain.width > 11:
            chain.scale(11 / chain.width)
        self.play(Write(change), run_time=1.5)
        self.play(Write(chain), run_time=1.6)
        self.play(Circumscribe(change[3], color=C_HL, run_time=0.9))
        self.hold()
        self.play(FadeOut(change), FadeOut(chain), run_time=0.5)

        # ---- 6. 两面性 -------------------------------------------------------
        self.say(
            "因此矩阵既有“坐标依赖”的一面，也有“动作不依赖坐标”的一面。"
            "区分这两层，是从算数字走向理解线性代数的关键一步。"
        )
        two = VGroup(
            card("坐标依赖", "数字外观随尺改变", C_SUB),
            card("动作不变", "对象本身与坐标无关", C_POS),
        ).arrange(RIGHT, buff=1.0).move_to(STAGE_CENTER)
        self.play(FadeIn(two[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(two[1], shift=UP * 0.3), run_time=0.8)
        self.hold()
        self.play(FadeOut(two), run_time=0.5)

        # ---- 7. 留尾：什么不随坐标改变？ --------------------------------------
        self.say(
            "如果换一套坐标只改变描述语言，那么同一个动作在不同语言中"
            "应该保留某些共同性质。至于哪些量不会改变，以及能否找到一套"
            "特别简单的坐标，要等后面的章节再回答。"
        )
        later = Text("哪些量不随坐标改变？——特征值的钩子", font=FONT, font_size=30, color=C_HL)
        later.move_to(STAGE_CENTER)
        self.play(FadeIn(later, scale=1.05), run_time=0.8)
        self.play(Circumscribe(later, color=C_HL, run_time=1.0))
        self.hold()
        self.wait(0.6)
