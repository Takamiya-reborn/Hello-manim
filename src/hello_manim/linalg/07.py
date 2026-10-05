"""第 7 课：点积、叉积与 Gram-Schmidt 正交化。

本课要回答三个问题：
    1. 点积 v·w 除了"对应分量相乘再求和"，几何上到底在量什么？
    2. 叉积为什么又叫"有向面积"？3D 里它为什么垂直于原来两个向量？
    3. Gram-Schmidt 凭什么能把任一组基"掰"成互相垂直的正交基？

原理速览：
    数学上，三件事是同一件事的三个侧面——"分解"：
      - 点积：v·w = |v||w|cosθ = vᵀw = v_x w_x + v_y w_y。几何上，
        点积 = "v 在 w 方向上的投影长度 × w 的长度"。θ 为锐角时
        为正，直角时为零（垂直 = 在对方方向毫无伸长量），钝角时
        为负。投影公式 proj_u(v) = (v·u / u·u)·u：分子 v·u 量出
        "沿 u 的伸长量"，分母 u·u = |u|² 把它换算成 u 的几倍；
      - 叉积：2D 里 v×w 的 z 分量 = v_x w_y − v_y w_x，绝对值正是
        v、w 张成的平行四边形面积（正负号记录转向）；3D 里
        |v×w| = |v||w|sinθ，方向由右手定则确定——v×w 同时垂直
        于 v 与 w，就是平行四边形的法向量；
      - Gram-Schmidt：逐个"减去已定方向上的分量"。u₁ = v₁，
        u₂ = v₂ − proj_{u₁}(v₂)。验证：u₂·u₁ = v₂·u₁ −
        (v₂·u₁/u₁·u₁)(u₁·u₁) = 0——垂直是构造出来的必然。
        正交基的好处：坐标 = 逐个做投影，各分量互不干扰。
    manim 手段：
      - Arrow（buff=0 让箭头精确指到端点）画向量；DashedLine 画
        垂足辅助线；RightAngle 在共点线之间标直角小方块；
      - ValueTracker + always_redraw：向量旋转时，箭头、投影段、
        DecimalNumber 读数逐帧重算——正/零/负三种状态自动换色；
      - ThreeDScene 默认相机正对 xy 平面，前半段照常当 2D 用，
        move_camera 一键切到 3D 视角；add_fixed_in_frame_mobjects
        让文字在 3D 视角下仍正对观众，不会被透视压扁。

最短运行：
    uv run hello-manim linalg 07

也可以用 manim 原生命令行渲染每一个场景：
    uv run manim -pql src/hello_manim/linalg/07.py DotProductAsProjection
    uv run manim -pql src/hello_manim/linalg/07.py CrossProductArea
    uv run manim -pql src/hello_manim/linalg/07.py GramSchmidt
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class DotProductAsProjection(Scene):
    def construct(self) -> None:
        title = Text("点积 = 投影", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 单位长度 = 长度/跨度：x 4.8/6、y 5.6/7 都是 0.8——两轴等比，
        # "垂直"在屏幕上才是真垂直（第 5 课 c2p 同样的道理）。
        axes = Axes(
            x_range=[-1.5, 4.5, 1], y_range=[-3, 4, 1],
            x_length=4.8, y_length=5.6, tips=False,
        ).move_to(LEFT * 4 + DOWN * 0.6)
        self.play(Create(axes))

        # v=(3,1)、w=(1,2)：v·w = 3·1+1·2 = 5，而 |w|² = 1+4 = 5。
        # 于是 proj_w(v) = (v·w/|w|²)·w = w——垂足恰好是 w 的终点，
        # 数字上的巧合正好用来把"点积与投影"绑在同一个画面上。
        v = Arrow(axes.c2p(0, 0), axes.c2p(3, 1), buff=0, color=BLUE)
        w = Arrow(axes.c2p(0, 0), axes.c2p(1, 2), buff=0, color=GREEN)
        vl = MathTex(r"\vec v=(3,1)", font_size=30, color=BLUE).next_to(v.get_end(), UP, buff=0.15)
        wl = MathTex(r"\vec w=(1,2)", font_size=30, color=GREEN).next_to(w.get_end(), UP, buff=0.15)
        self.play(GrowArrow(v), Write(vl), GrowArrow(w), Write(wl))

        # 垂足辅助线：从 v 的终点向 w 所在直线作垂线（虚线 = 辅助惯例）。
        dashed = DashedLine(axes.c2p(3, 1), axes.c2p(1, 2), color=GREY_B)
        # 投影段加粗：原点到垂足，压在 w 上——投影就是 w 本身。
        proj = Line(axes.c2p(0, 0), axes.c2p(1, 2), stroke_width=9, color=YELLOW)
        self.play(Create(dashed), Create(proj))

        # 右栏公式：代数定义与几何意义并排给。
        f1 = MathTex(
            r"\vec v\cdot\vec w", "=", r"|\vec v|\,|\vec w|\cos\theta", "=", r"\vec v^{T}\vec w",
            font_size=32,
        )
        f2 = MathTex(r"= 3\cdot 1 + 1\cdot 2 = 5", font_size=32, color=YELLOW)
        f1.next_to(title, DOWN, buff=0.45).to_edge(RIGHT, buff=0.6)
        f2.next_to(f1, DOWN, buff=0.25).align_to(f1, RIGHT)
        self.play(Write(f1), Write(f2))
        note = Text("点积 = v 在 w 上的投影长度 × |w|", font_size=26)
        note.next_to(f2, DOWN, buff=0.35).align_to(f1, LEFT)
        self.play(FadeIn(note))

        # ===== 旋转阶段：v 绕原点转动，看点积由正变零再变负 =====
        # ValueTracker 只存一个数（v 的辐角），所有画面元素都从它现算。
        t = ValueTracker(math.atan2(1, 3))

        def tip_foot():
            ang = t.get_value()
            # 模长 √10 固定，转动时 v 的终点落在半径 √10 的圆上。
            tip = (math.sqrt(10) * math.cos(ang), math.sqrt(10) * math.sin(ang))
            # 垂足 = (v·w/|w|²)·w = (v·w/5)·(1,2)；v·w 变负时垂足
            # 越过原点到 w 的反向延长线上——投影是往"直线"上投的。
            d = math.sqrt(10) * (math.cos(ang) + 2 * math.sin(ang)) / 5
            return tip, (d, 2 * d)

        # always_redraw：每帧先移除旧物体再调用函数重建，
        # 于是箭头/辅助线/加粗段自动跟随 tracker，无需逐帧 play。
        rot_v = always_redraw(
            lambda: Arrow(axes.c2p(0, 0), axes.c2p(*tip_foot()[0]), buff=0, color=BLUE)
        )
        rot_dash = always_redraw(
            lambda: DashedLine(axes.c2p(*tip_foot()[0]), axes.c2p(*tip_foot()[1]), color=GREY_B)
        )
        rot_proj = always_redraw(
            lambda: Line(axes.c2p(0, 0), axes.c2p(*tip_foot()[1]), stroke_width=9, color=YELLOW)
        )
        self.play(FadeOut(vl, dashed, proj, v))
        self.add(rot_v, rot_dash, rot_proj)

        # DecimalNumber 读数 = v(t)·w = √10(cos t + 2 sin t)，
        # updater 逐帧写入；再按符号换色：正绿 / 近零黄 / 负红。
        num = DecimalNumber(5, num_decimal_places=2, font_size=32, color=GREEN)
        head = MathTex(r"\vec v\cdot\vec w =", font_size=32)
        readout = VGroup(head, num).arrange(RIGHT, buff=0.15)
        readout.next_to(note, DOWN, buff=0.4).align_to(f1, LEFT)
        num.add_updater(lambda m: m.set_value(math.sqrt(10) * (math.cos(t.get_value()) + 2 * math.sin(t.get_value()))))
        num.add_updater(lambda m: m.next_to(head, RIGHT, buff=0.15))
        num.add_updater(
            lambda m: m.set_color(
                GREEN if m.get_value() > 0.05 else RED if m.get_value() < -0.05 else YELLOW
            )
        )
        state = Text("随 v 旋转：正 → 零（垂直）→ 负", font_size=22)
        state.next_to(readout, DOWN, buff=0.3).align_to(f1, LEFT)
        self.play(FadeIn(readout), FadeIn(state))

        # 转到 -45°：途中经过 v⊥w（v·w = 0 在 t = arctan(-1/2) 处），
        # 读数恰好归零的一瞬，就是"垂直 = 点积为零"的动画证据。
        self.play(t.animate.set_value(-PI / 4), run_time=6, rate_func=linear)
        num.clear_updaters()
        self.wait(1)


class CrossProductArea(ThreeDScene):
    def construct(self) -> None:
        title = Text("叉积 = 有向面积", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # --- 2D 阶段：ThreeDScene 默认相机正对 xy 平面，当普通 Scene 用。
        # 两轴跨度 6/4 对应长度 6/4，单位一致，平行四边形不变形。
        axes = Axes(
            x_range=[-0.5, 5.5, 1], y_range=[-0.5, 3.5, 1],
            x_length=6, y_length=4, tips=False,
        ).move_to(LEFT * 3.5 + DOWN * 0.8)
        # v、w 张成的平行四边形：四点按"绕一圈"的顺序给出，
        # 高亮填充的面积就是 |v×w| = |3·2 − 1·1| = 5。
        para = Polygon(
            axes.c2p(0, 0), axes.c2p(3, 1), axes.c2p(4, 3), axes.c2p(1, 2),
            fill_color=ORANGE, fill_opacity=0.45, stroke_width=2,
        )
        v = Arrow(axes.c2p(0, 0), axes.c2p(3, 1), buff=0, color=BLUE)
        w = Arrow(axes.c2p(0, 0), axes.c2p(1, 2), buff=0, color=GREEN)
        vl = MathTex(r"\vec v=(3,1)", font_size=28, color=BLUE).next_to(v.get_end(), DOWN, buff=0.15)
        wl = MathTex(r"\vec w=(1,2)", font_size=28, color=GREEN).next_to(w.get_end(), UP, buff=0.15)
        self.play(DrawBorderThenFill(para), GrowArrow(v), GrowArrow(w), Write(vl), Write(wl))

        # 2D 叉积只有 z 分量：v_x w_y − v_y w_x，绝对值 = 上面橙色面积。
        f1 = MathTex(r"|\vec v\times\vec w|", "=", r"|v_x w_y - v_y w_x|", font_size=32)
        f2 = MathTex(r"= |3\cdot 2 - 1\cdot 1| = 5", font_size=32, color=ORANGE)
        f1.next_to(title, DOWN, buff=0.45).to_edge(RIGHT, buff=0.6)
        f2.next_to(f1, DOWN, buff=0.25).align_to(f1, RIGHT)
        note = Text("平行四边形面积 = |v×w|", font_size=26, color=ORANGE)
        note.next_to(f2, DOWN, buff=0.35).align_to(f1, LEFT)
        self.play(Write(f1), Write(f2), FadeIn(note))
        self.wait(1)

        # --- 3D 阶段：擦掉 2D 内容，把相机转出仰角，看 v×w"立"起来。
        self.play(FadeOut(axes, para, v, w, vl, wl, f1, f2, note))
        axes3 = ThreeDAxes(
            x_range=[-0.5, 4.5, 1], y_range=[-0.5, 3.5, 1], z_range=[-1, 5.5, 1],
            x_length=5, y_length=4, z_length=4, tips=False,
        ).move_to(LEFT * 2.3 + DOWN * 0.4)
        self.add(axes3)
        # phi = 与 z 轴的夹角（俯视时为 0），theta = 方位角；转出 65°
        # 后 z 轴方向才"看得见"，平行四边形呈现为一块斜面。
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, run_time=2)

        para3 = Polygon(
            axes3.c2p(0, 0, 0), axes3.c2p(3, 1, 0),
            axes3.c2p(4, 3, 0), axes3.c2p(1, 2, 0),
            fill_color=ORANGE, fill_opacity=0.5, stroke_width=2,
        )
        # 3D 箭头用 Arrow3D（圆柱杆 + 圆锥头），2D 的三角箭头在斜视角下会破。
        v3 = Arrow3D(axes3.c2p(0, 0, 0), axes3.c2p(3, 1, 0), color=BLUE)
        w3 = Arrow3D(axes3.c2p(0, 0, 0), axes3.c2p(1, 2, 0), color=GREEN)
        # 注意：Arrow3D 不是 2D Arrow，GrowArrow 会报错，登场改用 FadeIn。
        self.play(DrawBorderThenFill(para3), FadeIn(v3), FadeIn(w3))
        # v×w = (0,0,5)：方向垂直于 v、w（即平行四边形的法向量），
        # 长度恰好等于面积 5——"有向面积"这个名字的由来。
        normal = Arrow3D(axes3.c2p(0, 0, 0), axes3.c2p(0, 0, 5), color=RED)
        self.play(FadeIn(normal))

        # 固定在屏幕坐标系的文字：不随相机倾斜，任何视角都可读。
        f3 = MathTex(r"|\vec v\times\vec w| = |\vec v|\,|\vec w|\sin\theta", font_size=32)
        area = Text("大小 = 平行四边形的面积 = 5", font_size=24, color=ORANGE)
        rule = Text("右手定则：四指从 v 转向 w，拇指指向 v×w", font_size=22, color=RED)
        f3.to_edge(RIGHT, buff=0.6).shift(UP * 1.8)
        area.next_to(f3, DOWN, buff=0.3).align_to(f3, LEFT)
        rule.next_to(area, DOWN, buff=0.35).align_to(f3, LEFT)
        self.add_fixed_in_frame_mobjects(f3, area, rule)
        self.play(FadeIn(f3), FadeIn(area), FadeIn(rule))
        self.wait(2)


class GramSchmidt(Scene):
    def construct(self) -> None:
        title = Text("Gram-Schmidt 正交化：把基“掰”成直角", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 跨度 x 5 / y 4 对应长度 5 / 4，两轴单位一致，直角才画得正。
        axes = Axes(
            x_range=[-1.5, 3.5, 1], y_range=[-1, 3, 1],
            x_length=5, y_length=4, tips=False,
        ).move_to(LEFT * 3.5 + DOWN * 0.7)
        self.play(Create(axes))

        # 原始基 v1=(2,1)、v2=(1,2)：v1·v2 = 2+2 = 4 ≠ 0，明显不垂直。
        v1 = Arrow(axes.c2p(0, 0), axes.c2p(2, 1), buff=0, color=BLUE)
        v2 = Arrow(axes.c2p(0, 0), axes.c2p(1, 2), buff=0, color=RED)
        l1 = MathTex(r"\vec v_1=(2,1)", font_size=28, color=BLUE).next_to(v1.get_end(), UP, buff=0.15)
        l2 = MathTex(r"\vec v_2=(1,2)", font_size=28, color=RED).next_to(v2.get_end(), UP, buff=0.15)
        self.play(GrowArrow(v1), Write(l1), GrowArrow(v2), Write(l2))

        # 第一步：u1 = v1，第一个向量原封不动入选新基（加粗描黄）。
        u1 = Line(axes.c2p(0, 0), axes.c2p(2, 1), stroke_width=9, color=YELLOW)
        f1 = MathTex(r"\vec u_1 = \vec v_1", font_size=30, color=YELLOW)
        f1.next_to(title, DOWN, buff=0.45).to_edge(RIGHT, buff=0.6)
        self.play(Create(u1), Write(f1))

        # 第二步：把 v2 拆成"沿 u1 的投影 + 垂直部分"。
        # proj = (v2·u1 / u1·u1)·u1 = (4/5)·(2,1) = (1.6, 0.8)，
        # 其中 v2·u1 = 1·2+2·1 = 4，u1·u1 = 2²+1² = 5。
        # 投影部分画成虚线箭头——它是"将要被减掉"的分量。
        projp = DashedLine(axes.c2p(0, 0), axes.c2p(1.6, 0.8), color=ORANGE).add_tip()
        pl = MathTex(r"\mathrm{proj}", font_size=26, color=ORANGE).next_to(projp.get_end(), DOWN, buff=0.2)
        self.play(Create(projp), FadeIn(pl))

        # 垂直部分：从垂足 (1.6,0.8) 连到 v2 终点 (1,2)，加粗高亮。
        perp = Line(axes.c2p(1.6, 0.8), axes.c2p(1, 2), stroke_width=9, color=PURPLE)
        self.play(Create(perp))
        f2 = MathTex(
            r"\vec u_2 = \vec v_2 - \frac{\vec v_2\cdot\vec u_1}{\vec u_1\cdot\vec u_1}\,\vec u_1",
            font_size=28,
        )
        f2.next_to(f1, DOWN, buff=0.3).align_to(f1, LEFT)
        self.play(Write(f2))

        # 垂直段本来就是 u2，只是先前"寄存"在垂足处——平移回原点现出真身。
        # u2 = (1,2) − (1.6,0.8) = (−0.6, 1.2)。
        self.play(perp.animate.shift(axes.c2p(0, 0) - axes.c2p(1.6, 0.8)))
        u2l = MathTex(r"\vec u_2", font_size=28, color=PURPLE).next_to(perp.get_end(), UP, buff=0.15)
        self.play(FadeIn(u2l))

        # 验证 u1 ⊥ u2：u2·u1 = −0.6·2 + 1.2·1 = 0。RightAngle 在两条
        # 共点线之间画直角小方块——代数结论有了几何凭证。
        ra = RightAngle(
            Line(axes.c2p(0, 0), axes.c2p(0.5, 0.25)),
            Line(axes.c2p(0, 0), axes.c2p(-0.15, 0.3)),
            length=0.25, color=WHITE,
        )
        check = MathTex(r"\vec u_1\cdot\vec u_2 = 0", font_size=28, color=GREEN)
        check.next_to(f2, DOWN, buff=0.3).align_to(f1, LEFT)
        self.play(Create(ra), Write(check))

        # 一般公式：每来一个新 v_k，就减去它在所有已定 u_j 上的投影。
        f3 = MathTex(
            r"\vec u_k = \vec v_k - \sum_{j<k}\frac{\vec v_k\cdot\vec u_j}{\vec u_j\cdot\vec u_j}\,\vec u_j",
            font_size=28,
        )
        f3.next_to(check, DOWN, buff=0.3).align_to(f1, LEFT)
        self.play(Write(f3))

        # 收尾点题：正交基下求坐标不需要解方程组，逐个投影即可。
        benefit = Text("正交基的好处：坐标 = 逐个做投影，各分量互不干扰", font_size=24, color=GREEN)
        benefit.next_to(f3, DOWN, buff=0.35).align_to(f1, LEFT)
        self.play(FadeIn(benefit))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="点积、叉积与 Gram-Schmidt 正交化")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg", "07", [DotProductAsProjection, CrossProductArea, GramSchmidt],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
