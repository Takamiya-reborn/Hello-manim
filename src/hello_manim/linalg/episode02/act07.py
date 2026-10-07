"""Act07 · 从数字表到变换语言（本集总结）。

对应 mindmap Episode02 Act07 的旁白。视觉主线：
    矩阵的三个身份重合（系数表 / 机器 / 两列的落点）
    → 同一对象的三种读法（行读公式 · 列读去向 · 整体读变形）
    → 运算语义回顾 → 矩阵为什么是中心语言（四向汇聚）
    → 留问：被变换的对象是什么？ → 下集预告（向量）。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.narration import EpisodeScene
from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_MAIN,
    C_POS,
    C_SUB,
    FONT,
    STAGE_CENTER,
)
from hello_manim.utils.widgets import card, chip, panel


class Act07Summary(EpisodeScene):
    def construct(self) -> None:
        self.act_title("Act 07", "从数字表到变换语言")

        # ---- 1. 三个身份重合 ------------------------------------------------
        self.say(
            "到这里，矩阵的几个身份已经逐渐重合：它可以写成一张系数表，"
            "也可以看成一台处理坐标的机器，还可以看成两种基本输入的输出记录。"
        )
        ids = VGroup(
            card("一张系数表", "行列排布的数字", C_SUB),
            card("一台机器", "对坐标生效的动作", C_MAIN),
            card("两列的落点", "基本输入的去向", C_HL),
        ).arrange(RIGHT, buff=0.7).move_to(STAGE_CENTER)
        if ids.width > 12:
            ids.scale(12 / ids.width)
        self.play(LaggedStart(*[FadeIn(i, scale=1.08) for i in ids], lag_ratio=0.25), run_time=1.6)
        self.hold()

        # ---- 2. 同一对象的三种读法 --------------------------------------------
        self.say(
            "这些说法不是三个不同的对象，而是同一个对象的三种观察角度："
            "行适合读输出公式，列适合读基本输入的去向，"
            "整体适合读图形的变形。"
        )
        reads = VGroup(
            panel("行 → 输出公式", C_MAIN),
            panel("列 → 输入去向", C_HL),
            panel("整体 → 图形变形", C_POS),
        ).arrange(RIGHT, buff=0.6).move_to(STAGE_CENTER)
        self.play(FadeOut(ids), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r, scale=1.08) for r in reads], lag_ratio=0.25), run_time=1.4)
        self.hold()
        self.play(FadeOut(reads), run_time=0.5)

        # ---- 3. 运算语义回顾 ---------------------------------------------------
        self.say(
            "矩阵加法和数乘描述变换的叠加与缩放；矩阵乘法描述变换的复合；"
            "单位矩阵描述什么都不做；逆矩阵描述动作的撤销；"
            "不同坐标语言则说明同一动作可以有不同的数字外观。"
        )
        ops_top = VGroup(
            panel("加法 · 数乘 ＝ 叠加 · 缩放", C_MAIN),
            panel("乘法 ＝ 复合", C_HL),
        ).arrange(RIGHT, buff=0.7)
        ops_bottom = VGroup(
            panel("I ＝ 什么都不做", C_POS),
            panel("逆矩阵 ＝ 撤销", C_POS),
            panel("换坐标 ＝ 换外观", C_SUB),
        ).arrange(RIGHT, buff=0.7)
        ops = VGroup(ops_top, ops_bottom).arrange(DOWN, buff=0.45).move_to(STAGE_CENTER)
        self.play(FadeIn(ops_top, shift=UP * 0.3), run_time=0.9)
        self.play(FadeIn(ops_bottom, shift=UP * 0.3), run_time=0.9)
        self.hold()
        self.play(FadeOut(ops), run_time=0.5)

        # ---- 4. 中心语言 -------------------------------------------------------
        self.say(
            "这也解释了为什么矩阵会成为线性代数的中心语言："
            "它把方程组、几何变形、坐标变换和代数运算装进了同一个框架。"
        )
        hub = chip("矩阵", C_HL, font_size=30)
        sats = VGroup(
            chip("方程组", C_MAIN),
            chip("几何变形", C_MAIN),
            chip("坐标变换", C_MAIN),
            chip("代数运算", C_MAIN),
        )
        sats[0].move_to(STAGE_CENTER + UP * 1.7)
        sats[1].move_to(STAGE_CENTER + RIGHT * 3.6)
        sats[2].move_to(STAGE_CENTER + DOWN * 1.4)
        sats[3].move_to(STAGE_CENTER + LEFT * 3.6)
        hub.move_to(STAGE_CENTER)
        # 连线在两芯片边缘之间画，避免穿过"矩阵"芯片的字。
        spokes = VGroup(*[
            Line(hub.get_edge_center(d), s.get_edge_center(-d), stroke_width=2.5, color=C_DIM)
            for d, s in zip((UP, RIGHT, DOWN, LEFT), sats)
        ])
        spokes.set_z_index(-1)
        self.play(FadeIn(hub, scale=1.2), run_time=0.7)
        self.play(Create(spokes), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(s, scale=1.1) for s in sats], lag_ratio=0.2), run_time=1.4)
        self.hold()
        self.play(FadeOut(hub), FadeOut(sats), FadeOut(spokes), run_time=0.6)

        # ---- 5. 留问：被变换的对象是什么？ --------------------------------------
        self.say(
            "但矩阵只是把变换写了下来，下一步的问题仍然悬着："
            "这些被变换的对象究竟是什么？"
            "它们除了坐标表之外，是否还有自己的几何意义？"
        )
        q = Text("被变换的对象，究竟是什么？", font=FONT, font_size=36, color=C_HL)
        q.move_to(STAGE_CENTER)
        self.play(FadeIn(q, scale=1.08), run_time=0.8)
        self.play(Circumscribe(q, color=C_HL, run_time=1.1))
        self.hold()
        self.play(FadeOut(q), run_time=0.5)

        # ---- 6. 下集预告 -------------------------------------------------------
        self.say(
            "在继续研究这些动作之前，我们还需要回头追问："
            "这些被搬运、被组合的对象究竟是什么？下一章先从向量本身开始。"
        )
        nxt = card("Episode 03 · 预告", "被变换的对象——向量", C_MAIN)
        nxt.move_to(STAGE_CENTER)
        self.play(FadeIn(nxt, scale=1.08), run_time=0.9)
        self.hold()
        self.wait(0.8)
