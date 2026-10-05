"""第 1 课：向量——线性组合、张成空间与线性相关。

本课要回答三个问题：
    1. 向量加法的"首尾相接法"与平行四边形法为什么是同一件事？
    2. 坐标 (x, y) 除了是一对数，还能被理解成什么？
    3. 什么时候两个向量张成整个平面，什么时候塌缩成一条直线？

原理速览：
    数学（3Blue1Brown 的几何视角）：
      - 向量 = 从原点出发的位移。加法 = 位移的叠加：先沿 v 走再沿
        w 走，与先 w 后 v 落在同一点——这就是平行四边形法则；
      - 线性组合 a·v + b·w：标量 a、b 负责"缩放"（取负 = 反向），
        加法负责"拼接"。对基向量 î=(1,0)、ĵ=(0,1)，组合 x·î + y·ĵ
        的终点恰好是 (x, y)——坐标的本质是"这组组合系数"；
      - 张成空间 span{v, w} = { a·v + b·w | a,b ∈ R }，即所有组合
        能到达的点集。v、w 不共线时它是整个平面；若 w = 2v（共线），
        则 a·v + b·w = (a+2b)·v，终点只能落在一条直线上——张成
        塌缩。此时 w 可由 v 线性表示，对张成没有新贡献，称 {v, w}
        线性相关；反之只有 a = b = 0 才能使组合为零向量时称线性无关。
    manim 手段：
      - Arrow(起点, 终点, buff=0) 画向量（buff=0 让箭头精确落在
        起止点），NumberPlane 提供淡网格参照，DashedLine 标示
        "被搬家的向量"；
      - ValueTracker + always_redraw 让箭头逐帧按当前标量重建；
        变化的数字用 DecimalNumber + updater——它走普通字形而非
        LaTeX 管线，逐帧刷新没有编译开销；
      - 公式一律 MathTex，需要 LaTeX 环境（base 第 6 课的管线）。

最短运行：
    uv run hello-manim linalg 01

也可以用 manim 原生命令行渲染同一个场景：
    uv run manim -pql src/hello_manim/linalg/01.py VectorAddition
    uv run manim -pql src/hello_manim/linalg/01.py LinearCombination
    uv run manim -pql src/hello_manim/linalg/01.py SpanAndDependence
"""

import argparse

from manim import *

from hello_manim.rendering import add_render_args, render_lesson


class VectorAddition(Scene):
    def construct(self) -> None:
        # NumberPlane 提供淡网格背景，给"平面上的箭头"一个坐标参照；
        # opacity 调低以免喧宾夺主。range 写法与 Axes 一致：[起, 止, 步长]。
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.25},
        )
        self.add(plane)

        # 标题固定在顶部边缘；之后所有元素都避开这条"横幅"。
        title = Text("向量加法：两个位移的叠加", font_size=30)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 向量 = 从原点出发的箭头。buff=0 让箭头精确落在起止点上
        # （Arrow 默认会在两端留空隙去"避让"其他物体，画向量必须关掉）。
        v = Arrow(ORIGIN, [2, 1, 0], buff=0, color=BLUE)
        w = Arrow(ORIGIN, [1, 2, 0], buff=0, color=YELLOW)
        # 标签用 MathTex 的向量记法 \vec，紧贴各自箭头的尖端。
        v_lab = MathTex(r"\vec{v}=(2,\,1)", color=BLUE, font_size=34)
        v_lab.next_to(v.get_end(), DOWN, buff=0.15)
        w_lab = MathTex(r"\vec{w}=(1,\,2)", color=YELLOW, font_size=34)
        w_lab.next_to(w.get_end(), RIGHT, buff=0.15)
        self.play(GrowArrow(v), FadeIn(v_lab))
        self.play(GrowArrow(w), FadeIn(w_lab))
        self.wait(1)

        # 首尾相接法：把 w 平移到 v 的终点——"先沿 v 走，再沿 w 走"。
        # 向量只由长度和方向决定，平移不改变它，所以这支"搬家"的
        # w 仍是同一个向量。
        w_moved = w.copy().shift(v.get_end())
        # 虚线标出 w 的搬运轨迹，提示观众这支箭头移动了。
        track = DashedLine(w.get_end(), w_moved.get_end(), color=GREY_B, stroke_width=2)
        hint = Text("先沿 v 走，再沿 w 走", font_size=26, color=GREY_A)
        hint.to_edge(DOWN, buff=0.3)
        # TransformFromCopy：把 w "复印一份"再变形到目标位置，
        # 原地的 w 保持不动——演示平移不变性正需要这一点。
        self.play(
            FadeIn(hint), Create(track), TransformFromCopy(w, w_moved), run_time=2
        )

        # 合向量：从原点直指 (3, 3)。逐分量算 (2,1)+(1,2)=(3,3)，
        # 几何上它就是"先 v 后 w"这段折线的净位移。
        s = Arrow(ORIGIN, [3, 3, 0], buff=0, color=RED)
        s_lab = MathTex(r"\vec{v}+\vec{w}=(3,\,3)", color=RED, font_size=34)
        s_lab.next_to(s.get_end(), RIGHT, buff=0.2)
        self.play(GrowArrow(s), FadeIn(s_lab))
        self.wait(1)

        # 平行四边形法对比：把 v 搬到 w 的终点——"先 w 后 v"。
        # 两条路径终点重合，合向量恰是平行四边形的主对角线：
        # 这正是"加法可交换"的几何版本。
        v_moved = v.copy().shift(w.get_end()).set_opacity(0.55)
        track2 = DashedLine(
            v.get_end(), v_moved.get_end(), color=GREY_B, stroke_width=2
        )
        hint2 = Text("或先沿 w 走，再沿 v 走——殊途同归", font_size=26, color=GREY_A)
        hint2.to_edge(DOWN, buff=0.3)
        self.play(
            TransformFromCopy(v, v_moved),
            Create(track2),
            FadeOut(hint),
            FadeIn(hint2),
            run_time=2,
        )
        self.wait(1)


class LinearCombination(Scene):
    def construct(self) -> None:
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.25},
        )
        self.add(plane)

        title = Text("线性组合：先缩放，再相加", font_size=30)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # ValueTracker 是一个"会发出更新通知的数字"，本身不上屏；
        # 绑定它的 Mobject 会在 play() 期间逐帧刷新（base 第 4 课）。
        a = ValueTracker(1.0)
        b = ValueTracker(1.0)

        # 参与组合的两支向量（与第 1 幕同色，保持连贯），半透明衬底。
        v = Arrow(ORIGIN, [2, 1, 0], buff=0, color=BLUE).set_opacity(0.6)
        w = Arrow(ORIGIN, [1, 2, 0], buff=0, color=YELLOW).set_opacity(0.6)
        v_lab = MathTex(r"\vec{v}", color=BLUE, font_size=32)
        v_lab.next_to(v.get_end(), DOWN, buff=0.12)
        w_lab = MathTex(r"\vec{w}", color=YELLOW, font_size=32)
        w_lab.next_to(w.get_end(), RIGHT, buff=0.12)
        self.play(GrowArrow(v), FadeIn(v_lab), GrowArrow(w), FadeIn(w_lab))

        # 组合向量 a·v + b·w：always_redraw 每帧用 tracker 的当前值
        # 重新构造箭头，"拖动滑块"就表现为箭头实时伸缩、转向。
        # v=(2,1)、w=(1,2)，故终点坐标为 (2a+b, a+2b)。
        combo = always_redraw(
            lambda: Arrow(
                ORIGIN,
                [
                    2 * a.get_value() + b.get_value(),
                    a.get_value() + 2 * b.get_value(),
                    0,
                ],
                buff=0,
                color=RED,
            )
        )
        self.add(combo)

        # 读数行：符号骨架是静态 MathTex；变化的数字用 DecimalNumber，
        # 它用普通字形而非 LaTeX，set_value 逐帧刷新零编译开销。
        da = DecimalNumber(
            a.get_value(), num_decimal_places=1, color=ORANGE, font_size=34
        )
        db = DecimalNumber(
            b.get_value(), num_decimal_places=1, color=ORANGE, font_size=34
        )
        dx = DecimalNumber(3.0, num_decimal_places=1, color=RED, font_size=34)
        dy = DecimalNumber(3.0, num_decimal_places=1, color=RED, font_size=34)
        da.add_updater(lambda m: m.set_value(a.get_value()))
        db.add_updater(lambda m: m.set_value(b.get_value()))
        dx.add_updater(lambda m: m.set_value(2 * a.get_value() + b.get_value()))
        dy.add_updater(lambda m: m.set_value(a.get_value() + 2 * b.get_value()))
        readout = VGroup(
            da,
            MathTex(r"\,\vec{v} + \,", font_size=34),
            db,
            MathTex(r"\,\vec{w} = (\,", font_size=34),
            dx,
            MathTex(r"\,,\,", font_size=34),
            dy,
            MathTex(r"\,)", font_size=34),
        )
        # 数字变号会变宽，每帧重排一次，保证行内元素不互相重叠。
        readout.add_updater(
            lambda m: m.arrange(RIGHT, buff=0.1).to_edge(DOWN, buff=0.3)
        )
        self.add(readout)

        # 拖动滑块：a 从 1 到 -1（标量取负 = 向量反向），b 从 1 到 2，
        # 再同时微调——观察红色组合箭头与底部读数同步变化。
        self.play(a.animate.set_value(-1.0), run_time=2)
        self.play(b.animate.set_value(2.0), run_time=2)
        self.play(a.animate.set_value(1.5), b.animate.set_value(0.5), run_time=2)

        # 本幕核心观念：坐标的本质就是组合系数。对基向量
        # î=(1,0)、ĵ=(0,1)，组合 x·î + y·ĵ 的终点恰好是 (x, y)。
        punch_txt = Text(
            "坐标不只是数对——它指定了一组组合系数", font_size=26, color=GREY_A
        )
        punch_sym = MathTex(
            r"(x,\,y)\;=\;x\,\hat{\imath}+y\,\hat{\jmath}", font_size=38
        )
        punch_txt.next_to(title, DOWN, buff=0.35)
        punch_sym.next_to(punch_txt, DOWN, buff=0.2)
        self.play(FadeIn(punch_txt), Write(punch_sym))
        self.wait(2)


class SpanAndDependence(Scene):
    def construct(self) -> None:
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.25},
        )
        self.add(plane)

        title = Text("张成空间：组合能到达的所有终点", font_size=30)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title))

        # 张成的定义：让标量 a、b 取遍全体实数，看终点铺出多大区域。
        span_def = MathTex(
            r"\mathrm{span}\{\vec{v},\vec{w}\}=\{\,a\vec{v}+b\vec{w}\mid a,b\in\mathbb{R}\,\}",
            font_size=32,
        )
        span_def.next_to(title, DOWN, buff=0.25)
        self.play(Write(span_def))

        v = Arrow(ORIGIN, [2, 1, 0], buff=0, color=BLUE)
        w = Arrow(ORIGIN, [1, 2, 0], buff=0, color=YELLOW)
        v_lab = MathTex(r"\vec{v}", color=BLUE, font_size=34)
        v_lab.next_to(v.get_end(), DOWN, buff=0.15)
        w_lab = MathTex(r"\vec{w}", color=YELLOW, font_size=34)
        w_lab.next_to(w.get_end(), RIGHT, buff=0.15)
        self.play(GrowArrow(v), FadeIn(v_lab), GrowArrow(w), FadeIn(w_lab))

        # v、w 不共线 ⇒ 张成是整个平面。蒙一层淡蓝全屏矩形做示意：
        # "平面上每一个点都可达"。
        # 全屏尺寸从 config 读取（0.21 的星号导入不直接暴露 frame_width）。
        cover = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0,
        )
        claim = Text("不共线：组合可以到达平面上的每一点", font_size=26, color=GREY_A)
        claim.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(claim), cover.animate.set_fill(opacity=0.15))
        self.wait(1)

        # 让 w 退化成 2v：两支向量共线。此时 a·v + b·w = (a+2b)·v，
        # 无论 a、b 取什么值，终点都被锁在 v 所在的直线上——
        # 张成空间从"平面"塌缩成"一条直线"。
        w_flat = Arrow(ORIGIN, [4, 2, 0], buff=0, color=YELLOW)
        w_lab2 = MathTex(r"\vec{w}=2\vec{v}", color=YELLOW, font_size=34)
        w_lab2.next_to([4, 2, 0], RIGHT, buff=0.15)
        self.play(
            Transform(w, w_flat),
            Transform(w_lab, w_lab2),
            cover.animate.set_fill(opacity=0),
            run_time=2,
        )

        # 把塌缩后的张成画出来：与 v 同方向、贯穿画面的整条直线。
        # normalize 把方向向量缩成单位长度，方便按屏幕尺寸取半长。
        d = normalize([2.0, 1.0, 0.0])
        span_line = Line(-8 * d, 8 * d, color=RED, stroke_width=4)
        claim2 = Text(
            "共线：所有组合的终点只能落在这条直线上", font_size=26, color=GREY_A
        )
        claim2.to_edge(DOWN, buff=0.3)
        self.play(Create(span_line), FadeOut(claim), FadeIn(claim2))

        # 概念收尾：w 能被 v 线性表示 ⇒ {v, w} 线性相关。
        dep = MathTex(
            r"\vec{w}=2\vec{v}\ \Longrightarrow\ a\vec{v}+b\vec{w}=(a+2b)\,\vec{v}",
            font_size=32,
        )
        dep.move_to(span_def)  # 顶替张成定义的位置
        defn = Text(
            "线性相关：存在不全为 0 的 a、b 使 a·v+b·w=0（几何上即共线）；"
            "能被表示的那个向量对张成没有新贡献",
            font_size=24,
            color=GREY_A,
        )
        defn.next_to(claim2, UP, buff=0.15)
        self.play(FadeOut(span_def), FadeIn(dep), FadeIn(defn))
        self.wait(2)


def main() -> None:
    parser = argparse.ArgumentParser(description="向量、线性组合与张成空间")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson(
        "linalg",
        "01",
        [VectorAddition, LinearCombination, SpanAndDependence],
        quality=args.quality,
        preview=args.preview,
        needs_latex=True,
    )


if __name__ == "__main__":
    main()
