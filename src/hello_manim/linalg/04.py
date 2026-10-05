r"""第 4 课：行列式——面积与体积的缩放因子。

本课要回答三个问题：
    1. 为什么 det A = ad − bc 恰好是"变换对面积的缩放因子"？
    2. det = 0 意味着什么？为什么它等价于矩阵不可逆？
    3. det(AB) = det(A)·det(B) 和 det(A⁻¹) = 1/det(A) 的直观依据是什么？

原理速览：
    数学原理：
      线性变换把单位正方形（由 î=(1,0) 和 ĵ=(0,1) 张成）变成一个
      平行四边形：î 被送到矩阵第一列，ĵ 被送到第二列。这个平行
      四边形的有向面积恰为 ad − bc——这就是行列式的几何定义：
      行列式 = 变换对（有向）面积的缩放因子。三种典型情形：
        det > 0：面积缩放 |det| 倍，平面定向不变；
        det = 0：平面被压扁成一条直线，面积缩放因子为 0——
                 一个维度被丢掉，信息不可恢复，故 det = 0 ⇔ 不可逆；
        det < 0：面积大小为 |det|，但平面被"翻面"（定向反转）。
      律则的直观依据：连续做两次变换，面积先缩放 det(A) 倍、再
      缩放 det(B) 倍，故 det(AB) = det(A)·det(B)；逆变换要把面积
      缩放"抵消"回 1，故 det(A⁻¹) = 1/det(A)。三维同理：
      3×3 行列式 = 变换对体积的缩放因子。
    manim 手段：
      - 单位正方形用 Polygon(ORIGIN, RIGHT, RIGHT + UP, UP) 精确
        指定四个顶点：顶点即数学坐标、锚在屏幕原点，apply_matrix
        默认以原点为中心做线性变换，图形与矩阵严格对应；
      - 变形用 mobject.animate.apply_matrix(M)：play 期间逐帧插值
        M·p，网格 NumberPlane 用同一个矩阵变形（3Blue1Brown 招牌
        画面：网格变形就是"线性变换本身"）；
      - 面积数值用 DecimalNumber + updater 每帧按鞋带公式从多边形
        顶点实时测出——"1 → 6"是测出来的，不是写死的；
      - 3D 用 ThreeDAxes + Cube，机位固定，文字用
        add_fixed_in_frame_mobjects 钉在屏幕画面层。

最短运行：
    uv run hello-manim linalg 04

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/linalg/04.py AreaScaling
    uv run manim -pql src/hello_manim/linalg/04.py CollapseAndOrientation
    uv run manim -pql src/hello_manim/linalg/04.py DeterminantLaws
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


def poly_area(polygon: VMobject) -> float:
    """鞋带公式：由多边形顶点实时算面积，供 DecimalNumber 显示。"""
    pts = polygon.get_start_anchors()  # Polygon 的各段起点 = 四个顶点
    return abs(
        sum(
            pts[i][0] * pts[(i + 1) % len(pts)][1]
            - pts[(i + 1) % len(pts)][0] * pts[i][1]
            for i in range(len(pts))
        )
    ) / 2


class AreaScaling(Scene):
    def construct(self) -> None:
        # 标题钉在画面上缘：to_edge 是"贴边布局"，不与图形争空间。
        title = Text("行列式：面积的缩放因子", font_size=32)
        title.to_edge(UP, buff=0.3)

        # NumberPlane 是带刻度的网格坐标系，铺满全屏当"背景纸"。
        # 背景线调淡，让前景的正方形与向量保持视觉焦点。
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.35},
        )

        # 单位正方形：四个顶点用屏幕坐标精确给出，分别对应数学点
        # O、î、î+ĵ、ĵ。锚在原点很关键——apply_matrix 以屏幕原点为
        # 中心，顶点即数学坐标，变形结果才严格等于矩阵作用。
        square = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP)
        square.set_stroke(BLUE, width=3).set_fill(BLUE, opacity=0.35)

        # 两条基向量：buff=0 让箭头精确从原点画到终点，不带留白。
        vec_i = Arrow(ORIGIN, RIGHT, buff=0, stroke_width=6, color=YELLOW)
        vec_j = Arrow(ORIGIN, UP, buff=0, stroke_width=6, color=GREEN)
        # 基向量记号用 MathTex（raw string 防止 \i \j 被 Python 转义）。
        lab_i = MathTex(r"\hat{\imath}", font_size=36, color=YELLOW)
        lab_j = MathTex(r"\hat{\jmath}", font_size=36, color=GREEN)
        # updater：每帧把标签钉回箭头终点旁——变形后标签自动跟随。
        lab_i.add_updater(lambda m: m.next_to(vec_i.get_end(), DOWN, buff=0.15))
        lab_j.add_updater(lambda m: m.next_to(vec_j.get_end(), LEFT, buff=0.15))

        self.play(FadeIn(grid), Write(title))
        self.play(Create(square), Create(vec_i), Create(vec_j), FadeIn(lab_i), FadeIn(lab_j))
        self.wait(1)

        # 本课主角矩阵 A：î→(2,0)，ĵ→(1,3)，det = 2×3 − 1×0 = 6。
        A = [[2, 1], [0, 3]]
        mat_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 0 & 3 \end{bmatrix}", font_size=40
        ).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)

        # 面积计数器：DecimalNumber 是"可以 set_value 的数字"。
        # updater 每帧用鞋带公式从 square 当前顶点算面积——变形过程
        # 中数字连续滚动，最终停在 6，是真实测量值而非预设脚本。
        area_num = DecimalNumber(1, num_decimal_places=1, font_size=40, color=BLUE)
        area_num.add_updater(lambda m: m.set_value(poly_area(square)))
        area_label = (
            VGroup(Text("面积", font_size=30), area_num)
            .arrange(RIGHT, buff=0.2)
            .to_edge(RIGHT, buff=0.5)
            .shift(DOWN * 1.5)
        )

        # det 的定义式与几何结论：公式一律 MathTex，中文一律 Text。
        det_def = MathTex(
            r"\det\begin{bmatrix} a & b \\ c & d \end{bmatrix} = ad - bc",
            font_size=40,
        ).to_edge(DOWN, buff=0.4)
        meaning = Text("行列式 = 变换对面积的缩放因子", font_size=28, color=YELLOW)
        meaning.next_to(det_def, UP, buff=0.25)

        self.play(Write(mat_tex), FadeIn(area_label))
        self.wait(1)
        # 变形：apply_matrix(M) 把每个点 p 替换为 M·p（列向量约定），
        # .animate 让 manim 在 play 期间逐帧插值——网格、正方形、
        # 基向量同时变形，这段画面就是"线性变换本身"。
        self.play(
            grid.animate.apply_matrix(A),
            square.animate.apply_matrix(A),
            vec_i.animate.apply_matrix(A),
            vec_j.animate.apply_matrix(A),
            run_time=4,
        )
        # 变形结束：面积停在 6 = det(A)，测量值与公式互相印证。
        self.play(Write(det_def), FadeIn(meaning))
        self.wait(2)


class CollapseAndOrientation(Scene):
    def construct(self) -> None:
        title = Text("det = 0 与定向翻转", font_size=32)
        title.to_edge(UP, buff=0.3)
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.35},
        )
        square = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP)
        square.set_stroke(BLUE, width=3).set_fill(BLUE, opacity=0.35)
        # 定向指示箭头：贴着正方形底边向右——顶点序 O→î→î+ĵ→ĵ 是
        # 逆时针（正定向），这个箭头就代表平面的"绕行方向"。
        orient = Arrow([0.15, 0.3, 0], [0.85, 0.3, 0], buff=0, stroke_width=5, color=ORANGE)
        self.play(FadeIn(grid), Write(title))
        self.play(Create(square), Create(orient))

        # 第一部分：列共线矩阵。第二列 (1, 0.5) = 0.5 × 第一列 (2, 1)，
        # det = 2×0.5 − 1×1 = 0——两列被压到同一条直线上。
        A = [[2, 1], [1, 0.5]]
        mat_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 0.5 \end{bmatrix}", font_size=40
        ).to_corner(UL, buff=0.5)
        det_tex = MathTex(
            r"\det A = 2 \times 0.5 - 1 \times 1 = 0", font_size=36
        ).next_to(mat_tex, DOWN, buff=0.3)
        self.play(Write(mat_tex), Write(det_tex))
        self.wait(1)
        # 变形到退化矩阵：平面被连续压扁成一条直线（斜率 0.5）。
        self.play(
            grid.animate.apply_matrix(A),
            square.animate.apply_matrix(A),
            orient.animate.apply_matrix(A),
            run_time=4,
        )
        # 结论字幕：面积缩放因子为 0 ⇒ 一个维度被丢掉 ⇒ 不可逆。
        # 数学上 det = 0 ⇔ 不可逆：压扁后无法唯一还原，信息已丢失。
        note = Text("面积缩放因子为 0：一个维度被压没了，变换不可逆", font_size=28, color=RED)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(2)

        # 清场进入第二部分（det < 0）：退化状态不适合直接复用，
        # 重画一套干净的网格与正方形。列表展开把清场写成一次 play。
        self.play(*[FadeOut(m) for m in self.mobjects])
        grid2 = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.35},
        )
        square2 = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP)
        square2.set_stroke(BLUE, width=3).set_fill(BLUE, opacity=0.35)
        orient2 = Arrow([0.15, 0.3, 0], [0.85, 0.3, 0], buff=0, stroke_width=5, color=ORANGE)
        self.play(FadeIn(grid2), FadeIn(square2), FadeIn(orient2))

        # 翻面矩阵 F：x 坐标取反。det F = −1——面积大小不变，定向反转。
        F = [[-1, 0], [0, 1]]
        f_tex = MathTex(
            r"F = \begin{bmatrix} -1 & 0 \\ 0 & 1 \end{bmatrix}", font_size=40
        ).to_corner(UL, buff=0.5)
        f_det = MathTex(r"\det F = -1 < 0", font_size=36).next_to(f_tex, DOWN, buff=0.3)
        self.play(Write(f_tex), Write(f_det))
        # 翻面：I 到 F 的线性插值矩阵是 diag(1−2s, 1)，s = 0.5 时
        # det = 0——连续地翻面必经过"压扁"时刻，这正是定向反转
        # ⇒ 行列式必变号的直观原因。
        self.play(
            grid2.animate.apply_matrix(F),
            square2.animate.apply_matrix(F),
            orient2.animate.apply_matrix(F),
            run_time=3,
        )
        # 箭头现在指向左了：面积大小没变，但"绕行方向"反了过来。
        note2 = Text("面积大小不变，但平面被翻了面：定向反转", font_size=28, color=ORANGE)
        note2.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note2))
        self.wait(2)


# 第三幕要用 3D 机位，所以继承 ThreeDScene 而不是 Scene：
# set_camera_orientation 是 ThreeDScene 才有的方法；默认机位下
# 它渲染 2D 物体的效果与普通 Scene 完全一致，可以混用。
class DeterminantLaws(ThreeDScene):
    def construct(self) -> None:
        title = Text("行列式的律则与三维推广", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.add(title)

        # 律则一：连续两次变换，面积先被 A 缩放 det(A) 倍、再被 B
        # 缩放 det(B) 倍——两次缩放自然相乘，这就是 det(AB) 的直观。
        law1 = MathTex(r"\det(AB) = \det(A) \cdot \det(B)", font_size=48)
        law1.shift(UP * 1.6)
        exp1 = Text("连续两次缩放，因子相乘", font_size=28)
        exp1.next_to(law1, DOWN, buff=0.3)
        self.play(Write(law1), FadeIn(exp1))
        self.wait(1)

        # 律则二：逆变换必须把面积缩放"抵消"回 1，
        # 所以 det(A⁻¹) = 1/det(A)——也再次暗示 det = 0 时无逆。
        law2 = MathTex(r"\det(A^{-1}) = \frac{1}{\det(A)}", font_size=48)
        law2.shift(DOWN * 0.4)
        exp2 = Text("逆变换把面积缩放抵消回 1", font_size=28)
        exp2.next_to(law2, DOWN, buff=0.3)
        self.play(Write(law2), FadeIn(exp2))
        self.wait(1)

        # 2D 部分清场，切换 3D：机位一次固定（phi=俯仰角、
        # theta=方位角），本课不演示镜头运动，保持画面简洁。
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 3, 1],
            x_length=6,
            y_length=6,
            z_length=3,
        )
        self.play(Create(axes))

        # 单位立方体：体积 1。半透明填充让内部棱线可见，
        # 3D 物体的"透明度 + 描边"是可读性的关键。
        cube = Cube(side_length=1).set_fill(BLUE, opacity=0.35).set_stroke(WHITE, width=1.5)
        self.play(FadeIn(cube))

        # 目标长方体：沿 x 拉伸 2 倍、沿 z 拉伸 1.5 倍 ⇒ 体积 2×1×1.5 = 3，
        # 对应对角矩阵 diag(2, 1, 1.5)，det = 3 = 体积缩放因子。
        # stretch(factor, dim) 沿第 dim 个坐标轴缩放，锚在中心。
        self.play(cube.animate.stretch(2, 0).stretch(1.5, 2), run_time=3)

        # 3D 场景里的文字要"钉在屏幕上"而不是躺在 xy 平面里：
        # add_fixed_in_frame_mobjects 把 mobject 放进固定画面层。
        vol_tex = MathTex(
            r"\det = 2 \times 1 \times 1.5 = 3", font_size=44, color=YELLOW
        ).to_corner(UL, buff=0.5)
        vol_note = Text("3×3 行列式 = 体积的缩放因子", font_size=28)
        vol_note.next_to(vol_tex, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(vol_tex, vol_note)
        self.play(FadeIn(vol_tex), FadeIn(vol_note))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="行列式：面积与体积的缩放因子")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "04",
        [AreaScaling, CollapseAndOrientation, DeterminantLaws],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
