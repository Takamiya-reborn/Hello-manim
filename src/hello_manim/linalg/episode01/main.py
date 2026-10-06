"""Episode01 成片入口：定义幕顺序，渲染与拼接交给共用管线。

用法：
    uv run python -m hello_manim.linalg.episode01.main            # 全集，480p15 快速预览
    uv run python -m hello_manim.linalg.episode01.main --quality high   # 1080p30 成片
    uv run python -m hello_manim.linalg.episode01.main --only act03     # 只重渲第三幕后重新拼接
"""

from __future__ import annotations

from hello_manim.utils.episode_render import run_episode_cli

# (文件名, 场景类名)。顺序即成片顺序。
SCENES: list[tuple[str, str]] = [
    ("intro", "EpisodeIntro"),
    ("act01", "Act01Birth"),
    ("act02", "Act02Theory"),
    ("act03", "Act03Geometry"),
    ("act04", "Act04Parity"),
    ("act05", "Act05Identity"),
]

SERIES = "linalg"
EPISODE = "episode01"


def main() -> None:
    run_episode_cli(SCENES, series=SERIES, episode=EPISODE)


if __name__ == "__main__":
    main()
