"""第 5 课：不定积分——原函数、换元法与分部积分。

本课要回答三个问题：
    1. 求导的逆运算"不定积分"，结果为什么是一族曲线、还都要写 +C？
    2. 复合函数的积分（如 ∫2x·cos(x²)dx）怎么用"凑微分"化简？
    3. 两类函数相乘（如 x·eˣ）时，分部积分的 u 和 dv 怎么选？

原理速览：
    数学上，三个场景是"求导的逆"这条主线的三级台阶：
      - 原函数：若 F'(x) = f(x)，则 F(x) 是 f 的一个原函数；任意两个
        原函数只相差一个常数，故 ∫f(x)dx = F(x) + C——几何上是一族
        上下平移的曲线，"+C" 不是习惯，而是"导数丢掉常数信息"的补偿；
      - 第一类换元（凑微分）：链式法则的逆用。∫f(g(x))g'(x)dx 中令
        u = g(x)、du = g'(x)dx，就化成基本积分 ∫f(u)du。例：
        ∫2x·cos(x²)dx，令 u = x²（du = 2x dx），得 ∫cos(u)du
        = sin(u)+C = sin(x²)+C；
      - 分部积分：对乘积法则 (uv)' = u'v + uv' 两边积分并移项，得
        ∫u dv = uv − ∫v du。选 u 的口诀"反、对、幂、指、三"：越靠前
        越优先当 u。例：x(幂) 排在 eˣ(指) 前，取 u = x、dv = eˣdx，
        得 xeˣ − eˣ + C。（每个结果都求导验证过。）
    manim 手段：
      - Axes.plot 画曲线，ValueTracker + always_redraw 让 "+C" 的
        曲线族随参数上下平移（base-04/05 课手法的组合）；
      - MathTex 按子串拆分后逐段上色：把被凑成 du 的"2x dx"与
        u = "x²" 染成同色，颜色就是换元的视觉线索；
      - TransformMatchingTex 按 token 配对做渐变，推导的每一步只动
        真正变化的部分（base-06 课手法的实战）。

最短运行：
    uv run hello-manim calculus 05

也可以用 manim 原生命令行逐个渲染同一课的场景：
    uv run manim -pql src/hello_manim/calculus/05.py AntiderivativeFamily
    uv run manim -pql src/hello_manim/calculus/05.py Substitution
    uv run manim -pql src/hello_manim/calculus/05.py IntegrationByParts
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson

# 坑（Windows + 杀毒软件实时防护）：manim 编译完每段 TeX 后会立刻
# 删除中间产物 .dvi，但 Defender（MsMpEng）正在扫描这个新建文件、
# 句柄未释放，unlink 抛 PermissionError（WinError 32）直接中断渲染。
# 本课公式最密集、编译次数最多，踩中概率极高——关闭自动清理，
# 中间产物留在 artifacts/media/Tex/（已 gitignore，还能当编译缓存复用）。
config.no_latex_cleanup = True


class AntiderivativeFamily(Scene):
    def construct(self) -> None:
        # 结论先行：不定积分的记号和"+C"写在画面最顶部（to_edge 贴边）。
        # MathTex 拆成子串后才能给 "C" 单独上色——它是本幕的主角。
        formula = MathTex(
            r"\int x^2 \,\mathrm{d}x", "=", r"\frac{x^3}{3}", "+", "C", font_size=44,
        )
        formula.set_color_by_tex("C", YELLOW)  # "C" 只在最后一个子串里出现，染色安全
        formula.to_edge(UP, buff=0.4)

        # 上方坐标系：原函数族 F(x) = x³/3 + C。ValueTracker 就是参数 C，
        # always_redraw 在 C 每次变化时重新 plot——曲线"活"了起来。
        axes_F = Axes(
            x_range=[-1.8, 1.8, 1], y_range=[-2.4, 2.4, 1],
            x_length=5.6, y_length=2.4, tips=False,
        ).next_to(formula, DOWN, buff=0.5)
        C = ValueTracker(0.0)
        family = always_redraw(
            lambda: axes_F.plot(
                lambda x: x**3 / 3 + C.get_value(), x_range=[-1.6, 1.6], color=YELLOW,
            )
        )
        F_label = MathTex(r"F(x) = \frac{x^3}{3} + C", font_size=34, color=YELLOW)
        F_label.next_to(axes_F, RIGHT, buff=0.5)

        # 下方坐标系：被积函数 f(x) = x²。plot 只画显函数，
        # x_range 是采样区间（base-05 课）。
        axes_f = Axes(
            x_range=[0, 2.4, 1], y_range=[0, 5, 1],
            x_length=5.6, y_length=2.0, tips=False,
        ).next_to(axes_F, DOWN, buff=0.6)
        f_curve = axes_f.plot(lambda x: x**2, x_range=[0, 2.1], color=BLUE)
        f_label = MathTex(r"f(x) = x^2", font_size=34, color=BLUE)
        f_label.next_to(axes_f.c2p(1.6, 2.56), UP, buff=0.2)

        # 开场先立"果"：f 的图像在下方，积分记号在顶部。
        self.play(Create(axes_f), Create(f_curve), Write(f_label), run_time=2)
        self.play(Write(formula))

        # 再立"因"：F 的导数是 f——所以 F 叫 f 的原函数。
        self.play(Create(axes_F), FadeIn(F_label))

        # "+C" 的几何意义：C 变化 = 整条曲线上下平移。
        # always_redraw 的物体直接 add 即可，它会自己跟随 tracker 更新。
        self.add(family)
        self.play(C.animate.set_value(0.9), run_time=1.5)
        self.play(C.animate.set_value(-0.9), run_time=2)
        self.play(C.animate.set_value(0.0), run_time=1.5)

        # 一句话收束：平移不改变导数值，族里每条曲线都"来历相同"。
        note = Text(
            "上下平移：每一条的导数都等于 f(x)，彼此只差一个常数 C",
            font_size=26, color=GREY_A,
        )
        note.next_to(axes_f, DOWN, buff=0.35)
        self.play(FadeIn(note))
        self.wait(2)


class Substitution(Scene):
    def construct(self) -> None:
        title = Text("第一类换元法：凑微分", font_size=32)
        title.to_edge(UP, buff=0.35)

        # 被积函数 = 复合 cos(x²) × 内层导数 2x——正是凑微分的标志形状。
        # 拆子串上色："2x"、"\,\mathrm{d}x"（即将凑成 du）与 "x^2"（u）同色。
        # 注意用普通括号：单独编译 "\left(" 会因括号不平衡而报错。
        prob = MathTex(
            r"\int", "2x", r"\cos(", "x^2", r")", r"\,\mathrm{d}x", "=", "?", font_size=40,
        )
        prob.next_to(title, DOWN, buff=0.5)
        prob[1].set_color(YELLOW)
        prob[3].set_color(YELLOW)
        prob[5].set_color(YELLOW)
        self.play(Write(title), Write(prob))

        # 换元声明：u = x²，du = 2x dx（x 的微分）。u 与 du 染成同一黄色，
        # 与公式里被标黄的部分一一对应——颜色就是"谁变成了谁"。
        sub = MathTex(
            r"u = x^2", r"\quad\Rightarrow\quad", r"\mathrm{d}u = 2x\,\mathrm{d}x",
            font_size=34,
        )
        sub[0].set_color(YELLOW)
        sub[2].set_color(YELLOW)
        sub.next_to(prob, DOWN, buff=0.55)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1)

        # 凑微分：把 2x dx 收进 du，剩下的 cos(x²) 换成 cos(u)，
        # 积分变成基本积分表里的形状 ∫cos(u)du。
        step_u = MathTex(r"\int", r"\cos(", "u", r")", r"\,\mathrm{d}u", font_size=40)
        step_u[2].set_color(YELLOW)
        step_u[4].set_color(YELLOW)
        step_u.next_to(sub, DOWN, buff=0.5)
        # TransformMatchingTex 按 token 配对：\int、\cos(、) 原地保留，
        # "x^2" 变成 "u"，"2x" 和 "dx" 被 du 吸收——只动该动的部分。
        self.play(TransformMatchingTex(prob, step_u))
        self.wait(1)

        # 基本积分：∫cos(u)du = sin(u) + C（sin 的导数是 cos，逆向读）。
        step_s = MathTex(r"\sin(", "u", r")", "+", "C", font_size=40)
        step_s[1].set_color(YELLOW)
        step_s.next_to(step_u, DOWN, buff=0.45)
        self.play(TransformMatchingTex(step_u, step_s))
        self.wait(1)

        # 回代：把 u 换回 x²。这一步只有 "u" → "x^2" 在动。
        step_x = MathTex(r"\sin(", "x^2", r")", "+", "C", font_size=40)
        step_x[1].set_color(YELLOW)
        step_x.next_to(step_s, DOWN, buff=0.45)
        self.play(TransformMatchingTex(step_s, step_x))
        self.wait(1)

        # 教学纪律：积分结果一律求导检验。链式法则：
        # d/dx[sin(x²)] = cos(x²)·(x²)' = cos(x²)·2x——与被积函数一致。
        verify = MathTex(
            r"\frac{\mathrm{d}}{\mathrm{d}x}\left[\sin\left(x^2\right)+C\right]",
            "=", r"\cos\left(x^2\right)\cdot 2x",
            r"= 2x\cos\left(x^2\right)", font_size=30,
        )
        verify.next_to(step_x, DOWN, buff=0.5)
        check = Text("与被积函数一致：结果正确", font_size=22, color=GREEN)
        check.next_to(verify, DOWN, buff=0.3)
        self.play(Write(verify), run_time=2)
        self.play(FadeIn(check))
        self.wait(2)


class IntegrationByParts(Scene):
    def construct(self) -> None:
        title = Text("分部积分", font_size=32)
        title.to_edge(UP, buff=0.35)

        # 公式来自乘积求导法则：对 (uv)' = u'v + uv' 两边积分再移项。
        # 拆子串上色：u 相关染蓝、v 相关染绿，公式里"谁对谁求导"一目了然。
        rule = MathTex(
            r"\int", "u", r"\,\mathrm{d}v", "=", r"u\,v", "-",
            r"\int", "v", r"\,\mathrm{d}u", font_size=38,
        )
        rule.next_to(title, DOWN, buff=0.45)
        rule[1].set_color(BLUE)   # u
        rule[2].set_color(BLUE)   # dv
        rule[7].set_color(GREEN)  # v
        rule[8].set_color(GREEN)  # du
        self.play(Write(title), Write(rule), run_time=2)

        # "谁当 u" 的口诀：反、对、幂、指、三，越靠前越优先当 u。
        # 直觉：排前面的求导后变简单（x → 1），排后面的好积分。
        hint = Text(
            "选 u 口诀：反、对、幂、指、三 —— 越靠前越优先当 u", font_size=26,
        )
        hint.next_to(rule, DOWN, buff=0.4)

        # 例 ∫x·eˣdx：x 是幂函数、eˣ 是指数函数，幂排在指之前，
        # 故取 u = x（蓝），剩下的 eˣdx 当 dv（绿）。
        assign = MathTex(
            "u = x", r"\qquad", r"\mathrm{d}v = e^x\,\mathrm{d}x", font_size=34,
        )
        assign[0].set_color(BLUE)
        assign[2].set_color(GREEN)
        assign.next_to(hint, DOWN, buff=0.4)
        self.play(FadeIn(hint), Write(assign))
        self.wait(1)

        # 第一步写原始积分：u 当蓝、dv 当绿，与上面的分配对应。
        e1 = MathTex(r"\int", "x", r"e^x", r"\,\mathrm{d}x", font_size=40)
        e1[1].set_color(BLUE)
        e1[2:].set_color(GREEN)
        e1.next_to(assign, DOWN, buff=0.55)
        self.play(Write(e1))

        # 代入公式 ∫u dv = uv − ∫v du：v = ∫eˣdx = eˣ（最简的 v 即可）。
        e2 = MathTex("x", r"e^x", "-", r"\int", r"e^x", r"\,\mathrm{d}x", font_size=40)
        e2[0].set_color(BLUE)
        e2[1].set_color(GREEN)
        e2[4:].set_color(GREEN)
        e2.next_to(e1, DOWN, buff=0.45)
        self.play(TransformMatchingTex(e1, e2))

        # 剩下的 ∫eˣdx 已是基本积分——用框把它"点名"。
        box = SurroundingRectangle(e2[4:], color=YELLOW, buff=0.12)
        self.play(Create(box))
        self.wait(1)

        # 收尾：∫eˣdx = eˣ，加上任意常数 C。
        e3 = MathTex("x", r"e^x", "-", r"e^x", "+", "C", font_size=40)
        e3[0].set_color(BLUE)
        e3[1].set_color(GREEN)
        e3[3].set_color(GREEN)
        e3.next_to(e2, DOWN, buff=0.45)
        # 框和被框的 ∫eˣdx 一起退场，换成语义等价的 eˣ + C。
        self.play(TransformMatchingTex(e2, e3), FadeOut(box))
        self.wait(1)

        # 求导验证：乘积法则 d/dx(x·eˣ) = eˣ + x·eˣ，再减 eˣ，恰好回到 xeˣ。
        verify = MathTex(
            r"\frac{\mathrm{d}}{\mathrm{d}x}\left[x\,e^x - e^x + C\right]",
            "=", r"e^x + x\,e^x - e^x", "=", r"x\,e^x", font_size=30,
        )
        verify.next_to(e3, DOWN, buff=0.45)
        check = Text("与被积函数一致：结果正确", font_size=22, color=GREEN)
        check.next_to(verify, DOWN, buff=0.25)
        self.play(Write(verify), run_time=2)
        self.play(FadeIn(check))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="不定积分：原函数族、凑微分与分部积分")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "calculus", "05",
        [AntiderivativeFamily, Substitution, IntegrationByParts],
        quality=args.quality, preview=args.preview, needs_latex=True,
    )


if __name__ == "__main__":
    main()
