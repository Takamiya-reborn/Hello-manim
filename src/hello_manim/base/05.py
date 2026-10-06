"""第 5 课：坐标系与函数图像——manim 的数学核心。

本课要回答三个问题：
    1. 数学坐标 (π/2, 1) 怎么变成屏幕上的位置？
    2. plot() 画的是什么，能画隐函数吗？
    3. 面积、切线这类"微积分可视化"怎么搭？

原理速览：
    Axes 是"数学坐标系"与"manim 屏幕坐标系"之间的翻译官：
      - c2p(coordinate to point)：数学坐标 → 屏幕坐标。
        永远用 axes.c2p(x, y) 定位，绝不手写缩放比例——
        改坐标范围时手写的比例会全部失真，c2p 不会；
      - p2c(point to coordinate)：反方向翻译。
    plot(f) 采样若干点再用折线/样条连成 VMobject，
    所以它只能画显函数 y = f(x)；x_range 就是采样区间。
    在此之上：
      - get_area：曲线与 x 轴之间的填充区域（定积分的直观形）；
      - TangentLine + 第 4 课的 ValueTracker：让切线沿曲线滑动，
        直观展示"导数是斜率"。

最短运行：
    uv run hello-manim base 05
"""

import argparse
import math

from manim import *

from hello_manim.utils.rendering import add_render_args, render_lesson


class GraphBasics(Scene):
    def construct(self) -> None:
        # 坐标范围 [起, 止, 刻度步长]；尺寸用屏幕单位。
        # 注意：include_numbers=True 的坐标数字底层是 MathTex，
        # 会要求 LaTeX 环境——本课刻意不开启，保持免 LaTeX 可运行。
        axes = Axes(
            x_range=[-0.5, 6.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=5,
            tips=False,
        )
        sin_curve = axes.plot(lambda x: math.sin(x), color=BLUE)
        label = Text("y = sin x", font_size=30, color=BLUE)
        label.next_to(axes.c2p(2.5, -1), UP, buff=0.3)

        self.play(Create(axes), run_time=2)
        self.play(Create(sin_curve), FadeIn(label))

        # c2p：数学坐标 → 屏幕坐标。峰值点 (π/2, 1)。
        peak = Dot(axes.c2p(PI / 2, 1), color=YELLOW)
        self.play(FadeIn(peak, scale=2))

        # get_area：[0, π] 区间曲线与 x 轴之间的区域，
        # 就是 ∫₀^π sin x dx = 2 的可视化。
        area = axes.get_area(
            sin_curve, x_range=[0, PI], color=GREEN, opacity=0.4
        )
        self.play(FadeIn(area))

        # 切线沿曲线滑动：TangentLine 的 alpha 参数是
        # "沿曲线的归一化位置"（0 = 起点，1 = 终点），
        # 用 tracker 驱动它，就得到"导数扫过整条曲线"。
        t = ValueTracker(0.15)
        tangent = always_redraw(
            lambda: TangentLine(
                sin_curve, alpha=t.get_value(), length=3, color=ORANGE
            )
        )
        self.add(tangent)
        self.play(t.animate.set_value(0.85), run_time=3)
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="函数图像、积分面积与滑动切线")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson("base", "05", [GraphBasics], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
