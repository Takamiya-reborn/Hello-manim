"""第 8 课：特征值与特征向量——变换的不变方向。

本课要回答三个问题：
    1. 矩阵把大多数向量都"掰弯"了，为什么有些向量只被伸缩、
       始终不离开自己的张成直线？
    2. det(A − λI) = 0 这个特征方程是怎么推出来的？90° 旋转
       为什么在实平面里一个特征向量都找不到？
    3. 对角化 A = PDP⁻¹ 好在哪里？怎么用它秒算矩阵幂，
       并看出斐波那契数列相邻项之比趋近黄金比 φ ≈ 1.618？

原理速览：
    数学原理：
      - 定义：若 Av = λv（v ≠ 0），则 v 是 A 的特征向量、λ 是对应的
        特征值——几何上，v 经过 A 只被伸缩 λ 倍，不拐弯。
      - 特征方程：Av = λv 移项得 (A − λI)v = 0；齐次方程有非零解
        ⇔ 系数矩阵不可逆 ⇔ det(A − λI) = 0。本课主角
        A = [[3,1],[0,2]] 是上三角阵，特征值就是对角元 λ₁=3、λ₂=2；
        代回解 (A−λI)v=0 得特征向量 v₁=(1,0)、v₂=(1,−1)（验算：
        A(1,0)=(3,0)=3(1,0)；A(1,−1)=(2,−2)=2(1,−1)）。
      - 反例：90° 旋转 R=[[0,−1],[1,0]] 的特征方程是 λ²+1=0，无实根
        ——旋转把每个向量都转离了原方向；特征值是复数 ±i，一句带过。
      - 对角化：把特征向量按列排成 P、特征值按对角线排成 D，则
        A = PDP⁻¹。直觉：P 是"换到特征向量坐标系"的翻译官，在那套
        基里变换只剩纯缩放。对角阵的幂就是对角元各自求幂，于是
        Aⁿ = PDⁿP⁻¹。斐波那契伴侣矩阵 M=[[1,1],[1,0]] 的特征值是
        φ=(1+√5)/2≈1.618 与 ψ≈−0.618；|ψ|<1，ψ 的贡献随 n 衰减，
        故 F(n+1)/F(n) → φ。
    manim 手段：
      - NumberPlane.animate.apply_matrix(mat3(M)) 让整张网格连续变形
        （mat3 把 2×2 补成 manim 要求的 3×3，见第 2 课）；
      - Arrow(buff=0) 与网格吃同一个矩阵：特征向量"只伸缩"肉眼可查；
        半透明残影保留原方向，对比"谁离开了直线"一目了然；
      - MathTex + TransformMatchingTex 做特征方程的逐步推导（引入
        bmatrix 的两步 token 差异大，改用整体 Transform 更稳）；
      - DecimalNumber + ChangeDecimalToValue 逐项滚动斐波那契比值，
        让"收敛到 1.618"变成看得见的过程。

最短运行：
    uv run hello-manim linalg 08

也可以用 manim 原生命令行渲染同一课的各个场景：
    uv run manim -pql src/hello_manim/linalg/08.py InvariantDirections
    uv run manim -pql src/hello_manim/linalg/08.py EigenEquation
    uv run manim -pql src/hello_manim/linalg/08.py Diagonalization
"""

import argparse

import numpy as np

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


def mat3(m2: list[list[float]]) -> list[list[float]]:
    """把 2×2 矩阵补齐成 manim 要求的 3×3：第三行第三列补成 (0,0,1)。"""
    return [
        [m2[0][0], m2[0][1], 0],
        [m2[1][0], m2[1][1], 0],
        [0, 0, 1],
    ]


class InvariantDirections(Scene):
    """幕 1：撒几条向量做同一变换——特征方向只伸缩，普通方向被掰弯。"""

    def construct(self) -> None:
        # 标题钉上缘、核心公式压下缘，中间整块留给网格"表演"。
        title = Text("哪些方向在变换中保持不变？", font_size=32)
        title.to_edge(UP, buff=0.3)

        # NumberPlane 就是"空间"本身：默认 1 格 = 1 屏幕单位（已实测
        # c2p(1,0)=(1,0,0)），所以箭头可以直接用字面坐标，与格线对齐。
        plane = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.4},
        )
        self.play(Create(plane), run_time=2)

        # 本课主角：上三角矩阵 A，特征值 = 对角元 3 和 2。
        # 底部公式同时给出矩阵与定义式 Av = λv。
        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        formula = MathTex(
            r"\mathbf{A}=\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix},"
            r"\qquad \mathbf{A}\mathbf{v}=\lambda\mathbf{v}",
            font_size=38,
        )
        formula.to_edge(DOWN, buff=0.3)
        self.play(Write(title), Write(formula))

        # 撒三条方向各异的向量（buff=0 让尖端精确落在端点）：
        # 黄 (1,0)、绿 (1,−1) 是验算过的特征向量；蓝 (0,1) 是普通向量
        # ——A(0,1)=(1,2)，方向注定被掰弯。箭头与网格吃同一个矩阵，
        # 两者始终同构，"箭头是否仍躺在原直线上"全程可比。
        arrows = [
            Arrow(ORIGIN, np.array([1.0, 0.0, 0.0]), buff=0, color=YELLOW, stroke_width=6),
            Arrow(ORIGIN, np.array([1.0, -1.0, 0.0]), buff=0, color=GREEN, stroke_width=6),
            Arrow(ORIGIN, np.array([0.0, 1.0, 0.0]), buff=0, color=BLUE, stroke_width=6),
        ]
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait(1)

        # 半透明残影：变换前复制一份留在原地。变换后对照残影，
        # "有没有离开自己的张成直线"一眼可见。
        ghosts = [a.copy().set_opacity(0.2) for a in arrows]
        self.add(*ghosts)

        # 一次 play 让网格 + 三支箭头吃同一个矩阵乘法：
        # 黄箭头→(3,0)（伸长 3 倍）、绿箭头→(2,−2)（伸长 2 倍），
        # 蓝箭头→(1,2)——长度和方向都变了。
        self.play(
            plane.animate.apply_matrix(mat3(A)),
            *[a.animate.apply_matrix(mat3(A)) for a in arrows],
            run_time=4,
        )

        # 给两条特征方向标注特征值：标签钉在变换后的箭头尖端旁。
        lab3 = MathTex(r"\lambda=3", font_size=34, color=YELLOW)
        lab3.next_to(arrows[0].get_end(), UP, buff=0.2)
        lab2 = MathTex(r"\lambda=2", font_size=34, color=GREEN)
        lab2.next_to(arrows[1].get_end(), RIGHT, buff=0.2)
        self.play(FadeIn(lab3), FadeIn(lab2))

        # 收束句沿用公式腾出的"底部槽位"：先清场再进场，布局不跳动。
        note = Text("黄、绿：只伸缩，没离开自己的直线；蓝：被掰弯了", font_size=26, color=YELLOW)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(formula), FadeIn(note))
        self.wait(2)


class EigenEquation(Scene):
    """幕 2：从 Av=λv 推出 det(A−λI)=0，再看"旋转没有实特征向量"。"""

    def construct(self) -> None:
        title = Text("特征方程：λ 藏在哪里？", font_size=32)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 推导链：每步一个 MathTex，全部摆进标题下方同一"槽位"——
        # 同位摆放后换形，公式原地演变、不跳动。
        eqs = [
            MathTex(r"\mathbf{A}\mathbf{v}=\lambda\mathbf{v}", font_size=40),
            MathTex(r"(\mathbf{A}-\lambda\mathbf{I})\mathbf{v}=\mathbf{0}", font_size=40),
            MathTex(r"\det(\mathbf{A}-\lambda\mathbf{I})=0", font_size=40),
            MathTex(
                r"\det\begin{bmatrix} 3-\lambda & 1 \\ 0 & 2-\lambda \end{bmatrix}=0",
                font_size=40,
            ),
            MathTex(r"(3-\lambda)(2-\lambda)=0", font_size=40),
            MathTex(r"\lambda_1=3,\quad \lambda_2=2", font_size=40),
        ]
        for eq in eqs:
            eq.next_to(title, DOWN, buff=0.75)

        # 每步配一句中文旁白，放公式正下方、逐步替换。
        caps = [
            "v ≠ 0：特征向量不许是零向量",
            "移项：要有非零解，A − λI 必须不可逆",
            "行列式 = 0 ⇔ 不可逆——这就是特征方程",
            "代入本课的 A",
            "三角矩阵的行列式 = 对角元之积",
            "两个特征值恰好是对角元 3 和 2",
        ]
        cap_mobs = [Text(t, font_size=24, color=GREY_A) for t in caps]
        for cap in cap_mobs:
            cap.next_to(eqs[0], DOWN, buff=0.65)

        # 第一步先单独写出；随后每步：旧旁白淡出 → 公式换形 → 新旁白淡入。
        self.play(Write(eqs[0]), FadeIn(cap_mobs[0]))
        self.wait(1.5)
        for i in range(1, 6):
            self.play(FadeOut(cap_mobs[i - 1]))
            # 引入/展开 bmatrix 的两步 token 结构差异大，整体 Transform
            # 更稳；其余步骤 token 相近，TransformMatchingTex 配对最自然。
            if i in (3, 4):
                self.play(Transform(eqs[i - 1], eqs[i]))
            else:
                self.play(TransformMatchingTex(eqs[i - 1], eqs[i]))
            self.play(FadeIn(cap_mobs[i]))
            self.wait(1)

        # ---- 反例：90° 旋转 ----
        title2 = Text("反例：90° 旋转找不到实特征向量", font_size=32)
        title2.to_edge(UP, buff=0.3)
        self.play(FadeOut(eqs[5], cap_mobs[5]), Transform(title, title2))

        # 新铺一张网格当"旋转舞台"，再撒三条方向的向量。
        plane2 = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.35},
        )
        self.play(Create(plane2), run_time=1.5)

        arrows2 = [
            Arrow(ORIGIN, np.array([1.0, 0.0, 0.0]), buff=0, color=YELLOW, stroke_width=6),
            Arrow(ORIGIN, np.array([1.0, 1.0, 0.0]), buff=0, color=TEAL, stroke_width=6),
            Arrow(ORIGIN, np.array([-1.0, 0.5, 0.0]), buff=0, color=PINK, stroke_width=6),
        ]
        self.play(*[GrowArrow(a) for a in arrows2])
        ghosts2 = [a.copy().set_opacity(0.2) for a in arrows2]
        self.add(*ghosts2)

        # 旋转 R=[[0,−1],[1,0]]：三条箭头连同残影一对照——全被转离
        # 原方向，没有任何方向"幸存"。
        r2 = [[0.0, -1.0], [1.0, 0.0]]
        self.play(
            plane2.animate.apply_matrix(mat3(r2)),
            *[a.animate.apply_matrix(mat3(r2)) for a in arrows2],
            run_time=3,
        )

        # 代数解释：特征方程 λ²+1=0 无实根；复特征值一句带过。
        eq_rot = MathTex(
            r"R=\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix},"
            r"\qquad \det(R-\lambda\mathbf{I})=\lambda^2+1=0",
            font_size=36,
        )
        eq_rot.to_edge(DOWN, buff=0.3)
        note = Text("无实根：每个向量都被转离原方向（复特征值 ±i 留给复数域）", font_size=24, color=GREY_A)
        note.next_to(eq_rot, UP, buff=0.2)
        self.play(Write(eq_rot))
        self.play(FadeIn(note))
        self.wait(2)


class Diagonalization(Scene):
    """幕 3：A=PDP⁻¹ 的"换基"直觉，与斐波那契比值 → 黄金比。"""

    def construct(self) -> None:
        title = Text("对角化：换到特征向量坐标系", font_size=32)
        title.to_edge(UP, buff=0.3)

        # 对角化等式：P 的两列正是幕 1 验算过的特征向量 (1,0)、(1,−1)，
        # D 把对应特征值 3、2 摆上对角线；underbrace 给矩阵起名字。
        eqA = MathTex(
            r"\underbrace{\begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}}_{\mathbf{A}}"
            r"=\underbrace{\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}}_{\mathbf{P}}"
            r"\underbrace{\begin{bmatrix} 3 & 0 \\ 0 & 2 \end{bmatrix}}_{\mathbf{D}}"
            r"\begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}^{-1}",
            font_size=38,
        )
        eqA.next_to(title, DOWN, buff=0.9)
        cap = Text("P：特征向量作列（换基）；D：新坐标下只剩纯缩放", font_size=24, color=GREY_A)
        cap.next_to(eqA, DOWN, buff=0.7)
        self.play(Write(title), Write(eqA), run_time=2)
        self.play(FadeIn(cap))
        self.wait(1.5)

        # ---- 第二段：对角化的威力 Aⁿ = PDⁿP⁻¹ ----
        title2 = Text("威力：Aⁿ = PDⁿP⁻¹，矩阵幂变成查表", font_size=32)
        title2.to_edge(UP, buff=0.3)
        self.play(FadeOut(eqA, cap), Transform(title, title2))

        eqN = MathTex(r"\mathbf{A}^n=\mathbf{P}\,\mathbf{D}^{\,n}\,\mathbf{P}^{-1}", font_size=40)
        eqN.next_to(title, DOWN, buff=0.5)
        # 斐波那契的伴侣矩阵：M·(Fₙ, Fₙ₋₁)ᵀ = (Fₙ₊₁, Fₙ)ᵀ——
        # 矩阵幂数着数着，就数到了斐波那契。
        eqF = MathTex(
            r"\mathbf{M}=\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix},"
            r"\qquad \lambda_\pm=\frac{1\pm\sqrt{5}}{2}",
            font_size=38,
        )
        eqF.next_to(eqN, DOWN, buff=0.5)
        self.play(Write(eqN), Write(eqF), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(eqN), FadeOut(eqF))

        # ---- 第三段：F(n+1)/F(n) → φ 的数值演示 ----
        fib = [1, 1]
        while len(fib) < 11:  # F1..F11，够算 9 个相邻比值
            fib.append(fib[-1] + fib[-2])

        # 比值读数行：公式骨架静态，数字交给 DecimalNumber。
        ratio_row = VGroup(
            MathTex(r"\frac{F_{n+1}}{F_n}", font_size=40),
            MathTex(r"=", font_size=40),
            DecimalNumber(fib[2] / fib[1], num_decimal_places=4, font_size=40, color=YELLOW),
        ).arrange(RIGHT, buff=0.25).move_to(DOWN * 0.4)
        note3 = Text(
            "另一特征值 |ψ|≈0.618 < 1：它的贡献随 n 增大而消失",
            font_size=24, color=GREY_A,
        )
        note3.next_to(ratio_row, DOWN, buff=0.55)
        self.play(
            Write(ratio_row[0]), Write(ratio_row[1]),
            FadeIn(ratio_row[2]), FadeIn(note3),
        )

        # ChangeDecimalToValue 让数字"滚动"到新值：逐项播出比值序列
        # 2 → 1.5 → 1.6667 → … 摆动越来越小，肉眼可见地夹向 1.618。
        for a, b in zip(fib[2:], fib[1:]):
            self.play(ChangeDecimalToValue(ratio_row[2], a / b), run_time=0.5)

        # 收敛终点亮出来：黄金比 φ。
        phi = MathTex(r"\varphi=\frac{1+\sqrt{5}}{2}\approx 1.618", font_size=40, color=GOLD)
        phi.next_to(note3, DOWN, buff=0.5)
        self.play(Write(phi))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="特征值、特征向量与对角化")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "08",
        [InvariantDirections, EigenEquation, Diagonalization],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
