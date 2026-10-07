"""Act06 · 逆矩阵：能不能把动作撤销。

对应 mindmap Episode02 Act06 的旁白。视觉主线：
    撤销的愿望 → A⁻¹A = AA⁻¹ = I（不是逐项取倒数）
    → 伴随矩阵恒等式与逆矩阵公式 → 可逆动作一览
    → 塌缩演示：B=[[1,1],[1,1]] 把两个不同输入送到同一落点
    → 信息一旦合并就无法恢复 → "有逆"= 信息守恒
    → det=0 ⇔ 塌缩 ⇔ 不可逆 等价链 → det≠0 的承诺。
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
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, panel


def lin_apply2(mat: np.ndarray, anchor: np.ndarray, p: np.ndarray) -> np.ndarray:
    """对网格坐标点 p 施加 2x2 线性映射（锚点 anchor，返回 3 维点）。"""
    w = mat @ (np.array(p)[:2] - anchor[:2])
    return anchor + np.array([w[0], w[1], 0.0])


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


class Act06Inverse(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 06", "逆矩阵：能不能把动作撤销")

        # ---- 1. 撤销的愿望 --------------------------------------------------
        self.say(
            "既然矩阵表示一个动作，就会自然产生一个生活化的问题："
            "一个动作做完之后，能不能完整撤销？"
        )
        undo = Text("做完之后，能完整撤销吗？", font=FONT, font_size=36, color=C_HL)
        undo.move_to(STAGE_CENTER)
        self.play(FadeIn(undo, scale=1.08), run_time=0.8)
        self.hold()
        self.play(FadeOut(undo), run_time=0.5)

        # ---- 2. 逆矩阵的定义 -------------------------------------------------
        self.say(
            "如果存在另一个矩阵 A⁻¹，使得先做 A、再做 A⁻¹ 等于什么都没做，"
            "就称 A 可逆。逆矩阵不是“把每个数字取倒数”，"
            "而是寻找一个真正能撤销原变换的动作。"
        )
        inv = MathTex(r"A^{-1}A", r"=", r"AA^{-1}", r"=", r"I", font_size=52)
        inv.move_to(STAGE_CENTER + UP * 0.4)
        inv[4].set_color(C_HL)
        note = card("不是", "把每个数字取倒数", C_NEG)
        note2 = card("而是", "寻找能撤销原变换的动作", C_POS)
        notes = VGroup(note, note2).arrange(RIGHT, buff=1.0).next_to(inv, DOWN, buff=0.6)
        self.play(Write(inv), run_time=1.5)
        self.play(FadeIn(note, shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(note2, shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(inv), FadeOut(notes), run_time=0.5)

        # ---- 3. 伴随矩阵与逆矩阵公式 -------------------------------------------
        self.say(
            "伴随矩阵 A* 由代数余子式按转置方式排列而成，"
            "天然满足 AA* = A*A = |A|I。这条恒等式一举给出逆矩阵公式，"
            "也带来伴随矩阵行列式的尺度规律。"
        )
        adj1 = MathTex(r"AA^{*}", r"=", r"A^{*}A", r"=", r"|A|\,I", font_size=44)
        adj2 = MathTex(r"A^{-1}", r"=", r"\dfrac{1}{|A|}\,A^{*}", font_size=44)
        adj3 = MathTex(r"|A^{*}|", r"=", r"|A|^{\,n-1}", font_size=44)
        adj1.move_to(STAGE_CENTER + UP * 1.1)
        adj2.next_to(adj1, DOWN, buff=0.5)
        adj3.next_to(adj2, DOWN, buff=0.5)
        adj2[2].set_color(C_HL)
        adj3[2].set_color(C_HL)
        self.play(Write(adj1), run_time=1.4)
        self.play(Write(adj2), run_time=1.2)
        self.play(Write(adj3), run_time=1.2)
        self.hold()
        self.play(FadeOut(adj1), FadeOut(adj2), FadeOut(adj3), run_time=0.5)

        # ---- 4. 可逆与不可逆的分界 ---------------------------------------------
        self.say(
            "拉伸可以被反向压缩，旋转可以被反向旋转，剪切也可以被反向剪切；"
            "但如果一个变换把整个平面压到一条直线上，"
            "两个不同的输入可能已经落到了同一个位置。"
        )
        goods = VGroup(
            panel("拉伸 → 反向压缩", C_POS),
            panel("旋转 → 反向旋转", C_POS),
            panel("剪切 → 反向剪切", C_POS),
        ).arrange(RIGHT, buff=0.55).move_to(STAGE_CENTER + UP * 0.4)
        if goods.width > 12:
            goods.scale(12 / goods.width)
        self.play(LaggedStart(*[FadeIn(g, scale=1.08) for g in goods], lag_ratio=0.25), run_time=1.4)
        self.hold()

        # 塌缩演示：B 的两列相同，e₁ 与 e₂ 被送到同一个落点。
        plane = NumberPlane(
            x_range=[-2.4, 2.4, 1],
            y_range=[-1.8, 1.8, 1],
            x_length=4.8,
            y_length=3.6,
            background_line_style={"stroke_color": C_DIM, "stroke_width": 1, "stroke_opacity": 0.5},
            axis_config={"stroke_width": 2},
        ).move_to(STAGE_CENTER + DOWN * 0.55)
        o = np.array(plane.c2p(0, 0))
        v1 = Dot(plane.c2p(1, 0), radius=0.09, color=C_MAIN)
        v2 = Dot(plane.c2p(0, 1), radius=0.09, color=C_HL)
        w1 = MathTex(r"\mathbf{e}_1", font_size=30, color=C_MAIN).next_to(v1, DOWN, buff=0.12)
        w2 = MathTex(r"\mathbf{e}_2", font_size=30, color=C_HL).next_to(v2, UL, buff=0.12)
        self.play(
            FadeOut(goods),
            Create(plane), FadeIn(v1), FadeIn(v2), FadeIn(w1), FadeIn(w2),
            run_time=1.2,
        )
        B = np.array([[1.0, 1.0], [1.0, 1.0]])
        lm = lin_map(B, o)
        self.play(
            ApplyPointwiseFunction(lm, plane),
            v1.animate.move_to(lin_apply2(B, o, plane.c2p(1, 0))),
            v2.animate.move_to(lin_apply2(B, o, plane.c2p(0, 1))),
            FadeOut(w1), FadeOut(w2),
            run_time=1.6,
        )
        same = Text("两个输入 → 同一个落点", font=FONT, font_size=26, color=C_NEG)
        same.to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
        self.play(FadeIn(same, shift=LEFT * 0.3), run_time=0.7)
        self.hold()

        # ---- 5. 信息一旦合并就无法恢复 ------------------------------------------
        self.say(
            "信息一旦被合并，就无法从结果中判断它原来来自哪里。"
            "此时不存在逆矩阵，因为没有任何动作可以凭空恢复已经丢失的方向。"
        )
        lost = Text("方向信息已丢失——撤销无从谈起", font=FONT, font_size=28, color=C_NEG)
        # 右缘对齐 same：居中跟随会撞出画面右边缘。
        lost.next_to(same, DOWN, buff=0.5).align_to(same, RIGHT)
        self.play(FadeIn(lost, shift=LEFT * 0.3), run_time=0.8)
        self.play(Circumscribe(VGroup(v1, v2), color=C_NEG, run_time=1.1))
        self.hold()
        self.play(
            FadeOut(plane), FadeOut(v1), FadeOut(v2), FadeOut(same), FadeOut(lost),
            run_time=0.6,
        )

        # ---- 6. 有逆 = 信息守恒 -------------------------------------------------
        self.say(
            "于是“有逆”不只是一个代数条件，也是一条信息守恒原则："
            "变换必须保留足够的信息，才能被完整撤回。"
        )
        conservation = panel("“有逆” ＝ 信息守恒原则", C_POS)
        conservation.move_to(STAGE_CENTER)
        self.play(FadeIn(conservation, scale=1.08), run_time=0.8)
        self.hold()
        self.play(FadeOut(conservation), run_time=0.5)

        # ---- 7. det 的等价链 ----------------------------------------------------
        self.say(
            "行列式为零时，几何上意味着面积塌缩，代数上意味着矩阵不可逆；"
            "矩阵把这个结论背后的动作保存了下来，而行列式把它提炼成了一个开关。"
        )
        chain = VGroup(
            panel("det ＝ 0", C_NEG),
            MathTex(r"\Longleftrightarrow", font_size=40, color=C_DIM),
            panel("面积塌缩", C_NEG),
            MathTex(r"\Longleftrightarrow", font_size=40, color=C_DIM),
            panel("矩阵不可逆", C_NEG),
        ).arrange(RIGHT, buff=0.45).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(c, scale=1.05) for c in chain], lag_ratio=0.25), run_time=1.6)
        self.hold()
        self.play(FadeOut(chain), run_time=0.5)

        # ---- 8. det ≠ 0 的承诺 ---------------------------------------------------
        self.say(
            "因此对方阵，行列式非零意味着这个动作不会把面积压成零，"
            "也意味着它能够被某个反向动作完整撤销。"
            "至于这种“不会丢失信息”还能用哪些方式表达，"
            "要等向量和空间的语言建立后再展开。"
        )
        promise = panel("det ≠ 0：动作可以被完整撤销", C_POS)
        promise.move_to(STAGE_CENTER)
        self.play(FadeIn(promise, scale=1.08), run_time=0.8)
        self.hold()
        self.wait(0.6)
