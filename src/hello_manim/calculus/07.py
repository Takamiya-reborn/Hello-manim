"""第 7 课：微分方程——可分离变量、一阶线性与二阶常系数。

本课要回答三个问题：
    1. dy/dx = f(x)·g(y) 这类方程为什么"可以分离"？
    2. 一阶线性方程两边乘积分因子后，为什么左边恰好是 (μy)'？
    3. 二阶常系数方程的解，为什么判别式一变就换一副面孔？

原理速览：
    数学上本课覆盖三种标准型：
      - 可分离变量：dy/dx = f(x)g(y) 改写成 dy/g(y) = f(x)dx，两边
        各自积分即得通解。几何上，解曲线由"斜率场"唯一确定：
        过每个初值点，顺着场中的短线段"流"下去；
      - 一阶线性：y' + P(x)y = Q(x)。取积分因子 μ = e^{∫P dx}，
        由链式法则 μ' = Pμ，于是 μy' + μPy = μ'y + μy' = (μy)'，
        方程变成 (μy)' = Qμ，一次积分得通解
        y = e^{-∫P dx}(∫Q e^{∫P dx} dx + C)；
      - 二阶常系数齐次 y'' + py' + qy = 0：设 y = e^{rx} 代入并约去
        e^{rx}，得特征方程 r² + pr + q = 0。判别式 Δ = p² - 4q 分三种：
        Δ>0 两相异实根（非振荡衰减，过阻尼）；Δ=0 二重根
        y = (C1 + C2x)e^{rx}（临界阻尼）；Δ<0 共轭复根 α±βi，
        解为 y = e^{αx}(C1·cos βx + C2·sin βx)（振荡衰减，欠阻尼）。
    manim 手段：
      - 斜率场：在网格点放短 Line 段，方向向量 (1, m) 归一化——前提是
        两轴"每数学单位的屏幕长度"相等，屏幕斜率才等于数学斜率；
      - MoveAlongPath 让初始点沿解曲线流动，直观展示"解贴合场"；
      - MathTex + TransformMatchingTex 承担全部逐步推导；
      - 多个 Axes 并排且统一 y 范围，三种解形的对比才公平。

最短运行：
    uv run hello-manim calculus 07

也可以用 manim 原生命令行渲染每一个场景：
    uv run manim -pql src/hello_manim/calculus/07.py SlopeField
    uv run manim -pql src/hello_manim/calculus/07.py LinearFirstOrder
    uv run manim -pql src/hello_manim/calculus/07.py SecondOrderTypes
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class SlopeField(Scene):
    def construct(self) -> None:
        # 中文走 Text（Pango 排版，不需要 LaTeX）；to_edge 固定在顶部。
        title = Text("斜率场与可分离变量：dy/dx = x/2", font_size=32)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 关键设置：x 方向 8 个单位占 10 格、y 方向 4 个单位占 5 格，
        # 每数学单位都是 1.25 屏幕单位——两轴等比，屏幕斜率 = 数学斜率，
        # 斜率场短线的方向才不会失真。
        axes = Axes(
            x_range=[-4, 4, 1], y_range=[-2, 2, 1],
            x_length=10, y_length=5, tips=False,
        )
        axes.to_edge(DOWN, buff=0.35)
        self.play(Create(axes), run_time=1.5)

        # 斜率场：在每个网格点放一条以该点为中心的短 Line。
        # 方向向量取 (1, m)（m = x/2 为该点斜率），归一化后乘半长 0.25，
        # 沿正反方向各取一半，短线关于网格点对称。
        field = VGroup()
        for gx in range(-4, 5):
            for gy in range(-4, 5):  # y 网格步长 0.5：gy * 0.5 ∈ [-2, 2]
                x, y = gx, gy * 0.5
                m = x / 2
                norm = math.hypot(1, m)
                field.add(
                    Line(
                        axes.c2p(x - 0.25 / norm, y - 0.25 * m / norm),
                        axes.c2p(x + 0.25 / norm, y + 0.25 * m / norm),
                        stroke_width=2.5, color=GREY_B,
                    )
                )
        self.play(Create(field), run_time=2)

        # 分离变量得通解 y = x²/4 + C——抛物线族，C 只做纵向平移。
        # 取两个不同初值（y(0) = -1.5 和 0.5）画两条特解。
        curve1 = axes.plot(lambda x: x * x / 4 - 1.5, x_range=[-2.4, 2.4], color=YELLOW)
        curve2 = axes.plot(lambda x: x * x / 4 + 0.5, x_range=[-2.4, 2.4], color=PINK)

        # MoveAlongPath：让初始点沿曲线"流"动，同时 Create 逐段画出曲线——
        # 点走到哪，切向就与那里的短线一致，这正是"解贴合斜率场"的含义。
        dot1 = Dot(axes.c2p(-2.4, -0.06), color=YELLOW, radius=0.07)
        self.play(Create(curve1), MoveAlongPath(dot1, curve1), run_time=3, rate_func=linear)
        dot2 = Dot(axes.c2p(-2.4, 1.94), color=PINK, radius=0.07)
        self.play(Create(curve2), MoveAlongPath(dot2, curve2), run_time=3, rate_func=linear)
        self.play(FadeOut(dot1, dot2))

        # 推导占据顶部空带（标题之下、坐标轴之上）。MathTex 拆成子串后，
        # TransformMatchingTex 按 token 配对：不变的部分原地保留，
        # 只动真正变化的部分——逐步推导观感自然的原因（见 base 第 6 课）。
        step = MathTex(r"\frac{dy}{dx}", "=", r"\frac{x}{2}").move_to(UP * 2.7)
        self.play(Write(step))
        # 分离变量：两边同乘 dx，x 只留在右边。
        step2 = MathTex(r"dy", "=", r"\frac{x}{2}\,dx").move_to(step)
        self.play(TransformMatchingTex(step, step2))
        # 两边各自积分：左边对 y，右边对 x。
        step3 = MathTex(r"\int dy", "=", r"\int \frac{x}{2}\,dx").move_to(step)
        self.play(TransformMatchingTex(step2, step3))
        # 积分出来就是抛物线族；给任意常数 C 上色，呼应两条特解的颜色。
        step4 = MathTex(r"y", "=", r"\frac{x^2}{4}", "+", r"C").move_to(step)
        step4.set_color_by_tex("C", YELLOW)
        self.play(TransformMatchingTex(step3, step4))
        self.wait(2)


class LinearFirstOrder(Scene):
    def construct(self) -> None:
        title = Text("一阶线性方程与积分因子", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 标准形。之后每一步推导都在同一位置做变换，画面不跳动。
        eq = MathTex(r"y'", "+", r"P(x)\,y", "=", r"Q(x)").move_to(UP * 2.6)
        self.play(Write(eq))

        # 积分因子 μ = e^{∫P dx}：链式法则给出 μ' = Pμ，于是
        # μy' + Pμy = μ'y + μy' = (μy)'——左边被"打包"成乘积导数。
        key = MathTex(
            r"\mu = e^{\int P\,dx}\;\Rightarrow\;(\mu\,y)' = \mu\,(y' + P\,y)",
        ).move_to(eq)
        self.play(TransformMatchingTex(eq, key))

        # 两边积分 μy = ∫Qμ dx + C，再除以 μ，就是通解公式（本课目标）。
        general = MathTex(
            r"y = e^{-\int P\,dx}\left(\int Q\,e^{\int P\,dx}\,dx + C\right)",
        ).move_to(UP * 1.5)
        box = SurroundingRectangle(general, color=BLUE, buff=0.15)
        self.play(Write(general), Create(box))
        self.wait(1)

        # 中间步骤退场，把画面让给具体例子——信息分层，一次只讲一件事。
        self.play(FadeOut(key))

        # 例：y' + y = e^{-x}，即 P = 1、Q = e^{-x}。
        # 回代验证：y = (x+C)e^{-x}，y' = (1 - x - C)e^{-x}，
        # y' + y = (1 - x - C + x + C)e^{-x} = e^{-x}，确实满足方程。
        ex_head = VGroup(
            Text("例：", font_size=28),
            MathTex(r"y' + y = e^{-x}", font_size=36),
            MathTex(r"\checkmark", font_size=30, color=GREEN),
        ).arrange(RIGHT, buff=0.25).move_to(LEFT * 3.4 + UP * 0.35)
        self.play(Write(ex_head))

        # 左列按公式走四步：μ = e^x；右边 Qμ = e^x·e^{-x} = 1 好积；
        # e^x y = x + C；除以 e^x 得通解。结果给 C 上色，呼应右图曲线族。
        steps = VGroup(
            MathTex(r"\mu = e^{\int 1\,dx} = e^{x}", font_size=28),
            MathTex(r"(e^{x}y)' = e^{x}e^{-x} = 1", font_size=28),
            MathTex(r"e^{x}y = x + C", font_size=28),
            MathTex(r"y = (x + C)\,e^{-x}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.next_to(ex_head, DOWN, aligned_edge=LEFT, buff=0.35)
        steps[-1].set_color_by_tex("C", YELLOW)
        self.play(Write(steps), run_time=3)

        # 右列小图：三条特解对应不同的 C，都是同一族曲线的成员。
        axes = Axes(
            x_range=[-0.5, 6, 1], y_range=[-1.5, 2.5, 1],
            x_length=5.6, y_length=3.6, tips=False,
        ).move_to(RIGHT * 3.9 + DOWN * 1.7)
        self.play(Create(axes), run_time=1)
        for c, color in [(2, RED), (0, BLUE), (-1, GREEN)]:
            # 曲线 y = (x + C)e^{-x}：x ≥ 0 段足够展示三种姿态。
            curve = axes.plot(lambda x, k=c: (x + k) * math.exp(-x), x_range=[0, 6], color=color)
            tag = MathTex(f"C = {c}", font_size=26, color=color)
            tag.next_to(axes.c2p(0, c), LEFT, buff=0.2)
            self.play(Create(curve), FadeIn(tag))
        self.wait(2)


class SecondOrderTypes(Scene):
    def construct(self) -> None:
        title = Text("二阶常系数齐次方程：三种阻尼", font_size=32).to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 特征方程法：设 y = e^{rx} 代入，y'' = r²e^{rx}、y' = re^{rx}，
        # 提出公因子 e^{rx}（恒不为零）约去——微分问题降为代数问题。
        head = MathTex(
            r"y'' + p\,y' + q\,y = 0 \;\Rightarrow\; r^2 + pr + q = 0", font_size=38,
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(head))
        self.wait(1)

        # 三种判别式情形各配一个真实例子（都可回代验证）：
        #   Δ>0：y''+3y'+2y=0，r=-1,-2，取 y=½(e^{-x}+e^{-2x})，y(0)=1；
        #   Δ=0：y''+2y'+y=0，r=-1 二重，取 y=(1+x)e^{-x}，y(0)=1；
        #   Δ<0：y''+y'+y=0，r=-1/2±(√3/2)i，取 y=e^{-x/2}cos(√3x/2)，y(0)=1。
        # 三条曲线都归一到 y(0)=1，并排对比才公平。
        cases = [
            (r"\Delta > 0:\ r_1 = -1,\ r_2 = -2",
             r"y = \tfrac{1}{2}\left(e^{-x} + e^{-2x}\right)",
             "过阻尼：无振动，单调衰减", RED,
             lambda x: 0.5 * (math.exp(-x) + math.exp(-2 * x))),
            (r"\Delta = 0:\ r_1 = r_2 = -1",
             r"y = (1 + x)\,e^{-x}",
             "临界阻尼：最快的无振动衰减", YELLOW,
             lambda x: (1 + x) * math.exp(-x)),
            (r"\Delta < 0:\ r = -\tfrac{1}{2} \pm \tfrac{\sqrt{3}}{2}\,i",
             r"y = e^{-x/2}\cos\tfrac{\sqrt{3}}{2}\,x",
             "欠阻尼：衰减振荡", GREEN,
             lambda x: math.exp(-x / 2) * math.cos(math.sqrt(3) / 2 * x)),
        ]

        # 每行：左侧"判别式 + 特征根"与解形标注，右侧 Axes 画对应解曲线。
        # 行距 1.85、每行 y_length 1.4，三行刚好填满标题以下的画面。
        for i, (case, sol, name, color, f) in enumerate(cases):
            row_y = 1.7 - i * 1.85
            ax = Axes(
                x_range=[0, 6, 2], y_range=[-1.2, 1.2, 1],
                x_length=7, y_length=1.4, tips=False,
            ).move_to(RIGHT * 2.8 + UP * (row_y - 0.25))
            curve = ax.plot(f, x_range=[0, 6], color=color)
            label = MathTex(case, font_size=30, color=color)
            label.move_to(LEFT * 4.1 + UP * (row_y + 0.35))
            sol_tex = MathTex(sol, font_size=28).next_to(label, DOWN, buff=0.15)
            name_tex = Text(name, font_size=20, color=color)
            name_tex.next_to(sol_tex, DOWN, buff=0.1)
            self.play(Create(ax), Write(label), run_time=1)
            self.play(Create(curve), FadeIn(sol_tex, name_tex), run_time=1.5)
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="微分方程：可分离变量、一阶线性与二阶常系数")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus", "07", [SlopeField, LinearFirstOrder, SecondOrderTypes],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
