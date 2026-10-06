"""所有系列课程共用的渲染辅助：统一质量选项、产物目录和预览行为。

设计动机：
    "渲到哪、什么质量、渲完做什么"是所有课程共享的横切关注点。
    集中到这一个文件后，每课的 main() 只剩三行：建 parser、
    加参数、调 render_lesson，避免每个系列各自复制粘贴渲染样板
    （这正是 base 第 8 课"工程化"思想的预演）。

课程分为多个系列（base / calculus / linalg），render_lesson 的第一个
参数就是系列名，视频按 artifacts/videos/<系列>/lessonNN/ 归档。
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from manim import Scene, config

# 产物根目录，与 Hello-YOLO 的 artifacts/ 约定一致，整体加入 .gitignore。
ARTIFACTS = Path("artifacts")


def add_render_args(parser: argparse.ArgumentParser) -> None:
    """给课程自己的 parser 追加统一的渲染参数。"""
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high"],
        default="low",
        help="渲染质量：low=480p15（默认，最快）、medium=720p30、high=1080p60",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="渲染完成后用系统默认播放器打开视频",
    )


def latex_available() -> bool:
    """PATH 上（或 MiKTeX 默认安装位置）能否找到 latex 与 dvisvgm。"""
    _ensure_miktex_on_path()
    return bool(shutil.which("latex") and shutil.which("dvisvgm"))


def require_latex() -> None:
    """数学公式走 latex→dvi→dvisvgm 管线，缺 LaTeX 时给出安装指引后退出。"""
    if latex_available():
        return
    print(
        "本课的数学公式需要 LaTeX 环境，但 PATH 上找不到 latex/dvisvgm。\n"
        "Windows 请安装 MiKTeX（https://miktex.org/download），安装后重开终端；\n"
        "Linux: sudo apt install texlive dvisvgm；macOS: brew install --cask mactex-no-gui",
        file=sys.stderr,
    )
    raise SystemExit(1)


def _ensure_miktex_on_path() -> None:
    """Windows 装完 MiKTeX 不重开终端时，PATH 里还没有它——主动探测默认安装位置。

    manim 用 subprocess 调 latex/dvisvgm，子进程继承本进程的 PATH，
    所以这里改 os.environ 就能让整条渲染管线找到 TeX。
    """
    if shutil.which("latex"):
        return
    appdata = os.environ.get("LOCALAPPDATA", "")
    candidates = [
        Path(appdata) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
        Path("C:/Program Files/MiKTeX/miktex/bin/x64"),
        Path("C:/Program Files (x86)/MiKTeX/miktex/bin/x64"),
    ]
    for directory in candidates:
        if (directory / "latex.exe").is_file():
            os.environ["PATH"] = f"{directory}{os.pathsep}{os.environ['PATH']}"
            return


def render_lesson(
    series: str,
    lesson_number: str,
    scene_classes: Sequence[type[Scene]],
    quality: str = "low",
    preview: bool = False,
    needs_latex: bool = False,
) -> None:
    """按系列统一约定渲染一组场景，并把最终视频归档到 artifacts/videos/<系列>/。"""
    if needs_latex:
        require_latex()
    # media_dir 是 manim 所有中间产物（partial movie files、LaTeX 缓存）
    # 的根目录。统一收进 artifacts/ 后，缓存在多次渲染之间可以复用。
    config.media_dir = str(ARTIFACTS / "media")
    # manim 0.21 的质量别名形如 'low_quality'；CLI 上保留简短写法。
    # low_quality 即 854x480 @ 15fps，是官方对"快速迭代"的推荐档。
    config.quality = f"{quality}_quality"

    for scene_class in scene_classes:
        # 坑（一课多场景必踩）：上一场 render() 结束后，manim 会把
        # config.output_file 改写成完整路径；Scene 实例化时又把它
        # 固化进 renderer。不重置的话，第二个场景会被命名并覆盖成
        # 第一个场景的视频。必须在实例化之前显式指定输出名。
        config.output_file = scene_class.__name__
        scene = scene_class()
        scene.render()
        # render() 结束后 FileWriter 记录了最终视频的真实位置。
        movie = Path(scene.renderer.file_writer.movie_file_path)

        # 中间产物留在 artifacts/media（供缓存复用），最终视频复制到
        # 按 系列/课 分类目录，查找时不用在 media 的层级里翻。
        out_dir = ARTIFACTS / "videos" / series / f"lesson{lesson_number}"
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / movie.name
        shutil.copyfile(movie, target)
        print(f"视频已生成: {target}")

        if preview:
            _open_with_default_player(target)


def _open_with_default_player(path: Path) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(path)
    elif system == "Darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)
