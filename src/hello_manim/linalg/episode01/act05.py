"""Act05 · 行列式的身份证：一个数够吗？

对应 mindmap Act05 的旁白。视觉主线：
    零散规律回顾 → 柯西整理成"身份证"（数表 → 一个数）
    → 但数不回答"每个方向去了哪里" → 方向被压扁的三个问题
    → 真正想保存的是变换本身 → 矩阵的轮廓 → 下一集预告。
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
from hello_manim.utils.widgets import card


class Act05Identity(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 05", "行列式的身份证")

        # ---- 1. 零散规律回顾 ------------------------------------------------
        self.say(
            "到十九世纪初，行列式已经积累了许多零散的计算规律：交换两行会变号；"
            "某一行乘以一个数，行列式也乘以这个数；两行相同或呈现重复关系时，行列式为零；"
            "对行做消元式变换，行列式的变化可以被准确追踪。"
        )
        rules = VGroup(
            card("交换两行", "变号", C_NEG),
            card("某行乘 k", "乘 k", C_MAIN),
            card("两行相同", "等于零", C_NEG),
            card("倍加消元", "可追踪", C_POS),
        ).arrange(RIGHT, buff=0.55).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(r, scale=1.08) for r in rules], lag_ratio=0.22), run_time=1.8)
        self.hold()
        self.play(FadeOut(rules), run_time=0.5)

        # ---- 2. 身份证：数表 → 一个数 ----------------------------------------
        self.say(
            "柯西等人开始用行标、列标和更系统的符号，把这些规律整理成一组稳定的性质。"
            "行列式不再依附于某个解题步骤，而像一个有明确“身份证”的数学对象。"
        )
        id_card = RoundedRectangle(
            corner_radius=0.2,
            width=10.5,
            height=3.2,
            stroke_color=C_HL,
            stroke_width=3,
            fill_color=C_HL,
            fill_opacity=0.08,
        ).move_to(STAGE_CENTER)
        id_title = Text("行列式 · 身份证", font=FONT, font_size=30, color=C_HL, weight=BOLD)
        id_title.next_to(id_card, UP, buff=0.25)
        # 函数机器：输入数表 → det → 输出一个数
        input_mob = MathTex(r"A\in\mathbb{R}^{n\times n}", font_size=34)
        input_lab = Text("输入：方形数表", font=FONT, font_size=20, color=C_DIM)
        det_machine = MathTex(r"\det", font_size=44, color=C_HL)
        det_lab = Text("严格响应每一次行列变化", font=FONT, font_size=20, color=C_DIM)
        output_mob = MathTex(r"\mathbb{R}", font_size=34)
        output_lab = Text("输出：一个数", font=FONT, font_size=20, color=C_DIM)
        in_grp = VGroup(input_mob, input_lab).arrange(DOWN, buff=0.2)
        mid_grp = VGroup(det_machine, det_lab).arrange(DOWN, buff=0.2)
        out_grp = VGroup(output_mob, output_lab).arrange(DOWN, buff=0.2)
        row = VGroup(in_grp, mid_grp, out_grp).arrange(RIGHT, buff=1.1).move_to(id_card)
        arrow1 = Arrow(in_grp.get_right(), mid_grp.get_left(), buff=0.12, stroke_width=3, color=C_DIM)
        arrow2 = Arrow(mid_grp.get_right(), out_grp.get_left(), buff=0.12, stroke_width=3, color=C_DIM)
        self.play(Create(id_card), Write(id_title), run_time=1.0)
        self.play(FadeIn(in_grp), GrowArrow(arrow1), run_time=0.8)
        self.play(FadeIn(mid_grp), GrowArrow(arrow2), FadeIn(out_grp), run_time=0.9)
        self.hold()

        # ---- 3. 一个数说不清"方向去了哪里" ------------------------------------
        self.say(
            "但“输出一个数”仍然像是在描述结果，而不是描述过程。"
            "我们真正想知道的，也许不是某个变换把体积放大了多少，"
            "而是它究竟把每一个方向带去了哪里。"
        )
        plane = NumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-2, 4, 1],
            x_length=4.4,
            y_length=4.4,
            background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.4},
        ).move_to(id_card.get_center() + DOWN * 0.2)
        self.play(
            FadeOut(row), FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(id_title), FadeOut(id_card),
            run_time=0.6,
        )
        O = plane.c2p(0, 0)
        au = Arrow(O, plane.c2p(2, 1), buff=0, color=C_MAIN, stroke_width=5)
        av = Arrow(O, plane.c2p(1, 2.5), buff=0, color=C_HL, stroke_width=5)
        au2 = Arrow(O, plane.c2p(3, 0.5), buff=0, color=C_MAIN, stroke_width=5)
        av2 = Arrow(O, plane.c2p(1.5, 3), buff=0, color=C_HL, stroke_width=5)
        badge = MathTex(r"\det=-3", font_size=40, color=C_HL)
        badge.to_edge(RIGHT, buff=1.0).shift(UP * 1.0)
        where = Text("每个方向去了哪里？", font=FONT, font_size=26, color=C_TEXT)
        where.next_to(badge, DOWN, buff=0.6)
        self.play(Create(plane), GrowArrow(au), GrowArrow(av), run_time=1.2)
        self.play(Write(badge), FadeIn(where, shift=LEFT * 0.3), run_time=0.8)
        self.play(Transform(au, au2), Transform(av, av2), run_time=1.3)
        self.hold()
        self.play(
            *[FadeOut(m) for m in (plane, au, av, badge, where)],
            run_time=0.6,
        )

        # ---- 4. 被压扁的方向：三个悬而未决的问题 ------------------------------
        self.say(
            "行列式已经把“动作是否塌缩”压成了一个数，却没有保存信息究竟从哪个方向流失。"
            "也许我们真正想保存的，从来不只是变换留下的这个数，而是变换本身。"
        )
        square = Square(side_length=2.2, color=C_MAIN, fill_color=C_MAIN, fill_opacity=0.3)
        square.move_to(STAGE_CENTER + LEFT * 2.6)
        squashed = Polygon(
            LEFT * 1.1, RIGHT * 1.1, RIGHT * 1.1 + UP * 0.001, LEFT * 1.1 + UP * 0.001,
            color=C_NEG, fill_color=C_NEG, fill_opacity=0.3,
        ).move_to(STAGE_CENTER + LEFT * 2.6).shift(DOWN * 1.2)
        questions = VGroup(
            Text("哪个方向被压扁了？", font=FONT, font_size=26, color=C_NEG),
            Text("哪些方向仍然可以抵达？", font=FONT, font_size=26, color=C_POS),
            Text("不同输入为何撞到同一输出？", font=FONT, font_size=26, color=C_HL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(STAGE_CENTER + RIGHT * 2.4)
        self.play(DrawBorderThenFill(square), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(q, shift=LEFT * 0.3) for q in questions], lag_ratio=0.3), run_time=1.4)
        self.hold()
        self.play(Transform(square, squashed), run_time=1.2)
        self.hold()
        self.play(*[FadeOut(m) for m in (square, questions)], run_time=0.5)

        # ---- 5. 把整台机器留下来 ---------------------------------------------
        self.say(
            "要追踪被压扁的方向、仍可抵达的方向，以及不同输入为何会撞到同一个输出，"
            "我们必须把整台机器留下来——而“机器”，正是下一集的主角。"
        )
        matrix = Matrix([["a", "b"], ["c", "d"]], include_background_rectangle=False)
        matrix.get_entries().set_color(C_MAIN)
        matrix.scale(1.2).move_to(STAGE_CENTER)
        machine = Text("整台机器，原样保存", font=FONT, font_size=28, color=C_HL)
        machine.next_to(matrix, DOWN, buff=0.55)
        self.play(Write(matrix), run_time=1.6)
        self.play(FadeIn(machine, shift=UP * 0.2), run_time=0.7)
        self.hold()

        # ---- 6. 下一集预告 ----------------------------------------------------
        self.play(FadeOut(matrix), FadeOut(machine), run_time=0.5)
        self.say("下集预告：把记录变换的整块数字，当作一个独立的代数实体。")
        next_ep = VGroup(
            Text("线性代数 · Episode 02", font=FONT, font_size=26, color=C_HL),
            Text("线性变换的本身——矩阵", font=FONT, font_size=42, weight=BOLD, color=C_TEXT),
        ).arrange(DOWN, buff=0.4).move_to(STAGE_CENTER)
        self.play(FadeIn(next_ep, shift=UP * 0.3), run_time=0.9)
        self.wait(1.6)
        self.play(FadeOut(next_ep), run_time=0.6)
        self.wait(0.4)
