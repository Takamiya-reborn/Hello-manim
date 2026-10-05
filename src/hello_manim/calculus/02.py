"""第 2 课：两个重要极限与函数的连续性。

本课要回答三个问题：
    1. (1+1/n)^n 在 n 增大时为什么会"卡"在 2.71828 附近？
    2. lim_{x→0} sin x / x = 1 怎么用一张单位圆图严格证出来？
    3. "不连续"有哪几种典型形态？连续性的精确定义是什么？

原理速览：
    数学侧：
      - 第一重要极限 lim_{n→∞}(1+1/n)^n = e：数列单调递增且有
        上界（< 3），由单调有界原理收敛；数值上 n=10000 时
        已经稳定在 2.71828。
      - 第二重要极限 lim_{x→0} sin x / x = 1：单位圆夹逼证明。
        x 取弧度制（弧长 = 半径 × 圆心角），在单位圆里比较
        三块面积（从小到大）：小三角形 (1/2)sin x·cos x <
        扇形 x/2 < 大三角形 (1/2)tan x。同除以正数 (1/2)sin x
        得 cos x < x/sin x < 1/cos x，再取倒数（各项为正，
        不等号反向）得 cos x < sin x/x < 1/cos x。x→0 时两端
        都趋于 1，夹逼定理逼出中间的极限也是 1。
      - 连续的定义：lim_{x→x₀} f(x) = f(x₀)，即"极限值等于
        函数值"。破坏它的方式对应三类间断点：可去（极限存在
        但函数值缺失或不等，补上/改定义即可修复）、跳跃（左
        右极限都存在但不相等，跳过去）、无穷（极限为 ∞，出现
        垂直渐近线）。
    manim 侧：
      - DecimalNumber + ValueTracker：让"数字本身"成为动画，
        配合 add_updater 每帧重算 (1+1/n)^n；
      - Axes.plot / c2p：函数图像与几何点共用同一套坐标翻译；
      - Sector / Polygon / Angle：把"面积"画成可高亮、可标注
        的实体，这是几何证明可视化的关键；
      - TransformMatchingTex：不等式链逐步变形的招牌手法。

最短运行：
    uv run hello-manim calculus 02

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/calculus/02.py LimitOfE
    uv run manim -pql src/hello_manim/calculus/02.py SqueezeProof
    uv run manim -pql src/hello_manim/calculus/02.py DiscontinuityTypes
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class LimitOfE(Scene):
    def construct(self) -> None:
        title = Text("第一重要极限：e 的诞生", font_size=32)
        title.to_edge(UP, buff=0.4)
        self.add(title)

        # e 不是随便规定的数，而是这个数列的极限。公式整体用
        # MathTex（原始字符串避免反斜杠转义），Write 逐笔画出。
        eq = MathTex(r"\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^{n} = e", font_size=44)
        eq.next_to(title, DOWN, buff=0.6)
        self.play(Write(eq))

        # 数值实验：n 用 ValueTracker 驱动，(1+1/n)^n 每帧重算。
        # add_updater 挂在 DecimalNumber 上：tracker 一动，数字
        # 自己跳——这就是"让数字成为动画"的标准做法。
        n = ValueTracker(1.0)
        anchor = eq.get_bottom() + DOWN * 1.1  # 数字的固定锚点
        value = DecimalNumber(2.0, num_decimal_places=5, font_size=40, color=YELLOW)
        value.add_updater(
            lambda m: (
                m.set_value((1 + 1 / n.get_value()) ** n.get_value()),
                m.move_to(anchor),  # 位数变多时保持居中，不往右漂
            )
        )
        # n 的标签用"预生成 + TransformMatchingTex"切换：每帧新建
        # MathTex（always_redraw）会每帧触发一次完整 LaTeX 编译，
        # 又慢又容易在 Windows 上撞文件锁，离散切换才是正解。
        n_label = MathTex("n = 1", font_size=34)
        n_label.next_to(value, DOWN, buff=0.4)
        self.play(FadeIn(value, n_label))

        # n 取 1, 10, 100, 1000, 10000：每一步数字都更靠近 e，
        # 直观演示"单调递增、越来越慢地逼近"。
        for step in (10, 100, 1000, 10000):
            next_label = MathTex(f"n = {step}", font_size=34)
            next_label.next_to(value, DOWN, buff=0.4)
            self.play(
                n.animate.set_value(step),
                TransformMatchingTex(n_label, next_label),
                run_time=1.4,
            )
            n_label = next_label
            self.wait(0.4)
        self.wait(1)

        # 清场，进入第二重要极限。先清 updater 再 FadeOut，
        # 否则 updater 会在淡出过程中继续搬动数字。
        value.clear_updaters()
        self.play(*[FadeOut(m) for m in (title, eq, value, n_label)])

        # ---- 第二重要极限：先给图像直觉 ----
        eq2 = MathTex(r"\lim_{x\to 0}\frac{\sin x}{x} = 1", font_size=44)
        eq2.to_edge(UP, buff=0.5)
        self.play(Write(eq2))

        axes = Axes(
            x_range=[-6.5, 6.5, 1],
            y_range=[-0.4, 1.6, 1],
            x_length=11,
            y_length=4,
            tips=False,
        ).next_to(eq2, DOWN, buff=0.6)

        # sin x / x 在 x=0 处没有定义（分母为 0），所以曲线分两段
        # 画，中间留一道缝——"极限存在"不要求"在该点有定义"。
        f = lambda x: math.sin(x) / x if abs(x) > 1e-6 else float("nan")
        left = axes.plot(f, x_range=[-6.5, -0.02], color=BLUE)
        right = axes.plot(f, x_range=[0.02, 6.5], color=BLUE)
        guide = DashedLine(axes.c2p(-6.5, 1), axes.c2p(6.5, 1), color=GREY)
        guide_label = MathTex("y = 1", font_size=28, color=GREY)
        guide_label.next_to(axes.c2p(6.5, 1), RIGHT, buff=0.15)
        self.play(Create(axes), Create(left), Create(right), Create(guide), FadeIn(guide_label))

        # 空心圆点：(0, 1) 处函数无定义，但极限存在——
        # fill_opacity=0 只描边不填充，正是"挖掉一点"的画法。
        hole = Dot(axes.c2p(0, 1), radius=0.08, fill_opacity=0, stroke_color=YELLOW, stroke_width=3)
        self.play(FadeIn(hole, scale=2))

        # 动点沿曲线滑向 x=0：tracker 从 5 收到 0.05，每帧
        # 重算曲线高度。可以看到高度被"吸"向 1。
        t = ValueTracker(5.0)
        dot = always_redraw(
            lambda: Dot(
                axes.c2p(t.get_value(), math.sin(t.get_value()) / t.get_value()),
                radius=0.09,
                color=YELLOW,
            )
        )
        self.add(dot)
        self.play(t.animate.set_value(0.05), run_time=3)
        self.wait(1.5)


class SqueezeProof(Scene):
    def construct(self) -> None:
        title = Text("夹逼法证明第二重要极限", font_size=30)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # 角 x 取 0.9 弧度：足够大，三块区域肉眼可分。
        # 几何按"半径 r 的图"放大画，数学上仍是单位圆（比例不变）。
        x = 0.9
        r = 1.5
        center = LEFT * 3.6 + DOWN * 0.7
        O = center                                        # 圆心
        A = center + RIGHT * r                            # 角的始边与圆的交点
        H = center + RIGHT * r * math.cos(x)              # B 在 x 轴上的垂足
        B = center + RIGHT * r * math.cos(x) + UP * r * math.sin(x)  # 圆上的点
        C = center + RIGHT * r + UP * r * math.tan(x)     # 角终边与切线 x=1 的交点

        circle = Circle(radius=r, color=WHITE, stroke_width=2).move_to(center)
        self.play(Create(circle), run_time=1.5)

        # 三块面积，从大到小依次加入（后加的盖在上层）：
        # 大三角形 OAC ⊃ 扇形 OAB ⊃ 小三角形 OHB。
        big = Polygon(O, A, C, fill_color=RED, fill_opacity=0.25, stroke_width=1)
        sector = Sector(radius=r, angle=x, fill_color=GREEN, fill_opacity=0.45, stroke_width=1)
        sector.shift(center)  # Sector 以原点为圆心生成，整体平移到圆心
        small = Polygon(O, H, B, fill_color=YELLOW, fill_opacity=0.6, stroke_width=1)
        self.play(FadeIn(big), FadeIn(sector), FadeIn(small))

        # Angle 标出圆心角：传两条共起点的边，radius 控制弧的半径。
        angle_mark = Angle(Line(O, A), Line(O, B), radius=0.4, color=ORANGE, stroke_width=3)
        x_label = MathTex("x", font_size=30, color=ORANGE)
        x_label.move_to(center + 0.65 * (RIGHT * math.cos(x / 2) + UP * math.sin(x / 2)))
        self.play(Create(angle_mark), FadeIn(x_label))

        # 三块面积各配一个标签，颜色与区域一一对应：
        # 小三角形 = (1/2)·底OH(cos x)·高HB(sin x)
        # 扇形     = (1/2)·r²·x = x/2（x 是弧度制！）
        # 大三角形 = (1/2)·底OA(1)·高AC(tan x)
        lab1 = MathTex(r"\tfrac{\sin x\cos x}{2}", font_size=26, color=YELLOW)
        lab1.next_to(H, DOWN, buff=0.2)
        lab2 = MathTex(r"\tfrac{x}{2}", font_size=26, color=GREEN)
        lab2.move_to(center + (r + 0.45) * (RIGHT * math.cos(x / 2) + UP * math.sin(x / 2)))
        lab3 = MathTex(r"\tfrac{\tan x}{2}", font_size=26, color=RED)
        lab3.move_to((O + A + C) / 3)  # 三角形重心处
        self.play(FadeIn(lab1), FadeIn(lab2), FadeIn(lab3))

        # ---- 右侧：不等式链逐步变形 ----
        # 第 1 步：三块面积从小到大排成一串。
        eq1 = MathTex(
            r"\frac{\sin x\cos x}{2}", "<", r"\frac{x}{2}", "<", r"\frac{\tan x}{2}", font_size=36
        )
        eq1.move_to(RIGHT * 3.4 + UP * 1.7)
        self.play(Write(eq1))

        # 第 2 步：同除以正数 (1/2)sin x，不等号方向不变。
        eq2 = MathTex(r"\cos x", "<", r"\frac{x}{\sin x}", "<", r"\frac{1}{\cos x}", font_size=36)
        eq2.move_to(RIGHT * 3.4 + UP * 0.4)
        note2 = Text("同除以正数 (1/2)sin x", font_size=20, color=GREY)
        note2.next_to(eq2, DOWN, buff=0.15)
        self.play(TransformMatchingTex(eq1, eq2), FadeIn(note2))

        # 第 3 步：各项为正，取倒数时不等号反向，得到目标形式。
        eq3 = MathTex(r"\cos x", "<", r"\frac{\sin x}{x}", "<", r"\frac{1}{\cos x}", font_size=36)
        eq3.move_to(RIGHT * 3.4 + DOWN * 0.7)
        note3 = Text("取倒数，不等号反向", font_size=20, color=GREY)
        note3.next_to(eq3, DOWN, buff=0.15)
        self.play(TransformMatchingTex(eq2, eq3), FadeIn(note3))

        # 第 4 步：x→0 时 cos x→1、1/cos x→1，两端夹住中间，
        # 由夹逼定理极限必为 1。
        eq4 = MathTex(r"\lim_{x\to 0}\frac{\sin x}{x} = 1", font_size=40, color=YELLOW)
        eq4.move_to(RIGHT * 3.4 + DOWN * 2.0)
        self.play(TransformMatchingTex(eq3, eq4))
        box = SurroundingRectangle(eq4, color=YELLOW, buff=0.15)
        self.play(Create(box))
        self.wait(1.5)


class DiscontinuityTypes(Scene):
    def construct(self) -> None:
        title = Text("连续性定义与三类间断点", font_size=30)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # 连续的精确定义：极限值 == 函数值。三个条件缺一不可：
        # 极限存在、函数值存在、两者相等。
        cont_def = MathTex(r"\lim_{x\to x_0} f(x) = f(x_0)", font_size=40)
        cont_def.next_to(title, DOWN, buff=0.3)
        self.play(Write(cont_def))
        self.wait(1)
        # 定义缩小挪到左上角让位，下方并排摆三个坐标系。
        self.play(cont_def.animate.scale(0.7).to_corner(UL, buff=0.35))

        # 三个面板共用同一套坐标设置；先建好再 arrange 排开。
        common = dict(x_range=[-2.2, 2.2, 1], y_range=[-1.6, 2.6, 1], x_length=4, y_length=3, tips=False)
        axes1, axes2, axes3 = Axes(**common), Axes(**common), Axes(**common)
        VGroup(axes1, axes2, axes3).arrange(RIGHT, buff=0.9).shift(DOWN * 1.3)

        # ---- 面板 1：可去间断点。f(x) = (x²-1)/(x-1) 在 x=1 处
        # 无定义，但极限是 2——曲线上"挖掉一点"。
        curve1 = axes1.plot(lambda x: (x * x - 1) / (x - 1) if abs(x - 1) > 1e-6 else x + 1,
                            x_range=[-2.2, 1.4], color=BLUE)
        hole1 = Dot(axes1.c2p(1, 2), radius=0.08, fill_opacity=0, stroke_color=RED, stroke_width=3)
        self.play(Create(axes1), Create(curve1), FadeIn(hole1, scale=2))

        # 补上 f(1)=2，空心点变实心——间断被"修复"，这就是"可去"。
        patch1 = Dot(axes1.c2p(1, 2), radius=0.08, color=RED)
        self.play(Transform(hole1, patch1))

        # ---- 面板 2：跳跃间断点。x<0 时 f=-1，x≥0 时 f=1，
        # 左右极限都存在但不相等——图象在 x=0 处"跳"了一格。
        seg_l = axes2.plot(lambda _: -1, x_range=[-2.2, 0], color=BLUE)
        seg_r = axes2.plot(lambda _: 1, x_range=[0, 2.2], color=BLUE)
        # 左极限 -1 画空心（函数在那里没有取值），f(0)=1 画实心。
        open2 = Dot(axes2.c2p(0, -1), radius=0.08, fill_opacity=0, stroke_color=RED, stroke_width=3)
        solid2 = Dot(axes2.c2p(0, 1), radius=0.08, color=RED)
        self.play(Create(axes2), Create(seg_l), Create(seg_r), FadeIn(open2), FadeIn(solid2))

        # ---- 面板 3：无穷间断点。f(x)=1/x 在 x→0 时极限为 ∞，
        # 出现垂直渐近线 x=0（DashedLine 是渐近线的标准画法）。
        left3 = axes3.plot(lambda x: 1 / x, x_range=[-2.2, -0.63], color=BLUE)
        right3 = axes3.plot(lambda x: 1 / x, x_range=[0.4, 2.2], color=BLUE)
        asym = DashedLine(axes3.c2p(0, -1.6), axes3.c2p(0, 2.6), color=RED)
        asym_label = MathTex("x = 0", font_size=24, color=RED)
        asym_label.next_to(axes3.c2p(0, 2.6), UP, buff=0.1)
        self.play(Create(axes3), Create(left3), Create(right3), Create(asym), FadeIn(asym_label))

        # 三个名字各挂在自己的坐标系正下方。
        names = [
            Text(name, font_size=24, color=color)
            for name, color in zip(("可去间断点", "跳跃间断点", "无穷间断点"), (RED, ORANGE, YELLOW))
        ]
        for name, axes in zip(names, (axes1, axes2, axes3)):
            name.next_to(axes, DOWN, buff=0.2)
        self.play(*[FadeIn(name) for name in names])
        self.wait(1.5)


def main() -> None:
    parser = argparse.ArgumentParser(description="两个重要极限与函数的连续性")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "02",
        [LimitOfE, SqueezeProof, DiscontinuityTypes],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
