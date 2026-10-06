"""圆角卡片类小组件：路线图节点、状态面板、知识卡片。

episode01 各幕各自手写过三种几乎相同的"圆角底板 + 文字"组件，
这里合并成三个工厂函数，各幕不再自带局部实现：

    chip()  —— 单行文字的小卡片（路线图节点、身份链节点）
    panel() —— 单行文字的面板（时间线节点、结论/状态面板）
    card()  —— 标题 + 副内容的两行知识卡片（副内容可传字符串或
               MathTex 等 Mobject）

chip 偏紧凑（字号大一点、内边距小、更透明），panel 偏舒展，
差异就是各自文档化在签名里的默认值；需要微调时用关键字参数覆盖。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.style import C_TEXT, FONT


def _label_card(
    text: str,
    color: ManimColor,
    *,
    font_size: float,
    pad: tuple[float, float],
    fill_opacity: float,
    corner_radius: float,
    stroke_width: float,
) -> VGroup:
    label = Text(text, font=FONT, font_size=font_size, color=C_TEXT)
    pad_h, pad_v = pad  # 底板在文字宽/高上追加的总量
    board = RoundedRectangle(
        corner_radius=corner_radius,
        width=label.width + pad_h,
        height=label.height + pad_v,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=stroke_width,
    )
    return VGroup(board, label)


def chip(text: str, color: ManimColor, *, font_size: float = 26, pad: tuple[float, float] = (0.5, 0.4),
         fill_opacity: float = 0.22, corner_radius: float = 0.15, stroke_width: float = 2) -> VGroup:
    """单行小卡片：路线图节点、身份链节点。"""
    return _label_card(
        text, color, font_size=font_size, pad=pad,
        fill_opacity=fill_opacity, corner_radius=corner_radius, stroke_width=stroke_width,
    )


def panel(title: str, color: ManimColor, *, font_size: float = 24, pad: tuple[float, float] = (0.55, 0.75),
          fill_opacity: float = 0.18, corner_radius: float = 0.15, stroke_width: float = 2) -> VGroup:
    """单行面板：时间线节点、"结论 ⇔ 结论"对照块。"""
    return _label_card(
        title, color, font_size=font_size, pad=pad,
        fill_opacity=fill_opacity, corner_radius=corner_radius, stroke_width=stroke_width,
    )


def card(
    title: str,
    sub: str | Mobject,
    color: ManimColor,
    *,
    title_font_size: float = 26,
    sub_font_size: float = 21,
    sub_scale: float = 1.0,
    pad: tuple[float, float] = (0.6, 0.5),
    fill_opacity: float = 0.14,
    corner_radius: float = 0.15,
    stroke_width: float = 2,
) -> VGroup:
    """两行知识卡片：加粗彩色标题 + 副内容。

    sub 传字符串时内部转成 Text（sub_font_size，白色）；传 MathTex
    等 Mobject 时按引用收编并统一成白色，由调用方负责字号——
    sub_scale 供 "MathTex 标 30 再缩 0.9" 这类组合复现原有观感。
    """
    if isinstance(sub, str):
        sub_mob: Mobject = Text(sub, font=FONT, font_size=sub_font_size, color=C_TEXT)
    else:
        sub_mob = sub.set_color(C_TEXT)
    if sub_scale != 1.0:
        sub_mob.scale(sub_scale)
    title_t = Text(title, font=FONT, font_size=title_font_size, color=color, weight=BOLD)
    group = VGroup(title_t, sub_mob).arrange(DOWN, buff=0.18)
    pad_h, pad_v = pad
    board = RoundedRectangle(
        corner_radius=corner_radius,
        width=max(title_t.width, sub_mob.width) + pad_h,
        height=group.height + pad_v,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=stroke_width,
    ).move_to(group)
    return VGroup(board, title_t, sub_mob)
