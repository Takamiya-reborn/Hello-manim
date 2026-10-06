"""Act04 · 排列与奇偶性：符号从哪里来。

对应 mindmap Act04 的旁白。视觉主线：
    为什么换序符号必须变（行交换演示）→ 逆序对的定义与计数
    → 三个排列的实例（弧线标逆序对）→ S₃ 的六排列符号表
    → sgn(σ) = (−1)^逆序数 → 代数与几何在此相遇。
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


def _inversions(nums: list[int]) -> list[tuple[int, int]]:
    """返回排列 nums 的全部逆序对下标 (i, j)，i<j 且 nums[i]>nums[j]。"""
    return [(i, j) for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j]]


def _perm_row(nums: list[int]) -> tuple[VGroup, int]:
    """画一行数字圆片 + 标出全部逆序对的弧线，返回 (群组, 逆序数)。"""
    radius = 0.3
    discs = VGroup()
    for i, n in enumerate(nums):
        disc = Circle(radius=radius, color=C_MAIN, stroke_width=3).move_to([i * 0.95, 0, 0])
        digit = Text(str(n), font=FONT, font_size=30, color=C_TEXT).move_to(disc)
        discs.add(VGroup(disc, digit))
    inv = _inversions(nums)
    arcs = VGroup()
    for i, j in inv:
        arc = ArcBetweenPoints(
            discs[i].get_center() + UP * radius,
            discs[j].get_center() + UP * radius,
            angle=-TAU / 3,  # 向上凸的弧
            color=C_NEG,
            stroke_width=3.5,
        )
        arcs.add(arc)
    return VGroup(discs, arcs), len(inv)


def _sign_chip(nums: list[int]) -> VGroup:
    """符号表中的一格：排列 + 由奇偶性决定的红绿符号。"""
    perm = Text(" ".join(map(str, nums)), font=FONT, font_size=28, color=C_TEXT)
    is_even = len(_inversions(nums)) % 2 == 0
    sign = (
        Text("＋", font=FONT, font_size=30, color=C_POS)
        if is_even
        else Text("−", font=FONT, font_size=30, color=C_NEG)
    )
    grp = VGroup(perm, sign).arrange(RIGHT, buff=0.35)
    board = RoundedRectangle(
        corner_radius=0.12,
        width=grp.width + 0.5,
        height=grp.height + 0.35,
        stroke_color=sign.get_color(),
        stroke_width=2,
        fill_color=sign.get_color(),
        fill_opacity=0.1,
    ).move_to(grp)
    return VGroup(board, grp)


class Act04Parity(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 04", "排列与奇偶性")

        # ---- 1. 为什么符号必须变？行交换给出最直接的证据 ---------------------
        self.say("先放下几何这条支线，回到代数内部一个更尖锐的问题：为什么排列换了顺序，展开式中的符号也必须改变？")
        det1 = MathTex(
            r"\begin{vmatrix}a&b\\c&d\end{vmatrix}", r"=ad-bc", font_size=44
        ).move_to(STAGE_CENTER + UP * 0.4)
        det1[1].set_color(C_POS)
        det2 = MathTex(
            r"\begin{vmatrix}c&d\\a&b\end{vmatrix}", r"=cb-da=-(ad-bc)", font_size=44
        ).move_to(STAGE_CENTER + UP * 0.4)
        det2[1].set_color(C_NEG)
        note = Text("交换两行 → 变号", font=FONT, font_size=28, color=C_NEG)
        note.next_to(det1, DOWN, buff=0.6)
        self.play(Write(det1), run_time=1.5)
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.hold()
        self.play(Transform(det1, det2), run_time=1.2)
        self.hold()
        self.play(FadeOut(det1), FadeOut(note), run_time=0.5)

        # ---- 2. 逆序对：自然的计数方式 ----------------------------------------
        self.say(
            "一个自然的计数方式是逆序对：排列中前面的数大于后面的数，就形成一对逆序。"
            "逆序对数量的奇偶性，恰好决定这一项取正号还是负号。"
        )
        # 例一：312 → 两对逆序 → 偶 → +
        row1, n_inv1 = _perm_row([3, 1, 2])
        row1.move_to(STAGE_CENTER + UP * 0.9)
        count1 = MathTex(r"(3,1,2):\ \tau=", str(n_inv1), font_size=36)
        sign1 = Text("偶排列 → 取 ＋", font=FONT, font_size=28, color=C_POS)
        count1.next_to(row1, DOWN, buff=0.4).shift(LEFT * 1.2)
        sign1.next_to(count1, RIGHT, buff=0.6)
        self.play(FadeIn(row1, shift=UP * 0.3), run_time=0.8)
        self.play(Create(row1[1]), run_time=0.8)  # 逆序弧
        self.play(Write(count1), FadeIn(sign1, shift=LEFT * 0.3), run_time=0.9)
        self.hold()

        # ---- 3. 再看一个奇排列 --------------------------------------------------
        self.say("再看一个：3,2,1 的逆序对有三对，是奇排列——这一项必须取负号。")
        row2, n_inv2 = _perm_row([3, 2, 1])
        row2.move_to(row1.get_center())  # 原地替换
        count2 = MathTex(r"(3,2,1):\ \tau=", str(n_inv2), font_size=36)
        sign2 = Text("奇排列 → 取 −", font=FONT, font_size=28, color=C_NEG)
        count2.next_to(row2, DOWN, buff=0.4).shift(LEFT * 1.2)
        sign2.next_to(count2, RIGHT, buff=0.6)
        self.play(Transform(row1, row2), FadeOut(count1), FadeOut(sign1), run_time=1.0)
        self.play(Write(count2), FadeIn(sign2, shift=LEFT * 0.3), run_time=0.9)
        self.hold()
        self.play(FadeOut(row1), FadeOut(count2), FadeOut(sign2), run_time=0.5)

        # ---- 4. S3 的六排列符号表 ------------------------------------------------
        self.say("把三阶的全部 3! 个排列排开：三个偶排列、三个奇排列——正负恰好各半。")
        table = VGroup(
            _sign_chip([1, 2, 3]),
            _sign_chip([1, 3, 2]),
            _sign_chip([2, 1, 3]),
            _sign_chip([2, 3, 1]),
            _sign_chip([3, 1, 2]),
            _sign_chip([3, 2, 1]),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.55, 0.45)).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(t, scale=1.08) for t in table], lag_ratio=0.15), run_time=1.8)
        self.hold()

        # ---- 5. sgn 公式 ----------------------------------------------------------
        self.say("把这件事写成公式：符号函数 sgn，就是逆序数 τ 的幂。")
        sgn = MathTex(
            r"\operatorname{sgn}(\sigma)=(-1)^{\tau(\sigma)}",
            font_size=46,
        ).move_to(STAGE_CENTER)
        self.play(Transform(table, sgn), run_time=1.1)
        self.hold()
        self.play(FadeOut(table), FadeOut(sgn), run_time=0.5)

        # ---- 6. 代数与几何相遇 ------------------------------------------------------
        self.say(
            "于是代数与几何在这里相遇：排列的奇偶性负责记录方向的翻转，"
            "行列式的零值负责记录维度的塌缩。一个是符号语言，一个是面积语言，说的却是同一件事。"
        )
        meet = VGroup(
            VGroup(
                Text("奇偶性", font=FONT, font_size=30, color=C_HL, weight=BOLD),
                Text("记录方向的翻转", font=FONT, font_size=24, color=C_TEXT),
            ).arrange(DOWN, buff=0.25),
            VGroup(
                Text("零值", font=FONT, font_size=30, color=C_NEG, weight=BOLD),
                Text("记录维度的塌缩", font=FONT, font_size=24, color=C_TEXT),
            ).arrange(DOWN, buff=0.25),
        )
        for half in meet:
            board = RoundedRectangle(
                corner_radius=0.15,
                width=half.width + 0.6,
                height=half.height + 0.6,
                fill_color=C_MAIN,
                fill_opacity=0.12,
                stroke_color=C_DIM,
                stroke_width=2,
            ).move_to(half)
            half.add_to_back(board)
        meet.arrange(RIGHT, buff=1.2).move_to(STAGE_CENTER)
        plus = MathTex(r"+", font_size=56, color=C_TEXT).move_to(meet.get_center())
        self.play(FadeIn(meet[0], shift=RIGHT * 0.4), run_time=0.8)
        self.play(FadeIn(meet[1], shift=LEFT * 0.4), run_time=0.8)
        self.play(FadeIn(plus, scale=1.8), run_time=0.5)
        self.hold()
        self.wait(0.6)
