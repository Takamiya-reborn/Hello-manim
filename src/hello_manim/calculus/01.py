"""第 1 课：函数与极限——数列极限、ε-N / ε-δ 语言与无穷小。

本课要回答三个问题：
    1. "1/n 越来越接近 0"这句话，怎样说才无懈可击？
    2. ε-δ 定义里，δ 凭什么"对每个 ε 都找得到"？
    3. 无穷小是一个"很小很小的数"吗？

原理速览：
    数学原理：
      - 数列极限（ε-N 语言）：lim_{n→∞} a_n = A，当且仅当任给
        ε>0，存在正整数 N，当 n>N 时恒有 |a_n−A|<ε。ε 刻画
        "要多近有多近"（任意性），N 只需存在、不必唯一（存在性）。
      - 函数极限（ε-δ 语言）：lim_{x→a} f(x) = A，当且仅当任给
        ε>0，存在 δ>0，当 0<|x−a|<δ 时恒有 |f(x)−A|<ε；其中
        δ>0，且 0<|x−a| 表明 x=a 这一点本身的取值不影响极限。
        以 f(x)=x²、a=1 为例：|x²−1| = |x−1|·|x+1|，先限制
        |x−1|<1 才有 |x+1|<3，故取 δ = min(ε/3, 1) 即可。
      - 无穷小：以 0 为极限的变量；用"阶"比较趋零快慢
        （1/n² = o(1/n)）；无穷大与（非零）无穷小互为倒数。
        关键澄清：无穷小是趋势，不是任何一个固定的很小的数。
    manim 手段：
      - NumberLine 直接在数轴上摆点，n2p() 把数值翻成屏幕坐标；
      - ε 邻域带 / ε 水平带 / δ 竖直带都是"宽窄随参数变的矩形"，
        交给 ValueTracker + always_redraw：tracker 只存数值，
        矩形每帧按最新值重画（base 04 课"参数驱动"的组合应用）；
      - 公式一律 MathTex（raw string），中文说明用 Text，两者用
        next_to / to_edge 摆放，互不重叠。

最短运行：
    uv run hello-manim calculus 01

也可以用 manim 原生命令行渲染同一课的各个场景：
    uv run manim -pql src/hello_manim/calculus/01.py SequenceLimit
    uv run manim -pql src/hello_manim/calculus/01.py EpsilonDelta
    uv run manim -pql src/hello_manim/calculus/01.py Infinitesimals
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class SequenceLimit(Scene):
    def construct(self) -> None:
        # 标题用 Text 排中文，to_edge(UP) 顶到画面上缘，独占一行。
        title = Text("数列极限：观察 a_n = 1/n 的落点", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 数轴：a_n 的项都落在 (0, 1]，右端取 1.1；左端越过 0 到
        # -0.3，给"关于 0 对称的 ε-邻域"留出负半轴的位置。
        number_line = NumberLine(
            x_range=[-0.3, 1.1, 0.1],
            length=11,
            include_numbers=True,
            font_size=22,
        ).shift(UP * 1.3)
        self.play(Create(number_line), run_time=2)

        # 前 12 项逐个落位数轴：n2p(number to point) 是 NumberLine
        # 的"数值 → 屏幕坐标"翻译（等价于坐标轴的 c2p）。标签只标
        # 几项，12 项全标会互相遮挡。
        terms = VGroup()
        for n in range(1, 13):
            dot = Dot(number_line.n2p(1 / n), radius=0.07, color=BLUE)
            group = VGroup(dot)
            if n in (1, 2, 3, 12):
                label = MathTex(rf"\frac{{1}}{{{n}}}", font_size=24)
                label.next_to(dot, DOWN, buff=0.15)
                group.add(label)
            terms.add(group)
        # LaggedStart 让 12 个点依次登场，"越来越贴近 0"一眼可见。
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in terms], lag_ratio=0.12))
        self.wait(0.5)

        # ε-邻域带：盖住 0 ± ε 的半透明矩形。宽度随 ε 变，所以把
        # ε 交给 ValueTracker，always_redraw 每帧按最新值重画矩形。
        eps = ValueTracker(0.3)
        band = always_redraw(
            lambda: Rectangle(
                width=number_line.n2p(eps.get_value())[0]
                - number_line.n2p(-eps.get_value())[0],
                height=1.5,
                stroke_width=0,
                fill_color=GREEN,
                fill_opacity=0.25,
            ).move_to(number_line.n2p(0))
        )
        # always_redraw 的物体不参与"入场动画"（每帧都会被重置成
        # 完整形态），直接 add 上场，之后靠驱动 ε 来让它动起来。
        self.add(band)

        # 极限等式沉底（to_edge(DOWN)），与数轴区域上下分离。
        limit_eq = MathTex(r"\lim_{n \to \infty} \frac{1}{n} = 0", font_size=40)
        limit_eq.to_edge(DOWN, buff=1.2)
        self.play(Write(limit_eq))

        # 演示 ε-N 两步曲——先"任给"：把 ε 缩到 0.12，邻域带收窄；
        # 再"存在"：1/n < 0.12 ⟺ n > 8.33，故取 N = 8 即可。
        step1 = Text("任给 ε = 0.12：邻域带随之收窄", font_size=26, color=GREEN)
        step1.next_to(limit_eq, UP, buff=0.25)
        self.play(FadeIn(step1))
        self.play(eps.animate.set_value(0.12), run_time=2)

        step2 = Text("存在 N = 8：n > 8 的所有项都落在带内", font_size=26, color=YELLOW)
        step2.next_to(step1, UP, buff=0.2)
        self.play(FadeIn(step2))
        # 把已入带的项逐个强调一下：验证"n>N 时 |a_n − 0| < ε"。
        self.play(*[Indicate(terms[n - 1][0], color=YELLOW) for n in (9, 10, 11, 12)])
        self.wait(2)


class EpsilonDelta(Scene):
    def construct(self) -> None:
        title = Text("函数极限的 ε-δ 定义：以 x² 在 x=1 处为例", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 坐标系放画面左侧；曲线只在纵轴范围内采样（1.84² ≈ 3.4），
        # 避免图像冲出坐标框。
        axes = Axes(
            x_range=[-0.5, 2.2, 0.5],
            y_range=[-0.5, 3.5, 0.5],
            x_length=6.2,
            y_length=4.6,
            tips=True,
        ).shift(DOWN * 0.4 + LEFT * 2.4)
        curve = axes.plot(lambda x: x**2, x_range=[-0.45, 1.84], color=BLUE)
        point = Dot(axes.c2p(1, 1), color=YELLOW, radius=0.07)
        # 从极限点向两轴引虚线，标出 a=1 与 f(a)=1 的位置。
        dash_x = DashedLine(axes.c2p(1, 0), axes.c2p(1, 1), stroke_width=2)
        dash_y = DashedLine(axes.c2p(0, 1), axes.c2p(1, 1), stroke_width=2)
        a_tex = MathTex("a=1", font_size=28).next_to(axes.c2p(1, 0), DOWN, buff=0.15)
        self.play(Create(axes), Create(curve), run_time=2)
        self.play(Create(dash_x), Create(dash_y), FadeIn(point), FadeIn(a_tex))

        # 矩形带的通用画法：给数学坐标下的左下角/右上角，用 c2p
        # 翻成屏幕坐标再取宽高——将来改坐标范围，代码不必跟着改。
        def band(x1: float, y1: float, x2: float, y2: float, color: str) -> Rectangle:
            p1, p2 = axes.c2p(x1, y1), axes.c2p(x2, y2)
            return Rectangle(
                width=p2[0] - p1[0],
                height=p2[1] - p1[1],
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.22,
            ).move_to((p1 + p2) / 2)

        # ε 是全场的"总开关"；δ = min(ε/3, 1) 由推导确定：
        # |x²−1| = |x−1|·|x+1|，限制 |x−1|<1 才有 |x+1|<3。
        # 两个带都盯住 ε 每帧重画，δ 带随之自动收缩（联动动画）。
        eps = ValueTracker(1.0)
        eps_band = always_redraw(
            lambda: band(-0.5, 1 - eps.get_value(), 2.2, 1 + eps.get_value(), GREEN)
        )
        delta_band = always_redraw(
            lambda: band(
                1 - min(eps.get_value() / 3, 1),
                -0.5,
                1 + min(eps.get_value() / 3, 1),
                3.5,
                YELLOW,
            )
        )
        eps_tex = always_redraw(
            lambda: MathTex(r"\varepsilon", font_size=30, color=GREEN).move_to(
                axes.c2p(-0.35, 1 + eps.get_value())
            )
        )
        delta_tex = always_redraw(
            lambda: MathTex(r"\delta", font_size=30, color=YELLOW).next_to(
                delta_band, DOWN, buff=0.15
            )
        )
        self.add(eps_band, delta_band, eps_tex, delta_tex)

        # 右侧文字栏：结论公式 → 定义的中文陈述 → δ 的来历。
        lim_eq = MathTex(r"\lim_{x \to 1} x^{2} = 1", font_size=40)
        lim_eq.to_edge(RIGHT, buff=0.6).next_to(title, DOWN, buff=0.5)
        def_tex = Text(
            "任给 ε>0，存在 δ>0，\n当 0<|x−1|<δ 时，恒有 |x²−1|<ε",
            font_size=26,
            line_spacing=0.8,
        )
        def_tex.next_to(lim_eq, DOWN, buff=0.4).to_edge(RIGHT, buff=0.6)
        why_tex = MathTex(
            r"|x^{2}-1| = |x-1| \cdot |x+1| < 3\delta \leq \varepsilon",
            font_size=32,
        )
        why_tex.next_to(def_tex, DOWN, buff=0.4).to_edge(RIGHT, buff=0.6)
        why_note = Text(
            "先限制 δ≤1 才有 |x+1|<3，\n故取 δ = min(ε/3, 1)",
            font_size=24,
            line_spacing=0.8,
        )
        why_note.next_to(why_tex, DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        self.play(Write(lim_eq))
        self.play(FadeIn(def_tex))
        self.play(Write(why_tex), FadeIn(why_note))

        # 联动演示：ε 任意缩小，δ = ε/3 自动跟着收缩——"对每个 ε
        # 都找得到 δ"，这正是极限定义的灵魂。
        moral = Text("ε 再小，也总找得到 δ", font_size=26, color=ORANGE)
        moral.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(moral))
        self.play(eps.animate.set_value(0.6), run_time=2)
        self.play(eps.animate.set_value(0.24), run_time=2)
        self.wait(2)


class Infinitesimals(Scene):
    def construct(self) -> None:
        title = Text("无穷小：比一比趋零的快慢", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 两个无穷小同台：横轴代表离散的 n（1, 2, 3, ...），
        # 用连续曲线近似展示趋势，这在教学中是标准做法。
        axes = Axes(
            x_range=[0, 4.2, 1],
            y_range=[0, 1.1, 0.5],
            x_length=6.0,
            y_length=3.4,
            tips=False,
        ).shift(DOWN * 0.5 + LEFT * 2.6)
        c1 = axes.plot(lambda x: 1 / x, x_range=[1, 4], color=BLUE)
        c2 = axes.plot(lambda x: 1 / x**2, x_range=[1, 4], color=RED)
        # 标签锚在同一条竖线 x=2.6 的两个函数值旁，上下错开。
        lab1 = MathTex(r"\frac{1}{n}", font_size=34, color=BLUE)
        lab1.next_to(axes.c2p(2.6, 1 / 2.6), UP, buff=0.2)
        lab2 = MathTex(r"\frac{1}{n^{2}}", font_size=34, color=RED)
        lab2.next_to(axes.c2p(2.6, 1 / 2.6**2), DOWN, buff=0.25)
        x_lab = MathTex("n", font_size=30).next_to(axes.x_axis, RIGHT, buff=0.15)
        y_lab = MathTex("a_n", font_size=30).next_to(axes.y_axis, UP, buff=0.1)
        self.play(Create(axes), run_time=2)
        self.play(Create(c1), FadeIn(lab1, x_lab, y_lab))
        self.play(Create(c2), FadeIn(lab2))

        # 阶的比较：两者之比 1/n → 0，说明 1/n² 趋零"更快"，
        # 记作 1/n² = o(1/n)，称 1/n² 是 1/n 的高阶无穷小。
        ratio = MathTex(
            r"\lim_{n \to \infty} \frac{1/n^{2}}{1/n}"
            r" = \lim_{n \to \infty} \frac{1}{n} = 0",
            font_size=34,
        )
        ratio.next_to(title, DOWN, buff=0.6).to_edge(RIGHT, buff=0.6)
        order_tex = MathTex(
            r"\frac{1}{n^{2}} = o\left(\frac{1}{n}\right)", font_size=36
        )
        order_tex.next_to(ratio, DOWN, buff=0.35).to_edge(RIGHT, buff=0.6)
        order_note = Text("1/n² 是 1/n 的高阶无穷小", font_size=24)
        order_note.next_to(order_tex, DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        self.play(Write(ratio))
        self.play(Write(order_tex), FadeIn(order_note))

        # 倒数关系：无穷小（非零）的倒数是无穷大，反之亦然。
        inv = MathTex(
            r"\lim_{n \to \infty} \frac{1}{1/n} = \lim_{n \to \infty} n = \infty",
            font_size=34,
        )
        inv.next_to(axes, DOWN, buff=0.4)
        inv_note = Text("无穷小（非零）的倒数是无穷大", font_size=24)
        inv_note.next_to(inv, DOWN, buff=0.25)
        self.play(Write(inv), FadeIn(inv_note))

        # 本课最易踩的概念坑：无穷小是"以 0 为极限的变量"，
        # 不是一个固定的很小的数——10^-100 是常数，它不变化，
        # 极限不是 0，所以不是无穷小。
        essence = Text(
            "无穷小是以 0 为极限的变量，\n不是一个很小的固定数",
            font_size=26,
            color=ORANGE,
            line_spacing=0.9,
        )
        essence.next_to(order_note, DOWN, buff=0.6).to_edge(RIGHT, buff=0.6)
        const_tex = MathTex(r"10^{-100}", font_size=34)
        const_tex.next_to(essence, DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        const_note = Text("是常数，不趋零，不是无穷小", font_size=24)
        const_note.next_to(const_tex, DOWN, buff=0.2).to_edge(RIGHT, buff=0.6)
        self.play(FadeIn(essence))
        self.play(Write(const_tex), FadeIn(const_note))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="数列极限、ε-δ 定义与无穷小")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "01",
        [SequenceLimit, EpsilonDelta, Infinitesimals],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
