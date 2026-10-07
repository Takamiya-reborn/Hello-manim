"""Act04 · 乘法就是变换的复合。

对应 mindmap Episode02 Act04 的旁白。视觉主线：
    x →(B) Bx →(A) (AB)x 流程图 → AB 的定义不再神秘
    → 行乘列的来源（第二台的行 × 第一台的列） → 结合律
    → 旋转/剪切顺序不可交换（两块小网格对比演示）
    → 单位矩阵 = 空动作 → 矩阵代数骨架 → 信息问题留尾。
"""

from __future__ import annotations

from manim import *

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


def lin_map(mat: np.ndarray, anchor: np.ndarray):
    """以 anchor 为锚点的线性映射（点级）。与 act03 同款。

    manim 的点坐标是 3 维 (x, y, z)，2x2 矩阵只作用于前两维，
    z 分量原样保留（置 0）。
    """
    def f(p: np.ndarray) -> np.ndarray:
        v = (p - anchor)[:2]
        w = mat @ v
        return anchor + np.array([w[0], w[1], 0.0])
    return f


def mini_plane(center: np.ndarray) -> tuple[NumberPlane, np.ndarray]:
    """并排对比用的小网格与其原点。"""
    plane = NumberPlane(
        x_range=[-2.0, 2.0, 1],
        y_range=[-1.6, 1.6, 1],
        x_length=3.8,
        y_length=3.0,
        background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.5},
        axis_config={"stroke_width": 2},
    ).move_to(center)
    return plane, np.array(plane.c2p(0, 0))


class Act04Composite(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 04", "乘法就是变换的复合")

        # ---- 1. 两台机器串起来 ---------------------------------------------
        self.say(
            "现在把两个矩阵看成两台机器：先让一组坐标通过 B，"
            "再让结果通过 A。最终动作可以写成一条流程链。"
        )
        n1 = MathTex(r"\mathbf{x}", font_size=44)
        n2 = MathTex(r"B\,\mathbf{x}", font_size=44)
        n3 = MathTex(r"A(B\,\mathbf{x})", font_size=44)
        flow = VGroup(n1, n2, n3).arrange(RIGHT, buff=1.2).move_to(STAGE_CENTER)
        if flow.width > 11:
            flow.scale(11 / flow.width)
        a1 = Arrow(n1.get_right(), n2.get_left(), buff=0.12, stroke_width=3.5, color=C_DIM)
        a2 = Arrow(n2.get_right(), n3.get_left(), buff=0.12, stroke_width=3.5, color=C_DIM)
        t1 = MathTex(r"B", font_size=36, color=C_MAIN).next_to(a1, UP, buff=0.12)
        t2 = MathTex(r"A", font_size=36, color=C_MAIN).next_to(a2, UP, buff=0.12)
        self.play(FadeIn(n1), Write(n2), Write(n3), run_time=1.2)
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(t1), FadeIn(t2), run_time=0.9)
        self.hold()

        # ---- 2. AB 的定义 ----------------------------------------------------
        self.say(
            "矩阵乘法的定义因此不再神秘：AB 就是"
            "“先 B、后 A”的复合变换。"
        )
        ab = MathTex(r"A(B\,\mathbf{x})", r"=", r"(AB)\,\mathbf{x}", font_size=52)
        ab.next_to(flow, DOWN, buff=0.7)
        ab[0].set_color(C_MAIN)
        ab[2].set_color(C_HL)
        self.play(Write(ab), run_time=1.4)
        self.play(Circumscribe(ab[2], color=C_HL, run_time=0.9))
        self.hold()
        self.play(FadeOut(ab), run_time=0.5)

        # ---- 3. 行乘列的来源 --------------------------------------------------
        self.say(
            "第一台机器改变了输入坐标，第二台机器处理的是已经改变过的结果。"
            "于是第二台机器的每一行，要和第一台机器的每一列重新配对，"
            "这正是行乘列规则的来源。"
        )
        pair = MathTex(
            r"\begin{pmatrix}\text{row of } A\end{pmatrix}",
            r"\begin{pmatrix}\text{col of } B\end{pmatrix}",
            font_size=42,
        ).move_to(STAGE_CENTER + UP * 0.5)
        pair[0].set_color(C_MAIN)
        pair[1].set_color(C_POS)
        src = Text("第二台的行 × 第一台的列", font=FONT, font_size=28, color=C_HL)
        src.next_to(pair, DOWN, buff=0.55)
        self.play(FadeOut(flow), FadeOut(a1), FadeOut(a2), FadeOut(t1), FadeOut(t2), run_time=0.5)
        self.play(Write(pair), run_time=1.2)
        self.play(FadeIn(src, shift=UP * 0.25), run_time=0.7)
        self.hold()
        self.play(FadeOut(pair), FadeOut(src), run_time=0.5)

        # ---- 4. 结合律 --------------------------------------------------------
        self.say(
            "复合带来结合律：无论先把哪两台机器合并，"
            "最终都是先做 C，再做 B，最后做 A。"
        )
        assoc = MathTex(r"(AB)C", r"=", r"A(BC)", font_size=52).move_to(STAGE_CENTER + UP * 0.5)
        assoc[0].set_color(C_MAIN)
        assoc[2].set_color(C_POS)
        chain = MathTex(
            r"\mathbf{x}",
            r"\xrightarrow{\;C\;}",
            r"C\,\mathbf{x}",
            r"\xrightarrow{\;B\;}",
            r"B(C\,\mathbf{x})",
            r"\xrightarrow{\;A\;}",
            r"A(B(C\,\mathbf{x}))",
            font_size=38,
        ).next_to(assoc, DOWN, buff=0.65)
        if chain.width > 11:
            chain.scale(11 / chain.width)
        self.play(Write(assoc), run_time=1.2)
        self.play(Write(chain), run_time=1.6)
        self.hold()
        self.play(FadeOut(assoc), FadeOut(chain), run_time=0.5)

        # ---- 5. 顺序不可交换：旋转 vs 剪切 -------------------------------------
        self.say(
            "但复合通常不能交换：先旋转再剪切，与先剪切再旋转，"
            "得到的网格形状一般不同。AB ≠ BA 不是需要修正的麻烦，"
            "而是矩阵在提醒我们：动作是有顺序的。"
        )
        plane_l, o_l = mini_plane(STAGE_CENTER + LEFT * 3.4)
        plane_r, o_r = mini_plane(STAGE_CENTER + RIGHT * 3.4)
        tag_l = Text("先旋转 → 再剪切", font=FONT, font_size=24, color=C_MAIN)
        tag_r = Text("先剪切 → 再旋转", font=FONT, font_size=24, color=C_POS)
        tag_l.next_to(plane_l, UP, buff=0.3)
        tag_r.next_to(plane_r, UP, buff=0.3)
        self.play(Create(plane_l), Create(plane_r), FadeIn(tag_l), FadeIn(tag_r), run_time=1.2)
        theta = 40 * DEGREES
        R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
        S = np.array([[1.0, 1.0], [0.0, 1.0]])
        # 左：先 R 后 S；右：先 S 后 R——同样的两个动作，顺序不同。
        self.play(
            ApplyPointwiseFunction(lin_map(R, o_l), plane_l),
            ApplyPointwiseFunction(lin_map(S, o_r), plane_r),
            run_time=1.4,
        )
        self.play(
            ApplyPointwiseFunction(lin_map(S, o_l), plane_l),
            ApplyPointwiseFunction(lin_map(R, o_r), plane_r),
            run_time=1.4,
        )
        diff = Text("结果不同：顺序被写进了形状", font=FONT, font_size=26, color=C_NEG)
        diff.move_to(STAGE_CENTER + DOWN * 1.9)
        self.play(FadeIn(diff, shift=UP * 0.25), run_time=0.8)
        self.hold()
        self.play(
            FadeOut(plane_l), FadeOut(plane_r), FadeOut(tag_l), FadeOut(tag_r), FadeOut(diff),
            run_time=0.6,
        )

        # ---- 6. 单位矩阵：空动作 ----------------------------------------------
        self.say(
            "单位矩阵 I 表示什么都不做。它像复合系统中的“空动作”。"
        )
        ident = MathTex(r"I\,\mathbf{x}=\mathbf{x},\qquad AI=IA=A", font_size=48)
        ident.move_to(STAGE_CENTER)
        self.play(Write(ident), run_time=1.5)
        self.hold()

        # ---- 7. 矩阵代数的骨架 -------------------------------------------------
        self.say(
            "到这里，矩阵代数的骨架已经出现：加法表示叠加，"
            "数乘表示统一缩放，乘法表示复合，单位矩阵表示不变。"
        )
        skeleton = VGroup(
            panel("加法 ＝ 叠加", C_MAIN),
            panel("数乘 ＝ 缩放", C_MAIN),
            panel("乘法 ＝ 复合", C_HL),
            panel("I ＝ 不变", C_POS),
        ).arrange(RIGHT, buff=0.55).move_to(STAGE_CENTER)
        if skeleton.width > 12:
            skeleton.scale(12 / skeleton.width)
        self.play(FadeOut(ident), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, scale=1.08) for p in skeleton], lag_ratio=0.2), run_time=1.6)
        self.hold()

        # ---- 8. 留尾：复合中的信息丢失 ------------------------------------------
        self.say(
            "复合的每一步都可能丢掉一些输入信息：先做哪一个动作、后做哪一个动作，"
            "可能决定最后还能不能区分原来的输入。"
            "这个信息问题会在后面用更精确的空间语言重新描述。"
        )
        self.play(Circumscribe(skeleton[2], color=C_HL, run_time=1.1))
        self.hold()
        self.wait(0.6)
