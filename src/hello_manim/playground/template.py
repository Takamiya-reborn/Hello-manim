"""playground 起手模板：复制或改名这个文件，往里写你自己的场景。

写好后运行（--preview 渲完自动打开播放器）：
    uv run hello-manim play template --preview

一个文件里可以写任意多个 Scene 子类，play 命令会把它们全部渲出来，
视频按 <场景类名>.mp4 归档到 artifacts/videos/playground/<脚本名>/ 下。
渲染参数与正式课程一致：--quality low / medium / high。
"""

from manim import *


class MyFirstScene(Scene):
    def construct(self) -> None:
        square = Square(side_length=2, color=BLUE)
        self.play(Create(square))
        self.play(square.animate.scale(1.5).set_color(YELLOW))
        self.wait(1)


class AnotherScene(Scene):
    def construct(self) -> None:
        text = Text("在这里写自己的 manim", font_size=36)
        self.play(Write(text))
        self.wait(1)
