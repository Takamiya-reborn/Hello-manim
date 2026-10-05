"""第 1 课：第一个场景——manim 的世界观。

本课要回答三个问题：
    1. Scene 和 Mobject 是什么关系？
    2. manim 的坐标系和数学课本里的有什么不同？
    3. 渲染参数 -ql / --quality low 到底设置了什么？

原理速览：
    manim 的核心是两个抽象：
      - Mobject（Mathematical OBJECT）：画面上的一切——圆、文字、
        坐标轴——都是 Mobject。它们只是"描述"（点集 + 样式），
        本身不含任何像素；
      - Scene（场景）：舞台 + 导演。construct() 是剧本，按顺序
        执行 play()/add()/wait()；render() 时 manim 把每一帧的
        Mobject 状态光栅化成图像，再编码成视频。
    坐标系：原点在画面正中心，y 向上为正，默认高 8 个单位、
    宽约 14.2 个单位（单位 = frame_height / frame_width）——
    和"原点在左下角"的屏幕像素坐标相反。
    质量参数只影响两件事：分辨率和帧率。480p15 渲染最快，
    适合学习迭代；成片再用 1080p60。

最短运行：
    uv run hello-manim base 01

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/base/01.py FirstScene
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class FirstScene(Scene):
    def construct(self) -> None:
        # 惯例：教程代码都写 from manim import *，本套课程保持一致。
        # Mobject 只是数据：此刻还没有渲染任何东西，
        # square 只是内存里"一个正方形的描述"。
        square = Square(side_length=2, color=BLUE)

        # play(Create(...)) 是"画出来"：Create 逐段显示物体轮廓，
        # 是 manim 最常用的登场动画。manim 会按 run_time（默认 1 秒）
        # 和当前质量的帧率，插值出中间每一帧。
        self.play(Create(square))

        # 所有 Mobject 都支持链式几何操作。.animate 是语法糖：
        # 把"目标状态"（右移 2、放大 1.5 倍）交给 manim，
        # 由它在 play() 期间插值出过渡帧——第 3 课详细拆解。
        self.play(square.animate.shift(RIGHT * 2).scale(1.5))

        # Text 用 Pango 排版（不需要 LaTeX）。Unicode 字符（α ∑ √）
        # 可以直接用——这是第 6 课之前写"数学符号"的权宜之计。
        title = Text("Hello, manim!", font_size=36, color=YELLOW)
        # next_to 是布局方法：把 title 放在 square 正下方 0.5 个单位处。
        # 布局一律用这类相对定位 API，不要手写绝对坐标。
        title.next_to(square, DOWN, buff=0.5)
        self.play(Write(title))
        self.wait(1)  # 停 1 秒，让观众看清最终画面


def main() -> None:
    parser = argparse.ArgumentParser(description="第一个 manim 场景")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson("base", "01", [FirstScene], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
