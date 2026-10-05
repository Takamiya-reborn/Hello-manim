"""第 6 课：定积分——黎曼和、牛顿-莱布尼茨公式与旋转体体积。

本课要回答三个问题：
    1. "曲线下面积"这句模糊的话，怎样用矩形和的极限变成严格定义？
    2. 积分上限 x 滑动时，"扫过的面积"为什么恰好长出原函数 F(x)？
    3. 曲线绕 x 轴转一圈扫出的立体，体积为什么是 π∫f²(x)dx？

原理速览：
    定积分的定义走"分割、求和、取极限"三步：
      - 分割：把 [a,b] 切成 n 份，每份宽 Δx = (b-a)/n；
      - 求和：任取样本点 ξᵢ，黎曼和 Σf(ξᵢ)Δx 是面积的近似值；
      - 取极限：f 连续时 n→∞ 的极限存在，记作 ∫ₐᵇ f(x)dx。
    牛顿-莱布尼茨公式把"无限求和"变成"找原函数"：固定下限、
    让上限滑动，A(x) = ∫₀ˣ f(t)dt 是"面积的累加器"，x 处的
    增长速度恰为被积函数值 f(x)，即 A'(x) = f(x)，于是
    ∫ₐᵇ f(x)dx = F(b) - F(a)。
    旋转体用圆盘法切片：x 处垂直于轴的截面是半径 f(x) 的圆盘，
    薄片体积 πf²(x)Δx，求和取极限得 V = π∫ₐᵇ f²(x)dx。
    manim 手段：
      - get_riemann_rectangles 直接生成黎曼矩形，改小 dx 后
        Transform 一次，就是"分割无限加细"的动画；
      - ValueTracker 充当积分上限，always_redraw 让阴影面积、
        F 曲线与动点三者同步生长（第 4 课的参数驱动思想）；
      - 2D 里没有真旋转：把 Ellipse 压扁后沿轴堆叠，"挤"出
        圆盘的立体感——这是平面动画表现旋转体的常用替身。

最短运行：
    uv run hello-manim calculus 06

也可以用 manim 原生命令行渲染同一个场景（本课公式需要 LaTeX 环境）：
    uv run manim -pql src/hello_manim/calculus/06.py RiemannSum
    uv run manim -pql src/hello_manim/calculus/06.py VolumeOfRevolution
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class RiemannSum(Scene):
    def construct(self) -> None:
        # 标题用 Text（中文走 Pango，不需要 LaTeX）；定义式用
        # MathTex（走 latex→dvisvgm 管线，得到可上色的矢量公式）。
        # 原始字符串 r"..." 避免 \n \t 之类被 Python 先吃掉。
        title = Text("黎曼和：用矩形逼近曲边梯形", font_size=32)
        title.to_edge(UP, buff=0.25)
        defn = MathTex(
            r"\int_a^b f(x)\,\mathrm{d}x = \lim_{n \to \infty} \sum_{i=1}^{n} f(\xi_i)\,\Delta x_i",
            font_size=36,
        )
        defn.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(defn, shift=DOWN * 0.3))

        # f(x)=x²/2 在 [0,4]：x=4 时 y=8，所以 y 轴顶到 8.5。
        # x_range/y_range 的第三项是刻度步长，尺寸用屏幕单位。
        axes = Axes(
            x_range=[0, 4.5, 1],
            y_range=[0, 8.5, 1],
            x_length=8,
            y_length=3.8,
            tips=True,
        )
        axes.next_to(defn, DOWN, buff=0.35)
        curve = axes.plot(lambda x: x**2 / 2, x_range=[0, 4], color=BLUE)
        func = MathTex(r"f(x) = \frac{x^2}{2}", color=BLUE, font_size=36)
        func.next_to(axes.c2p(4, 8), UR, buff=0.15)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(curve), FadeIn(func))

        # get_riemann_rectangles 是 manim 自带的黎曼矩形生成器：
        # dx = (b-a)/n，n=4 即 dx=1；input_sample_type="center" 表示
        # 每个矩形取子区间中点的高——对应定义里的样本点 ξᵢ。
        rects = axes.get_riemann_rectangles(
            curve, x_range=[0, 4], dx=1, input_sample_type="center",
            stroke_width=1, stroke_color=WHITE, fill_opacity=0.6,
        )
        n_label = MathTex("n = 4", font_size=36)
        n_label.next_to(axes, RIGHT, buff=0.5)
        self.play(Create(rects), FadeIn(n_label))
        self.wait(1)

        # 分割加细：n=4 → 16 → 32。每次生成一套更窄的矩形再
        # Transform 过去——manim 对矩形逐个插值，视觉上就是
        # 矩形变多变密、阶梯一步步贴合曲线。
        for dx, n in ((0.25, 16), (0.125, 32)):
            finer = axes.get_riemann_rectangles(
                curve, x_range=[0, 4], dx=dx, input_sample_type="center",
                stroke_width=1, stroke_color=WHITE, fill_opacity=0.6,
            )
            new_label = MathTex(f"n = {n}", font_size=36).move_to(n_label)
            self.play(Transform(rects, finer), Transform(n_label, new_label))
            self.wait(1)

        # 极限的归宿：∫₀⁴ x²/2 dx = x³/6 |₀⁴ = 32/3 ≈ 10.67，
        # 而矩形和 S₄=5.5、S₃₂≈10.35，确实在向 32/3 收敛。
        value = MathTex(
            r"\int_0^4 \frac{x^2}{2}\,\mathrm{d}x = \frac{32}{3} \approx 10.67",
            font_size=36, color=YELLOW,
        )
        value.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(value, shift=UP * 0.2))
        self.wait(2)


class AccumulationFunction(Scene):
    def construct(self) -> None:
        title = Text("变上限积分：面积累加出原函数", font_size=32)
        title.to_edge(UP, buff=0.25)
        self.add(title)

        # 左图放被积函数 f(x)=x²，右图放"面积函数" F(x)=∫₀ˣt²dt。
        # 两幅图独立取 y 范围（17 与 22），因为坐标架只负责翻译，
        # 各画各的刻度并不影响数学关系。
        f_axes = Axes(x_range=[0, 4.5, 1], y_range=[0, 17, 4], x_length=5, y_length=3.6)
        F_axes = Axes(x_range=[0, 4.5, 1], y_range=[0, 22, 5], x_length=5, y_length=3.6)
        f_axes.next_to(title, DOWN, buff=0.9).shift(LEFT * 3.3)
        F_axes.next_to(f_axes, RIGHT, buff=1.6)
        f_curve = f_axes.plot(lambda x: x**2, x_range=[0, 4], color=BLUE)
        # 右图先画一条淡淡的"影子"作为参考，生长的部分盖在上面。
        F_curve = F_axes.plot(
            lambda x: x**3 / 3, x_range=[0, 4], color=ORANGE
        ).set_stroke(opacity=0.3)
        f_label = MathTex(r"f(x)=x^2", color=BLUE, font_size=36)
        f_label.next_to(f_axes, UP, buff=0.15)
        F_label = MathTex(
            r"F(x)=\int_0^x t^2\,\mathrm{d}t = \frac{x^3}{3}", color=ORANGE, font_size=36
        )
        F_label.next_to(F_axes, UP, buff=0.15)
        self.play(Create(f_axes), Create(F_axes), run_time=1.5)
        self.play(Create(f_curve), Create(F_curve), FadeIn(f_label), FadeIn(F_label))

        # ValueTracker 充当积分上限 x，从 0 扫到 4（第 4 课手法）。
        x = ValueTracker(0.0)
        # always_redraw 每帧重建阴影面积：get_area 的 x_range 右端
        # 绑定 tracker，面积随 x 同步生长；max(…, 0.01) 防止 x=0
        # 时退化成空多边形。
        area = always_redraw(
            lambda: f_axes.get_area(
                f_curve, x_range=[0, max(x.get_value(), 0.01)],
                color=GREEN, opacity=0.5,
            )
        )
        # 右图同步：F 曲线只画到当前 x，动点钉在曲线端头——
        # "左图面积长一格，右图曲线走一格"就是累加器的本质。
        F_grow = always_redraw(
            lambda: F_axes.plot(
                lambda t: t**3 / 3, x_range=[0, max(x.get_value(), 0.01)], color=ORANGE
            )
        )
        dot = always_redraw(
            lambda: Dot(F_axes.c2p(x.get_value(), x.get_value() ** 3 / 3), color=YELLOW)
        )
        insight = Text("面积的生长速度 = f(x)，即 F'(x) = f(x)", font_size=26, color=GREEN)
        insight.next_to(VGroup(f_axes, F_axes), DOWN, buff=0.25)
        self.add(area, F_grow, dot)
        self.play(FadeIn(insight))
        self.play(x.animate.set_value(4), run_time=4)
        self.wait(1)

        # 收尾：牛顿-莱布尼茨公式 + 算例验算。
        # ∫₀⁴ x²dx = F(4) - F(0) = 4³/3 - 0 = 64/3。
        nl = MathTex(
            r"\int_a^b f(x)\,\mathrm{d}x = F(b) - F(a)", r"\qquad \int_0^4 x^2\,\mathrm{d}x = \frac{4^3}{3} = \frac{64}{3}",
            font_size=36, color=YELLOW,
        )
        nl.next_to(insight, DOWN, buff=0.25)
        self.play(FadeIn(nl, shift=UP * 0.2))
        self.wait(2)


class VolumeOfRevolution(Scene):
    def construct(self) -> None:
        title = Text("旋转体体积：圆盘法", font_size=32)
        title.to_edge(UP, buff=0.25)
        self.add(title)

        # y = √x 在 [0,4] 绕 x 轴旋转：x 处的截面是半径 √x 的圆盘。
        # 曲线平缓（最高 2），y 轴给到 2.5 就够了。
        axes = Axes(x_range=[0, 4.5, 1], y_range=[0, 2.5, 1], x_length=7, y_length=2.8)
        axes.next_to(title, DOWN, buff=0.7).shift(LEFT * 1.8 + DOWN * 0.6)
        curve = axes.plot(lambda t: t**0.5, x_range=[0, 4], color=BLUE)
        curve_label = MathTex(r"y = \sqrt{x}", color=BLUE, font_size=36)
        curve_label.next_to(axes.c2p(4, 2), UR, buff=0.1)
        self.play(Create(axes), Create(curve), FadeIn(curve_label), run_time=1.5)

        # 先画几条竖直线段：每条长 2f(x)，在轴两侧对称——圆盘
        # 绕 x 轴转出来，轴上下各占一半半径。
        xs = [0.4, 1.2, 2.0, 2.8, 3.6]
        radii = VGroup(
            *[Line(axes.c2p(s, -s**0.5), axes.c2p(s, s**0.5), color=YELLOW) for s in xs]
        )
        self.play(LaggedStart(*[Create(r) for r in radii], lag_ratio=0.2))
        self.wait(0.5)

        # "旋转"在 2D 里的替身：每条线段变成压扁的椭圆。
        # Ellipse(width=…, height=…) 中 height 是竖直总高，给足
        # 直径 2f(x)；width 压到 0.45 倍制造透视感，圆心贴在轴上。
        disks = VGroup(
            *[
                Ellipse(width=0.9 * s**0.5, height=2 * s**0.5, color=YELLOW)
                .move_to(axes.c2p(s, 0))
                .set_fill(YELLOW, opacity=0.35)
                for s in xs
            ]
        )
        self.play(Transform(radii, disks))

        # 再沿区间密密堆一排圆盘：取每片中心点做样本，n=30 片
        # 薄片拼成整个立体——这就是"切片求和"的视觉版本。
        n = 30
        solid = VGroup(
            *[
                Ellipse(width=0.9 * s**0.5, height=2 * s**0.5)
                .move_to(axes.c2p(s, 0))
                .set_stroke(WHITE, width=0.5)
                .set_fill(BLUE, opacity=0.4)
                for s in [(i + 0.5) * 4 / n for i in range(n)]
            ]
        )
        self.play(FadeIn(solid, lag_ratio=0.05))
        self.wait(1)

        # 圆盘法：薄片体积 = 底面积 × 厚度 = πf²(x)Δx，无限求和
        # 即 V = π∫f²(x)dx。本例 (√x)² = x，∫₀⁴x dx = 8，得 8π。
        formula = VGroup(
            MathTex(r"V = \pi \int_a^b f^2(x)\,\mathrm{d}x", font_size=36),
            MathTex(r"V = \pi \int_0^4 \left(\sqrt{x}\right)^2 \mathrm{d}x", font_size=36),
            MathTex(
                r"= \pi \int_0^4 x\,\mathrm{d}x = \pi \cdot 8 = 8\pi",
                font_size=36, color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        formula.next_to(axes, RIGHT, buff=0.6)
        self.play(Write(formula))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="定积分：黎曼和、牛顿-莱布尼茨公式与旋转体体积")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "06",
        [RiemannSum, AccumulationFunction, VolumeOfRevolution],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
