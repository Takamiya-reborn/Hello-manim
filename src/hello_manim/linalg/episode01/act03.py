"""Act03 · 行列式的几何意义：面积、体积与方向。

对应 mindmap Act03 的旁白。本幕用 ThreeDScene：
    前半段（平行四边形）在正面机位下进行（phi=0，看起来就是 2D），
    中段 move_camera 抬起视角看平行六面体，末段回到正面机位做总结。
这样全片 2D/3D 视觉语言统一，字幕条全程 fixed-in-frame。

视觉主线：
    面积 = 有向行列式 → 交换方向（面积不变、符号翻转）
    → 共线塌缩（= 0）→ 三维平行六面体（= 带方向体积）
    → 共面塌缩 → 回联代数：det = 0 ⇔ 方向依赖 ⇔ 唯一解失效。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.geometry import parallelepiped
from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_MAIN,
    C_NEG,
    C_POS,
    C_TEXT,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import panel


class Act03Geometry(EpisodeScene, ThreeDScene):
    def construct(self) -> None:
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)  # 正面机位 = 2D 观感
        self.act_title("Act 03", "行列式的几何意义")

        # ---- 1. 转场：行列式还在描述另一件事 -------------------------------
        self.say(
            "行列式原本为解方程服务，但它的规则似乎还在描述另一件事："
            "空间中由若干个方向共同撑起的面积与体积。"
        )
        plane = NumberPlane(
            x_range=[-0.5, 4.5, 1],
            y_range=[-0.5, 4.5, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.5},
            axis_config={"stroke_width": 2},
        ).move_to(STAGE_CENTER + DOWN * 0.1)
        self.play(Create(plane), run_time=1.4)

        # ---- 2. 平行四边形：两条方向张成的有向面积 --------------------------
        O = plane.c2p(0, 0)
        U = plane.c2p(2, 1)
        V = plane.c2p(1, 2)
        UV = plane.c2p(3, 3)
        arrow_u = Arrow(O, U, buff=0, color=C_MAIN, stroke_width=5)
        arrow_v = Arrow(O, V, buff=0, color=C_HL, stroke_width=5)
        para = Polygon(O, U, UV, V, fill_color=C_MAIN, fill_opacity=0.3, stroke_width=0)
        label_u = MathTex(r"\mathbf{u}", font_size=36, color=C_MAIN).next_to(U, RIGHT, buff=0.15)
        label_v = MathTex(r"\mathbf{v}", font_size=36, color=C_HL).next_to(V, UP, buff=0.15)
        det_label = MathTex(r"\det = 3", font_size=40, color=C_TEXT)
        det_lab_bg = det_label.to_edge(RIGHT, buff=0.8).shift(UP * 1.2)
        self.play(Create(arrow_u), Write(label_u), run_time=0.9)
        self.play(Create(arrow_v), Write(label_v), run_time=0.9)
        self.play(FadeIn(para), run_time=0.8)
        self.play(Write(det_lab_bg), run_time=0.7)
        self.say("在平面上，两条有方向的线段张成一个平行四边形——行列式给出的正是它的有向面积。")
        self.hold()

        # ---- 3. 交换顺序：面积不变，方向翻转 ---------------------------------
        self.say("交换它们的顺序，面积大小不变，但方向反转——行列式从正变负。")
        # 两支箭头互换颜色与标签，面积数值翻成负值。
        det_neg = MathTex(r"\det = -3", font_size=40, color=C_NEG).move_to(det_lab_bg)
        swap_note = Text("面积不变 · 方向反转", font=FONT, font_size=26, color=C_NEG)
        swap_note.next_to(det_lab_bg, DOWN, buff=0.5).align_to(det_lab_bg, RIGHT)
        self.play(Transform(det_lab_bg, det_neg), run_time=0.8)
        self.play(
            label_u.animate.move_to(label_v.get_center()).set_color(C_HL),
            label_v.animate.move_to(label_u.get_center()).set_color(C_MAIN),
            arrow_u.animate.set_color(C_HL),
            arrow_v.animate.set_color(C_MAIN),
            FadeIn(swap_note, shift=LEFT * 0.3),
            run_time=1.2,
        )
        self.hold()
        self.play(FadeOut(swap_note), run_time=0.4)

        # ---- 4. 共线：塌缩成线，面积归零 --------------------------------------
        self.say("如果两条线段共线，平行四边形塌成一条线——带方向的面积变成零。")
        V2 = plane.c2p(1, 0.5)  # v' = 0.5·u，正好落在 u 上
        UV2 = plane.c2p(3, 1.5)
        para_flat = Polygon(O, U, UV2, V2, fill_color=C_NEG, fill_opacity=0.3, stroke_width=0)
        arrow_v2 = Arrow(O, V2, buff=0, color=C_HL, stroke_width=5)
        det_zero = MathTex(r"\det = 0", font_size=40, color=C_NEG).move_to(det_lab_bg)
        self.play(
            Transform(arrow_v, arrow_v2),
            Transform(para, para_flat),
            label_v.animate.next_to(plane.c2p(1, 0.5), DOWN, buff=0.2),
            Transform(det_lab_bg, det_zero),
            run_time=1.4,
        )
        self.hold()
        self.play(
            *[FadeOut(m) for m in (plane, arrow_u, arrow_v, label_u, label_v, para, det_lab_bg)],
            run_time=0.6,
        )

        # ---- 5. 三维：平行六面体 = 带方向的体积 -------------------------------
        self.say(
            "在三维中，三条有方向的线段张成平行六面体。行列式给出的不只是“装了多少空间”，"
            "还记录这组方向是否保持了空间的取向。"
        )
        self.move_camera(phi=68 * DEGREES, theta=-50 * DEGREES, run_time=1.5)
        u3 = np.array([2.0, 0.0, 0.4])
        v3 = np.array([0.6, 2.0, 0.4])
        w3 = np.array([0.4, 0.6, 2.0])
        solid = parallelepiped(u3, v3, w3, C_MAIN, 0.32)
        a3 = Arrow3D(ORIGIN, u3, color=C_MAIN, thickness=0.015)
        b3 = Arrow3D(ORIGIN, v3, color=C_HL, thickness=0.015)
        c3 = Arrow3D(ORIGIN, w3, color=C_POS, thickness=0.015)
        self.play(DrawBorderThenFill(solid), run_time=1.4)
        # 注意：3D 箭头不能用 GrowArrow（其内部 scale 带 scale_tips，
        # Arrow3D 不支持），用 Create / FadeIn 登场。
        self.play(Create(a3), Create(b3), Create(c3), run_time=1.2)
        vol_label = Text("det = 有方向的体积", font=FONT, font_size=28, color=C_TEXT)
        self.fixed(vol_label)
        vol_label.to_edge(RIGHT, buff=0.6).shift(UP * 1.2)
        self.play(FadeIn(vol_label, shift=LEFT * 0.3), run_time=0.7)
        self.hold()
        self.say("三条线段一旦落在同一个平面内，体积就塌缩为零。")
        # 第三条棱倒向 u、v 张成的平面：体积消失。
        w_flat = np.array([0.4, 0.6, 0.0])
        solid_flat = parallelepiped(u3, v3, w_flat, C_NEG, 0.32)
        c3_flat = Arrow3D(ORIGIN, w_flat, color=C_POS, thickness=0.015)
        vol_zero = Text("det = 0：体积塌缩", font=FONT, font_size=28, color=C_NEG).move_to(vol_label)
        self.play(Transform(solid, solid_flat), Transform(c3, c3_flat), run_time=1.4)
        self.play(Transform(vol_label, vol_zero), run_time=0.7)
        self.hold()
        self.play(
            FadeOut(solid), FadeOut(a3), FadeOut(b3), FadeOut(c3),
            FadeOut(vol_label),
            run_time=0.6,
        )

        # ---- 6. 回联代数 ------------------------------------------------------
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=1.2)
        self.say(
            "这让前面的代数现象获得了几何解释：行列式为零，不仅意味着消元时分母消失，"
            "也意味着方向之间发生了依赖，几何图形失去了维度。"
        )
        bridge = VGroup(
            panel("消元分母消失", C_NEG),
            MathTex(r"\Longleftrightarrow", font_size=44, color=C_TEXT),
            panel("方向相互依赖", C_NEG),
            MathTex(r"\Longleftrightarrow", font_size=44, color=C_TEXT),
            panel("图形失去维度", C_NEG),
        ).arrange(RIGHT, buff=0.5).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(b, scale=1.05) for b in bridge], lag_ratio=0.25), run_time=1.6)
        self.hold()
        self.play(FadeOut(bridge), run_time=0.5)

        # ---- 7. 收束：向量的轮廓 ----------------------------------------------
        self.say(
            "行列式既在描述一组数如何决定方程组，也在描述几条有方向的线段如何共同决定面积、体积和取向。"
            "向量这个名称还没有正式登场，但它所对应的对象，已经在这些问题中露出了轮廓。"
        )
        silhouette = MathTex(r"\mathbf{u}", r",\ \mathbf{v}", r",\ \mathbf{w}", font_size=52)
        silhouette.set_color_by_tex(r"\mathbf{u}", C_MAIN)
        silhouette.set_color_by_tex(r"\mathbf{v}", C_HL)
        silhouette.set_color_by_tex(r"\mathbf{w}", C_POS)
        q = Text("它们是什么？——下一集之后见分晓", font=FONT, font_size=28, color=C_DIM)
        q.next_to(silhouette, DOWN, buff=0.6)
        self.play(Write(silhouette), run_time=1.2)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.7)
        self.hold()
        self.say(
            "此时还不必急着给这种塌缩命名。只要记住一个现象："
            "如果若干方向中有一个可以由其余方向拼出来，它们共同撑起的面积或体积就会消失。"
            "这个现象会在后面向量登场后，得到更准确的语言。"
        )
        recall = MathTex(r"\mathbf{v}=c\,\mathbf{u}\ \Longrightarrow\ \det=0", font_size=44, color=C_HL)
        self.play(FadeOut(q), FadeOut(silhouette), run_time=0.5)
        self.play(Write(recall), run_time=1.2)
        self.hold()
        self.wait(0.6)
