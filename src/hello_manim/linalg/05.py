"""第 5 课：逆矩阵、列空间与零空间——秩的几何意义。

本课要回答三个问题：
    1. "矩阵的逆"为什么就是"变换的撤销"？什么样的变换撤销不了？
    2. 平面被压扁后，哪些 b 还有落点？——列空间与 Ax = b 的解
    3. 哪些向量被压到原点？秩 + 零空间维数为什么恰好等于 n？

原理速览：
    数学上，三个场景围绕"可逆 = 不丢信息"这条主线展开：
      - 逆矩阵：AA⁻¹ = A⁻¹A = I，"先 A 后 A⁻¹"与"先 A⁻¹ 后 A"都
        回到恒等变换。可逆 ⇔ det ≠ 0：det = 0 的变换把平面压成一条
        线，两个不同的向量落到同一点，信息已丢失，无法撤销；
      - 列空间 Col(A)：两个列向量的全部线性组合，即"所有落点的
        集合"。Ax = b 有解 ⇔ b 落在列空间里。满秩时列空间是全平面，
        任何 b 都有解；B = [[1,2],[2,4]] 两列共线，列空间塌缩成过
        原点的直线 span{(1,2)}，只有落在这条线上的 b 才有解；
      - 零空间 ker(A)：被 A 压到原点的所有向量，即 Ax = 0 的解集。
        对 B 解 x + 2y = 0 得 ker(B) = span{(2,-1)}，恰与列空间直线
        垂直。秩 = 列空间的维数；秩-零化度定理说
        dim ker(A) + rank(A) = n：压没的维数 + 留下的维数 = 列数。
    manim 手段：
      - NumberPlane 充当"空间本身"的替身，网格被揉捏、压扁的过程
        就是变换与降维本身；
      - mobject.animate.apply_matrix(M, about_point=o)：把矩阵作用
        写成动画。about_point 指定不动点——网格被平移过时必须把
        不动点设回网格自己的原点，否则"线性变换"会偷偷掺进平移；
      - Arrow 画向量、Line 画子空间；公式走 MathTex（raw string），
        中文一律走 Text，二者各司其职。

最短运行：
    uv run hello-manim linalg 05

也可以用 manim 原生命令行逐个渲染同一课的场景：
    uv run manim -pql src/hello_manim/linalg/05.py InverseAsUndo
    uv run manim -pql src/hello_manim/linalg/05.py ColumnSpace
    uv run manim -pql src/hello_manim/linalg/05.py RankAndKernel
"""

import argparse

import numpy as np
from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class InverseAsUndo(Scene):
    def construct(self) -> None:
        # 标题与核心等式贴上边缘：to_edge 把物体推到画面指定边，
        # 是"标题区"的惯用布局，保证不与画面主体争位置。
        title = Text("逆矩阵：变换的撤销键", font_size=32)
        title.to_edge(UP, buff=0.35)
        # MathTex 写标准 LaTeX（raw string 防转义）；bmatrix 是 amsmath
        # 的矩阵环境，manim 默认模板已包含。拆子串是为了后面能单独染色。
        eq = MathTex(
            r"A = \begin{bmatrix} 2 & 0 \\ 1 & 2 \end{bmatrix}",
            r"\qquad",
            r"A^{-1}A = AA^{-1} = I",
            font_size=36,
        )
        eq.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), Write(eq), run_time=2)

        # NumberPlane 充当"空间本身"：网格怎么被揉捏，变换就怎么作用。
        # 整体下移给顶部文字带让位；线透明度调低，文字压在网格上仍可读。
        plane = NumberPlane(
            x_range=[-7.5, 7.5, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5},
        ).shift(DOWN * 0.6)
        # 网格平移过了，"不动点"必须设回网格自己的原点——否则矩阵
        # 绕屏幕中心作用，线性变换里会掺进平移，几何就错了。
        origin = plane.c2p(0, 0)
        self.add(plane)
        self.wait(0.5)

        # A = [[2,0],[1,2]]：横向拉伸 2 倍并带切变，det = 4 ≠ 0，可逆。
        # 逆矩阵用 np.linalg.inv 现场算，数值不手抄——正确性交给库。
        A = np.array([[2.0, 0.0], [1.0, 2.0]])
        A_inv = np.linalg.inv(A)

        # apply_matrix 把每个点 p 映到 Ap；.animate 让 manim 插值出
        # 中间帧，网格的拉伸与切变就"演"了出来。
        self.play(plane.animate.apply_matrix(A, about_point=origin), run_time=2)

        # 撤销：同一网格再吃一个 A⁻¹。复合 A⁻¹A = I，网格精确复原——
        # "逆矩阵"就是能撤销这次变换的那个矩阵。
        self.play(plane.animate.apply_matrix(A_inv, about_point=origin), run_time=2)

        # 复原成功，点亮等式右端：恒等变换 = 什么都没做的变换。
        self.play(eq[2].animate.set_color(YELLOW))
        self.wait(1)

        # 反例点题：det = 0 的变换把平面压成一条线，两个不同的向量
        # 落到同一点——信息已丢失，任何矩阵都撤不回来，所以无逆。
        note = Text(
            "det = 0 的变换把平面压扁：信息丢失，无法撤销——逆不存在",
            font_size=24, color=GREY_A,
        )
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(2)


class ColumnSpace(Scene):
    def construct(self) -> None:
        title = Text("列空间：所有落点的集合", font_size=32)
        title.to_edge(UP, buff=0.35)
        # 说明文字放在标题下方的同一"槽位"，先后 Transform 换词——
        # 布局稳定不跳动，观众只注意文字内容的变化。
        caption = Text("满秩：平面映到全平面，任何 b 都有解", font_size=24, color=GREY_A)
        caption.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(caption))

        # 满秩矩阵 A1：两列 (2,1)、(1,3) 不共线，det = 5 ≠ 0。
        A_full = np.array([[2.0, 1.0], [1.0, 3.0]])
        plane1 = NumberPlane(
            x_range=[-7.5, 7.5, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5},
        ).shift(DOWN * 0.6)
        self.add(plane1)
        # 变形后网格仍铺满整个画面：每个方向都有落点，列空间 = 全平面。
        self.play(
            plane1.animate.apply_matrix(A_full, about_point=plane1.c2p(0, 0)),
            run_time=2,
        )
        self.wait(1)

        # 降秩矩阵 B：两列 (1,2)、(2,4) 共线（后者是前者的 2 倍），
        # det = 0——整张网格将被压进一条过原点的直线。
        B = np.array([[1.0, 2.0], [2.0, 4.0]])
        plane2 = NumberPlane(
            x_range=[-7.5, 7.5, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5},
        ).shift(DOWN * 0.6)
        self.play(FadeOut(plane1))
        caption_new = Text(
            "降秩：列共线，落点被压到一条过原点的直线上", font_size=24, color=GREY_A,
        )
        self.play(Transform(caption, caption_new))
        self.add(plane2)
        self.play(plane2.animate.apply_matrix(B, about_point=plane2.c2p(0, 0)), run_time=2)

        # 把塌缩后的网格描粗上色：这条线就是列空间 span{(1,2)}——
        # 所有 Ax 的落点全在上面，再没有别的可能。
        col_line = Line(
            ORIGIN, 3.2 * np.array([1.0, 2.0, 0]) / np.sqrt(5),
            color=GREEN, stroke_width=8,
        ).shift(DOWN * 0.6)
        span_label = MathTex(
            r"\operatorname{span}\{\,(1,\ 2)\,\}", font_size=34, color=GREEN,
        )
        span_label.next_to(col_line, RIGHT, buff=0.4)
        self.play(Create(col_line), Write(span_label))

        # Ax = b 有解 ⇔ b 落在列空间里。b1 = 1.3·(1,2) 在线上：有解；
        # b2 = (2.5,-1) 不在线上：无解。Arrow 从原点指向 b 的位置。
        b1 = Arrow(ORIGIN, 1.3 * np.array([1.0, 2.0, 0]), color=BLUE, buff=0).shift(DOWN * 0.6)
        b2 = Arrow(ORIGIN, np.array([2.5, -1.0, 0]), color=RED, buff=0).shift(DOWN * 0.6)
        b1_label = MathTex("b_1", font_size=32, color=BLUE).next_to(b1.get_end(), UP, buff=0.15)
        b2_label = MathTex("b_2", font_size=32, color=RED).next_to(b2.get_end(), RIGHT, buff=0.2)
        self.play(GrowArrow(b1), GrowArrow(b2), FadeIn(b1_label), FadeIn(b2_label))
        self.wait(1)

        # 结论放画面底部，左右各一条，与上方图形互不遮挡。
        sol = Text("b₁ 在列空间里：Ax = b₁ 有解", font_size=22, color=BLUE)
        unsol = Text("b₂ 不在列空间里：Ax = b₂ 无解", font_size=22, color=RED)
        sol.to_edge(DOWN, buff=0.35).shift(LEFT * 3.5)
        unsol.next_to(sol, RIGHT, buff=0.9)
        self.play(FadeIn(sol), FadeIn(unsol))
        self.wait(2)


class RankAndKernel(Scene):
    def construct(self) -> None:
        title = Text("秩与零空间", font_size=32)
        title.to_edge(UP, buff=0.35)
        # 秩的定义：列空间的维数。满秩矩阵秩为 2；下面这个降秩的 B 只有 1。
        rank_def = MathTex(
            r"\operatorname{rank}(A) = \dim(\operatorname{Col} A)", font_size=32,
        )
        rank_def.next_to(title, DOWN, buff=0.25)
        self.play(Write(title), Write(rank_def))

        # 仍用降秩矩阵 B，先把网格压扁：秩 1 的世界一目了然。
        B = np.array([[1.0, 2.0], [2.0, 4.0]])
        plane = NumberPlane(
            x_range=[-7.5, 7.5, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5},
        ).shift(DOWN * 0.7)
        origin = plane.c2p(0, 0)
        self.add(plane)
        self.play(plane.animate.apply_matrix(B, about_point=origin), run_time=2)

        # 零空间：解 Bx = 0。B 的两个方程同为 x + 2y = 0，解集是
        # span{(2,-1)}——画成双向延长的直线（橙），恰与列空间直线垂直。
        u = np.array([2.0, -1.0, 0]) / np.sqrt(5)
        kernel_line = Line(-4.2 * u, 4.2 * u, color=ORANGE, stroke_width=6).shift(DOWN * 0.7)
        ker_label = MathTex(r"x + 2y = 0", font_size=32, color=ORANGE)
        ker_label.next_to(kernel_line.get_end(), DOWN, buff=0.3)
        self.play(Create(kernel_line), Write(ker_label))

        # 零空间里的向量取 k·(2,-1)（正负对称取四个）；再放一个不在
        # 零空间的 (1,0) 作对照。buff=0 让箭头尖恰好落在终点向量处。
        kernel_arrows = VGroup(
            *[
                Arrow(ORIGIN, k * np.array([2.0, -1.0, 0]), color=YELLOW, buff=0)
                for k in (1.0, 0.5, -0.5, -1.0)
            ]
        ).shift(DOWN * 0.7)
        other = Arrow(ORIGIN, np.array([1.0, 0.0, 0]), color=BLUE, buff=0).shift(DOWN * 0.7)
        self.play(*[GrowArrow(a) for a in kernel_arrows], GrowArrow(other))
        self.wait(1)

        # 施加 B：零空间向量满足 Bv = 0，四支黄箭头收缩成原点一个点；
        # 对照向量 (1,0) 被送到 (1,2)——落在列空间直线上，没消失。
        # 三个物体共用同一个不动点 origin，保证是同一个线性变换。
        self.play(
            kernel_line.animate.apply_matrix(B, about_point=origin),
            kernel_arrows.animate.apply_matrix(B, about_point=origin),
            other.animate.apply_matrix(B, about_point=origin),
            run_time=2,
        )
        self.wait(1)

        # 一句话总结观察，贴下边缘。
        note = Text(
            "零空间整条直线被压到原点；其余向量全部落在列空间直线上",
            font_size=22, color=GREY_A,
        )
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note))
        self.wait(1)

        # 清场后压轴总结：秩-零化度定理——压没的维数 + 留下的维数 = 列数。
        self.play(
            FadeOut(plane), FadeOut(kernel_line), FadeOut(kernel_arrows),
            FadeOut(other), FadeOut(ker_label), FadeOut(note),
        )
        theorem = VGroup(
            Text("秩-零化度定理", font_size=28),
            MathTex(
                r"\dim\,\ker(A)", "+", r"\operatorname{rank}(A)", "=", "n", font_size=42,
            ),
            MathTex("1", "+", "1", "=", "2", font_size=42),
            Text("零空间维数 1 + 秩 1 = 列数 n = 2（例：B = [[1, 2], [2, 4]]）",
                 font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        theorem.next_to(rank_def, DOWN, buff=0.7)
        # 上色对应：零空间维数（黄）与秩（绿），两行公式一一呼应。
        theorem[1][0].set_color(YELLOW)
        theorem[1][2].set_color(GREEN)
        theorem[2][0].set_color(YELLOW)
        theorem[2][2].set_color(GREEN)
        self.play(Write(theorem))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="逆矩阵、列空间与零空间：秩的几何意义")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg", "05",
        [InverseAsUndo, ColumnSpace, RankAndKernel],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
