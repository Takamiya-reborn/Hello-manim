"""第 2 课：矩阵即线性变换——旋转、缩放、剪切与基。

本课要回答三个问题：
    1. 矩阵乘向量 Mv 到底"做"了什么？为什么说矩阵的每一列
       恰好就是基向量 î、ĵ 变换后的落点？
    2. 旋转、缩放、剪切这些常见变换，矩阵长什么样？
       怎么在网格上把它们的作用"看"出来？
    3. 同一个向量，换一组基坐标为什么就变了？
       "新坐标"和"标准坐标"之间靠哪个矩阵换算？

原理速览：
    数学原理：
      - 线性变换由它对基向量的作用完全决定：任何向量都能写成
        v = x·î + y·ĵ，而线性性保证 Mv = x·(Mî) + y·(Mĵ)。
        把 Mî、Mĵ 这两个落点按列排好，得到的正是 M 本身——
        **矩阵是空间变换的数字快照，每一列就是基向量的落点**。
      - 以 M = [[2,1],[0,1]]（剪切 + 拉伸的复合体）为例：
        î→(2,0)，ĵ→(1,1)；对 v=(-1,2) 有
        Mv = (−1)·(2,0) + 2·(1,1) = (0,2)。
        "老坐标乘矩阵 = 新位置"——箭还是那支箭，数字换了。
      - 常见变换画廊：逆时针转 90°：[[0,−1],[1,0]]（î 竖起来、
        ĵ 指向左）；等比放大 2 倍：[[2,0],[0,2]]（两根基箭头都
        变长一倍）；水平剪切：[[1,1],[0,1]]（î 不动，ĵ 被推斜）。
      - 基变换：取非标准基 b₁=(1,1)、b₂=(−1,1)。同一向量 v=(1,2)
        在标准基下坐标是 (1,2)；解 v = c₁b₁ + c₂b₂ 得 c₁=3/2、
        c₂=1/2，即新坐标 (3/2, 1/2)。把基向量按列排成的矩阵
        B = [[1,−1],[1,1]] 满足 v_标准 = B·v_B：B 是"新坐标 →
        标准坐标"的翻译官（反方向要乘 B⁻¹，即第 5 课的逆矩阵）。
    manim 手段：
      - Mobject.apply_matrix 只认 3×3 矩阵（manim 的点是 [x,y,z]
        三元组），2D 矩阵必须补齐成 [[a,b,0],[c,d,0],[0,0,1]]，
        或者改用 apply_function(lambda p: np.dot(M, p))；
      - apply_matrix 默认以原点为不动点，恰好满足"线性变换
        不动原点"的几何要求；它直接对 mobject 的全部采样点做
        矩阵乘法——对整个 NumberPlane 调一次，整张网格同步变形，
        Arrow 的箭头尖也是采样点，会精确落到 Mî、Mĵ 处；
      - 文字标签绝不能跟着做矩阵乘法（一乘就歪），用 updater
        把标签重新锚定在箭头尖端旁边（base 04 课的手法）。

最短运行：
    uv run hello-manim linalg 02

也可以用 manim 原生命令行渲染同一课的各个场景：
    uv run manim -pql src/hello_manim/linalg/02.py MatrixAsTransform
    uv run manim -pql src/hello_manim/linalg/02.py RotationAndScale
    uv run manim -pql src/hello_manim/linalg/02.py BasisChange
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


def mat3(m2: list[list[int]]) -> list[list[int]]:
    """把 2×2 矩阵补齐成 manim 要求的 3×3：第三行第三列补成 (0,0,1)。"""
    return [
        [m2[0][0], m2[0][1], 0],
        [m2[1][0], m2[1][1], 0],
        [0, 0, 1],
    ]


class MatrixAsTransform(Scene):
    def construct(self) -> None:
        # 标题只占一行；真正的主角是整张网格和基向量。
        title = Text("矩阵即线性变换", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # NumberPlane 就是"空间"本身：原点在画面中心，1 格 = 1 单位。
        # 网格线调淡让箭头当主角；范围取 [-8,8]，保证拉伸变形后仍铺满画面。
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(grid), run_time=2)

        # 标准基向量：î=(1,0) 绿、ĵ=(0,1) 红。buff=0 让箭尾精确压在原点。
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=7)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=7)
        i_label = MathTex(r"\hat{\imath}", color=GREEN).scale(0.9)
        j_label = MathTex(r"\hat{\jmath}", color=RED).scale(0.9)
        # 文字不做矩阵乘法（一乘就歪）：用 updater 把标签"钉"在
        # 箭头尖端旁边，箭头动、标签跟着走。
        i_label.add_updater(lambda m: m.next_to(i_hat.get_end(), DOWN, buff=0.15))
        j_label.add_updater(lambda m: m.next_to(j_hat.get_end(), UP, buff=0.15))
        self.play(GrowArrow(i_hat), GrowArrow(j_hat), FadeIn(i_label), FadeIn(j_label))

        # 任意示例向量 v=(-1,2)：稍后用它验证"老坐标 × M = 新位置"。
        v_vec = Arrow(ORIGIN, [-1, 2, 0], buff=0, color=YELLOW, stroke_width=7)
        v_label = MathTex(r"v=(-1,\,2)", color=YELLOW).scale(0.8)
        v_label.add_updater(lambda m: m.next_to(v_vec.get_end(), UP, buff=0.15))
        self.play(GrowArrow(v_vec), FadeIn(v_label))

        # 变换矩阵按列拆 token 上色：第一列 (2,0) 绿 = Mî 的落点，
        # 第二列 (1,1) 红 = Mĵ 的落点。这套配色贯穿全课。
        matrix_tex = MathTex(
            r"M=", r"\begin{bmatrix}",
            r"2", r"&", r"1", r"\\",
            r"0", r"&", r"1",
            r"\end{bmatrix}",
        )
        matrix_tex.set_color_by_tex("2", GREEN)
        matrix_tex.set_color_by_tex("0", GREEN)
        matrix_tex.set_color_by_tex("1", RED)
        matrix_tex.to_corner(UL, buff=0.5).shift(DOWN * 1.1)
        self.play(Write(matrix_tex))

        # 先抛出本课核心命题，再让观众亲眼看它成立。
        key_line = Text("矩阵的每一列 = 基向量变换后的落点", font_size=26, color=YELLOW)
        key_line.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(key_line))
        self.wait(1)

        # 一次 play 让"整个空间"做同一个矩阵乘法：网格 + 三根箭头。
        # M = [[2,1],[0,1]]：î 被拉长到 (2,0)，ĵ 被推斜到 (1,1)。
        m2 = [[2, 1], [0, 1]]
        self.play(
            grid.animate.apply_matrix(mat3(m2)),
            i_hat.animate.apply_matrix(mat3(m2)),
            j_hat.animate.apply_matrix(mat3(m2)),
            v_vec.animate.apply_matrix(mat3(m2)),
            FadeOut(key_line),
            run_time=4,
        )

        # 验算"老坐标 = 新位置"：Mv = (−1)·Mî + 2·Mĵ = (0,2)。
        # 箭还是那支箭，只是描述它的数字变了——这正是"变换"的含义。
        check = MathTex(
            r"Mv=(-1)\cdot M\hat{\imath}+2\cdot M\hat{\jmath}",
            r"=(-1)\!\begin{bmatrix}2\\0\end{bmatrix}+2\!\begin{bmatrix}1\\1\end{bmatrix}",
            r"=\begin{bmatrix}0\\2\end{bmatrix}",
        ).scale(0.8)
        check.to_edge(DOWN, buff=0.4)
        self.play(Write(check), run_time=3)

        # 收束到本课主题：矩阵是空间变换的数字快照。
        theme = Text("矩阵是空间变换的数字快照", font_size=32, color=YELLOW)
        theme.to_edge(UP, buff=0.3)
        self.play(FadeOut(title), FadeIn(theme))
        self.wait(2)


class RotationAndScale(Scene):
    def construct(self) -> None:
        title = Text("常见线性变换画廊", font_size=30)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # (说明文字, 2×2 矩阵, LaTeX) 三连：每个变换都从"标准网格 +
        # 标准基"出发，看完一个换一套全新的舞台，避免复合互相干扰。
        gallery = [
            ("逆时针旋转 90°", [[0, -1], [1, 0]],
             r"R=\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}"),
            ("等比缩放 2 倍", [[2, 0], [0, 2]],
             r"S=\begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}"),
            ("水平剪切", [[1, 1], [0, 1]],
             r"H=\begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}"),
        ]
        previous = None
        for name, m2, tex in gallery:
            stage = self._standard_stage()
            plane, i_hat, j_hat = stage
            if previous is not None:
                self.play(FadeOut(previous))
            self.play(Create(plane), GrowArrow(i_hat), GrowArrow(j_hat), run_time=1.5)

            matrix_tex = MathTex(tex).scale(0.9)
            # 矩阵摆左上（标题下方），说明文字跟在矩阵正下方对齐。
            matrix_tex.to_edge(LEFT, buff=0.6).shift(UP * 2.2)
            name_tex = Text(name, font_size=26, color=YELLOW)
            name_tex.next_to(matrix_tex, DOWN, buff=0.3).align_to(matrix_tex, LEFT)
            self.play(Write(matrix_tex), FadeIn(name_tex))

            # 网格和绿/红两根基箭头做同一个矩阵乘法：
            # 旋转——î 竖起来 (0,1)、ĵ 指向左 (−1,0)；
            # 缩放——两根箭头都变长一倍，网格变疏；
            # 剪切——î 不动（第一列 (1,0)），ĵ 被推斜（第二列 (1,1)）。
            self.play(
                plane.animate.apply_matrix(mat3(m2)),
                i_hat.animate.apply_matrix(mat3(m2)),
                j_hat.animate.apply_matrix(mat3(m2)),
                run_time=3,
            )
            self.wait(1.5)
            previous = VGroup(stage, matrix_tex, name_tex)
        self.wait(1)

    @staticmethod
    def _standard_stage() -> VGroup:
        """一套全新的"标准网格 + 标准基"，保证每个变换互不叠加。"""
        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=7)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=7)
        return VGroup(plane, i_hat, j_hat)


class BasisChange(Scene):
    def construct(self) -> None:
        title = Text("基变换：换个坐标系看同一个向量", font_size=30)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={"stroke_opacity": 0.35},
        )
        self.play(Create(grid), run_time=1.5)

        # 非标准基 b₁=(1,1)、b₂=(−1,1)：用橙色和标准基的绿/红区分开。
        b1 = Arrow(ORIGIN, [1, 1, 0], buff=0, color=ORANGE, stroke_width=7)
        b2 = Arrow(ORIGIN, [-1, 1, 0], buff=0, color=ORANGE, stroke_width=7)
        b1_label = MathTex(r"\mathbf{b}_1=(1,\,1)", color=ORANGE).scale(0.8)
        b2_label = MathTex(r"\mathbf{b}_2=(-1,\,1)", color=ORANGE).scale(0.8)
        b1_label.next_to(b1.get_end(), DR, buff=0.1)
        b2_label.next_to(b2.get_end(), UL, buff=0.1)
        self.play(GrowArrow(b1), GrowArrow(b2), FadeIn(b1_label), FadeIn(b2_label))

        # 同一个向量 v：在标准基下坐标是 (1,2)——这是它的"标准地址"。
        v_vec = Arrow(ORIGIN, [1, 2, 0], buff=0, color=YELLOW, stroke_width=7)
        v_label = MathTex(r"v=(1,\,2)", color=YELLOW).scale(0.8)
        v_label.next_to(v_vec.get_end(), UP, buff=0.1)
        self.play(GrowArrow(v_vec), FadeIn(v_label))

        # 在新基下分解 v = (3/2)b₁ + (1/2)b₂：用虚线画出
        # "先沿 b₁ 走 1.5 步，再沿 b₂ 走 0.5 步"的平行四边形路径。
        step1 = DashedLine(ORIGIN, 1.5 * np.array([1, 1, 0]), color=ORANGE, stroke_width=3)
        step2 = DashedLine(
            1.5 * np.array([1, 1, 0]),
            1.5 * np.array([1, 1, 0]) + 0.5 * np.array([-1, 1, 0]),
            color=ORANGE, stroke_width=3,
        )
        coeff_tex = MathTex(
            r"v=\tfrac{3}{2}\,\mathbf{b}_1+\tfrac{1}{2}\,\mathbf{b}_2",
            r"\;\Rightarrow\;",
            r"[v]_{B}=\left(\tfrac{3}{2},\,\tfrac{1}{2}\right)",
        ).scale(0.85)
        coeff_tex.to_edge(RIGHT, buff=0.6).shift(UP * 1.5)
        self.play(Create(step1), Create(step2), Write(coeff_tex), run_time=3)

        # 基变换矩阵：把 b₁、b₂ 按列排起来就是 B。
        b_tex = MathTex(
            r"B=\begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}", color=ORANGE
        ).scale(0.9)
        b_tex.to_corner(UL, buff=0.5).shift(DOWN * 1.1)
        b_caption = Text("基变换矩阵：把基向量按列排起来", font_size=22, color=ORANGE)
        b_caption.next_to(b_tex, DOWN, buff=0.3).align_to(b_tex, LEFT)
        self.play(Write(b_tex), FadeIn(b_caption))

        # 转换关系：v_标准 = B·v_B。代入验算 B·(3/2,1/2) = (1,2)。
        # 反方向自然要乘 B⁻¹——逆矩阵正是第 5 课的主角。
        conv = MathTex(
            r"\begin{bmatrix} 1 \\ 2 \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} 1 & -1 \\ 1 & 1 \end{bmatrix}",
            r"\begin{bmatrix} \tfrac{3}{2} \\[2pt] \tfrac{1}{2} \end{bmatrix}",
        ).scale(0.85)
        conv.to_edge(DOWN, buff=0.35)
        conv_note = Text("B 负责“新坐标 → 标准坐标”的换算", font_size=22, color=YELLOW)
        conv_note.next_to(conv, UP, buff=0.25)
        self.play(Write(conv), run_time=2)
        self.play(FadeIn(conv_note))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="矩阵即线性变换：旋转、缩放、剪切与基")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "02",
        [MatrixAsTransform, RotationAndScale, BasisChange],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
