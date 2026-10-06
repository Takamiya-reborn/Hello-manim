"""第 6 课：LaTeX 数学排版与逐步推导——3Blue1Brown 的招牌手法。

本课要回答三个问题：
    1. 为什么只有这一课需要安装 LaTeX？
    2. MathTex 的"子串拆分"是干什么的？
    3. TransformMatchingTex 凭什么比整体 Transform 自然？

原理速览：
    MathTex 的管线需要两个外部程序：latex 把 TeX 源码编译成
    dvi，dvisvgm 再把 dvi 转成矢量 SVG。manim 读取 SVG 里的
    glyph 路径生成 Mobject——所以它不是"渲染图片"，而是
    真正的矢量对象，可以逐个字符上色和变形。
    substrings_to_isolate 把公式拆成独立子 Mobject：拆开后
    才能局部上色、局部变换。TransformMatchingTex 按 token
    配对做渐变——相同的部分原地保留，只动真正变化的部分，
    这正是"逐步推导"看起来自然的原因。
    没有 LaTeX 环境时本课 main() 会检测并给出安装指引，
    其余课程完全不受影响。

最短运行：
    uv run hello-manim base 06
"""

import argparse
import shutil

from manim import *

from hello_manim.utils.rendering import add_render_args, latex_available, render_lesson


class Pythagoras(Scene):
    def construct(self) -> None:
        # 字符串是标准 LaTeX 数学语法（用原始字符串避免转义）。
        # 拆成子串后，eq[0] = "a^2"、eq[1] = "+"……
        # 每一段都是可独立操作的 Mobject。
        eq1 = MathTex("a^2", "+", "b^2", "=", "c^2")
        eq1.set_color_by_tex("c^2", YELLOW)
        self.play(Write(eq1))

        # 目标等式：同样的 token 拆分方式，配对才有依据。
        eq2 = MathTex("c^2", "=", "a^2", "+", "b^2")
        eq2.set_color_by_tex("c^2", YELLOW)

        # TransformMatchingTex 按 token 配对："c^2" 从等号右侧
        # 滑到左侧，"+" 和 "=" 原地保留，其余部分依次归位——
        # 对比整体 Transform 的"全部形变"，观感自然得多。
        self.play(TransformMatchingTex(eq1, eq2))

        # 拆分的另一个用途：给局部加强调标记。
        box = SurroundingRectangle(eq2[0], color=YELLOW, buff=0.15)
        self.play(Create(box))
        self.wait(1)


def check_latex() -> bool:
    """检测 LaTeX 环境；缺失时打印安装指引而不是甩原始报错。"""
    # 共享探测逻辑在 rendering.py：会顺手把装完没重开终端的
    # MiKTeX 默认安装位置补进 PATH。
    if latex_available():
        return True
    missing = [name for name in ("latex", "dvisvgm") if shutil.which(name) is None]
    if missing:
        print("第 6 课需要 LaTeX 环境，但找不到以下命令: " + ", ".join(missing))
        print()
        print("安装方式：")
        print("  Windows: winget install MiKTeX.MiKTeX（安装后重开终端）")
        print("  macOS:   brew install --cask mactex-no-gui")
        print("  Linux:   sudo apt install texlive dvisvgm")
        print()
        print("其余课程不依赖 LaTeX，可以先跳过本课。")
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="LaTeX 公式与逐步推导")
    add_render_args(parser)
    args = parser.parse_args()

    # 环境检查放在渲染之前：失败要早、信息要能指导行动。
    if not check_latex():
        raise SystemExit(1)

    render_lesson("base", "06", [Pythagoras], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
