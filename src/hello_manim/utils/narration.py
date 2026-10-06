"""剧集共用的视觉与旁白基建：底部字幕条 + 场景基类。

本仓库课程的叙事单元是"旁白 + 配合动画"：mindmap 文案里的每条
叙述以底部字幕条的形式呈现（无人声，字幕就是观众读取信息的通道），
画面上部留给数学演示。这里集中解决三件全幕共享的事：

    1. wrap_cjk —— 中文自动断行（Pango 不会替中文换行）；
    2. NarrationBar —— 底部字幕条：按文字长度自适应底板宽度；
    3. EpisodeScene —— 场景基类：say() 换字幕、hold() 按字数自动
       停留（代替旁白的朗读时长）、act_title() 幕标题开场并缩成角标。

节奏常量与调色板见 utils/style.py。
"""

from __future__ import annotations

from manim import *

from hello_manim.utils.style import (
    C_DIM,
    C_HL,
    C_TEXT,
    FONT,
    LINE_HOLD_BASE,
    LINE_HOLD_MIN,
    LINE_HOLD_PER_CHAR,
    LINE_SWAP_TIME,
    NARR_FONT_SIZE,
    NARR_MAX_CHARS,
)


def wrap_cjk(text: str, max_chars: int = NARR_MAX_CHARS) -> str:
    """按"显示宽度"给中文文案断行，优先在标点后断。

    Pango 对 CJK 文本不做自动换行（没有空格可断），长字幕会横向
    溢出画面，所以必须在生成 Text 之前手动插 \n。宽度规则：
    CJK 字符与全角标点算 1，ASCII 字母数字算 0.5——中英混排时
    行宽仍然均匀。
    """

    def width(ch: str) -> float:
        return 0.5 if ord(ch) < 0x2E80 else 1.0

    # 可以跟在断点后面的"收尾标点"：断在这些字符之后最自然。
    closers = "，。、；：）】》？！%·—…"
    lines: list[str] = []
    line = ""
    line_w = 0.0
    for ch in text:
        w = width(ch)
        if line_w + w > max_chars and line:
            # 顶到行宽上限：回退到本行最后一个"收尾标点"之后断行，
            # 找不到就硬断。
            cut = -1
            for i, c in enumerate(line):
                if c in closers and i + 1 < len(line):
                    cut = i + 1
            if cut > 0:
                lines.append(line[:cut])
                line = line[cut:] + ch
                line_w = sum(width(c) for c in line)
            else:
                lines.append(line)
                line, line_w = ch, w
        else:
            line += ch
            line_w += w
    if line:
        lines.append(line)
    return "\n".join(lines)


class NarrationBar(VGroup):
    """底部字幕条：半透明底板 + 自动断行的中文字幕。"""

    def __init__(self, text: str = "", **kwargs):
        super().__init__(**kwargs)
        self.raw_text = text
        if text:
            shown = wrap_cjk(text)
        else:
            shown = ""
        self.label = Text(
            shown,
            font=FONT,
            font_size=NARR_FONT_SIZE,
            line_spacing=0.45,
            color=C_TEXT,
            should_center=True,
        )
        # 底板宽度自适应文字，但不超过画面宽度；空文案时给一条细线占位。
        pad_h, pad_v = 0.55, 0.28
        if self.label.width > 0:
            board_w = min(self.label.width + 2 * pad_h, config.frame_width - 0.8)
            self.board = RoundedRectangle(
                corner_radius=0.18,
                width=board_w,
                height=self.label.height + 2 * pad_v,
                fill_color=BLACK,
                fill_opacity=0.62,
                stroke_width=0,
            )
            self.add(self.board, self.label)
        else:
            self.board = Rectangle(width=0, height=0, stroke_width=0, fill_opacity=0)
            self.add(self.board)
        # 字幕条整体贴底居中，底部留 0.35 个单位边距。
        self.to_edge(DOWN, buff=0.35)

    @property
    def char_count(self) -> int:
        """实际字符数（不含换行），供 hold() 估算阅读时长。"""
        return len(self.raw_text.replace("\n", ""))


class EpisodeScene(Scene):
    """各幕的场景基类：管理字幕条与幕标题角标。

    字幕是"单行滚动"式：一条旁白按宽度拆成若干行，say() 只显示
    首行（与动画同屏），hold() 把剩余行逐条快切展示完。这个节奏
    既不挡画面，又保证观众每行都读得到。

    子类写 construct() 时的节奏约定：
        self.say("旁白文本")   # 显示该旁白的第一行
        self.play(...)         # 配合旁白的演示动画
        self.hold()            # 轮播剩余行并逐行停留
    hold() 放在动画之后，轮播才正确——观众先看动画，再逐行读字。
    """

    def setup(self) -> None:
        # 3D 幕里字幕必须固定在镜头平面上，否则会被相机投影变形。
        self.bar = NarrationBar()
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(self.bar)
        else:
            self.add(self.bar)
        self.act_tag: VGroup | None = None
        self._lines: list[str] = [""]
        self._line_idx = 0
        self._line0_at = 0.0

    def fixed(self, mob: Mobject) -> Mobject:
        """3D 幕里把 UI 元素钉在镜头平面上；2D 幕原样返回。"""
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(mob)
        return mob

    # -- 字幕 ------------------------------------------------------------
    def say(self, text: str) -> None:
        """开始一条旁白：把文案按单行宽度拆行，**只显示第一行**。

        一条旁白可能有 2~4 行，若一次性全部摆出会挡住画面——所以
        首行与配合的动画同屏，剩余行由 hold() 逐条快切展示。
        """
        self._lines = wrap_cjk(text, NARR_MAX_CHARS).split("\n")
        self._line_idx = 0
        self._line0_at = self._now()
        self._swap_bar(self._lines[0], LINE_SWAP_TIME + 0.15)

    def _now(self) -> float:
        """场景时间轴（秒）。Cairo 渲染器在 play/wait 中精确累计。"""
        return float(getattr(self.renderer, "time", 0.0))

    def _swap_bar(self, text: str, run_time: float) -> None:
        new_bar = NarrationBar(text)
        new_bar.set_z_index(50)
        # 3D 幕：字幕属于镜头平面，必须先注册 fixed-in-frame 再做动画，
        # 否则一旦相机离开正面机位，字幕会被投影变形。
        self.fixed(new_bar)
        if self.bar.char_count == 0:
            self.play(FadeIn(new_bar, shift=UP * 0.2), run_time=run_time)
        else:
            self.play(
                FadeOut(self.bar, shift=DOWN * 0.12),
                FadeIn(new_bar, shift=UP * 0.12),
                run_time=run_time,
            )
        self.bar = new_bar

    def _line_hold(self, line: str) -> float:
        n = len(line)
        return max(LINE_HOLD_MIN, LINE_HOLD_BASE + n * LINE_HOLD_PER_CHAR)

    def hold(self, factor: float = 1.0, extra: float = 0.0) -> None:
        """把当前旁白剩余的字幕行逐条展示完。

        首行在 say() 之后的动画期间已经展示了若干秒，这里只**补足
        差额**（读字时间 - 动画已占时间），而不是整个重等一遍——
        否则一句话会因为"动画 + 重复停留"被拖到 20 秒以上。
        之后每行切换展示，停留满各自的标准时长。
        """
        lines = self._lines if self._lines else [""]
        # 动画期间若再次 hold() 而各行已轮播完，就让最后一行继续停留。
        i = min(self._line_idx, len(lines) - 1)
        need = self._line_hold(lines[i]) * factor + extra
        elapsed = self._now() - self._line0_at
        self._line_idx = i + 1
        gap = max(0.0, need - elapsed)
        if gap > 0:  # manim 不接受 wait(0)
            self.wait(gap)
        for i in range(self._line_idx, len(lines)):
            self._swap_bar(lines[i], LINE_SWAP_TIME)
            self._line_idx = i + 1
            self.wait(self._line_hold(lines[i]) * factor + extra)

    # -- 幕标题 ------------------------------------------------------------
    def act_title(self, kicker: str, title: str, hold_s: float = 1.6) -> None:
        """幕标题开场：居中大字停留，然后缩小成左上角角标常驻。"""
        banner = (
            VGroup(
                Text(kicker, font=FONT, font_size=30, color=C_HL),
                Text(title, font=FONT, font_size=52, weight=BOLD, color=C_TEXT),
            )
            .arrange(DOWN, buff=0.45)
            .move_to(ORIGIN + UP * 0.3)
        )
        self.fixed(banner)
        self.play(FadeIn(banner, shift=UP * 0.4), run_time=0.8)
        self.wait(hold_s)

        tag = VGroup(
            Text(kicker, font=FONT, font_size=20, color=C_HL),
            Text(title, font=FONT, font_size=20, color=C_DIM),
        ).arrange(RIGHT, buff=0.3)
        tag.to_corner(UL, buff=0.45)
        if isinstance(self, ThreeDScene):
            self.add_fixed_in_frame_mobjects(tag)
        # 大字缩小滑向角标位，到位后瞬时换成清晰的小字文本。
        self.play(banner.animate.scale(0.45).move_to(tag), run_time=0.7)
        self.play(FadeOut(banner, run_time=0.2), FadeIn(tag, run_time=0.2))
        self.act_tag = tag

    # -- 清场 ------------------------------------------------------------
    def clear_visuals(self, *mobs: Mobject, keep_tag: bool = True) -> None:
        """淡出演示内容，保留字幕条与幕标题角标。"""
        targets = [m for m in mobs if m is not None]
        if not targets:
            return
        self.play(*[FadeOut(m) for m in targets], run_time=0.6)
