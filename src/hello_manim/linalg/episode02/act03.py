"""Act03 · 只看两列，就能看见整个变换。

对应 mindmap Episode02 Act03 的旁白。本幕是全集的几何核心：
    无穷多输入要都试一遍？ → 任意输入 = x·e₁ + y·e₂
    → 矩阵的列 = 基本输入的落点 → 网格整体变形演示
    （示例矩阵 A=[[2,1],[1,2]]，列 (2,1) 与 (1,2)）
    → 两列共线时整张平面塌成一条线（B=[[1,1],[1,1]]）。

实现要点：
    - 线性映射动画统一用 ApplyPointwiseFunction、以网格原点为锚点，
      避免 ApplyMatrix 默认绕屏面原点、把居中放置的平面带跑；
    - 网格与基箭头从登场起就按最终版式（网格偏左、矩阵在右）摆放，
      中途不做缩放搬移，箭头落点不需要重算；
    - MathTex 高亮某段必须拆成独立 tex 参数（单参数字符串按下标
      切子 mobject 不可靠）。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import C_DIM, C_HL, C_MAIN, C_NEG, FONT, STAGE_CENTER
from hello_manim.utils.widgets import panel


def lin_apply2(mat: np.ndarray, anchor: np.ndarray, p: np.ndarray) -> np.ndarray:
    """对网格坐标点 p 施加 2x2 线性映射（锚点 anchor，返回 3 维点）。"""
    w = mat @ (np.array(p)[:2] - anchor[:2])
    return anchor + np.array([w[0], w[1], 0.0])


def lin_map(mat: np.ndarray, anchor: np.ndarray):
    """以 anchor 为锚点的线性映射（点级）。

    manim 的点坐标是 3 维 (x, y, z)，2x2 矩阵只作用于前两维，
    z 分量原样保留（置 0）。
    """
    def f(p: np.ndarray) -> np.ndarray:
        v = (p - anchor)[:2]
        w = mat @ v
        return anchor + np.array([w[0], w[1], 0.0])
    return f


def make_plane(center: np.ndarray = STAGE_CENTER + LEFT * 1.9) -> tuple[NumberPlane, np.ndarray]:
    """标准演示网格与它的原点坐标（c2p(0,0)，即线性映射的锚点）。"""
    plane = NumberPlane(
        x_range=[-2.6, 2.6, 1],
        y_range=[-2.0, 2.0, 1],
        x_length=4.8,
        y_length=3.7,
        background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.5},
        axis_config={"stroke_width": 2},
    ).move_to(center)
    return plane, np.array(plane.c2p(0, 0))


class Act03Columns(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 03", "只看两列，就能看见整个变换")

        # ---- 1. 无穷多输入，都要试一遍？ -----------------------------------
        self.say(
            "一个变换作用于无穷多组坐标，难道需要把每一组输入都试一遍，"
            "才能知道它是什么样子吗？"
        )
        dots = VGroup(
            *[
                Dot(LEFT * 3.6 + RIGHT * i * 0.75 + UP * j * 0.7, radius=0.05, color=C_DIM)
                for i in range(10)
                for j in range(5)
            ]
        ).move_to(STAGE_CENTER)
        q = Text("无穷多组输入，都要试一遍？", font=FONT, font_size=32, color=C_HL)
        q.next_to(dots, DOWN, buff=0.5)
        self.play(FadeIn(dots, lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(q, shift=UP * 0.25), run_time=0.7)
        self.hold()
        self.play(FadeOut(dots), FadeOut(q), run_time=0.5)

        # ---- 2. 任意输入 = 两组基本坐标的组合 -------------------------------
        self.say(
            "不需要。对二维坐标来说，任意输入都可以写成"
            "两组最基本坐标的组合。"
        )
        decomp = MathTex(
            r"\begin{pmatrix}x\\y\end{pmatrix}"
            r"=x\begin{pmatrix}1\\0\end{pmatrix}"
            r"+y\begin{pmatrix}0\\1\end{pmatrix}",
            font_size=46,
        ).move_to(STAGE_CENTER)
        self.play(Write(decomp), run_time=1.8)
        self.hold()
        self.play(FadeOut(decomp), run_time=0.5)

        # ---- 3. 两组基本输入登场 -------------------------------------------
        self.say(
            "只要知道这两组基本坐标经过变换后得到什么，"
            "就能利用线性性推出它对任意输入的作用。"
        )
        plane, o = make_plane()
        e1 = Arrow(o, plane.c2p(1, 0), buff=0, color=C_MAIN, stroke_width=5)
        e2 = Arrow(o, plane.c2p(0, 1), buff=0, color=C_HL, stroke_width=5)
        l1 = MathTex(r"\mathbf{e}_1", font_size=34, color=C_MAIN).next_to(plane.c2p(1, 0), DR, buff=0.12)
        l2 = MathTex(r"\mathbf{e}_2", font_size=34, color=C_HL).next_to(plane.c2p(0, 1), UL, buff=0.12)
        self.play(Create(plane), run_time=1.2)
        self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.hold()

        # ---- 4. 矩阵的列 = 基本输入的落点 ------------------------------------
        self.say(
            "对矩阵 A 来说，第一列记录第一组基本输入的输出，"
            "第二列记录第二组基本输入的输出。矩阵的列不是排版上的竖条，"
            "而是两种基本输入经过变换后的落点。"
        )
        Amat = MathTex(
            r"A=\begin{pmatrix}",
            r"2", r"&", r"1", r"\\",
            r"1", r"&", r"2",
            r"\end{pmatrix}",
            font_size=44,
        )
        Amat[1].set_color(C_MAIN)  # (1,1)
        Amat[5].set_color(C_MAIN)  # (2,1)
        Amat[3].set_color(C_HL)    # (1,2)
        Amat[7].set_color(C_HL)    # (2,2)
        Amat.next_to(plane, RIGHT, buff=0.8)
        note1 = Text("第一列 ＝ 第 1 组基本输入的落点", font=FONT, font_size=24, color=C_MAIN)
        note2 = Text("第二列 ＝ 第 2 组基本输入的落点", font=FONT, font_size=24, color=C_HL)
        notes = VGroup(note1, note2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        notes.next_to(Amat, DOWN, buff=0.5).align_to(Amat, LEFT)
        self.play(FadeIn(Amat, shift=LEFT * 0.4), run_time=0.9)
        self.play(FadeIn(note1, shift=UP * 0.25), run_time=0.7)
        self.play(FadeIn(note2, shift=UP * 0.25), run_time=0.7)
        self.hold()

        # ---- 5. 变换整张网格 -------------------------------------------------
        self.say(
            "输入坐标原本如何由两种基本输入拼出来，"
            "输出坐标就如何由两列重新拼出来。"
        )
        formula = MathTex(
            r"A\begin{pmatrix}x\\y\end{pmatrix}",
            r"=",
            r"x\begin{pmatrix}2\\1\end{pmatrix}",
            r"+",
            r"y\begin{pmatrix}1\\2\end{pmatrix}",
            font_size=36,
        )
        formula[2].set_color(C_MAIN)
        formula[4].set_color(C_HL)
        # 右上角贴角摆放：居中的话会与"第 2 列"标签（箭头终点上方）同高打架。
        formula.to_corner(UR, buff=0.6)
        self.play(FadeOut(notes), Write(formula), run_time=1.6)
        A = np.array([[2.0, 1.0], [1.0, 2.0]])
        # 落点必须在网格变形前取好：变形后 c2p 读到的是已变换位置，
        # 再套一次 A 会变成 A²，箭头直冲画面外。
        e1_pt = plane.c2p(1, 0)
        e2_pt = plane.c2p(0, 1)
        self.play(ApplyPointwiseFunction(lin_map(A, o), plane), run_time=2.0)
        # 基箭头换成两列：e₁ → (2,1)，e₂ → (1,2)（按锚点线性映射算落点）。
        p1 = lin_apply2(A, o, e1_pt)
        p2 = lin_apply2(A, o, e2_pt)
        c1 = Arrow(o, p1, buff=0, color=C_MAIN, stroke_width=5)
        c2 = Arrow(o, p2, buff=0, color=C_HL, stroke_width=5)
        t1 = Text("第 1 列", font=FONT, font_size=22, color=C_MAIN)
        t2 = Text("第 2 列", font=FONT, font_size=22, color=C_HL)
        t1.next_to(c1.get_end(), DOWN, buff=0.12)
        t2.next_to(c2.get_end(), UP, buff=0.12)
        self.play(
            FadeOut(e1), FadeOut(e2), FadeOut(l1), FadeOut(l2),
            GrowArrow(c1), GrowArrow(c2), FadeIn(t1), FadeIn(t2),
            run_time=1.0,
        )
        self.hold()

        # ---- 6. 最具几何意味的读法 -------------------------------------------
        self.say(
            "这给出了矩阵最具几何意味的读法：不要先盯着四个数字，"
            "而要看两种基本输入被搬到了哪里。"
            "整个平面的网格如何变形，已经被这两个落点决定了。"
        )
        self.play(Circumscribe(VGroup(c1, c2), color=C_HL, run_time=1.2))
        self.hold()

        # ---- 7. 两列共线：塌成一条线 ------------------------------------------
        self.say(
            "一旦矩阵的两列落在同一条直线上，原本二维的图形就会被压到一条线上；"
            "如果两列仍然撑起一个平面，变换就保留了二维的形状。"
            "行列式会把这种“是否塌缩”压缩成一个数，但矩阵本身保留了更完整的过程。"
        )
        self.play(
            FadeOut(plane), FadeOut(c1), FadeOut(c2), FadeOut(t1), FadeOut(t2),
            FadeOut(Amat), FadeOut(formula),
            run_time=0.6,
        )
        plane2, o2 = make_plane(STAGE_CENTER)
        f1 = Arrow(o2, plane2.c2p(1, 0), buff=0, color=C_MAIN, stroke_width=5)
        f2 = Arrow(o2, plane2.c2p(0, 1), buff=0, color=C_HL, stroke_width=5)
        self.play(Create(plane2), GrowArrow(f1), GrowArrow(f2), run_time=1.2)
        B = np.array([[1.0, 1.0], [1.0, 1.0]])
        lm = lin_map(B, o2)
        # 两支基箭头连同网格一起被压到 y=x 这条线上——不同的输入，同一个落点。
        self.play(
            ApplyPointwiseFunction(lm, plane2),
            ApplyPointwiseFunction(lm, f1),
            ApplyPointwiseFunction(lm, f2),
            run_time=1.8,
        )
        collapsed = Text("两列共线 → 平面塌成一条线", font=FONT, font_size=28, color=C_NEG)
        collapsed.to_edge(UP, buff=0.75)
        self.play(FadeOut(f1), FadeOut(f2), FadeIn(collapsed, shift=DOWN * 0.25), run_time=0.8)
        self.hold()
        # 塌缩后 plane2 的边界框退化为对角线本身（下探到 y≈-3.5），
        # next_to(plane2, DOWN) 会把面板压进字幕条。对角线只穿过
        # 左下与右上，右下象限是空的：竖排贴右下角、抬到字幕条上方。
        contrast = VGroup(
            panel("行列式 ＝ 塌缩开关（一个数）", C_NEG),
            panel("矩阵 ＝ 保留完整过程", C_MAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        contrast.to_corner(DR, buff=0.7).shift(UP * 1.05)
        self.play(FadeIn(contrast[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(contrast[1], shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(plane2), FadeOut(collapsed), FadeOut(contrast), run_time=0.5)

        # ---- 8. 遗留问题，暂不命名 --------------------------------------------
        self.say(
            "至于所有可能输出的集合、会被送到零的输入，"
            "以及这些对象之间的关系，现在还不必急着命名。"
            "它们会在向量和空间的语言中重新出现。"
        )
        later = Text("值域 · 核 · 及其关系——留待向量语言", font=FONT, font_size=28, color=C_DIM)
        later.move_to(STAGE_CENTER)
        self.play(FadeIn(later, shift=UP * 0.2), run_time=0.8)
        self.hold()
        self.wait(0.6)
