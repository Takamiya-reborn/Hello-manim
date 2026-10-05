"""第 3 课：动画的本质——play() 的每一帧发生了什么。

本课要回答三个问题：
    1. scene.play() 到底做了什么？
    2. 为什么 Transform 是"形变"而不是"沿轨迹移动"？
    3. rate_func 如何控制节奏？

原理速览：
    manim 的动画就是"逐帧插值"：play() 按当前帧率渲染若干帧，
    每一帧把动画进度 α ∈ [0,1] 先经 rate_func 映射（默认 smooth，
    即慢-快-慢的缓动），再交给 Animation.interpolate_mobject
    计算 Mobject 在该时刻的状态。改 rate_func 就是在改时间轴的
    "形状"——同样的位移，linear 是匀速，rush_into 是越走越快。
    .animate 语法糖只是"目标状态"写法：manim 对比前后状态后
    自动生成插值。而 Transform 插值的是轮廓点集：起点和终点
    物体的点按参数化路径一一配对后线性过渡，所以圆变方块是
    "形变"；想要沿轨迹移动要用 MoveAlongPath。

最短运行：
    uv run hello-manim base 03
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class RateFuncRace(Scene):
    def construct(self) -> None:
        title = Text("rate_func：同样的时长，不同的节奏", font_size=30).to_edge(UP)
        self.add(title)

        # 三条赛道、同一个终点、同样的 run_time，只换 rate_func。
        races = [
            ("linear 匀速", linear),
            ("smooth 缓入缓出（默认）", smooth),
            ("rush_into 越走越快", rush_into),
        ]
        for row, (name, func) in enumerate(races):
            y = 1.2 - row * 1.6
            self.add(Text(name, font_size=24).next_to(ORIGIN, UP).shift(UP * y + LEFT * 2.5))
            track = Line(LEFT * 5, RIGHT * 5).shift(UP * y)
            dot = Dot(LEFT * 5 + UP * y, color=YELLOW)
            self.add(track, dot)
            # .animate(rate_func=..., run_time=...) 可以就地覆盖节奏和时长。
            self.play(dot.animate(rate_func=func, run_time=2).shift(RIGHT * 10))
        self.wait(1)


class AnimateVsTransform(Scene):
    def construct(self) -> None:
        # .animate：目标状态写法，等价于 ApplyMethod(square.shift, RIGHT)。
        square = Square(color=BLUE).shift(LEFT * 3)
        self.add(square)
        self.play(square.animate.shift(RIGHT * 1.5).rotate(PI / 4).scale(1.5))

        # Transform：插值的是轮廓点集。square 的点被逐帧"变"成
        # circle 的点，所以中间帧既不是方也不是圆——这是形变。
        circle = Circle(radius=1.2, color=RED).shift(RIGHT * 3)
        self.play(Transform(square, circle))
        # 经典陷阱：Transform 之后场景里仍然只有 square 这一个对象，
        # 只是它的点集变成了圆的形状。想继续操作"那个圆"，
        # 必须继续用 square 变量；circle 从头到尾没被 add 进场景。
        self.play(square.animate.set_opacity(0.4))
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="rate_func 节奏与两种变换写法")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "base",
        "03",
        [RateFuncRace, AnimateVsTransform],
        quality=args.quality,
        preview=args.preview,
    )


if __name__ == "__main__":
    main()
