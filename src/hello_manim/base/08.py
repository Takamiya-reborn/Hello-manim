"""第 8 课：工程化——从教程脚本到可维护的动画工程。

本课要回答三个问题：
    1. 场景代码怎么组织才能复用（工厂函数、自定义 Animation）？
    2. 渲染慢，manim 的缓存机制在帮我们省什么？
    3. 质量层级该怎么选？

原理速览：
    教程代码是"剧本"，工程代码要"分层"：
      - 样式层：工厂函数把"这个项目里卡片长什么样"集中到
        一处，场景代码只声明内容——改配色只动一行；
      - 动画层：继承 Animation、实现 interpolate_mobject(alpha)
        就能造出自己的动画原语。starting_mobject 是开场快照，
        每帧 become() 回快照再形变，保证插值幂等（帧间无累积
        漂移）——这是自定义动画最容易踩的坑。
    缓存机制：manim 把每个 play() 拆成 partial movie file，
    哈希由"场景代码 + 动画参数"决定。没改到的动画直接命中
    缓存跳过渲染——所以 media/ 目录（本课程收在
    artifacts/media/）不要随手删，它是增量渲染的本钱。
    质量选择：迭代用 low（480p15，秒级），分享/成片才用
    medium/high（渲染时间随分辨率与帧率相乘增长）。

最短运行：
    uv run hello-manim base 08
"""

import argparse
import math

from manim import *

from hello_manim.utils.rendering import add_render_args, render_lesson

# ---------- 样式层：工厂函数 ----------

ACCENT = BLUE


def make_card(text: str) -> VGroup:
    """项目统一的"卡片"样式：圆角框 + 文字。改样式只改这里。"""
    label = Text(text, font_size=30)
    box = SurroundingRectangle(label, corner_radius=0.15, color=ACCENT, buff=0.25)
    return VGroup(box, label)


# ---------- 动画层：自定义 Animation ----------


class Pulse(Animation):
    """心跳动画：物体先胀后缩，回到原样。

    自定义动画只需实现 interpolate_mobject(alpha)：alpha 是经
    rate_func 映射后的进度。每帧从开场快照出发重新计算，
    而不是在上一帧的基础上叠加——幂等性是正确性的关键。
    """

    def interpolate_mobject(self, alpha: float) -> None:
        # sin(απ)：0 → 1 → 0，天然形成"胀了再缩"的包络。
        strength = math.sin(alpha * PI)
        scale = 1 + 0.2 * strength
        self.mobject.become(self.starting_mobject.copy()).scale(scale)


class EngineeredScene(Scene):
    def construct(self) -> None:
        # 场景代码只剩"内容声明"：样式细节全部在工厂函数里。
        cards = VGroup(
            make_card("加载"),
            make_card("渲染"),
            make_card("导出"),
        ).arrange(RIGHT, buff=0.8)
        self.play(FadeIn(cards, shift=UP))

        # 自定义动画和内置动画的调用方式完全一致。
        self.play(Pulse(cards[1]), run_time=1.5)

        # 工厂函数保证一致性：改一处 ACCENT，三张卡片全部变化。
        card = make_card("新卡片")
        card.next_to(cards, DOWN, buff=0.8)
        self.play(FadeIn(card))
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="工厂函数、自定义动画与缓存机制")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson("base", "08", [EngineeredScene], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
