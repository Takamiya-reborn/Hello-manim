"""第 4 课：微分中值定理与导数的应用。

本课要回答三个问题：
    1. 罗尔定理凭什么保证"至少有一处切线是水平的"？
    2. 把割线平移成切线，怎么就变成了拉格朗日中值定理？
    3. 导数的正负如何决定单调性？洛必达法则凭什么能用、
       用的时候必须检查哪些条件？

原理速览：
    数学上，这三个场景是一条主线：中值定理 → 导数符号 → 求极限。
      - 罗尔定理：f 在 [a,b] 连续、(a,b) 内可微、f(a)=f(b)，
        则存在 c 使 f'(c)=0。依据是费马引理——闭区间连续必取得
        最值，而可微函数在"内部最值"处切线必水平；
      - 拉格朗日中值定理是罗尔定理"解除等高约束"后的推广：
        f'(ξ) = [f(b)−f(a)]/(b−a)，几何上是"割线总能平移到
        与曲线相切"，物理上是"平均速度总等于某时刻的瞬时速度"；
      - 导数应用：f'>0 则递增、f'<0 则递减，极值点两侧 f' 变号；
        洛必达法则把 0/0 或 ∞/∞ 型未定式的"函数比"换成"导数比"，
        本质是比较分子分母趋零（或趋∞）的速度。
    manim 手段：
      - TangentLine(curve, alpha)：alpha 是沿曲线的归一化位置
        （0 = 起点，1 = 终点），配 ValueTracker 就能让切线滑动；
      - Line(p1, p2) 直接连两点，就是割线；
      - Axes.plot 的 x_range 支持分段采样，天然实现"分区间上色"；
      - Arrow 画增减箭头；MathTex 排公式（raw string 防转义）。

最短运行：
    uv run hello-manim calculus 04

也可以用 manim 原生命令行逐个渲染同一课的场景：
    uv run manim -pql src/hello_manim/calculus/04.py RolleTheorem
    uv run manim -pql src/hello_manim/calculus/04.py LagrangeTheorem
    uv run manim -pql src/hello_manim/calculus/04.py MonotonicAndLHopital
"""

import argparse
import math

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class RolleTheorem(Scene):
    def construct(self) -> None:
        # 数学设定：f(x) = x²−4x+3 = (x−1)(x−3)，开口向上的抛物线。
        # 取区间 [1,3]：f(1)=f(3)=0，两端恰好等高——这正是罗尔
        # 定理要求的 f(a)=f(b)，也是它和拉格朗日版的唯一差别。
        f = lambda x: x**2 - 4 * x + 3

        # Axes 负责"数学坐标 → 屏幕坐标"的翻译；x_length/y_length
        # 用屏幕单位控制大小，整体左移给右侧的条件清单腾位置。
        axes = Axes(
            x_range=[-0.3, 4.3, 1], y_range=[-1.6, 1.6, 1],
            x_length=6.6, y_length=4.4, tips=False,
        ).shift(LEFT * 2.2)
        # plot 只在 [1,3] 上采样——区间外不画，"定理只在区间内成立"。
        curve = axes.plot(f, x_range=[1, 3], color=BLUE)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(curve))

        # 端点 A(a,f(a))、B(b,f(b))：永远用 c2p 换算坐标，
        # 改坐标范围时不会失真（手写缩放比例才会）。
        dots = VGroup(Dot(axes.c2p(1, f(1))), Dot(axes.c2p(3, f(3))))
        labels = MathTex("a", "b", font_size=36)  # 拆成子对象才能各贴各的点
        labels[0].next_to(axes.c2p(1, f(1)), DOWN, buff=0.2)
        labels[1].next_to(axes.c2p(3, f(3)), DOWN, buff=0.2)
        self.play(FadeIn(dots), FadeIn(labels))

        # 三个条件逐条列出：中文叙述用 Text，公式行用 MathTex。
        conds = VGroup(
            Text("罗尔定理的条件", font_size=28, color=YELLOW),
            Text("① [a,b] 上连续", font_size=26),
            Text("② (a,b) 内可微", font_size=26),
            MathTex(r"f(a)=f(b)", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.7)
        self.play(Write(conds), run_time=2)

        # TangentLine 的 alpha 是"沿曲线的归一化位置"（0=起点 1=终点）。
        # 用 ValueTracker 驱动 alpha 从 0.1 滑到 0.5：切线扫过曲线，
        # 停在 c=2（alpha=(2−1)/2=0.5）——f'(x)=2x−4，f'(2)=0，切线水平。
        t = ValueTracker(0.1)
        tangent = always_redraw(
            lambda: TangentLine(curve, alpha=t.get_value(), length=3.2, color=ORANGE)
        )
        self.add(tangent)
        self.play(t.animate.set_value(0.5), run_time=3)

        # 标出切点 c：x=2 是抛物线对称轴，也是 [1,3] 上唯一的驻点——
        # 定理只说"至少一个"，这个例子恰好只有一个。
        c_dot = Dot(axes.c2p(2, f(2)), color=ORANGE)
        c_label = MathTex("c=2", font_size=34, color=ORANGE)
        c_label.next_to(c_dot, DOWN, buff=0.15)
        concl = MathTex(r"\exists\, c\in(a,b),\ \ f'(c)=0", font_size=36)
        concl.next_to(conds, DOWN, buff=0.5)
        self.play(FadeIn(c_dot, scale=2), FadeIn(c_label))
        self.play(Write(concl))
        self.wait(2)


class LagrangeTheorem(Scene):
    def construct(self) -> None:
        # 数学设定：f(x)=x²/4，区间 [1,3]。割线斜率
        # k = [f(3)−f(1)]/(3−1) = (9/4−1/4)/2 = 1；
        # f'(x)=x/2，令 f'(c)=1 得 c=2——切点恰是区间中点（抛物线的性质）。
        f = lambda x: x**2 / 4

        axes = Axes(
            x_range=[0.2, 4.3, 1], y_range=[-0.4, 3.0, 1],
            x_length=6.8, y_length=4.4, tips=False,
        ).shift(LEFT * 2.2)
        curve = axes.plot(f, x_range=[1, 3], color=BLUE)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(curve))

        # 割线：Line 直接连 A、B 两个屏幕点。割线斜率就是平均变化率。
        A, B = axes.c2p(1, f(1)), axes.c2p(3, f(3))
        dots = VGroup(Dot(A), Dot(B))
        secant = Line(A, B, color=YELLOW)
        sec_label = Text("割线 AB", font_size=24, color=YELLOW)
        sec_label.move_to(axes.c2p(2.45, 0.5))  # 放在曲线下方，避免遮挡
        self.play(FadeIn(dots), Create(secant), FadeIn(sec_label))

        # 右侧面板：先给出"平均"一侧的含义（k_eq），中文解释用 Text。
        panel = VGroup(
            MathTex(r"k=\frac{f(b)-f(a)}{b-a}", font_size=36, color=YELLOW),
            Text("割线斜率 = 平均变化率", font_size=24),
            Text("（物理：平均速度）", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.6).shift(UP)
        self.play(Write(panel))

        # 切线：TangentLine 在 alpha=0.5（即 x=c=2）处取切线。
        tangent = TangentLine(curve, alpha=0.5, length=5, color=ORANGE)
        self.play(Create(tangent))

        # 经典演示：复制割线，Transform 成切线。因为两者斜率相等
        # （这正是定理要证的结论），这个形变看起来就是"割线平移
        # 直到与曲线相切"——平移不改变斜率，切点就是 ξ。
        mover = secant.copy()
        self.play(Transform(mover, tangent), run_time=2)
        self.remove(mover)  # 形变完成后移除副本，画面上只留真切线

        # 标出切点 ξ，并写出定理本身；中文直觉用 Text 收尾。
        xi_dot = Dot(axes.c2p(2, f(2)), color=ORANGE)
        xi_label = MathTex(r"\xi", font_size=40, color=ORANGE)
        xi_label.next_to(xi_dot, DOWN, buff=0.15)
        theorem = MathTex(
            r"f'(\xi)=\frac{f(b)-f(a)}{b-a}", font_size=44,
        ).to_edge(UP, buff=0.45)
        intuition = Text("物理直觉：平均速度总等于某一时刻的瞬时速度", font_size=26)
        intuition.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(xi_dot, scale=2), Write(xi_label), FadeOut(sec_label))
        self.play(Write(theorem))
        self.play(FadeIn(intuition))
        self.wait(2)


class MonotonicAndLHopital(Scene):
    def construct(self) -> None:
        # —— 第一幕：导数符号与单调性 ——
        # 设定 f(x)=x³−3x：f'(x)=3x²−3，在 (−∞,−1)∪(1,+∞) 为正、
        # (−1,1) 内为负；x=−1 处由正变负（极大值 2），x=1 处由负变正（极小值 −2）。
        f = lambda x: x**3 - 3 * x

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-4.5, 4.5, 2],
            x_length=7.0, y_length=4.6, tips=False,
        )
        # 分区间采样、分段配色：绿 = 递增（f'>0），红 = 递减（f'<0）。
        # plot 的 x_range 就是采样区间，"分区间上色"不用任何额外 API。
        left = axes.plot(f, x_range=[-2.2, -1], color=GREEN)
        mid = axes.plot(f, x_range=[-1, 1], color=RED)
        right = axes.plot(f, x_range=[1, 2.2], color=GREEN)
        self.play(Create(axes), run_time=1.5)
        self.play(Create(left), Create(mid), Create(right))

        # 每段配一枚方向箭头：导数符号 → 增减趋势，一眼可读。
        # buff=0 让箭头两端精确落在起止点上。
        up1 = Arrow(axes.c2p(-1.8, -1.6), axes.c2p(-1.8, 1.6), buff=0, color=GREEN)
        down = Arrow(axes.c2p(0, 1.6), axes.c2p(0, -1.6), buff=0, color=RED)
        up2 = Arrow(axes.c2p(1.8, -1.6), axes.c2p(1.8, 1.6), buff=0, color=GREEN)
        self.play(GrowArrow(up1), GrowArrow(down), GrowArrow(up2))

        # 极值点 = f' 变号的点；符号法则写成"公式 + 中文"两行。
        ext = VGroup(
            Dot(axes.c2p(-1, 2), color=YELLOW), Dot(axes.c2p(1, -2), color=YELLOW)
        )
        rule = VGroup(
            VGroup(
                MathTex(r"f'(x)>0", color=GREEN, font_size=38),
                Text("单调递增", font_size=24),
            ).arrange(RIGHT, buff=0.25),
            VGroup(
                MathTex(r"f'(x)<0", color=RED, font_size=38),
                Text("单调递减", font_size=24),
            ).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rule.to_edge(UP, buff=0.45).shift(RIGHT * 3.4)
        note = Text("极值点两侧 f′ 变号", font_size=26, color=YELLOW)
        note.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(ext, scale=2), Write(rule), FadeIn(note))
        self.wait(1)

        # —— 第二幕：洛必达法则 ——
        # 整体清场切换话题：中值定理管"导数与单调"，接下来管"导数与极限"。
        self.play(*[FadeOut(m) for m in (axes, left, mid, right, up1, down, up2, ext, rule, note)])

        # 例：lim_{x→0} sin x / x。分子分母同时→0，是 0/0 型未定式，
        # 不能直接"代入"，也不能拆成 0/0 做除法——必须整体求极限。
        top = MathTex(r"\lim_{x\to 0}\frac{\sin x}{x}", font_size=44)
        top.to_edge(UP, buff=0.6).shift(LEFT * 3.5)

        # "趋零速度"演示：ValueTracker 让 x 缩小，always_redraw 实时
        # 重写数值——分子 sin x 与分母 x 一起→0，但两者比值→1。
        # manim 按 TeX 源码字符串缓存编译结果，同一数值只编译一次。
        x = ValueTracker(0.5)
        demo = always_redraw(
            lambda: MathTex(
                r"\frac{\sin %s}{%s}\approx %.4f"
                % (f"{x.get_value():.2f}", f"{x.get_value():.2f}",
                   math.sin(x.get_value()) / x.get_value()),
                font_size=36,
            ).next_to(top, DOWN, buff=0.7)
        )
        self.play(Write(top), FadeIn(demo))
        self.play(x.animate.set_value(0.01), run_time=2.5)

        # 法则与使用条件：右半屏一次列全，条件缺一不可。
        lhop = VGroup(
            MathTex(
                r"\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}",
                font_size=34,
            ),
            Text("使用条件（缺一不可）", font_size=26, color=YELLOW),
            Text("① 0/0 或 ∞/∞ 型未定式", font_size=24),
            Text("② 分子分母在去心邻域内可导", font_size=24),
            Text("③ 分母的导数不为 0", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        self.play(Write(lhop), run_time=2)

        # 收尾：数值演示的终点 + 一句话点破本质（比较趋零速度）。
        result = MathTex(
            r"\Rightarrow\ \lim_{x\to 0}\frac{\sin x}{x}=1", font_size=40, color=BLUE
        )
        result.next_to(lhop, DOWN, buff=0.5)
        moral = Text("本质：比较分子与分母趋于 0 的速度", font_size=26)
        moral.to_edge(DOWN, buff=0.4)
        self.play(Write(result), FadeIn(moral))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="微分中值定理与导数的应用")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus", "04",
        [RolleTheorem, LagrangeTheorem, MonotonicAndLHopital],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
