"""第 8 课：多元函数微分学——偏导数、全微分与梯度。

本课要回答三个问题：
    1. 二元函数"各有各的方向"，导数怎么定义？
    2. 切平面凭什么是"最好的线性近似"，dz 和 Δz 差在哪？
    3. 梯度 ∇f 和等高线之间有什么几何关系？

原理速览：
    （数学）偏导数：固定 y = y₀，把 f(x, y₀) 当一元函数对 x 求导——
      几何上是曲面被平面 y = y₀ 截出的曲线在该点的斜率；
    全微分：dz = f_x dx + f_y dy 是切平面上竖直方向的增量，
      与真正的 Δz 之差是 ρ = √(Δx² + Δy²) 的高阶小量 o(ρ)，
      于是 f(x₀+Δx, y₀+Δy) ≈ f(x₀,y₀) + f_x Δx + f_y Δy；
    梯度：∇f = (f_x, f_y)，方向是 f 上升最快的方向，
      且处处垂直于等高线 f(x, y) = C（本例 f = x²+y² 的等高线
      是同心圆，∇f = (2x, 2y) 恰好沿半径向外）。
    （manim）3D 部分：ThreeDAxes + Surface 画曲面，切片曲线用
      ParametricFunction 沿参数采样；add_fixed_in_frame_mobjects
      把 2D 公式"钉"在屏幕坐标系里——不随相机转动，也就不会被
      曲面挡住。机位 phi≈70° 兼顾俯视全貌与侧视斜率，theta=-45°
      是经典的斜前方展示角。
    2D 部分：本课刻意把坐标轴设成"1 数学单位 = 1 屏幕单位"且
      原点居中，这样 ArrowVectorField 在屏幕坐标里算出的方向
      就是数学方向，梯度场不用做任何缩放换算。

最短运行：
    uv run hello-manim calculus 08

也可以用 manim 原生命令行逐个场景渲染：
    uv run manim -pql src/hello_manim/calculus/08.py PartialDerivative3D
    uv run manim -pql src/hello_manim/calculus/08.py TangentPlane
    uv run manim -pql src/hello_manim/calculus/08.py GradientField
"""

import argparse

import numpy as np
from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class PartialDerivative3D(ThreeDScene):
    def construct(self) -> None:
        # 曲面：z = (x² + y²)/4，一个开口向上的抛物面。
        f = lambda x, y: (x**2 + y**2) / 4
        # ThreeDAxes 是 Axes 的 3D 版：c2p 接受三个数学坐标，
        # 返回 3D 屏幕坐标。z 轴范围按曲面最高点 (3²+3²)/4 = 4.5 修剪。
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[-0.5, 4, 1],
            x_length=6.5,
            y_length=6.5,
            z_length=3.5,
        )
        # Surface 把参数方程 (u, v) → 三维点采样成网格面；
        # 这里参数恰好就是 (x, y)，经 axes.c2p 翻译成屏幕坐标。
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.75,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        # 机位怎么选：phi=70° 留 20° 俯角——全俯视（phi 小）看不清
        # "斜率"，纯平视（phi=90°）曲面又叠成一条线；theta=-45° 让
        # x 轴斜向右下，切片曲线的走向一目了然。
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.play(Create(surface), run_time=2)

        # 环境旋转：先转一圈让观众看清曲面的整体形状。
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        # 旋转停在任意 theta；演示斜率前必须把机位"扶正"，
        # move_camera 用 play 驱动相机插值回初始角度。
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES)

        # 3D 场景里 2D 公式会跟着相机转、还会被曲面遮住；
        # add_fixed_in_frame_mobjects 把它"钉"在屏幕坐标系，
        # 之后 to_edge 定位的就是屏幕位置而非空间位置。
        title = Text("偏导数：固定 y，把二元当一元", font_size=30)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # 切片：固定 y = y₀，曲面被竖直平面截出一条平面曲线
        # z = f(x, y₀)。ParametricFunction 沿 t ∈ [-3, 3] 采样。
        y0 = 1.5
        slice_curve = ParametricFunction(
            lambda t: axes.c2p(t, y0, f(t, y0)),
            t_range=[-3, 3, 0.02],
            color=ORANGE,
        )
        note = Text(f"固定 y = {y0}：截出一条平面曲线", font_size=24, color=ORANGE)
        note.next_to(title, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(note)
        self.play(Create(slice_curve), FadeIn(note))

        # 点沿切片移动，黄色小段始终是该点的切线。
        # 切向的数学方向是 (1, 0, f_x)，f_x = ∂f/∂x = x/2；
        # c2p 是仿射映射，两个 c2p 之差 = 各轴缩放后的方向向量，
        # 所以用 c2p(1, 0, f_x) - c2p(0, 0, 0) 就得到屏幕坐标下的切向。
        fx = lambda x: x / 2
        t = ValueTracker(-2.2)

        def slice_point() -> np.ndarray:
            x = t.get_value()
            return axes.c2p(x, y0, f(x, y0))

        def tangent_dir() -> np.ndarray:
            x = t.get_value()
            d = axes.c2p(1, 0, fx(x)) - axes.c2p(0, 0, 0)
            return d / np.linalg.norm(d)

        # always_redraw：每帧重建这两个小物体，位置/方向跟着 t 走。
        dot = always_redraw(lambda: Dot3D(slice_point(), radius=0.09, color=YELLOW))
        tangent_seg = always_redraw(
            lambda: Line(
                slice_point() - tangent_dir(),
                slice_point() + tangent_dir(),
                color=YELLOW,
            )
        )
        self.add(dot, tangent_seg)
        self.play(t.animate.set_value(1.6), run_time=4)

        # 偏导数定义：分子里 y 恒为 y₀——"只动 x"正是切片的含义。
        defn = MathTex(
            r"\frac{\partial f}{\partial x}\Bigg|_{(x_0,\, y_0)}"
            r"= \lim_{\Delta x \to 0}"
            r"\frac{f(x_0 + \Delta x,\, y_0) - f(x_0,\, y_0)}{\Delta x}",
        )
        defn.set_color_by_tex("partial", YELLOW)
        defn.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(defn)
        self.play(Write(defn))
        self.wait(2)


class TangentPlane(ThreeDScene):
    def construct(self) -> None:
        f = lambda x, y: (x**2 + y**2) / 4
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[-0.5, 4, 1],
            x_length=6.5,
            y_length=6.5,
            z_length=3.5,
        )
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            fill_opacity=0.65,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        # 机位固定不转：本幕要比较两段竖直线段的长短，
        # 相机一动长度对比就不直观了。theta=-50° 让切平面
        # 的白色网格和两条线段都朝向观众。
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
        self.add(axes)
        self.play(Create(surface), run_time=2)

        # 切点 P₀ = (1, 1, 0.5)；f_x = x/2、f_y = y/2，故 f_x = f_y = 0.5。
        x0, y0 = 1.0, 1.0
        f0 = f(x0, y0)
        p0 = axes.c2p(x0, y0, f0)
        self.play(FadeIn(Dot3D(p0, radius=0.1, color=YELLOW)))

        # 切平面：z = f₀ + f_x(x-x₀) + f_y(y-y₀)，法向量 (f_x, f_y, -1)。
        # 在 (x₀, y₀) 附近取一小片 Surface 即可——切平面本是局部的。
        plane = Surface(
            lambda u, v: axes.c2p(u, v, f0 + 0.5 * (u - x0) + 0.5 * (v - y0)),
            u_range=[0.0, 2.0],
            v_range=[0.0, 2.0],
            fill_opacity=0.5,
            checkerboard_colors=[YELLOW_D, YELLOW_E],
        )
        self.play(Create(plane), run_time=2)

        # 顶部公式区：fixed-in-frame + 左对齐排布，与 3D 图形互不遮挡。
        eq_dz = MathTex(r"\mathrm{d}z = \frac{\partial f}{\partial x}\mathrm{d}x + \frac{\partial f}{\partial y}\mathrm{d}y")
        eq_lin = MathTex(
            r"f(x_0{+}\Delta x,\, y_0{+}\Delta y)"
            r"\approx f(x_0, y_0) + f_x\,\Delta x + f_y\,\Delta y",
        )
        legend = VGroup(
            Text("绿：dz——切平面上的线性增量", font_size=22, color=GREEN),
            Text("红：两者之差 = o(ρ)，高阶小量", font_size=22, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        panel = VGroup(eq_dz, eq_lin, legend).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.to_corner(UL, buff=0.4).set_z_index(3)
        self.add_fixed_in_frame_mobjects(panel)
        self.play(Write(eq_dz), FadeIn(eq_lin, legend))

        # 取增量 (Δx, Δy) = (0.9, 0.7)：
        #   Δz（真实）= f(1.9, 1.7) - f(1, 1) = 1.625 - 0.5 = 1.125
        #   dz（线性）= 0.5·0.9 + 0.5·0.7 = 0.8
        #   差 0.325 = (Δx² + Δy²)/4，正是二阶小量。
        dx, dy = 0.9, 0.7
        p_tan = axes.c2p(x0 + dx, y0 + dy, f0 + 0.5 * dx + 0.5 * dy)  # 切平面上的点
        p_surf = axes.c2p(x0 + dx, y0 + dy, f(x0 + dx, y0 + dy))      # 曲面上的点
        seg_dz = Line(p0, p_tan, color=GREEN, stroke_width=6)
        seg_err = DashedLine(p_tan, p_surf, color=RED, stroke_width=6)
        self.play(Create(seg_dz), run_time=1.5)
        self.play(Create(seg_err), run_time=1.5)
        self.wait(2)


class GradientField(Scene):
    def construct(self) -> None:
        # 刻意让缩放比 1:1：x/y 各 8/6 个数学单位映射到 8/6 个屏幕
        # 单位，且对称范围 + 默认居中 ⇒ c2p(x, y) 恰好 = (x, y)。
        # 这样 ArrowVectorField 在屏幕坐标里算方向就是数学方向。
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            tips=False,
        )
        title = Text("f(x, y) = x² + y² 的等高线与梯度场", font_size=28)
        title.to_edge(UP)

        # 等高线 f = C（C = 1, 4, 9）是半径 √C 的同心圆；
        # 闭包陷阱：lambda 默认参数 r=r 把当前值"冻结"进函数，
        # 否则三条曲线会全用最后一个 r。
        levels = [1, 2, 3]
        contours = VGroup(
            *(
                ParametricFunction(
                    lambda t, r=r: axes.c2p(r * np.cos(t), r * np.sin(t)),
                    t_range=[0, TAU, 0.05],
                    color=TEAL,
                )
                for r in levels
            )
        )
        # 等高线标签放在每条圆 135° 方向的点上，稍向外让开线条。
        labels = VGroup(
            *(
                MathTex(f"x^2+y^2={r * r}").next_to(
                    axes.c2p(-0.72 * r, 0.72 * r), UP, buff=0.12
                )
                for r in levels
            )
        )
        self.play(Write(title), Create(axes))
        self.play(Create(contours), FadeIn(labels))

        # 单点演示"垂直"：取圆 r=2 上 60° 处的点 (1, √3)。
        # 半径方向 (cos60°, sin60°)，梯度 ∇f = (2, 2√3) 方向恰好相同。
        px, py = 1.0, np.sqrt(3.0)
        radius_line = DashedLine(axes.c2p(0, 0), axes.c2p(px, py), color=WHITE)
        g = np.array([2 * px, 2 * py])
        g_unit = g / np.linalg.norm(g)
        grad_arrow = Arrow(
            axes.c2p(px, py),
            axes.c2p(px + 1.3 * g_unit[0], py + 1.3 * g_unit[1]),
            color=YELLOW,
            buff=0,
            max_tip_length_to_length_ratio=0.25,
        )
        self.play(Create(radius_line), GrowArrow(grad_arrow))
        self.wait(1)

        # 完整梯度场：func 输入/输出都是屏幕坐标；由 1:1 缩放，
        # 向量 (2x, 2y) 无需换算。length_func 把箭头长度夹到 0.55
        # 以内，防止角落（|∇f| 大）的箭头撑爆画面。
        field = ArrowVectorField(
            lambda p: np.array([2 * p[0], 2 * p[1], 0]),
            x_range=[-3.7, 3.8, 0.9],
            y_range=[-2.7, 2.8, 0.9],
            length_func=lambda norm: min(norm, 8) / 8 * 0.55,
        )
        eq_grad = MathTex(r"\nabla f = \left( \frac{\partial f}{\partial x},\ \frac{\partial f}{\partial y} \right) = (2x,\ 2y)")
        eq_grad.to_edge(DOWN, buff=0.25)
        self.play(FadeOut(radius_line), FadeOut(grad_arrow))
        self.play(Create(field), run_time=2)
        self.play(Write(eq_grad))

        # 结论文字压轴：两条性质合写一行，避免与底部公式重叠。
        concl = Text("梯度垂直于等高线，指向 f 上升最快的方向", font_size=24, color=YELLOW)
        concl.next_to(eq_grad, UP, buff=0.2)
        self.play(Write(concl))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="多元函数微分学：偏导数、全微分与梯度")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus",
        "08",
        [PartialDerivative3D, TangentPlane, GradientField],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
