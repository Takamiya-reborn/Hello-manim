r"""第 6 课：线性方程组与高斯消元。

本课要回答三个问题：
    1. 一个线性方程组在几何上长什么样，"解"究竟是什么？
    2. 高斯消元的每步行变换，凭什么不改变解集？
    3. 不解到底，怎么提前判断方程组"有没有解、有几个解"？

原理速览：
    数学上，二元线性方程组的每个方程 ax+by=e 都对应平面上一条
    直线，解就是所有直线的公共点。高斯消元做的是"变形不改解"：
    三类行变换（换位、倍乘、倍加）都可逆，因此变换前后的方程组
    同解；消成上三角后从最后一行开始回代，逐个把未知数"解套"。
    判定解的个数看秩：r(A) 是行阶梯形中非零行的个数，r(A|b) 再
    把常数列算进去（n 为未知数个数）：
      - r(A) = r(A|b) = n：唯一解（直线相交于一点）；
      - r(A) < r(A|b)：无解（出现 0 = 非零的矛盾行，直线平行）；
      - r(A) = r(A|b) < n：无穷多解（直线重合，留有自由变量）。
    manim 手段：Axes + plot 画直线（幕 1）；增广矩阵用
    \left[\begin{array}{cc|c} 排版，两行拆成子串后可分别上色，
    TransformMatchingTex 按 token 配对做行变换渐变（幕 2）；
    VGroup.arrange 把三个面板一字排开做对比（幕 3）。

最短运行：
    uv run hello-manim linalg 06

也可以用 manim 原生命令行渲染单个场景：
    uv run manim -pql src/hello_manim/linalg/06.py EquationsAsIntersections
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class EquationsAsIntersections(Scene):
    """幕 1：方程组的几何面貌——两个方程两条直线，解 = 交点。"""

    def construct(self) -> None:
        # 标题顶置：to_edge(UP) 是最稳妥的"不挡内容"位置。
        title = Text("方程组的几何面貌：解 = 交点", font_size=32)
        title.to_edge(UP, buff=0.3)

        # Axes 是数学坐标与屏幕坐标的翻译官（第 5 课）。
        # 范围按两条直线的走势选：x∈[-1,5] 足够容纳交点 (2,1) 的邻域。
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 4, 1],
            x_length=6,
            y_length=4.5,
            tips=False,
        )
        axes.shift(LEFT * 2.8)  # 整体左移，右侧留给方程与增广矩阵
        self.play(FadeIn(title), Create(axes), run_time=1.5)

        # plot 只吃显函数，所以先把每个方程解出 y：
        # x + 2y = 4 → y = (4-x)/2；3x - y = 5 → y = 3x - 5。
        line1 = axes.plot(lambda x: (4 - x) / 2, x_range=[-1, 5], color=BLUE)
        # 第二条斜率是 3，只取 y 不越出 [-2,4] 的 x 段，免得冲出坐标区。
        line2 = axes.plot(lambda x: 3 * x - 5, x_range=[1, 3], color=ORANGE)
        self.play(Create(line1), Create(line2), run_time=1.5)

        # 方程标签颜色 = 直线颜色 = 矩阵行颜色，三方对应一眼可读。
        eq1 = MathTex("x + 2y = 4", font_size=34, color=BLUE)
        eq2 = MathTex("3x - y = 5", font_size=34, color=ORANGE)
        eqs = VGroup(eq1, eq2)
        # aligned_edge=LEFT 让两条方程左对齐，看起来像"一组"。
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        eqs.next_to(axes, RIGHT, buff=0.8)
        self.play(Write(eq1), Write(eq2))

        # 增广矩阵：竖线用 LaTeX 的 array 环境写 {cc|c}——前两列是
        # 系数、竖线右边是常数。两行拆成独立子串，才能分别上色。
        mat = MathTex(
            r"\left[\begin{array}{cc|c}",
            r"1 & 2 & 4 \\",
            r"3 & -1 & 5",
            r"\end{array}\right]",
            font_size=44,
        )
        mat[1].set_color(BLUE)    # 第 1 行 ↔ 蓝直线 x+2y=4
        mat[2].set_color(ORANGE)  # 第 2 行 ↔ 橙直线 3x-y=5
        mat.next_to(eqs, DOWN, buff=0.8)
        self.play(Write(mat))

        # 解 (2,1)：代回验证 2+2·1=4、3·2-1=5 都成立。几何上它就是
        # 两条直线的公共点——"解 = 交点"。
        dot = Dot(axes.c2p(2, 1), color=YELLOW, radius=0.09)
        dot_label = MathTex("(2,\\ 1)", font_size=32, color=YELLOW)
        dot_label.next_to(dot, LEFT, buff=0.25)
        self.play(FadeIn(dot, scale=2), FadeIn(dot_label))

        # 收束句放底部边缘，与图形互不重叠。
        note = Text("两个方程两条直线，公共点就是解", font_size=26, color=YELLOW)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(1.5)


class GaussianElimination(Scene):
    """幕 2：高斯消元全程——行变换、上三角、回代，几何画面同步。"""

    def construct(self) -> None:
        title = Text("高斯消元：行变换化上三角，再回代", font_size=32)
        title.to_edge(UP, buff=0.3)

        # 右侧摆一个"几何同步"小坐标系：幕 1 的两条直线原样画上，
        # 全程不动——行变换只改代数形式，不改变解集（交点）。
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-2, 4, 1],
            x_length=4.5,
            y_length=3.5,
            tips=False,
        )
        axes.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.5)
        line1 = axes.plot(lambda x: (4 - x) / 2, x_range=[-1, 5], color=BLUE)
        line2 = axes.plot(lambda x: 3 * x - 5, x_range=[1, 3], color=ORANGE)
        geo_note = Text(
            "消元 = 用组合消去变量\n几何上直线不动，坐标逐步锁定",
            font_size=20,
            color=GREY,
            line_spacing=0.8,
        )
        geo_note.next_to(axes, DOWN, buff=0.35)
        self.play(
            Create(axes), Create(line1), Create(line2), FadeIn(geo_note), run_time=2
        )

        # 左侧主战场：增广矩阵。两行拆子串，便于分别上色、参与变换。
        m1 = MathTex(
            r"\left[\begin{array}{cc|c}",
            r"1 & 2 & 4 \\",
            r"3 & -1 & 5",
            r"\end{array}\right]",
            font_size=46,
        )
        m1[1].set_color(BLUE)
        m1[2].set_color(ORANGE)
        m1.next_to(title, DOWN, buff=0.55).shift(LEFT * 3.2)
        self.play(Write(m1))

        # 消元：R2 -= 3R1。用第一行的 3 倍抵消第二行的 x 系数：
        # (3,-1,5) - 3·(1,2,4) = (0,-7,-7)。行算式摆在矩阵正下方。
        op1 = MathTex(r"R_2 \to R_2 - 3R_1", font_size=32, color=GREEN)
        op1.next_to(m1, DOWN, buff=0.45)
        detail = MathTex(
            r"(3,\,-1,\,5) - 3\,(1,\,2,\,4) = (0,\,-7,\,-7)", font_size=26
        )
        detail.next_to(op1, DOWN, buff=0.3)
        self.play(Write(op1), run_time=1.5)
        self.play(Write(detail))

        # 新矩阵：第二行的 x 系数已归零。两份矩阵的第 1 行子串完全
        # 一致，TransformMatchingTex 会让它原地保留、只渐变第二行
        # ——这正是"部分变化"看起来自然的原因（base 第 6 课）。
        m2 = MathTex(
            r"\left[\begin{array}{cc|c}",
            r"1 & 2 & 4 \\",
            r"0 & -7 & -7",
            r"\end{array}\right]",
            font_size=46,
        )
        m2[1].set_color(BLUE)
        m2[2].set_color(ORANGE)
        m2.move_to(m1)
        self.play(TransformMatchingTex(m1, m2), run_time=2)
        self.wait(0.5)

        # 上三角完成：最后一行只含 y，直接解出；再代回第一行求 x。
        # 每步行变换都可逆 ⇒ 前后方程组同解，这里的解就是原方程组的解。
        back1 = MathTex(r"-7y = -7 \;\Rightarrow\; y = 1", font_size=30, color=YELLOW)
        back1.next_to(detail, DOWN, buff=0.45)
        self.play(Write(back1))
        back2 = MathTex(
            r"x + 2 \cdot 1 = 4 \;\Rightarrow\; x = 2", font_size=30, color=YELLOW
        )
        back2.next_to(back1, DOWN, buff=0.3)
        self.play(Write(back2))

        # 数值落定的一刻，交点在小坐标系里亮起——与幕 1 的结论呼应。
        dot = Dot(axes.c2p(2, 1), color=YELLOW, radius=0.09)
        self.play(FadeIn(dot, scale=2))
        self.wait(1.5)


class SolutionTypes(Scene):
    """幕 3：解的三种情况——三面板对比，秩 r(A) vs r(A|b) 一锤定音。"""

    def construct(self) -> None:
        title = Text("解的三种情况：看秩 r(A) 与 r(A|b)", font_size=32)
        title.to_edge(UP, buff=0.25)

        # 三个面板共用同一套坐标设置；先建好再用 arrange 一字排开。
        common = dict(
            x_range=[-2, 4, 1],
            y_range=[-2, 4, 1],
            x_length=3.6,
            y_length=2.6,
            tips=False,
        )
        ax1, ax2, ax3 = Axes(**common), Axes(**common), Axes(**common)
        VGroup(ax1, ax2, ax3).arrange(RIGHT, buff=0.8).shift(DOWN * 0.6)

        # ---- 面板 1：唯一解。x+y=3 与 x-y=1 斜率不同，交于 (2,1)。
        # x 段取 [-1,4]，保证两条线的 y 值都不越出 [-2,4]。
        l1a = ax1.plot(lambda x: 3 - x, x_range=[-1, 4], color=BLUE)
        l1b = ax1.plot(lambda x: x - 1, x_range=[-1, 4], color=ORANGE)
        d1 = Dot(ax1.c2p(2, 1), color=YELLOW, radius=0.07)
        self.play(Create(ax1), Create(l1a), Create(l1b), run_time=1.5)
        self.play(FadeIn(d1, scale=2))

        # ---- 面板 2：无解。x+y=1 与 x+y=3 斜率同、截距异——平行。
        # 代数上消元会出现 "0 = 2" 的矛盾行：r(A) < r(A|b)。
        l2a = ax2.plot(lambda x: 1 - x, x_range=[-1, 3.5], color=BLUE)
        l2b = ax2.plot(lambda x: 3 - x, x_range=[-1, 3.5], color=ORANGE)
        self.play(Create(ax2), Create(l2a), Create(l2b), run_time=1.5)

        # ---- 面板 3：无穷多解。2x+2y=2 与 x+y=1 是同一条直线。
        # 橙色方程画成虚线叠在蓝线上：两个方程一图象，解布满全线。
        l3a = ax3.plot(lambda x: 1 - x, x_range=[-1, 3], color=BLUE)
        l3b = DashedVMobject(
            ax3.plot(lambda x: 1 - x, x_range=[-1, 3], color=ORANGE),
            num_dashes=25,
        )
        self.play(Create(ax3), Create(l3a), Create(l3b), run_time=1.5)

        # 每个面板下方：结论名 + 秩判定。r(A) 是消元后非零行数，
        # r(A|b) 把常数列也算进去；n = 2 是未知数个数。
        names = [
            Text(t, font_size=26, color=c)
            for t, c in zip(("唯一解", "无解", "无穷多解"), (GREEN, RED, PURPLE))
        ]
        ranks = [
            MathTex(tex, font_size=26)
            for tex in (
                r"r(A) = r(A|b) = 2 = n",
                r"r(A) = 1 < r(A|b) = 2",
                r"r(A) = r(A|b) = 1 < 2 = n",
            )
        ]
        for name, rank, axes in zip(names, ranks, (ax1, ax2, ax3)):
            name.next_to(axes, DOWN, buff=0.25)
            rank.next_to(name, DOWN, buff=0.2)
        self.play(*[FadeIn(m) for m in names + ranks])

        # 底部总结：中文结论用 Text，绕开 LaTeX 的中文排版难题。
        summary = Text(
            "唯一解: r(A)=r(A|b)=n；无解: r(A)<r(A|b)；无穷多解: r(A)=r(A|b)<n",
            font_size=24,
            color=YELLOW,
        )
        summary.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(summary))
        self.wait(1.5)


def main() -> None:
    parser = argparse.ArgumentParser(description="线性方程组、高斯消元与解的判定")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "06",
        [EquationsAsIntersections, GaussianElimination, SolutionTypes],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
