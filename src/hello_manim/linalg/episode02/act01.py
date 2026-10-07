"""Act01 · 把矩阵直接当作代数实体。

对应 mindmap Episode02 Act01 的旁白。视觉主线：
    凯莱 1858 → 方阵 A 记录两条依赖关系 → 加法/数乘逐项
    → 乘法必须行乘列 → 交换律失效 = 时间顺序被保存
    → 凯莱的贡献 → 分块管理 → 遗留问题（凭什么代表"线性"？）

坑位备忘：MathTex 内禁中文；高亮某段拆独立 tex 参数；
    中文引号一律全角""。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_MAIN,
    C_POS,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, panel


class Act01Algebra(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 01", "把矩阵直接当作代数实体")

        # ---- 1. 凯莱登场 --------------------------------------------------
        self.say("1858 年，凯莱发表了关于矩阵理论的论文。")
        cayley = card("凯莱 · 1858", "《矩阵理论回忆录》", C_HL).move_to(STAGE_CENTER)
        self.play(FadeIn(cayley, scale=1.1), run_time=1.0)
        self.hold()
        self.play(FadeOut(cayley), run_time=0.5)

        # ---- 2. 更直接的想法 ----------------------------------------------
        self.say(
            "他面对的不是“如何把数字排成方阵”这个初等问题，而是一个更直接的想法："
            "既然线性变换需要被记录，而变换的复合又必须有统一的写法，"
            "能不能把记录变换的这一整块数字，当作一个独立的代数实体？"
        )
        matrix = MathTex(r"A=\begin{pmatrix}a&b\\c&d\end{pmatrix}", font_size=56)
        box = SurroundingRectangle(matrix, color=C_MAIN, buff=0.3, corner_radius=0.1)
        grp = VGroup(matrix, box).move_to(STAGE_CENTER)
        self.play(Write(matrix), Create(box), run_time=1.6)
        self.hold()
        self.play(FadeOut(grp), run_time=0.5)

        # ---- 3. 记录两条依赖关系 ------------------------------------------
        self.say(
            "把一个二元线性关系写成方阵：它不再只是四个互不相干的数字，"
            "而是同时记录了两条输出如何依赖两个输入。"
        )
        m2 = MathTex(
            r"\begin{pmatrix}",
            r"a", r"&", r"b", r"\\",
            r"c", r"&", r"d",
            r"\end{pmatrix}",
            font_size=48,
        )
        m2[1].set_color(C_MAIN)  # a
        m2[3].set_color(C_MAIN)  # b
        m2[5].set_color(C_POS)   # c
        m2[7].set_color(C_POS)   # d
        row1 = MathTex(r"y_1", r"=ax+by", font_size=38, color=C_MAIN)
        row2 = MathTex(r"y_2", r"=cx+dy", font_size=38, color=C_POS)
        rows = VGroup(row1, row2).arrange(DOWN, buff=0.55)
        dep = VGroup(m2, rows).arrange(RIGHT, buff=1.1).move_to(STAGE_CENTER)
        links = VGroup(
            Line(m2.get_right() + UP * 0.4, row1.get_left() + LEFT * 0.1, stroke_width=2.5, color=C_DIM),
            Line(m2.get_right() + DOWN * 0.4, row2.get_left() + LEFT * 0.1, stroke_width=2.5, color=C_DIM),
        )
        self.play(Write(m2), run_time=1.2)
        self.play(Create(links), run_time=0.7)
        self.play(FadeIn(row1, shift=LEFT * 0.3), FadeIn(row2, shift=LEFT * 0.3), run_time=0.8)
        self.hold()
        self.play(FadeOut(dep), FadeOut(links), run_time=0.5)

        # ---- 4. 加法与数乘：逐项进行 ----------------------------------------
        self.say(
            "矩阵的加法可以逐项进行，因为两个变换的结果可以相加；"
            "数乘也可以逐项进行，因为整个变换可以统一放大或缩小。"
        )
        add = MathTex(
            r"\begin{pmatrix}a&b\\c&d\end{pmatrix}+\begin{pmatrix}e&f\\g&h\end{pmatrix}"
            r"=\begin{pmatrix}a{+}e&b{+}f\\c{+}g&d{+}h\end{pmatrix}",
            font_size=38,
        ).move_to(STAGE_CENTER + UP * 1.0)
        scale = MathTex(
            r"k\begin{pmatrix}a&b\\c&d\end{pmatrix}=\begin{pmatrix}ka&kb\\kc&kd\end{pmatrix}",
            font_size=38,
        ).move_to(STAGE_CENTER + DOWN * 0.6)
        self.play(Write(add), run_time=1.6)
        self.play(Write(scale), run_time=1.4)
        self.hold()
        self.play(FadeOut(add), FadeOut(scale), run_time=0.5)

        # ---- 5. 乘法：行与列相遇 --------------------------------------------
        self.say(
            "但矩阵乘法不能照搬普通数字的乘法。两个矩阵相乘时，"
            "第一个矩阵的一行与第二个矩阵的一列相遇，得到一个内积；"
            "这个规则恰好把“先做一次线性组合，再做另一次线性组合”"
            "压缩成了一次线性组合。"
        )
        mul = MathTex(
            r"\begin{pmatrix}a&b\\c&d\end{pmatrix}\begin{pmatrix}e&f\\g&h\end{pmatrix}"
            r"=\begin{pmatrix}ae{+}bg&af{+}bh\\ce{+}dg&cf{+}dh\end{pmatrix}",
            font_size=36,
        ).move_to(STAGE_CENTER + UP * 0.7)
        inner = MathTex(
            r"(a\ \ b)\begin{pmatrix}e\\g\end{pmatrix}=ae+bg",
            font_size=38, color=C_HL,
        ).next_to(mul, DOWN, buff=0.55)
        self.play(Write(mul), run_time=1.8)
        self.play(Write(inner), run_time=1.2)
        self.play(Circumscribe(inner, color=C_HL, run_time=0.9))
        self.hold()
        self.play(FadeOut(mul), FadeOut(inner), run_time=0.5)

        # ---- 6. 交换律失效 ---------------------------------------------------
        self.say(
            "于是一个反直觉的现象出现了：矩阵乘法一般不满足交换律。"
            "AB 表示先做 B 再做 A，而 BA 表示先做 A 再做 B；"
            "动作的顺序不同，结果当然可能不同。"
        )
        abba = MathTex(r"AB", r"\neq", r"BA", font_size=60).move_to(STAGE_CENTER + UP * 0.6)
        abba[0].set_color(C_MAIN)
        abba[2].set_color(C_POS)
        note1 = Text("AB：先 B 后 A", font=FONT, font_size=26, color=C_MAIN)
        note2 = Text("BA：先 A 后 B", font=FONT, font_size=26, color=C_POS)
        notes = VGroup(note1, note2).arrange(RIGHT, buff=1.2).next_to(abba, DOWN, buff=0.6)
        self.play(Write(abba), run_time=1.2)
        self.play(FadeIn(note1, shift=UP * 0.25), FadeIn(note2, shift=UP * 0.25), run_time=0.8)
        self.hold()

        # ---- 7. 顺序被忠实保存 -------------------------------------------------
        self.say(
            "这不是矩阵运算的缺陷，而是它忠实保存了变换的时间顺序。"
            "交换律失效，反而说明矩阵乘法正在描述真实的复合过程。"
        )
        n1 = MathTex(r"\mathbf{x}", font_size=42)
        n2 = MathTex(r"B\,\mathbf{x}", font_size=42)
        n3 = MathTex(r"(AB)\,\mathbf{x}", font_size=42)
        flow = VGroup(n1, n2, n3).arrange(RIGHT, buff=1.1).move_to(STAGE_CENTER)
        a1 = Arrow(n1.get_right(), n2.get_left(), buff=0.12, stroke_width=3, color=C_DIM)
        a2 = Arrow(n2.get_right(), n3.get_left(), buff=0.12, stroke_width=3, color=C_DIM)
        t1 = MathTex(r"B", font_size=34, color=C_MAIN).next_to(a1, UP, buff=0.12)
        t2 = MathTex(r"A", font_size=34, color=C_MAIN).next_to(a2, UP, buff=0.12)
        self.play(FadeOut(abba), FadeOut(notes), run_time=0.5)
        self.play(FadeIn(n1), FadeIn(n2), FadeIn(n3), Create(a1), Create(a2), run_time=1.2)
        self.play(Write(t1), Write(t2), run_time=0.8)
        self.hold()
        self.play(*[FadeOut(m) for m in (flow, a1, a2, t1, t2)], run_time=0.5)

        # ---- 8. 凯莱的贡献 ---------------------------------------------------
        self.say(
            "凯莱的贡献不只是给方阵规定了一套计算规则，"
            "而是允许我们把“变换的组合”当作一种新的代数运算来研究。"
            "矩阵从此拥有了不依赖具体方程题的生命。"
        )
        legacy = card("凯莱的贡献", "把“变换的组合”变成代数运算", C_HL).move_to(STAGE_CENTER)
        self.play(FadeIn(legacy, scale=1.08), run_time=1.0)
        self.hold()
        self.play(FadeOut(legacy), run_time=0.5)

        # ---- 9. 分块管理 ---------------------------------------------------
        self.say(
            "大矩阵还可以切块管理：把矩阵分成若干小块后，"
            "加法与乘法都可以按块进行，规则与数字版完全相同。"
        )
        blocks = MathTex(
            r"\left(\begin{array}{cc|cc}"
            r"A_{11} & A_{12} & 0 & 0 \\"
            r"A_{21} & A_{22} & 0 & 0 \\ \hline"
            r"0 & 0 & B_{11} & B_{12} \\"
            r"0 & 0 & B_{21} & B_{22}"
            r"\end{array}\right)",
            font_size=42,
        ).move_to(STAGE_CENTER + UP * 0.35)
        self.play(Write(blocks), run_time=1.8)
        self.hold()
        self.say(
            "分块对角的矩阵，行列式等于各对角块行列式的乘积，"
            "可逆时逆矩阵也沿对角块分别求出。"
        )
        props = VGroup(
            panel("det ＝ 各对角块行列式之积", C_POS),
            panel("逆矩阵沿对角块分别求出", C_HL),
        ).arrange(RIGHT, buff=0.9).next_to(blocks, DOWN, buff=0.5)
        self.play(FadeIn(props[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(props[1], shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(blocks), FadeOut(props), run_time=0.5)

        # ---- 10. 遗留问题 ---------------------------------------------------
        self.say(
            "但矩阵凭什么有权代表一个“线性”的变换？"
            "这个问题要先回到被变换的对象上，才能得到准确的回答。"
        )
        q = Text("矩阵凭什么代表“线性”变换？", font=FONT, font_size=36, color=C_HL)
        q.move_to(STAGE_CENTER)
        self.play(FadeIn(q, scale=1.1), run_time=0.8)
        self.play(Circumscribe(q, color=C_HL, run_time=1.0))
        self.hold()
        self.wait(0.6)
