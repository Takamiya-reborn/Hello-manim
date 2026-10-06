"""多幕剧集的成片管线：逐幕渲染 + 无损拼接为单集 mp4。

一集视频由多个 .py 文件构成（intro + act01..actNN，一幕一文件），
"按表渲每一幕、再用 PyAV 拼成单集"是所有剧集共享的流程，集中在
这里之后，每集的 main.py 只剩三样东西：SCENES 顺序表、系列/集名、
一次 run_episode_cli() 调用。

管线做两件事：
    1. 按顺序渲染每一幕为独立片段（segments/，可用 --only 单独
       重渲某一幕，其余片段沿用缓存）；
    2. 用 PyAV 把片段无损拼接（stream copy，不重新编码）成
       artifacts/videos/<系列>/<集名>.mp4。

拼接不用 ffmpeg concat demuxer（用户机器上没有 ffmpeg），而是用
manim 自带的 PyAV 做包级拷贝：两段视频由同一编码器以相同参数产出，
直接搬 H.264 包即可，毫秒级完成且零画质损失；只需把每段的时间戳
换算到输出流时基并加上前段累计偏移。
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from importlib import import_module
from pathlib import Path

from manim import Scene, config

from hello_manim.utils.rendering import ARTIFACTS, add_render_args, require_latex


def configure_quality(quality: str, high_fps: int = 30) -> None:
    """质量别名 -> manim config。high 档帧率覆盖为 high_fps。

    manim 内置 high 是 1080p60，对无快速运动的数学动画，60fps 只
    带来双倍渲染时间，画面几乎没有差别，故默认覆盖为 30fps。
    """
    config.media_dir = str(ARTIFACTS / "media")
    if quality == "low":
        config.quality = "low_quality"
    elif quality == "medium":
        config.quality = "medium_quality"
    else:  # high
        config.quality = "high_quality"
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_rate = high_fps


def render_episode(
    scenes: list[tuple[str, str]],
    *,
    series: str,
    episode: str,
    quality: str = "low",
    only: list[str] | None = None,
) -> list[Path]:
    """渲染（或补渲）各幕，返回按成片顺序排列的片段路径。

    scenes 是 (文件名, 场景类名) 的列表，顺序即成片顺序。
    """
    require_latex()
    configure_quality(quality)
    segments_dir = ARTIFACTS / "videos" / series / episode / "segments"
    targets = scenes if only is None else [s for s in scenes if s[0] in only]
    if not targets:
        raise SystemExit(f"--only 没有匹配任何一幕，可选: {', '.join(k for k, _ in scenes)}")

    for key, class_name in targets:
        module = import_module(f"hello_manim.{series}.{episode}.{key}")
        scene_class = getattr(module, class_name)
        # 与 rendering.render_lesson 相同的坑：多场景渲染前必须显式
        # 重置 output_file，否则第二幕会复用并覆盖第一幕的文件名。
        config.output_file = f"{key}.mp4"
        scene = scene_class()
        scene.render()
        movie = Path(scene.renderer.file_writer.movie_file_path)
        segments_dir.mkdir(parents=True, exist_ok=True)
        target = segments_dir / f"{key}.mp4"
        if movie.resolve() != target.resolve():
            target.unlink(missing_ok=True)
            movie.rename(target)
        print(f"片段已生成: {target}")
    return [
        segments_dir / f"{key}.mp4"
        for key, _ in scenes
        if (segments_dir / f"{key}.mp4").exists()
    ]


def concat_videos(segments: list[Path], out_path: Path) -> None:
    """PyAV 包级拷贝拼接：时间戳换算 + 前段偏移，不重编码。"""
    import av

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out = av.open(str(out_path), "w")
    out_stream = None
    offset = 0  # 已拼接内容的总时长，单位 = 输出流 time_base
    try:
        for seg in segments:
            with av.open(str(seg)) as src:
                stream = src.streams.video[0]
                if out_stream is None:
                    out_stream = out.add_stream_from_template(stream)
                conv = Fraction(stream.time_base) / Fraction(out_stream.time_base)
                for packet in src.demux(stream):
                    if packet.dts is None:
                        continue
                    if packet.pts is not None:
                        packet.pts = offset + round(packet.pts * conv)
                    packet.dts = offset + round(packet.dts * conv)
                    packet.stream = out_stream
                    out.mux(packet)
                offset += round(stream.duration * conv)
    finally:
        out.close()
    print(f"成片已拼接: {out_path}")


def run_episode_cli(scenes: list[tuple[str, str]], *, series: str, episode: str) -> None:
    """剧集 main.py 的标准入口：建 parser、渲染、拼接、按需预览。"""
    # Windows 重定向时默认 GBK，manim logger 写 UTF-8，混流必乱码。
    import sys

    for stream in (sys.stdout, sys.stderr):
        if stream is not None:
            stream.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description=f"{series} {episode} 成片（多幕渲染 + 拼接）")
    add_render_args(parser)
    parser.add_argument(
        "--only",
        help="只重渲指定幕（逗号分隔，如 intro,act03），其余片段沿用缓存，最后重新拼接",
    )
    args = parser.parse_args()
    only = [s.strip() for s in args.only.split(",")] if args.only else None

    segments = render_episode(
        scenes, series=series, episode=episode, quality=args.quality, only=only
    )
    final_video = ARTIFACTS / "videos" / series / f"{episode}.mp4"
    concat_videos(segments, final_video)
    if args.preview:
        import os

        os.startfile(final_video)
