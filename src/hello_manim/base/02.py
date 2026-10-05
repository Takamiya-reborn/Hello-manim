"""第 2 课：图形、文字与布局——搭画面的基本功。

本课要回答三个问题：
    1. 一个 Mobject 的"样式"由哪些部分组成？
    2. VGroup 是什么，为什么布局前要先把物体打包？
    3. 文字有哪些排版控制？

原理速览：
    视觉样式分两层：
      - stroke（描边）：轮廓线，控制颜色 / 线宽 / 透明度；
      - fill（填充）：内部区域，控制颜色 / 透明度。
        fill_opacity=0 就只剩线框——数学示意图的常见风格。
    VGroup 把多个 Mobject 打包成一个整体：打包后 arrange()
    能让成员等间距排列，整个组还能被当作单个物体平移、
    缩放、做动画。布局的本质是 manim 帮你算好包围盒
    （bounding box）再相对定位，人永远不写绝对坐标。
    Text（Pango）负责普通文字：字号、颜色、粗斜体、字间距；
    真正的数学公式排版（LaTeX）留到第 6 课。

最短运行：
    uv run hello-manim base 02
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class ShapeGallery(Scene):
    def construct(self) -> None:
        # 描边 vs 填充：circle 只有半透明填充；square 同时指定
        # 填充色和描边色；triangle 纯线框（fill_opacity 默认 0）。
        circle = Circle(radius=0.8, color=BLUE, fill_opacity=0.3)
        square = Square(side_length=1.5, color=GREEN, fill_color=RED, fill_opacity=0.5)
        triangle = Triangle(color=ORANGE).scale(0.8)

        # 打包成组再布局：arrange(RIGHT, buff=1) 让三个形状沿
        # 水平方向排开、间距 1 个单位，整组自动居中。
        shapes = VGroup(circle, square, triangle).arrange(RIGHT, buff=1.0)
        self.play(Create(circle), Create(square), Create(triangle))

        caption = Text("VGroup.arrange：打包 → 等间距排列", font_size=28)
        caption.next_to(shapes, DOWN, buff=0.8)
        self.play(Write(caption))

        # 整组动画：对 VGroup 做 Transform，成员的相对布局保持不变。
        self.play(shapes.animate.scale(0.6).to_edge(UP))
        self.wait(1)


class TextStyle(Scene):
    def construct(self) -> None:
        # Text 的常用控制：字号、颜色、粗体、斜体。
        # font 参数可指定系统字体名（如 "Microsoft YaHei"），
        # 不指定时 Pango 自动回退到能显示对应字符的字体。
        normal = Text("常规件", font_size=36)
        bold = Text("粗体", font_size=36, weight=BOLD, color=YELLOW)
        italic = Text("斜体 slant", font_size=36, slant=ITALIC, color=TEAL)

        lines = VGroup(normal, bold, italic).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(lines, shift=RIGHT))  # FadeIn 支持 shift：淡入时带位移
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="图形样式、VGroup 布局与文字排版")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "base",
        "02",
        [ShapeGallery, TextStyle],
        quality=args.quality,
        preview=args.preview,
    )


if __name__ == "__main__":
    main()
