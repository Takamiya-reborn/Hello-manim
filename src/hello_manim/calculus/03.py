"""第 3 课：导数——定义、几何意义与求导法则。

本课要回答三个问题：
    1. 导数 f'(x0) 的严格定义是什么？"差商"和它是什么关系？
    2. 为什么说"导数就是切线斜率"？导函数 f'(x) 又是什么？
    3. 四则运算法则和链式法则怎么用？链式法则"由外向内"
       到底在乘什么？

原理速览：
    数学上，导数是差商的极限：
        f'(x0) = lim_{h->0} [f(x0+h) - f(x0)] / h。
    差商是过 P(x0, f(x0)) 与 Q(x0+h, f(x0+h)) 两点的割线斜率；
    h -> 0 时 Q 沿曲线滑向 P，割线的极限位置就是切线——
    于是"极限定义"与"几何意义"在同一个动画里合一。
    若对每个 x 都求出斜率，就得到"斜率函数"即导函数：
    对 f(x)=x^2 有 f'(x)=2x。
    求导法则把"按定义取极限"变成机械操作：四则法则照抄结构；
    链式法则 [f(g(x))]' = f'(g(x))·g'(x) 是"外层导数 × 内层
    导数"，例如 (sin x^2)' = cos(x^2)·2x。
    manim 手段：ValueTracker 是一个"会广播的数字"，配合
    always_redraw 让割线/切线/读数每帧按最新值重建；
    DecimalNumber 显示实时数值；MathTex 按子串拆开后可以切片
    上色，用颜色把"外层/内层"在公式里的去向对应起来。

最短运行：
    uv run hello-manim calculus 03

也可以用 manim 原生命令行逐个渲染本课场景：
    uv run manim -pql src/hello_manim/calculus/03.py SecantToTangent
    uv run manim -pql src/hello_manim/calculus/03.py SlopeIsDerivative
    uv run manim -pql src/hello_manim/calculus/03.py DerivativeRules
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class SecantToTangent(Scene):
    def construct(self) -> None:
        # 数学设定：f(x) = x^2/2，固定点取 x0 = 1（此处 f'(1)=1，好验证）。
        X0 = 1.0
        f = lambda x: x ** 2 / 2

        # 顶部先给出导数定义——本课一切动画都是为它服务的。
        # MathTex 必须配 raw string，否则 \f 会被 Python 当成转义符。
        definition = MathTex(
            r"f'(x_0)", r"=", r"\lim_{h \to 0}", r"\frac{f(x_0+h)-f(x_0)}{h}",
        )
        definition[0].set_color(YELLOW)  # 强调"导数"本体
        definition[3].set_color(TEAL)    # 强调"差商"——它就是割线斜率
        definition.to_edge(UP, buff=0.4)
        self.play(Write(definition))

        # 坐标系与曲线。定位一律交给 to_edge / next_to，不手写绝对坐标。
        axes = Axes(
            x_range=[-0.5, 3.3, 1], y_range=[-0.5, 4.6, 1],
            x_length=6.0, y_length=4.2, tips=False,
        )
        axes.to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        curve = axes.plot(f, x_range=[-0.4, 3.1], color=BLUE)
        curve_label = MathTex(r"f(x)=\frac{x^2}{2}", color=BLUE, font_size=36)
        curve_label.next_to(axes.c2p(0.2, 3.6), RIGHT, buff=0.3)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(curve), Write(curve_label))

        # 固定点 P(x0, f(x0))——切线最终要"贴"在这里。
        p_dot = Dot(axes.c2p(X0, f(X0)), color=YELLOW)
        p_label = MathTex("P", color=YELLOW, font_size=36)
        p_label.next_to(p_dot, DL, buff=0.12)
        self.play(FadeIn(p_dot, scale=2), Write(p_label))

        # ValueTracker 就是"会广播的数字"：get_value() 永远返回最新 h。
        h = ValueTracker(2.0)

        # 动点 Q(x0+h, f(x0+h))：always_redraw 让它每帧按 h 重建，
        # 于是 play(h.animate...) 时 Q 会自己沿曲线滑向 P。
        q_group = always_redraw(
            lambda: VGroup(
                Dot(axes.c2p(X0 + h.get_value(), f(X0 + h.get_value())), color=RED),
                MathTex("Q", color=RED, font_size=36).next_to(
                    axes.c2p(X0 + h.get_value(), f(X0 + h.get_value())), UR, buff=0.1
                ),
            )
        )

        # 割线：过 P、Q 两点。scale(倍数, about_point=P) 把线段以 P 为锚
        # 拉长到 7 个单位——方向不变，只"延长"，这正是割线的画法。
        def make_secant() -> Line:
            hh = h.get_value()
            p = axes.c2p(X0, f(X0))
            q = axes.c2p(X0 + hh, f(X0 + hh))
            line = Line(p, q, color=ORANGE, stroke_width=4)
            return line.scale(7 / line.get_length(), about_point=p)

        secant = always_redraw(make_secant)

        # 差商读数：DecimalNumber 每帧重建并贴在固定标签右侧，
        # 学生能亲眼看着数值收敛到 1（= f'(1)）。
        readout_label = Text("差商 =", font_size=28)
        readout_label.next_to(axes, RIGHT, buff=0.7).shift(UP * 1.3)
        self.play(FadeIn(readout_label))
        readout = always_redraw(
            lambda: DecimalNumber(
                (f(X0 + h.get_value()) - f(X0)) / h.get_value(),
                num_decimal_places=3, color=ORANGE,
            ).next_to(readout_label, RIGHT, buff=0.15)
        )

        # h: 2 -> 0.01：Q 沿曲线滑向 P，割线绕 P 转到极限位置。
        self.add(secant, q_group, readout)
        self.play(h.animate.set_value(0.01), run_time=5)

        # 结论：用几何语言把定义再说一遍。
        conclusion = Text("h→0：割线的极限位置就是切线", font_size=26)
        conclusion.next_to(readout_label, DOWN, buff=1.0)
        conclusion.align_to(readout_label, LEFT)
        limit = MathTex(r"f'(1) = 1", color=YELLOW, font_size=40)
        limit.next_to(conclusion, DOWN, buff=0.4)
        limit.align_to(readout_label, LEFT)
        self.play(FadeIn(conclusion), Write(limit))
        self.wait(1.5)


class SlopeIsDerivative(Scene):
    def construct(self) -> None:
        # 原函数与导函数：f = x^2 在每点的斜率恰为 2x。
        f = lambda x: x ** 2
        df = lambda x: 2 * x
        XL, XR = -1.7, 1.7  # 曲线采样区间；TangentLine 的 alpha 按它归一化

        title = Text("导数的几何意义：导函数是斜率函数", font_size=30)
        title.to_edge(UP, buff=0.3)

        # 上半屏画 f、下半屏画 f'：两套 Axes 的 x 范围一致，
        # 同一个 x0 在两图里才能左右对齐（下面用虚线强调）。
        axes_f = Axes(x_range=[-1.9, 1.9, 1], y_range=[-0.4, 3.2, 1],
                      x_length=5.5, y_length=2.6, tips=False)
        axes_df = Axes(x_range=[-1.9, 1.9, 1], y_range=[-3.5, 3.5, 1],
                       x_length=5.5, y_length=2.6, tips=False)
        axes_f.next_to(title, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        axes_df.to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        curve_f = axes_f.plot(f, x_range=[XL, XR], color=BLUE)
        curve_df = axes_df.plot(df, x_range=[XL, XR], color=GREEN)
        label_f = MathTex(r"f(x)=x^2", color=BLUE, font_size=34)
        label_f.next_to(axes_f, RIGHT, buff=0.8)
        label_df = MathTex(r"f'(x)=2x", color=GREEN, font_size=34)
        label_df.next_to(axes_df, RIGHT, buff=0.8)
        self.play(FadeIn(title))
        self.play(Create(axes_f), Create(curve_f), Write(label_f))
        self.play(Create(axes_df), Create(curve_df), Write(label_df))

        # x0 用 ValueTracker 驱动：一个数字变，切线/动点/读数全跟着动。
        x0 = ValueTracker(-1.5)

        # TangentLine 的 alpha 是"沿曲线的归一化位置"（0=起点，1=终点），
        # 所以要把数学坐标 x0 换算成 (x0-XL)/(XR-XL)。
        tangent = always_redraw(
            lambda: TangentLine(
                curve_f, alpha=(x0.get_value() - XL) / (XR - XL),
                length=2.4, color=ORANGE,
            )
        )
        # 上图动点 (x0, f(x0)) 与下图动点 (x0, 2x0) 同步滑动。
        p_dot = always_redraw(
            lambda: Dot(axes_f.c2p(x0.get_value(), f(x0.get_value())), color=YELLOW)
        )
        d_dot = always_redraw(
            lambda: Dot(axes_df.c2p(x0.get_value(), df(x0.get_value())), color=YELLOW)
        )
        # 竖直虚线：强调上下两图取的是"同一个 x0"。
        vline = always_redraw(
            lambda: DashedLine(
                axes_f.c2p(x0.get_value(), f(x0.get_value())),
                axes_df.c2p(x0.get_value(), df(x0.get_value())),
                color=GREY, stroke_width=2,
            )
        )

        # 斜率读数：DecimalNumber 实时显示 2x0，观众可直接对照下图。
        slope_label = Text("切线斜率 =", font_size=26)
        slope_label.next_to(label_f, DOWN, buff=1.2)
        slope_label.align_to(label_f, LEFT)
        slope_val = always_redraw(
            lambda: DecimalNumber(
                2 * x0.get_value(), num_decimal_places=2, color=ORANGE,
            ).next_to(slope_label, RIGHT, buff=0.15)
        )

        # x0 从 -1.5 扫到 1.5：切线跟着转，下图逐点描出斜率函数。
        self.add(tangent, vline, p_dot, d_dot, slope_label, slope_val)
        self.play(x0.animate.set_value(1.5), run_time=6)

        # 结论：下图曲线每个点的高度 = 上图切线的斜率。
        conclusion = Text("下图曲线每点的高度\n= 上图切线的斜率",
                          font_size=26, line_spacing=0.6)
        conclusion.next_to(slope_label, DOWN, buff=0.8)
        conclusion.align_to(slope_label, LEFT)
        self.play(FadeIn(conclusion))
        self.wait(1.5)


class DerivativeRules(Scene):
    def construct(self) -> None:
        title = Text("求导法则速览", font_size=32)
        title.to_edge(UP, buff=0.35)

        # 四则运算法则：u = u(x)、v = v(x) 都可导，C 为常数。
        rules = VGroup(
            MathTex(r"(u \pm v)' = u' \pm v'", font_size=38),
            MathTex(r"(Cu)' = C\,u'", font_size=38),
            MathTex(r"(uv)' = u'v + uv'", font_size=38),
            MathTex(r"\left( \frac{u}{v} \right)' = \frac{u'v - uv'}{v^2}",
                    font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rules.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=2.4)

        # 每条法则配一个中文名，扫一眼就知道什么时候用哪条。
        names = VGroup(
            Text("加减法则", font_size=22),
            Text("数乘法则", font_size=22),
            Text("乘法法则", font_size=22),
            Text("除法法则", font_size=22),
        )
        for name, rule in zip(names, rules):
            name.next_to(rule, LEFT, buff=0.5)
        for name, rule in zip(names, rules):
            self.play(FadeIn(name, shift=RIGHT * 0.3), Write(rule), run_time=1.1)

        # 链式法则：复合函数 = 外层导数 × 内层导数。
        chain_form = MathTex(
            r"\big[f(g(x))\big]' = f'\big(g(x)\big) \cdot g'(x)", font_size=36,
        )
        chain_form.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.6)
        self.play(Write(chain_form))

        # 例题 y = sin(x^2)：MathTex 按子串拆开后切片上色——
        # 外层 sin（连同括号）涂蓝，内层 x^2 涂黄。
        expr = MathTex("y", "=", r"\sin(", r"x^2", r")", font_size=48)
        expr[2].set_color(BLUE)    # 外层函数 sin
        expr[3].set_color(YELLOW)  # 内层函数 x^2
        expr[4].set_color(BLUE)
        expr.next_to(chain_form, DOWN, buff=0.8)
        self.play(Write(expr))

        # 结果：cos(x^2) 是外层导数（蓝），2x 是内层导数（黄）。
        # 同色 = 公式里同一块在求导前后的去向，一眼看清 dy/dx 的来源。
        result = MathTex(
            r"\frac{dy}{dx}", r"=", r"\cos(", r"x^2", r")", r"\cdot", r"2x",
            font_size=44,
        )
        result[2].set_color(BLUE)   # 外层的导数 cos(x^2)
        result[4].set_color(BLUE)
        result[3].set_color(YELLOW)  # 内层 x^2 原样抄进 cos 里
        result[6].set_color(YELLOW)  # 内层的导数 2x
        result.next_to(expr, DOWN, buff=0.8)
        self.play(Write(result))

        # 圈出两处黄色：先"抄内层"，再"乘内层的导数"。
        self.play(
            Circumscribe(result[3], color=YELLOW),
            Circumscribe(result[6], color=YELLOW),
        )
        note = Text("由外向内：外层导数（蓝）\n乘以内层导数（黄）",
                    font_size=24, line_spacing=0.6)
        note.next_to(result, DOWN, buff=0.6)
        self.play(FadeIn(note))
        self.wait(1.5)


def main() -> None:
    parser = argparse.ArgumentParser(description="导数的定义、几何意义与求导法则")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus", "03",
        [SecantToTangent, SlopeIsDerivative, DerivativeRules],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
