"""第 7 课：相机与 3D——把时间维换成空间维。

本课要回答三个问题：
    1. ThreeDScene 和普通 Scene 差在哪？
    2. 相机的两个角度 phi / theta 分别控制什么？
    3. Surface 是怎么把一个参数方程变成画面的？

原理速览：
    ThreeDScene 的本质是给场景装了一个可编程的 3D 相机：
      - phi：极角（从 z 轴量起）。0 = 从正上方俯视，
        90° = 水平平视，这是 2D 场景的默认视角；
      - theta：方位角（绕 z 轴旋转）。
    set_camera_orientation 定初始机位，move_camera /
    begin_ambient_camera_rotation 让相机本身成为动画主角——
    "转一圈展示"就是后者以恒定角速度转动实现的。
    Surface 把参数方程 (u, v) → (x, y, z) 采样成网格面：
    u_range/v_range 是参数采样范围，checkerboard_colors 给
    相邻网格块交替着色，让曲面的空间走向肉眼可辨。

最短运行：
    uv run hello-manim base 07
"""

import argparse

import numpy as np
from manim import *

from hello_manim.utils.rendering import add_render_args, render_lesson


class MobiusBand(ThreeDScene):
    def construct(self) -> None:
        axes = ThreeDAxes()
        # 莫比乌斯带的标准参数方程：u 绕轴转一圈，
        # v 沿带宽方向；注意 u/2——半圈翻面正是"只有一个面"的来源。
        mobius = Surface(
            lambda u, v: np.array(
                [
                    (2 + v * np.cos(u / 2)) * np.cos(u),
                    (2 + v * np.cos(u / 2)) * np.sin(u),
                    v * np.sin(u / 2),
                ]
            ),
            u_range=[0, TAU],
            v_range=[-0.5, 0.5],
            fill_opacity=0.9,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        # 定初始机位：phi=75° 接近平视、略带俯角，theta=-45°
        # 是"斜前方 45 度"的经典展示角度。
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)
        self.play(Create(mobius), run_time=2)

        # 环境旋转：相机以恒定角速度自转，wait 的时长 = 展示时长。
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        # 相机也可以被 play 驱动：拉高到俯视角度，看清"单侧曲面"。
        # 注意 ThreeDCamera 不是普通 Mobject，没有 .animate，
        # 驱动相机要用 ThreeDScene 专属的 move_camera。
        self.move_camera(phi=15 * DEGREES)
        self.wait(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="3D 场景：相机控制与参数曲面")
    add_render_args(parser)
    args = parser.parse_args()
    render_lesson("base", "07", [MobiusBand], quality=args.quality, preview=args.preview)


if __name__ == "__main__":
    main()
