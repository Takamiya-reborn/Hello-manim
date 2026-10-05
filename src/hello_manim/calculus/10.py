"""第 10 课：无穷级数——收敛判别、幂级数与泰勒展开。

本课要回答三个问题：
    1. 无穷多项相加，"和"什么时候才存在？几何级数为什么收敛，
       而通项同样趋于 0 的调和级数却发散？
    2. 面对一个具体级数，比较判别法、比值判别法、莱布尼茨判别法
       各自的适用条件是什么？p-级数为什么是最常用的"标尺"？
    3. 泰勒多项式凭什么能在 x = 0 附近"贴住" sin x？阶数升高的
       过程在图像上是什么样子？

原理速览：
    数学上，级数 Σaₙ 的"和"定义为部分和数列 Sₙ = a₁+…+aₙ 的极限：
    极限存在称收敛，否则称发散。"通项趋于 0"只是收敛的必要条件，
    不是充分条件——调和级数就是最著名的反例。
      - 几何级数 Σ rⁿ：|r|<1 时收敛于 a₁/(1-r)。单位正方形每次
        取走剩余面积的一半，1/2+1/4+1/8+… 恰好铺满整个正方形，
        这就是 Σ 1/2ⁿ = 1 的"面积证明"；
      - 调和级数 Σ 1/n：通项趋于 0 却发散——部分和增长虽慢，
        却会突破任何上界（欧拉的分组比较证明）；
      - p-级数 Σ 1/nᵖ：p>1 收敛、p≤1 发散（积分判别法的结论）；
      - 比值判别法（达朗贝尔）：ρ = lim|aₙ₊₁/aₙ|，ρ<1 收敛、
        ρ>1 发散、ρ=1 时失效——调和级数与 Σ1/n² 的 ρ 都是 1，
        命运却完全不同；
      - 莱布尼茨判别法：交错级数 Σ(-1)ⁿ⁺¹aₙ 在 |aₙ| 单调递减且
        趋于 0 时必收敛；
      - 泰勒公式：f(x) = Σ f⁽ⁿ⁾(0)/n! · xⁿ。sin x 在 0 处的偶数阶
        导数全为 0，奇数阶轮流取 ±1，故
        sin x = x − x³/3! + x⁵/5! − x⁷/7! + …，对一切实数收敛。
    manim 手段：几何级数用 Square 逐层铺色 + ValueTracker 驱动
    DecimalNumber 展示 Sₙ→1；判别法一幕以 MathTex 排版为主，
    配 SurroundingRectangle 做卡片；泰勒一幕用 Axes.plot 画各阶
    多项式曲线，Transform 让曲线逐阶"进化"，收敛过程一目了然。

最短运行：
    uv run hello-manim calculus 10

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/calculus/10.py GeometricSeries
    uv run manim -pql src/hello_manim/calculus/10.py ConvergenceTests
    uv run manim -pql src/hello_manim/calculus/10.py TaylorPolynomials
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class GeometricSeries(Scene):
    def construct(self) -> None:
        # 标题用 to_edge(UP) 贴顶——贴边布局，不写绝对坐标。
        title = Text("几何级数：把一个正方形分到无穷", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 这个边长 2.4 的正方形代表"面积为 1"的单位正方形。
        # 整体左移，把右侧留给公式面板——先分区，再填内容。
        side = 2.4
        square = Square(side_length=side, color=WHITE).shift(LEFT * 3.5 + DOWN * 0.3)
        self.play(Create(square))

        # 右上：级数的记号。MathTex 一律用 raw string，避免反斜杠转义。
        series = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{2^n}", font_size=44)
        series.next_to(title, DOWN, buff=0.5).shift(RIGHT * 3.2)
        self.play(Write(series))

        # ValueTracker 是"会变的数"；DecimalNumber 绑定 updater 后
        # 每帧读取 tracker——tracker 动，数字就跟着动（第 4 课的套路）。
        tracker = ValueTracker(0.0)
        s_label = Text("部分和 ", font_size=28)
        s_num = DecimalNumber(0.00, num_decimal_places=2, color=YELLOW)
        s_num.add_updater(lambda m: m.set_value(tracker.get_value()))
        s_group = VGroup(s_label, s_num).arrange(RIGHT, buff=0.1)
        s_group.next_to(series, DOWN, buff=0.7)
        self.play(FadeIn(s_group))

        # 逐层铺色：第 k 层是"剩余面积的一半"，即面积 1/2^k 的横条，
        # 从正方形底部向上堆叠；铺 7 层共 1 - 1/128 ≈ 0.992。
        colors = [BLUE, TEAL, GREEN, YELLOW, ORANGE, RED, PURPLE]
        filled, stacked = 0.0, 0.0
        for k in range(1, 8):
            strip = Rectangle(
                width=side,
                height=side / 2**k,
                fill_color=colors[k - 1],
                fill_opacity=0.85,
                stroke_width=0,
            )
            # next_to(..., buff=0) 让横条底边贴住正方形底边，
            # 再抬升前面所有层的高度和——依然只用相对定位。
            strip.next_to(square.get_bottom(), UP, buff=0).shift(UP * stacked)
            self.play(FadeIn(strip), run_time=0.5)
            filled += 1 / 2**k
            stacked += side / 2**k
            # 铺一块、走一步数字：面积与部分和一一对应。
            self.play(tracker.animate.set_value(filled), run_time=0.5)

        # 数学结论：剩下的空隙面积 1/128、1/256、… → 0，所以 Sₖ → 1。
        conclusion = MathTex(
            r"\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\cdots", "=", "1", font_size=40
        )
        conclusion[2].set_color(YELLOW)
        conclusion.next_to(s_group, DOWN, buff=0.7)
        self.play(FadeIn(conclusion))

        # 反例压轴：调和级数通项同样趋于 0，部分和却无上界——发散。
        # 对照用文字讲清即可，不再画图。
        note = VGroup(
            MathTex(r"1+\frac{1}{2}+\frac{1}{3}+\frac{1}{4}+\cdots", font_size=36),
            Text("调和级数：通项趋于 0，部分和却无限增长 —— 发散", font_size=24, color=RED),
        ).arrange(DOWN, buff=0.25)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(2)


class ConvergenceTests(Scene):
    def construct(self) -> None:
        title = Text("判别法速览：拿到级数，先问哪一句？", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 三张"卡片"：名称 + 判别条件 + 结论，先纵向排好再横向铺开。
        # 注意：MathTex 里只能写 LaTeX，中文结论一律用 Text 分开排版。
        compare = VGroup(
            Text("比较判别法", font_size=26, color=BLUE),
            MathTex(r"0 \le a_n \le b_n", font_size=36),
            Text("Σbₙ 收敛 ⇒ Σaₙ 收敛", font_size=22),
        ).arrange(DOWN, buff=0.25)
        ratio = VGroup(
            Text("比值判别法（达朗贝尔）", font_size=26, color=GREEN),
            MathTex(r"\rho=\lim_{n\to\infty}\left|\frac{a_{n+1}}{a_n}\right|", font_size=36),
            Text("ρ<1 收敛，ρ>1 发散", font_size=22),
            Text("ρ = 1 时失效", font_size=22, color=RED),
        ).arrange(DOWN, buff=0.25)
        leibniz = VGroup(
            Text("莱布尼茨判别法", font_size=26, color=ORANGE),
            MathTex(r"\sum_{n=1}^{\infty} (-1)^{n+1} a_n", font_size=36),
            Text("|aₙ| 单调递减趋于 0 ⇒ 收敛", font_size=22),
        ).arrange(DOWN, buff=0.25)

        cards = VGroup(compare, ratio, leibniz).arrange(RIGHT, buff=0.6)
        cards.next_to(title, DOWN, buff=0.6)
        # 卡片总宽超出画面就整体等比缩小——先排版后兜底，一行搞定。
        if cards.width > 13:
            cards.scale_to_fit_width(13)

        # 每张卡片配一个同色边框，Create 依次登场。
        for card, accent in [(compare, BLUE), (ratio, GREEN), (leibniz, ORANGE)]:
            frame = SurroundingRectangle(card, color=accent, buff=0.25)
            self.play(Create(card), FadeIn(frame))
        self.wait(1)

        # p-级数是"标尺"：它的 ρ 恒等于 1，比值判别法在这里必然失效，
        # 收敛与否要看积分判别法给出的结论。
        ruler = MathTex(r"\sum_{n=1}^{\infty} \frac{1}{n^p}", font_size=40)
        ruler.next_to(cards, DOWN, buff=0.55)
        self.play(Write(ruler))

        results = VGroup(
            Text("p=1/2：发散", font_size=26, color=RED),
            Text("p=1：发散（调和级数）", font_size=26, color=RED),
            Text("p=2：收敛", font_size=26, color=GREEN),
        ).arrange(RIGHT, buff=0.7)
        results.next_to(ruler, DOWN, buff=0.4)
        self.play(FadeIn(results))

        summary = Text("结论：p ≤ 1 发散，p > 1 收敛", font_size=28, color=YELLOW)
        summary.next_to(results, DOWN, buff=0.35)
        self.play(Write(summary))
        self.wait(2)


class TaylorPolynomials(Scene):
    def construct(self) -> None:
        # 压轴：泰勒多项式逐阶逼近 sin x。公式先挂出来，图形随后对照。
        title = Text("泰勒展开：用多项式逼近 sin x", font_size=32)
        title.to_edge(UP, buff=0.3)
        # 逐段拆分：x³/3!、x⁵/5! 等是独立子 Mobject，符号一目了然。
        formula = MathTex(
            r"\sin x", "=", "x", "-",
            r"\frac{x^3}{3!}", "+", r"\frac{x^5}{5!}", "-",
            r"\frac{x^7}{7!}", "+", r"\cdots",
            font_size=38,
        )
        formula.next_to(title, DOWN, buff=0.35)
        self.play(Write(title), Write(formula))

        # 坐标系压扁一点，给上下公式让位；y 范围 [-2,2] 装得下 7 阶的振荡。
        axes = Axes(
            x_range=[-8, 8, 2],
            y_range=[-2, 2, 1],
            x_length=12.5,
            y_length=4.6,
            tips=False,
        ).shift(DOWN * 0.7)
        # plot 只会采样连线，所以显函数 sin x 直接传 math.sin 即可。
        sin_curve = axes.plot(math.sin, x_range=[-7.5, 7.5], color=BLUE)
        sin_label = Text("y = sin x", font_size=24, color=BLUE)
        sin_label.next_to(axes.c2p(2.4, 1.4), UP, buff=0.05)
        self.play(Create(axes), Create(sin_curve), FadeIn(sin_label))

        # 泰勒系数：sin x 在 0 处偶数阶导数全为 0，奇数阶轮流取 ±1，
        # 故多项式只含奇次项：Σ (-1)^k · x^(2k+1)/(2k+1)!。
        def taylor_sin(order: int):
            k_max = (order - 1) // 2  # order 阶 → 最高奇次项的编号 k

            def f(x: float) -> float:
                return sum(
                    (-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1)
                    for k in range(k_max + 1)
                )

            return f

        # 各阶的绘图区间逐阶放宽：贴合区从 0 向两侧扩张，
        # 区间端点都控制在 |y| ≤ 2 内，避免曲线冲出坐标系。
        stages = [(1, RED, 2.0), (3, ORANGE, 3.0), (5, GREEN, 4.0), (7, PURPLE, 4.2)]

        # 1 阶多项式就是 y = x——只在 0 附近贴合。
        order, color, span = stages[0]
        poly = axes.plot(taylor_sin(order), x_range=[-span, span], color=color)
        stage = Text(f"{order} 阶", font_size=26, color=color)
        stage.next_to(formula, RIGHT, buff=0.4)
        self.play(Create(poly), FadeIn(stage))

        # Transform 到 3、5、7 阶：当前曲线逐阶"进化"为更高阶曲线，
        # 每升 2 阶，贴合 sin x 的范围就向两侧扩张——收敛的直观画面。
        for order, color, span in stages[1:]:
            target = axes.plot(taylor_sin(order), x_range=[-span, span], color=color)
            new_stage = Text(f"{order} 阶", font_size=26, color=color)
            new_stage.next_to(formula, RIGHT, buff=0.4)
            self.play(Transform(poly, target), Transform(stage, new_stage))
        self.wait(1)

        # 顺势一提：e^x 的泰勒级数没有交错、没有奇偶之分，
        # 对一切实数收敛——幂级数里最"温和"的一个。
        note = VGroup(
            MathTex(r"e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!}", font_size=34),
            Text("对所有实数 x 收敛", font_size=24, color=YELLOW),
        ).arrange(RIGHT, buff=0.4)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="无穷级数与泰勒展开")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "10",
        [GeometricSeries, ConvergenceTests, TaylorPolynomials],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
