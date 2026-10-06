"""Act02 · 独立理论的形成：从口诀到结构。

对应 mindmap Act02 的旁白。视觉主线：
    萨鲁斯口诀（只能三阶）→ 删一行一列 → 余子式成为递归入口
    → 拉普拉斯展开定理 → 展开式是接口不是本体 → 结构语言（子式/
    余子式/展开）→ 性质规则链。
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


def _grid3() -> tuple[VGroup, list[list[MathTex]]]:
    """3x3 元素网格：每个元素独立成 mobject，便于取坐标、做高亮。

    返回 (扁平 VGroup 供整体操作, 二维表 grid[i][j] 供按行列取元素)。
    """
    entries = [
        [r"a_{11}", r"a_{12}", r"a_{13}"],
        [r"a_{21}", r"a_{22}", r"a_{23}"],
        [r"a_{31}", r"a_{32}", r"a_{33}"],
    ]
    cells = VGroup()
    grid: list[list[MathTex]] = []
    for i in range(3):
        row: list[MathTex] = []
        for j in range(3):
            cell = MathTex(entries[i][j], font_size=36)
            cell.move_to(np.array([j * 1.0, (1 - i) * 0.85, 0.0]))
            cells.add(cell)
            row.append(cell)
        grid.append(row)
    return cells, grid


def _sarrus_arcs(grid: list[list[MathTex]], color: Color, up: bool) -> VGroup:
    """萨鲁斯的一组斜线弧：沿 (i, i+k) 模 3 的对角线连弧。

    up=True 画向上凸的弧（正项组），否则向下凹（负项组）。
    """
    arcs = VGroup()
    for k in range(3):
        pts = [grid[i][(i + k) % 3].get_center() for i in range(3)]
        angle = TAU / 8 if up else -TAU / 8
        # 不用 CurvedArrow：它的箭头会盖住网格元素，纯弧线更干净。
        arcs.add(ArcBetweenPoints(pts[0], pts[-1], angle=angle, color=color, stroke_width=3))
    return arcs


class Act02Theory(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 02", "独立理论的形成")

        # ---- 1. 萨鲁斯口诀 -----------------------------------------------
        self.say("三阶行列式常被教成一套“画线连接”的口诀——萨鲁斯法则。它适合三阶，却不能自然推广到四阶、五阶。")
        cells, grid = _grid3()
        cells.move_to(STAGE_CENTER + UP * 0.2)
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in cells], lag_ratio=0.04), run_time=1.2)
        arcs_pos = _sarrus_arcs(grid, C_POS, up=True)
        arcs_neg = _sarrus_arcs(grid, C_NEG, up=False)
        self.play(Create(arcs_pos), run_time=1.0)
        self.play(Create(arcs_neg), run_time=1.0)
        legend = VGroup(
            Text("＋ 三条对角线", font=FONT, font_size=24, color=C_POS),
            Text("− 三条反对角线", font=FONT, font_size=24, color=C_NEG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.7)
        self.play(FadeIn(legend, shift=LEFT * 0.3), run_time=0.6)
        self.hold()
        self.say(
            "它解决的是“怎么记住这一次计算”，而不是“为什么这些项必须这样出现”。"
            "真正更有生命力的问题是：如果删掉某一行、某一列，剩下的较小行列式，与原来的行列式有什么关系？"
        )
        self.hold(extra=0.5)

        # ---- 2. 删掉一行一列：余子式现身 -----------------------------------
        # 淡出第一行与第一列，剩下右下角的 2x2 即 M_11。
        faded = VGroup(*[grid[0][j] for j in range(3)] + [grid[1][0], grid[2][0]])
        keep = VGroup(grid[1][1], grid[1][2], grid[2][1], grid[2][2])
        self.play(FadeOut(arcs_pos), FadeOut(arcs_neg), FadeOut(legend), run_time=0.5)
        self.play(faded.animate.set_opacity(0.25), run_time=0.8)
        minor_box = SurroundingRectangle(keep, color=C_HL, buff=0.15, corner_radius=0.1)
        minor = MathTex(r"M_{11}=\begin{vmatrix}a_{22}&a_{23}\\a_{32}&a_{33}\end{vmatrix}", font_size=40)
        minor.to_edge(RIGHT, buff=0.9)
        arrow = Arrow(minor_box.get_right(), minor.get_left(), buff=0.15, stroke_width=3, color=C_HL)
        self.play(Create(minor_box), GrowArrow(arrow), Write(minor), run_time=1.4)
        self.hold()
        self.play(*[FadeOut(m) for m in (cells, minor_box, arrow, minor)], run_time=0.6)

        # ---- 3. 范德蒙德：每一项 = 系数 × 低阶行列式 ------------------------
        self.say(
            "范德蒙德已经注意到，展开式中的每一项，都可以看作一个系数乘上一个低阶行列式。"
            "余子式不再只是计算中的碎片，而成了递归理解高阶行列式的入口。"
        )
        expansion = MathTex(
            r"\det(A)", r"=\ ", r"a_{11}", r"\cdot", r"M_{11}",
            r"\ -\ ", r"a_{12}", r"\cdot", r"M_{12}",
            r"\ +\ ", r"a_{13}", r"\cdot", r"M_{13}",
            font_size=42,
        ).move_to(STAGE_CENTER + UP * 0.3)
        for coef, minor_part in ((2, 4), (6, 8), (10, 12)):
            expansion[coef].set_color(C_MAIN)
            expansion[minor_part].set_color(C_HL)
        signs = VGroup(expansion[5], expansion[9])
        signs.set_color(C_TEXT)
        self.play(Write(expansion), run_time=2.2)
        self.play(
            Indicate(expansion[4], color=C_HL),
            Indicate(expansion[8], color=C_HL),
            Indicate(expansion[12], color=C_HL),
            run_time=1.1,
        )
        self.hold()

        # ---- 4. 拉普拉斯展开定理 ------------------------------------------
        self.say(
            "拉普拉斯面对天文学和大规模计算中的高阶方程组，把这种想法整理成按行或按列展开的定理："
            "一个高阶对象，可以沿着一行，拆成若干个低阶对象。"
        )
        lap = MathTex(
            r"\det(A)=\sum_{j=1}^{n}a_{ij}\,C_{ij}",
            r",\qquad C_{ij}=(-1)^{i+j}M_{ij}",
            font_size=42,
        ).move_to(STAGE_CENTER + DOWN * 1.1)
        self.play(Write(lap), run_time=1.8)
        self.hold()
        self.play(*[FadeOut(m) for m in (expansion, lap)], run_time=0.6)

        # ---- 5. 展开式是接口，不是本体 --------------------------------------
        self.say(
            "这带来一个重要的认识：行列式的展开式不是它的本体，而是它的一种计算接口。"
            "我们可以换行、换列、递归展开，却仍在研究同一个对象。"
        )
        left = MathTex(r"\text{det } A", font_size=44)
        left_lab = Text("沿第一行展开", font=FONT, font_size=22, color=C_DIM)
        right = MathTex(r"\text{det } A", font_size=44)
        right_lab = Text("沿第二列展开", font=FONT, font_size=22, color=C_DIM)
        same = Text("同一个对象", font=FONT, font_size=30, color=C_HL, weight=BOLD)
        left_grp = VGroup(left, left_lab).arrange(DOWN, buff=0.25)
        right_grp = VGroup(right, right_lab).arrange(DOWN, buff=0.25)
        left_grp.move_to(STAGE_CENTER + LEFT * 3.2)
        right_grp.move_to(STAGE_CENTER + RIGHT * 3.2)
        same.move_to(STAGE_CENTER + UP * 0.2)
        arrow_l = Arrow(left_grp.get_right(), same.get_bottom() + LEFT * 0.6, buff=0.15, stroke_width=3, color=C_DIM)
        arrow_r = Arrow(right_grp.get_left(), same.get_bottom() + RIGHT * 0.6, buff=0.15, stroke_width=3, color=C_DIM)
        self.play(FadeIn(left_grp), FadeIn(right_grp), run_time=0.9)
        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r), Write(same), run_time=1.1)
        self.hold()
        self.play(*[FadeOut(m) for m in (left_grp, right_grp, same, arrow_l, arrow_r)], run_time=0.6)

        # ---- 6. 结构语言 ----------------------------------------------------
        self.say(
            "计算技巧逐渐让位于结构。行列式开始拥有自己的语言：子式、余子式、展开，"
            "以及由这些结构导出的性质。"
        )
        vocab = VGroup(
            card("子式", MathTex(r"M_{ij}", font_size=30), C_MAIN, sub_scale=0.9),
            card(
                "余子式",
                MathTex(r"C_{ij}=(-1)^{i+j}M_{ij}", font_size=30),
                C_HL,
                sub_scale=0.9,
            ),
            card("拉普拉斯展开", Text("沿任一行 / 列拆成低阶", font=FONT, font_size=21), C_POS, sub_scale=0.9),
        ).arrange(RIGHT, buff=0.7).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(v, scale=1.08) for v in vocab], lag_ratio=0.3), run_time=1.6)
        self.hold()
        self.play(FadeOut(vocab), run_time=0.6)

        # ---- 7. 性质规则链 ---------------------------------------------------
        self.say(
            "这些性质最终汇成一条稳定的规则链：交换行会改变方向，倍乘行会改变尺度，倍加行却不改变它；"
            "行与列互换不改变它；三角形排布的行列式，只需把对角线连乘。"
        )
        rules = VGroup(
            card("交换两行", "行列式变号", C_NEG),
            card("某行乘 k", "行列式乘 k", C_MAIN),
            card("某行加上另一行的倍数", "行列式不变", C_POS),
            card("转置（行 ⇆ 列）", "行列式不变", C_POS),
            card("三角形排布", "对角线连乘", C_HL),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.6, 0.5)).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(r, scale=1.08) for r in rules], lag_ratio=0.22), run_time=2.2)
        self.hold()
        self.say(
            "行列式不再是某一种算法，而是对各种“改写”作出精确响应的结构——"
            "它像一台记录仪，把每一次行变换的后果都如实记下来。"
        )
        self.play(Circumscribe(rules, color=C_HL, run_time=1.1))
        self.hold()
        self.wait(0.6)
