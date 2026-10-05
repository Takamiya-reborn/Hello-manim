"""第 4 课：ValueTracker 与 updater——参数驱动的动画。

本课要回答三个问题：
    1. play() 播完就停了，"持续运动"怎么实现？
    2. ValueTracker 在其中扮演什么角色？
    3. updater 的执行时机是什么，用完为什么要移除？

原理速览：
    play() 是一次性插值：给定起点和终点，播完即静止。
    想要"随时间持续变化"，就把变化抽象成一个数值——
    ValueTracker 是一个可以动画化的 float：
        self.play(tracker.animate.set_value(TAU))
    play 驱动的是 tracker 的值，而不是某个物体的属性。

    updater 是"每当场景要渲染一帧，先执行我"的回调：
    always_redraw(lambda: ...) 每帧用最新值重新构造物体，
    适合"形状随参数变"的场景（曲线、切线）；普通 updater
    f(mobject) 则每帧修改现有物体。本课的经典例子——单位圆
    上的动点水平展开成正弦曲线——正是"一个 tracker 驱动
    多个 always_redraw 物体"的组合。

    注意生命周期：updater 绑定在物体上，物体留在场景一天，
    回调就执行一天。不再需要的物体要 scene.remove() 或
    clear_updaters()，否则后续动画会被它每帧拖慢甚至干扰。

最短运行：
    uv run hello-manim base 04
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class UnitCircleSine(Scene):
    def construct(self) -> None:
        # t 是全场的"总开关"：动点位置、半径线、曲线都盯着它。
        t = ValueTracker(0)

        # 左侧：单位圆（圆心在 (-3.5, 0)，半径 1）。
        circle = Circle(radius=1, color=BLUE).shift(LEFT * 3.5)

        # always_redraw 每帧调用一次 lambda，用 t 的当前值
        # 重新生成 Dot——点永远钉在圆上角度 t 处。
        moving_dot = always_redraw(
            lambda: Dot(circle.point_at_angle(t.get_value()), color=YELLOW)
        )
        radius_line = always_redraw(
            lambda: Line(
                circle.get_center(),
                moving_dot.get_center(),
                color=YELLOW,
            )
        )

        # 右侧：正弦曲线的坐标系。
        axes = Axes(
            x_range=[0, TAU, PI / 2],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            y_length=3,
        ).shift(RIGHT * 2.5)

        # 曲线每帧重画：画出 [0, t] 区间的 sin——"生长"效果
        # 不是动画做出来的，而是每帧的静态重绘叠出来的。
        curve = always_redraw(
            lambda: axes.plot(
                lambda x: math.sin(x),
                x_range=[0, max(t.get_value(), 1e-3)],
                color=YELLOW,
            )
        )
        # 连接线：从圆上的动点拉到曲线上 (t, sin t) 处，展示
        # "圆的纵坐标 = 曲线的高度"这一同构关系。
        connector = always_redraw(
            lambda: DashedLine(
                moving_dot.get_center(),
                axes.c2p(t.get_value(), math.sin(t.get_value())),
                stroke_width=1,
            )
        )

        self.add(circle, axes)
        self.play(Create(moving_dot), Create(radius_line), Create(curve))
        # play 只驱动 tracker：0 → 2π，所有 updater 自动跟着动。
        self.play(t.animate.set_value(TAU), run_time=4, rate_func=linear)
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="单位圆展开成正弦曲线")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson("base", "04", [UnitCircleSine], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
