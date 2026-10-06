"""Act01 · 行列式的诞生：从消元分母长出一个对象。

对应 mindmap Act01 的旁白。视觉主线：
    方程组 → 消元 → 同一个分母反复出现 → 它是"唯一解"的开关
    → 把它单独拿出来 → 推广到三元（莱布尼茨结构）→ 克拉默记号
    → 命名史 → 遗留问题（0=c 还是自由方向？）

坑位备忘（写后续幕时同样适用）：
    - MathTex 里禁止出现中文字符（latex 编不过），中文一律用 Text；
    - 不按数字下标切 MathTex 子串，需要高亮某段就把那段拆成独立的
      tex 参数（每个参数 = 一个子 mobject），或用 tex_to_color_map。
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
    C_SUB,
    C_TEXT,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, panel


class Act01Birth(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 01", "行列式的诞生")

        # ---- 1. 方程组登场 ----------------------------------------------
        self.say("先看最小的非平凡例子——两个未知数、两条线性方程。")
        system = MathTex(
            r"\begin{cases}ax+by=e\\[2pt]cx+dy=f\end{cases}",
            font_size=48,
        )
        system_box = SurroundingRectangle(system, color=C_MAIN, buff=0.3, corner_radius=0.1)
        system_grp = VGroup(system, system_box).move_to(STAGE_CENTER + UP * 0.2)
        self.play(Write(system), Create(system_box), run_time=1.6)
        self.hold()

        # ---- 2. 消元：同一个分母反复出现 ---------------------------------
        self.say("消元时，未知数前面会出现同一个组合 ad−bc——它在 x 和 y 的表达式里各出现一次。")
        solved = MathTex(
            r"x=\dfrac{de-bf}{ad-bc},\qquad y=\dfrac{af-ce}{ad-bc}",
            font_size=44,
            tex_to_color_map={r"ad-bc": C_HL},
        ).move_to(STAGE_CENTER + DOWN * 0.9)
        system_grp.generate_target()
        system_grp.target.scale(0.8).to_edge(UP, buff=1.15)
        self.play(MoveToTarget(system_grp), Write(solved), run_time=2.0)
        self.play(Circumscribe(solved, color=C_HL, run_time=1.0))
        self.hold()

        # ---- 3. 它是开关：两条直线的两种命运 -----------------------------
        self.say(
            "它不是某一步偶然留下的算术垃圾：当它等于零时，两条方程的方向发生了塌缩，唯一解可能消失；"
            "当它不等于零时，消元才能顺利进行。"
        )
        axes = Axes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=6.2,
            y_length=4.0,
            axis_config={"stroke_color": C_DIM, "stroke_width": 1.5, "include_ticks": False},
        ).move_to(STAGE_CENTER + UP * 0.1)
        # ad-bc != 0：两线相交
        l1 = axes.plot(lambda t: 0.6 * t + 0.4, color=C_MAIN, stroke_width=3.5)
        l2 = axes.plot(lambda t: -0.8 * t - 0.6, color=C_POS, stroke_width=3.5)
        inter = axes.c2p(0.4 / 1.4, 0.6 * 0.4 / 1.4 + 0.4)
        dot = Dot(inter, color=C_HL, radius=0.09)
        tag_ok = Text("ad−bc ≠ 0：交于一点", font=FONT, font_size=26, color=C_POS)
        tag_ok.to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.play(FadeOut(solved), run_time=0.5)
        self.play(Create(axes), Create(l1), Create(l2), run_time=1.4)
        self.play(FadeIn(tag_ok, shift=LEFT * 0.3), GrowFromCenter(dot), run_time=0.8)
        self.hold()
        # ad-bc == 0：平行
        l3 = axes.plot(lambda t: 0.6 * t + 1.6, color=C_NEG, stroke_width=3.5)
        tag_bad = Text("ad−bc = 0：方向塌缩", font=FONT, font_size=26, color=C_NEG)
        tag_bad.next_to(tag_ok, DOWN, buff=0.45)
        self.play(Transform(l2, l3), run_time=1.2)
        self.play(FadeOut(dot), FadeIn(tag_bad, shift=LEFT * 0.3), run_time=0.7)
        self.hold()
        self.play(
            *[FadeOut(m) for m in (axes, l1, l2, tag_ok, tag_bad, system_grp)],
            run_time=0.6,
        )

        # ---- 4. 把它单独拿出来 -------------------------------------------
        self.say(
            "于是第一个问题出现了：这个反复出现的组合，能不能被单独拿出来研究？"
            "它似乎在消元之前，就已经在提示方程组解的情况。"
        )
        det = MathTex(
            r"D", r"=\begin{vmatrix}a&b\\c&d\end{vmatrix}=ad-bc",
            font_size=52,
        ).move_to(STAGE_CENTER + UP * 0.2)
        det[0].set_color(C_HL)
        name = Text("给它一个名字：行列式", font=FONT, font_size=30, color=C_HL)
        name.next_to(det, DOWN, buff=0.6)
        self.play(Write(det), run_time=1.6)
        self.play(Circumscribe(det[0], color=C_HL, run_time=0.9), FadeIn(name, shift=UP * 0.3))
        self.hold()
        self.play(FadeOut(det), FadeOut(name), run_time=0.5)

        # ---- 5. 推广到三元 ------------------------------------------------
        self.say("推广到三个未知数，分母不再只有两项，而是许多项的加减组合。")
        det3_mat = MathTex(
            r"\begin{vmatrix}a_{11}&a_{12}&a_{13}\\a_{21}&a_{22}&a_{23}\\a_{31}&a_{32}&a_{33}\end{vmatrix}",
            font_size=46,
        )
        det3_pos = MathTex(
            r"a_{11}a_{22}a_{33}", r"+", r"a_{12}a_{23}a_{31}", r"+", r"a_{13}a_{21}a_{32}",
            font_size=36,
        )
        det3_neg = MathTex(
            r"-", r"a_{11}a_{23}a_{32}", r"-", r"a_{12}a_{21}a_{33}", r"-", r"a_{13}a_{22}a_{31}",
            font_size=36,
        )
        det3_pos.next_to(det3_mat, RIGHT, buff=0.4)
        det3_neg.next_to(det3_pos, DOWN, buff=0.25).align_to(det3_pos, LEFT)
        det3 = VGroup(det3_mat, det3_pos, det3_neg).move_to(STAGE_CENTER)
        det3_pos.set_color(C_POS)
        det3_neg.set_color(C_NEG)
        self.play(Write(det3_mat), run_time=1.2)
        self.play(Write(det3_pos), run_time=1.2)
        self.play(Write(det3_neg), run_time=1.2)
        self.hold()

        # ---- 6. 每行每列各取一个 ------------------------------------------
        self.say(
            "每一项都从每一行、每一列各取一个系数；"
            "同一组系数的不同取法，正好对应未知数下标的不同排列——一共 3! = 6 项。"
        )
        term = det3_pos[0]  # a_{11}a_{22}a_{33}（独立参数，索引可靠）
        box = SurroundingRectangle(term, color=C_HL, buff=0.08)
        perm = MathTex(r"(1,2,3)", font_size=34, color=C_HL)
        perm.next_to(box, UP, buff=0.3)
        count = Text("3! = 6 项，符号由排列决定", font=FONT, font_size=26, color=C_TEXT)
        count.to_edge(RIGHT, buff=0.7)
        self.play(det3.animate.scale(0.92), Create(box), run_time=0.9)
        self.play(FadeIn(perm, shift=DOWN * 0.2), run_time=0.5)
        self.play(FadeIn(count, shift=LEFT * 0.3), run_time=0.7)
        self.hold()
        self.play(*[FadeOut(m) for m in (det3, box, perm, count)], run_time=0.6)

        # ---- 7. 莱布尼茨结构：排列决定符号 ---------------------------------
        self.say(
            "这就是莱布尼茨公式背后的关键观察：复杂的分母并不是杂乱的乘法堆积，"
            "而是“所有排列都参与、再由排列的奇偶性决定正负号”的统一结构。"
        )
        leib = MathTex(
            r"\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\,"
            r"a_{1\sigma(1)}a_{2\sigma(2)}\cdots a_{n\sigma(n)}",
            font_size=46,
        ).move_to(STAGE_CENTER + UP * 0.3)
        sign_rule = VGroup(
            Text("偶排列 → +", font=FONT, font_size=28, color=C_POS),
            Text("奇排列 → −", font=FONT, font_size=28, color=C_NEG),
        ).arrange(RIGHT, buff=1.2).next_to(leib, DOWN, buff=0.7)
        self.play(Write(leib), run_time=2.0)
        self.play(FadeIn(sign_rule, shift=UP * 0.2), run_time=0.8)
        self.hold()
        self.play(*[FadeOut(m) for m in (leib, sign_rule)], run_time=0.5)

        # ---- 8. 克拉默公式：记号成型 ---------------------------------------
        self.say(
            "克拉默公式把这种分母关系组织成了可重复使用的记号。"
            "此时它仍然主要是求解方程组的工具，但工具已经有了自己的形状。"
        )
        cramer = MathTex(
            r"x=\dfrac{\begin{vmatrix}e&b\\f&d\end{vmatrix}}{D},\qquad"
            r" y=\dfrac{\begin{vmatrix}a&e\\c&f\end{vmatrix}}{D}",
            font_size=44,
        ).move_to(STAGE_CENTER + UP * 0.2)
        self.play(Write(cramer), run_time=2.0)
        self.hold()

        # ---- 9. 命名史：先独立成对象，再谈名字 ------------------------------
        self.say(
            "随着范德蒙德、拉普拉斯等人的工作，这个记号逐渐脱离具体的某一道方程题，"
            "成为可以独立研究的对象——范德蒙德 1772 年的消元论文，"
            "是第一个把行列式当独立对象系统处理的文本，但他并没有给它起名字。"
        )
        self.play(FadeOut(cramer), run_time=0.5)
        timeline = VGroup(
            panel("范德蒙德 1772 · 独立对象（未命名）", C_SUB),
            panel("拉普拉斯 · 按行按列展开", C_SUB),
        ).arrange(RIGHT, buff=0.8).move_to(STAGE_CENTER)
        link = Line(timeline[0].get_right(), timeline[1].get_left(), stroke_width=3, color=C_DIM)
        self.play(LaggedStart(*[FadeIn(t, scale=1.1) for t in timeline], lag_ratio=0.3), run_time=1.6)
        self.play(Create(link), run_time=0.6)
        self.hold()
        self.play(FadeOut(timeline), FadeOut(link), run_time=0.5)

        self.say(
            "至于命名：高斯 1801 年在《算术研究》里用过 determinans 一词，"
            "但说的是二次型的判别量——后来判别式的源头，并不是方程组消元里的这个分母；"
            "柯西 1812 年在不知晓高斯工作的情况下独立使用了 déterminant，"
            "后来才把这个词在现代意义上固定下来，"
            "强调的正是它对方程组解的存在与唯一性具有决定作用。"
        )
        naming = VGroup(
            card("高斯 1801", "determinans ＝ 二次型判别量，并非此分母", C_DIM),
            card("柯西 1812", "独立使用 déterminant，固定现代意义", C_HL),
        ).arrange(RIGHT, buff=0.9).move_to(STAGE_CENTER)
        self.play(LaggedStart(*[FadeIn(n, scale=1.1) for n in naming], lag_ratio=0.35), run_time=1.6)
        self.hold()
        self.play(FadeOut(naming), run_time=0.5)

        # ---- 9.5 最初的动机：把“塌不塌”提前编码 -----------------------------
        self.say(
            "行列式最初并不是为了制造一种漂亮的展开式，"
            "而是为了把“消元是否会塌掉”这件事提前编码出来。"
        )
        core = MathTex(r"ad-bc", font_size=56, color=C_HL).move_to(STAGE_CENTER + UP * 0.35)
        tags = VGroup(
            panel("= 0：塌缩风险被提前预警", C_NEG),
            panel("≠ 0：消元安全通行", C_POS),
        ).arrange(RIGHT, buff=1.0).next_to(core, DOWN, buff=0.7)
        self.play(Write(core), run_time=1.0)
        self.play(FadeIn(tags[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(tags[1], shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.play(FadeOut(core), FadeOut(tags), run_time=0.5)

        # ---- 10. 遗留问题：矛盾还是自由？ -----------------------------------
        self.say(
            "可是当 ad−bc = 0 时，消元只告诉我们唯一解的条件失效了，"
            "还没有告诉我们此时留下的是矛盾，还是一整条自由方向。"
            "于是我们必须把未知数的系数与右端的常数一起排开，"
            "继续追问哪些未知数已经被锁定，哪些还暂时没有被决定。"
        )
        aug = MathTex(
            r"\left(\begin{array}{cc|c}a&b&e\\c&d&f\end{array}\right)",
            font_size=48,
        ).move_to(STAGE_CENTER + UP * 0.5)
        self.play(Write(aug), run_time=1.6)
        self.hold()
        self.say(
            "带着这张系数与常数的对照表继续消元，我们会遇到两种不同的结果："
            "一行可能变成 0 = c 这样的矛盾，也可能留下可以自由取值的未知数。"
            "行列式只能提前提示“唯一解可能失效”，却不能独自区分这两种情况。"
        )
        outcomes = VGroup(
            panel("0 = c：矛盾 → 无解", C_NEG),
            panel("出现自由变量 → 无穷多解", C_HL),
        ).arrange(RIGHT, buff=1.1).next_to(aug, DOWN, buff=0.7)
        self.play(FadeIn(outcomes[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(outcomes[1], shift=UP * 0.3), run_time=0.7)
        self.hold()
        self.wait(0.6)
