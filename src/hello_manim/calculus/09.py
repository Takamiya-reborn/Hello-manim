"""第 9 课：二重积分——曲顶柱体、累次积分与极坐标。

本课要回答三个问题：
    1. ∬ f(x,y) dσ 的"曲顶柱体体积"直觉是怎么来的？
    2. 一个二重积分为什么能拆成两次一元积分（累次积分）？
    3. 极坐标换元时多出来的那个 r 是什么、从哪来？

原理速览：
    数学原理：
      - 二重积分是"分割—近似—求和—取极限"的平面版本：把区域 D
        切成小格，每格面积 Δσᵢ，任取一点 (ξᵢ,ηᵢ) 以 f(ξᵢ,ηᵢ) 为高
        立起细柱体，和式 Σ f·Δσᵢ 在分割无限加细时的极限就是
        V = ∬_D f(x,y) dσ；
      - X 型区域（0≤x≤1，x²≤y≤√x）：竖直条带内先"沿 y 累加"
        （内层积分 ∫ f dy），条带再"从左扫到右"（外层 ∫ dx）——
        这就是累次积分；富比尼定理保证交换次序结果不变；
      - 极坐标下小格是扇环：面积 ≈ 弧长 rΔθ × 厚度 Δr，取极限得
        dA = r dr dθ。多出来的 r 是换元的雅可比因子——同样的
        ΔrΔθ，越靠外张出的真实面积越大。
    manim 手段：
      - 3D 曲顶：ThreeDAxes + Surface，参数域直接取 (r,θ)∈[0,1]×
        [0,2π] 采样圆盘，避免矩形参数域出界；Prism 立起采样柱体；
      - 2D 区域：Axes.get_area(bounded_graph=...) 填两曲线之间；
        always_redraw + ValueTracker 让扫描条带边移动边变形；
      - 扇环面积元：AnnularSector 自带内径/外径/张角三个参数；
      - 公式推导用 MathTex + TransformMatchingTex（第 6 课手法）。

最短运行：
    uv run hello-manim calculus 09

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/calculus/09.py CurvedTopSolid
"""

import argparse

import numpy as np
from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class CurvedTopSolid(ThreeDScene):
    """第一幕：曲顶柱体——二重积分的体积直觉与定义。"""

    def construct(self) -> None:
        # 3D 坐标系：xoy 平面放底面区域 D，z 轴竖直向上表示函数值（高）。
        axes = ThreeDAxes(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[0, 1.5, 1],
            x_length=4.5, y_length=4.5, z_length=2.5,
        )
        # 曲顶 z = f(x,y) = 1 − (x²+y²)/2：定义在单位圆盘上，
        # 中心高 1、边界高 1/2，是一个开口向下的旋转抛物面。
        f = lambda x, y: 1 - (x * x + y * y) / 2
        # Surface 把参数方程 (u,v) → 空间点采样成网格面。取 (r,θ) 作
        # 参数：r∈[0,1] 扫半径、θ∈[0,2π] 转一圈，参数域恰好就是单位
        # 圆盘——比用矩形参数域再"裁"出圆盘干净得多。
        top = Surface(
            lambda r, th: axes.c2p(
                r * np.cos(th), r * np.sin(th), f(r * np.cos(th), r * np.sin(th))
            ),
            u_range=[0, 1],
            v_range=[0, TAU],
            fill_opacity=0.75,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        # 机位：phi=70° 略带俯角，theta=-45° 斜前方 45°，经典展示角。
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.play(Create(top), run_time=2)

        # "分割—近似"：挑几个采样点 (ξᵢ,ηᵢ)，在底面格点上立起以
        # f(ξᵢ,ηᵢ) 为高的细柱体。屏幕高度要按 z 轴比例换算：
        # 每数学单位 = z_length / z 范围跨度 = 2.5/1.5。
        unit_z = 2.5 / 1.5
        for gx, gy in [(-0.6, -0.6), (0.6, -0.6), (0, 0), (-0.6, 0.6), (0.6, 0.6)]:
            h = f(gx, gy) * unit_z
            # Prism(dimensions) 是以原点为中心的长方体：先按
            # (格宽, 格宽, 柱高) 定尺寸，再平移到底面格点并抬高
            # 半个柱高，让柱底正好贴住 z=0 平面。
            bar = Prism(dimensions=[0.3, 0.3, h], fill_opacity=0.85, color=ORANGE)
            bar.shift(axes.c2p(gx, gy, 0) + UP * h / 2)
            self.play(FadeIn(bar), run_time=0.4)

        # 定义式。3D 场景里普通物体都会被透视投影，公式的字会被拉歪；
        # add_fixed_in_frame_mobjects 把物体"钉"在屏幕平面上。它同时
        # 会把物体加入场景，所以先移掉再 Write，避免"先出现后书写"。
        dfn = MathTex(
            r"V = \iint_D f(x,y)\,d\sigma"
            r" = \lim_{\lambda\to 0} \sum_{i=1}^{n} f(\xi_i,\eta_i)\,\Delta\sigma_i",
            font_size=36,
        )
        dfn.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(dfn)
        self.remove(dfn)
        self.play(Write(dfn), run_time=2)
        self.wait(1)


class IteratedIntegral(Scene):
    """第二幕：累次积分——X 型区域上的"先 y 后 x"扫描。"""

    def construct(self) -> None:
        # 布局：图形居左、公式居右，互不重叠（第 1 课的布局原则）。
        axes = Axes(
            x_range=[-0.4, 1.6, 1], y_range=[-0.4, 1.4, 1],
            x_length=5, y_length=4.5, tips=False,
        ).shift(LEFT * 3.2 + DOWN * 0.4)
        upper = axes.plot(lambda x: np.sqrt(x), x_range=[0, 1], color=GREEN)
        lower = axes.plot(lambda x: x ** 2, x_range=[0, 1], color=BLUE)
        # get_area 的 bounded_graph 参数：填充 graph 与 bounded_graph
        # "之间"——正好是 X 型区域 D = {(x,y) | x² ≤ y ≤ √x}。
        region = axes.get_area(
            upper, x_range=[0, 1], bounded_graph=lower, color=BLUE_C, opacity=0.35
        )
        self.play(Create(axes), run_time=1.5)
        self.play(Create(upper), Create(lower), FadeIn(region))

        # 主公式放右上角，下面逐步补两步口诀与验算。
        eq = MathTex(
            r"\iint_D f\,d\sigma = \int_0^1\! dx \int_{x^2}^{\sqrt{x}} f\,dy",
            font_size=40,
        )
        eq.to_edge(UP, buff=0.6).shift(RIGHT * 2.6)
        self.play(Write(eq))

        # 扫描条带：always_redraw 每帧按 tracker 重建——横坐标固定为
        # t，上下端点取该处的边界值，条带高度自动贴合区域（第 4 课
        # 的"参数驱动"手法，比逐帧手摆 Rectangle 优雅得多）。
        t = ValueTracker(0.0)
        strip = always_redraw(
            lambda: Line(
                axes.c2p(t.get_value(), t.get_value() ** 2),
                axes.c2p(t.get_value(), np.sqrt(t.get_value())),
                stroke_width=14,
                stroke_color=ORANGE,
            )
        )
        self.add(strip)
        self.play(t.animate.set_value(1.0), run_time=4)

        # 两步口诀：先对 y 积分（条带内的长度），再对 x 积分（条带扫过区间）。
        step1 = Text("先对 y 积分：条带内的长度", font_size=24, color=ORANGE)
        step1.next_to(eq, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(step1))
        step2 = Text("再对 x 积分：条带从 0 扫到 1", font_size=24, color=GREEN)
        step2.next_to(step1, DOWN, aligned_edge=LEFT, buff=0.25)
        self.play(FadeIn(step2))

        # 验算：取 f = 1，二重积分就是区域面积。内层积出条带长
        # √x − x²，再对 x 从 0 到 1 积分：2/3 − 1/3 = 1/3。
        eq2 = MathTex(r"A = \int_0^1 \left(\sqrt{x} - x^2\right) dx", font_size=40)
        eq2.next_to(step2, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(eq2))
        eq3 = MathTex(
            r"= \left[\frac{2}{3}x^{3/2} - \frac{x^3}{3}\right]_0^1 = \frac{1}{3}",
            font_size=40,
        )
        eq3.next_to(eq2, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(1.5)


class PolarTransform(Scene):
    """第三幕：极坐标——面积元里多出来的那个 r。"""

    def construct(self) -> None:
        scale = 2.0  # 数学 1 单位 → 屏幕 2 单位
        origin = LEFT * 3.6 + DOWN * 0.8
        # 极坐标网格 = 同心圆（r = 常数）+ 放射线（θ = 常数）。
        # 本课不需要 Axes：极坐标里没有"坐标轴"，只有网格。
        grid = VGroup()
        for r in (0.25, 0.5, 0.75, 1.0):
            grid.add(
                Circle(radius=r * scale, color=GREY_B, stroke_width=1.5).move_to(origin)
            )
        for k in range(12):
            ang = k * TAU / 12
            grid.add(
                Line(
                    origin,
                    origin + scale * np.array([np.cos(ang), np.sin(ang), 0]),
                    color=GREY_B, stroke_width=1.5,
                )
            )
        self.play(Create(grid), run_time=2)

        # 一小块扇环：内径 0.6、外径 0.75（Δr = 0.15），张角 30°
        # （Δθ = π/6）。AnnularSector 画在原点处，平移到网格中心。
        cell = AnnularSector(
            inner_radius=0.6 * scale, outer_radius=0.75 * scale,
            angle=TAU / 12, start_angle=TAU / 12,
            fill_opacity=0.6, color=YELLOW, stroke_width=2,
        ).shift(origin)
        self.play(FadeIn(cell))

        # 放大展示：拷贝一份放大 2 倍放到右侧，好观察扇环的两条边。
        big = cell.copy().scale(2.0).move_to(RIGHT * 3.6 + UP * 0.9)
        self.play(TransformFromCopy(cell, big), run_time=1.5)

        # 面积近似：外弧长 ≈ rΔθ（内弧更短，取极限后差是高阶小量），
        # 厚度 = Δr，所以 ΔA ≈ r·Δr·Δθ。
        approx = MathTex(r"\Delta A \approx r\,\Delta r\,\Delta\theta", font_size=36)
        approx.next_to(big, DOWN, buff=0.4)
        self.play(Write(approx))

        # 本幕主角：取极限后多出来的那个 r（雅可比因子）。单独上红
        # 加框强调——没有它，dr dθ 乘出来就不是真实面积。
        dA = MathTex(r"dA = ", r"r", r"\,dr\,d\theta", font_size=44)
        dA[1].set_color(RED)
        dA.next_to(approx, DOWN, buff=0.35)
        box = SurroundingRectangle(dA[1], color=RED, buff=0.1)
        self.play(Write(dA), Create(box))

        # 例：单位圆盘面积。r 从 0 到 1，θ 转 2π；∫₀¹ r dr = 1/2，
        # ∫₀^{2π} dθ = 2π，相乘得 π——与圆面积 π·1² 一致，验算通过。
        ex1 = MathTex(
            r"\iint_{x^2+y^2\le 1} dA = \int_0^{2\pi}\!\!\int_0^1 r\,dr\,d\theta",
            font_size=36,
        )
        ex1.to_edge(UP, buff=0.5).shift(LEFT * 3.6)
        ex2 = MathTex(
            r"= \left(\int_0^{2\pi} d\theta\right)\!\left(\int_0^1 r\,dr\right)"
            r" = 2\pi \cdot \frac{1}{2} = \pi",
            font_size=36,
        )
        ex2.next_to(ex1, DOWN, buff=0.35)
        check = Text("与圆面积 π·1² = π 一致", font_size=24, color=GREEN)
        check.next_to(ex2, DOWN, buff=0.3)
        self.play(Write(ex1))
        self.play(TransformMatchingTex(ex1, ex2), FadeIn(check))
        self.wait(1.5)


def main() -> None:
    parser = argparse.ArgumentParser(description="二重积分：曲顶柱体、累次积分与极坐标")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "09",
        [CurvedTopSolid, IteratedIntegral, PolarTransform],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
