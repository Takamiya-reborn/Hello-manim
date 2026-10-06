"""可复用的几何构件：与具体课程内容无关的空间图形。"""

from __future__ import annotations

import numpy as np
from manim import ManimColor, Polygon, VGroup


def parallelepiped(
    u: np.ndarray, v: np.ndarray, w: np.ndarray, color: ManimColor, opacity: float = 0.35
) -> VGroup:
    """由三个棱向量张成的平行六面体：六个四边形面。"""
    O = np.zeros(3)
    corners = {
        "o": O, "u": u, "v": v, "w": w,
        "uv": u + v, "uw": u + w, "vw": v + w, "uvw": u + v + w,
    }
    quads = [
        ("o", "u", "uv", "v"),      # 底面（u, v 张成）
        ("w", "uw", "uvw", "vw"),   # 顶面
        ("o", "u", "uw", "w"),      # u, w 面
        ("v", "uv", "uvw", "vw"),   # 平行面
        ("o", "v", "vw", "w"),      # v, w 面
        ("u", "uv", "uvw", "uw"),   # 平行面
    ]
    faces = VGroup()
    for q in quads:
        faces.add(
            Polygon(
                *[corners[k] for k in q],
                fill_color=color,
                fill_opacity=opacity,
                stroke_color=color,
                stroke_width=1.5,
            )
        )
    return faces
