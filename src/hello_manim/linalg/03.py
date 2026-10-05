"""第 3 课：矩阵乘法——变换的复合与顺序。

本课要回答三个问题：
    1. "先做一个变换、再做另一个"，为什么恰好等于矩阵相乘？
    2. 乘积矩阵的每一列代表什么？
    3. 为什么 AB ≠ BA（一般而言），(AB)C = A(BC) 却永远成立？

原理速览：
    数学原理：
      - 复合：先作用 M₁、再作用 M₂，对向量 v 的净效果是
        M₂(M₁v) = (M₂M₁)v——矩阵从左往右写，作用顺序却要从
        右往左读，这就是"矩阵乘法 = 变换的复合"；
      - 乘积的列：M₂M₁ 的第 j 列 = M₂(M₁e_j)，即第 j 个基向量
        走完两步后的最终落点——所以"盯住 î、ĵ 去哪"就能验证乘积；
      - 顺序：取 A = 旋转 90°、B = 剪切，则 BA 的 î 落在 (1,1)、
        AB 的 î 落在 (0,1)——两种顺序结果不同，故一般 AB ≠ BA；
      - 结合律：(AB)Cv 与 A(BC)v 都等于 A(B(Cv))——都是"从右
        往左依次应用 C、B、A"，括号只是打包方式，不改变最终复合。
    manim 手段：
      - NumberPlane.animate.apply_matrix(M) 让整张网格连续变形；
        网格被移到画面半边时必须传 about_point，把变换中心钉在
        该网格自己的原点上（否则会围绕屏幕中心"甩"出去）；
      - Arrow 从原点指向 (1,0)/(0,1) 充当基向量"探针"，标签用
        updater 每帧贴住箭头尖端，省去每步手动挪位；
      - 公式一律 MathTex（raw string + bmatrix），中文用 Text，
        布局全交给 to_edge / next_to / to_corner。

最短运行：
    uv run hello-manim linalg 03

也可以用 manim 原生命令行渲染同一课的各个场景：
    uv run manim -pql src/hello_manim/linalg/03.py Composition
    uv run manim -pql src/hello_manim/linalg/03.py OrderMatters
    uv run manim -pql src/hello_manim/linalg/03.py Associativity
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson

# 本课反复用到的两个矩阵（约定全程不变）：
# A = 逆时针旋转 90°，B = 水平剪切（x += y）。
A = [[0, -1], [1, 0]]
B = [[1, 1], [0, 1]]


class Composition(Scene):
    def construct(self) -> None:
        # 标题钉在上缘：to_edge 相对画面边缘定位，保证不与内容重叠。
        title = Text("矩阵乘法 = 变换的复合", font_size=34)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # NumberPlane 满幅铺开且中心就是 manim 原点：apply_matrix 默认
        # 围绕原点变形，网格居中时基向量的落点一眼可见，无需平移。
        # background_line_style 调淡网格线，给上层公式让出对比度。
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.4})

        # Arrow(buff=0) 让尖端精确落在终点上（默认会往回缩一点）。
        # î、ĵ 是线性变换的"探针"：看它们去哪，就知道矩阵干了什么。
        i_arrow = Arrow(ORIGIN, RIGHT, buff=0, color=YELLOW, stroke_width=6)
        j_arrow = Arrow(ORIGIN, UP, buff=0, color=PINK, stroke_width=6)
        i_lab = MathTex(r"\hat{i}", color=YELLOW, font_size=34)
        j_lab = MathTex(r"\hat{j}", color=PINK, font_size=34)
        # updater：每一帧把标签重新贴到箭头尖端旁。之后箭头被矩阵
        # 连续变形时标签自动跟随，不必在每个 play() 后手动挪。
        i_lab.add_updater(lambda m: m.next_to(i_arrow.get_end(), DOWN, buff=0.15))
        j_lab.add_updater(lambda m: m.next_to(j_arrow.get_end(), LEFT, buff=0.15))
        self.play(Create(plane), run_time=2)
        self.play(GrowArrow(i_arrow), GrowArrow(j_arrow), FadeIn(i_lab), FadeIn(j_lab))

        # 右侧公式列：M₁ 即 A（旋转），M₂ 即 B（剪切）。数学约定矩阵
        # 左乘列向量，所以"先 M₁ 后 M₂"写出来就是乘积 M₂M₁。
        f1 = MathTex(r"M_1 = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}", font_size=34)
        f2 = MathTex(r"M_2 = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}", font_size=34)
        f1.next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)
        f2.next_to(f1, DOWN, buff=0.45)
        self.play(Write(f1), Write(f2))

        # 两步接力各配一条左上角字幕，观众始终知道演到哪一步。
        # apply_matrix 对网格每一点左乘矩阵（列向量约定）；animate 版
        # 只描述起点与终点，中间帧的"连续变形"交给 manim 插值。
        cap = None
        for txt, M in (("第 1 步：旋转 90°", A), ("第 2 步：剪切（x += y）", B)):
            new_cap = Text(txt, font_size=24, color=BLUE)
            new_cap.to_edge(LEFT, buff=0.4).shift(UP * 2.3)
            self.play(
                plane.animate.apply_matrix(M),
                i_arrow.animate.apply_matrix(M),
                j_arrow.animate.apply_matrix(M),
                *(FadeOut(cap), FadeIn(new_cap)) if cap else (FadeIn(new_cap),),
                run_time=2,
            )
            cap = new_cap
            self.wait(0.5)

        # 乘积矩阵亮出来。手算验证：B@A 的两列恰是 î、ĵ 此刻的
        # 落点 (1,1) 与 (-1,0)——"乘积的列 = 基向量的最终落点"。
        f3 = MathTex(r"M_2 M_1 = \begin{bmatrix} 1 & -1 \\ 1 & 0 \end{bmatrix}", font_size=34)
        f3.next_to(f2, DOWN, buff=0.45)
        note = Text("两列 = î、ĵ 的最终落点", font_size=20, color=GREEN)
        note.next_to(f3, DOWN, buff=0.25)
        self.play(Write(f3), FadeIn(note))
        self.wait(1)

        # 验证"一步到位"：清场重建原始网格，直接左乘乘积矩阵。
        # clear_updaters 必须先于 FadeOut：否则标签在消失途中还会
        # 执行"贴箭头"的更新逻辑，产生不必要的抖动。
        for m in (i_lab, j_lab):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in (plane, i_arrow, j_arrow, i_lab, j_lab, cap)])

        # 重建探针（与开场完全相同的构造参数），一步 apply_matrix。
        plane2 = NumberPlane(background_line_style={"stroke_opacity": 0.4})
        i2 = Arrow(ORIGIN, RIGHT, buff=0, color=YELLOW, stroke_width=6)
        j2 = Arrow(ORIGIN, UP, buff=0, color=PINK, stroke_width=6)
        cap3 = Text("一步到位：左乘乘积矩阵", font_size=24, color=BLUE)
        cap3.to_edge(LEFT, buff=0.4).shift(UP * 2.3)
        self.play(Create(plane2), GrowArrow(i2), GrowArrow(j2), FadeIn(cap3))

        # 乘积 [[1,-1],[1,0]] 恰为 B@A：一步作用的最终形态与两步
        # 接力完全相同——这就是"乘积矩阵 = 复合变换"的直观验证。
        P = [[1, -1], [1, 0]]
        self.play(
            plane2.animate.apply_matrix(P),
            i2.animate.apply_matrix(P),
            j2.animate.apply_matrix(P),
            run_time=2,
        )
        # 只作用一次，标签无需 updater：play 结束后按最终位置静态摆放。
        i_lab2 = MathTex(r"\hat{i}", color=YELLOW, font_size=34)
        j_lab2 = MathTex(r"\hat{j}", color=PINK, font_size=34)
        i_lab2.next_to(i2.get_end(), DOWN, buff=0.15)
        j_lab2.next_to(j2.get_end(), LEFT, buff=0.15)
        bot = Text("最终形态与两步接力完全相同", font_size=22, color=GREEN)
        bot.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(i_lab2), FadeIn(j_lab2), FadeIn(bot))
        self.wait(2)


class OrderMatters(Scene):
    def construct(self) -> None:
        title = Text("顺序很重要：先旋转后剪切 ≠ 先剪切后旋转", font_size=30)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 两边实验台共用同一套矩阵：A = 旋转 90°，B = 剪切。
        defs = MathTex(
            r"A = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}", r"\qquad",
            r"B = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}", font_size=28,
        )
        defs.next_to(title, DOWN, buff=0.25)
        self.play(Write(defs))

        # 坑：apply_matrix 默认围绕 manim 原点变形，网格被移到画面
        # 半边后旋转会整体"甩"出画面——必须用 about_point 把变换
        # 中心钉在各自网格自己的原点上。
        ops = (LEFT * 3.5 + DOWN * 0.5, RIGHT * 3.5 + DOWN * 0.5)
        planes, arrow_pairs, label_pairs = [], [], []
        for op in ops:
            # x_length/y_length 与范围匹配：6 格跨 6 个屏幕单位，
            # 于是网格 1 格 = 1 个坐标单位，箭头长度 1 正好对齐。
            plane = NumberPlane(
                x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                x_length=6, y_length=3.6,
                background_line_style={"stroke_opacity": 0.5},
            ).shift(op)
            pair = [
                Arrow(op, op + RIGHT, buff=0, color=YELLOW, stroke_width=5),
                Arrow(op, op + UP, buff=0, color=PINK, stroke_width=5),
            ]
            labels = [
                MathTex(r"\hat{i}", color=YELLOW, font_size=28),
                MathTex(r"\hat{j}", color=PINK, font_size=28),
            ]
            # 闭包陷阱：lambda 捕获的是变量本身，循环里四个标签会
            # 共享最后一个箭头——用默认参数 a=... 把当前箭头"冻"进去。
            labels[0].add_updater(lambda m, a=pair[0]: m.next_to(a.get_end(), DOWN, buff=0.12))
            labels[1].add_updater(lambda m, a=pair[1]: m.next_to(a.get_end(), LEFT, buff=0.12))
            planes.append(plane)
            arrow_pairs.append(pair)
            label_pairs.append(labels)
        self.play(Create(planes[0]), Create(planes[1]), run_time=1.5)
        self.play(
            *[GrowArrow(a) for pair in arrow_pairs for a in pair],
            *[FadeIn(l) for labels in label_pairs for l in labels],
        )

        # 左边"先 A 后 B"（净效果 = BA），右边"先 B 后 A"（净效果 = AB）：
        # 同一个起点、同一对矩阵、同步演示——只有顺序不同。
        for first, second in ((A, B), (B, A)):
            self.play(
                planes[0].animate.apply_matrix(first, about_point=ops[0]),
                *[a.animate.apply_matrix(first, about_point=ops[0]) for a in arrow_pairs[0]],
                planes[1].animate.apply_matrix(second, about_point=ops[1]),
                *[a.animate.apply_matrix(second, about_point=ops[1]) for a in arrow_pairs[1]],
                run_time=2,
            )

        # 反例的核心：左边 î 落在 (1,1)，右边 î 落在 (0,1)——
        # 顺序不同，同一个基向量的最终落点就不同。
        self.play(
            Indicate(arrow_pairs[0][0], color=YELLOW),
            Indicate(arrow_pairs[1][0], color=YELLOW),
        )

        # 各自的总结字幕：文字说明步骤，公式给出对应的净矩阵。
        cap_l = VGroup(
            Text("先旋转 A，后剪切 B", font_size=22),
            MathTex(r"= B\,A", font_size=30),
        ).arrange(DOWN, buff=0.1).next_to(planes[0], DOWN, buff=0.2)
        cap_r = VGroup(
            Text("先剪切 B，后旋转 A", font_size=22),
            MathTex(r"= A\,B", font_size=30),
        ).arrange(DOWN, buff=0.1).next_to(planes[1], DOWN, buff=0.2)
        self.play(FadeIn(cap_l), FadeIn(cap_r))

        # 结论公式：把 ≠ 单独标红，视觉焦点落在"不相等"上。
        concl = MathTex(r"A\,B", r"\neq", r"B\,A", font_size=56)
        concl[1].set_color(RED)
        concl.to_edge(DOWN, buff=0.3)
        tag = Text("（一般而言；个别特殊矩阵才可交换）", font_size=18, color=GREY)
        tag.next_to(concl, RIGHT, buff=0.35)
        self.play(Write(concl), FadeIn(tag))
        self.wait(2)


class Associativity(Scene):
    def construct(self) -> None:
        title = Text("结合律：(AB)C = A(BC)", font_size=34)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 主角公式。拆成子串是为了稍后 TransformMatchingTex 能按
        # token 配对：相同的部分原地保留，只动真正变化的部分。
        eq1 = MathTex(r"(A\,B)\,C", r"=", r"A\,", r"(B\,C)", font_size=56)
        eq1.next_to(title, DOWN, buff=0.7)
        self.play(Write(eq1))

        # 结合律的直觉：不管括号怎么加，读法都是同一个——从右往左
        # 依次应用 C、B、A。括号只决定"谁和谁先打包成一步"。
        why = Text("两种读法是同一个：从右往左依次应用 C、B、A", font_size=24, color=GREY)
        why.next_to(eq1, DOWN, buff=0.45)
        self.play(FadeIn(why))

        # 三步流程示意：v 先经 C、再经 B、最后经 A——与公式"从右
        # 往左"的读法一一对应。SurroundingRectangle 给矩阵画框。
        chain = VGroup(MathTex("v", font_size=40))
        prev = chain[0]
        for s in ("C", "B", "A"):
            arrow = Arrow(ORIGIN, RIGHT, buff=0, stroke_width=4, color=BLUE)
            arrow.next_to(prev, RIGHT, buff=0.3)
            sym = MathTex(s, font_size=36, color=YELLOW)
            sym.next_to(arrow, RIGHT, buff=0.3)
            chain.add(arrow, sym, SurroundingRectangle(sym, color=BLUE, buff=0.15))
            prev = sym
        chain.move_to(DOWN * 1.9)
        # 先长出三个箭头（chain[1]/[4]/[7]），再浮现字母和方框。
        self.play(*[GrowArrow(chain[i]) for i in (1, 4, 7)])
        self.play(*[FadeIn(chain[i]) for i in (2, 3, 5, 6, 8, 9)])

        # 按 C → B → A 依次高亮方框：应用从表达式最右端开始。
        # LaggedStart 让三个 Indicate 依次错开，节奏对应"接力"。
        self.play(LaggedStart(
            *[Indicate(VGroup(chain[i], chain[i + 1])) for i in (2, 5, 8)],
            lag_ratio=0.7,
        ))

        # 补上"不加分组的写法"：三者相等。TransformMatchingTex 按
        # token 配对渐变，A、B、C 原地保留，只有括号在消失/移动。
        eq2 = MathTex(r"(A\,B)\,C", r"=", r"A\,", r"(B\,C)", r"=", r"A\,B\,C", font_size=56)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="矩阵乘法：变换的复合、顺序与结合律")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "03",
        [Composition, OrderMatters, Associativity],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
