"""hello-manim 命令行入口：按 系列 + 课程编号 调度对应的教程脚本。

用法：
    uv run hello-manim base 01              # manim 基础第 1 课
    uv run hello-manim calculus 03          # 高等数学第 3 课
    uv run hello-manim linalg 02 --quality medium
    uv run hello-manim 01                   # 只给编号时默认 base 系列
    uv run hello-manim                      # 打印课程列表

每课文件仍然可以独立运行（uv run python src/hello_manim/base/01.py），
因为每课自带 if __name__ == "__main__" 块——两种入口共用同一个 main()。
"""

import sys
from importlib import import_module

# 系列 -> (展示名, 课程编号 -> 一句话简介)。
# 编号是系列内的调度键；dict 在 Python 3.7+ 保持插入顺序，
# 列表展示顺序即定义顺序。
SERIES: dict[str, tuple[str, dict[str, str]]] = {
    "base": (
        "manim 基础（库的使用方法）",
        {
            "01": "第一个场景：Scene 与 Mobject 的世界观",
            "02": "图形、文字与布局",
            "03": "动画的本质：play() 与插值",
            "04": "ValueTracker 与 updater：参数驱动的动画",
            "05": "坐标系与函数图像",
            "06": "LaTeX 数学排版与逐步推导（需要 LaTeX 环境）",
            "07": "相机与 3D 场景",
            "08": "工程化：工厂、自定义动画与渲染配置",
        },
    ),
    "calculus": (
        "高等数学专项（大学完整课程，需要 LaTeX 环境）",
        {
            "01": "函数与极限：数列极限、ε-N 语言与无穷小",
            "02": "两个重要极限与函数的连续性",
            "03": "导数：定义、几何意义与求导法则",
            "04": "微分中值定理与导数的应用",
            "05": "不定积分：原函数、换元法与分部积分",
            "06": "定积分：黎曼和、牛顿-莱布尼茨公式与求积",
            "07": "微分方程：可分离变量、一阶线性与二阶常系数",
            "08": "多元函数微分学：偏导数、全微分与梯度",
            "09": "二重积分：累次积分、极坐标与体积",
            "10": "无穷级数：收敛判别、幂级数与泰勒展开",
        },
    ),
    "linalg": (
        "线性代数专项（大学完整课程，几何优先，需要 LaTeX 环境）",
        {
            "01": "向量：线性组合、张成空间与线性相关",
            "02": "矩阵即线性变换：旋转、缩放与基",
            "03": "矩阵乘法：变换的复合与顺序",
            "04": "行列式：面积与体积的缩放因子",
            "05": "逆矩阵、列空间与零空间：秩的几何意义",
            "06": "线性方程组与高斯消元",
            "07": "点积、叉积与正交化",
            "08": "特征值与特征向量：变换的不变方向",
        },
    ),
}

# "linalg" 等别名 -> 目录名。目录名必须同时是合法的 Python 包名。
SERIES_ALIASES: dict[str, str] = {"linear_algebra": "linalg", "la": "linalg"}
DEFAULT_SERIES = "base"


def main() -> None:
    # Windows 中文系统下，输出重定向到管道/文件时 Python 默认用 GBK，
    # 而 manim 的 logger 向 stderr 写 UTF-8，两种编码混流必然乱码。
    # 入口处统一成 UTF-8：真实终端走 Unicode API 不受影响，重定向全程一致。
    for stream in (sys.stdout, sys.stderr):
        if stream is not None:
            stream.reconfigure(encoding="utf-8")

    argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print("用法: hello-manim [系列] <课程编号> [--quality ...] [--preview]")
        print()
        for name, (title, lessons) in SERIES.items():
            print(f"[{name}] {title}")
            for number, summary in lessons.items():
                print(f"  {number}  {summary}")
        print()
        print("示例: uv run hello-manim calculus 03 --quality medium")
        return

    # 第一个参数是系列名还是编号？编号是纯数字，系列名不是——
    # 因此 "01" 走默认系列 base，"calculus 03" 显式指定系列。
    first = argv[0].lower()
    if first.isdigit():
        series, argv = DEFAULT_SERIES, argv
    elif first in SERIES:
        series, argv = first, argv[1:]
    elif first in SERIES_ALIASES:
        series, argv = SERIES_ALIASES[first], argv[1:]
    else:
        print(
            f"hello-manim: 未知系列 '{argv[0]}'，可用: {', '.join(SERIES)}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    if not argv:
        print(f"hello-manim: 系列 '{series}' 需要一个课程编号", file=sys.stderr)
        raise SystemExit(2)

    _, lessons = SERIES[series]
    number = argv[0].zfill(2)  # 允许 "1" 这种简写，补齐成 "01"
    if number not in lessons:
        print(
            f"hello-manim: 系列 '{series}' 中未知课程 '{argv[0]}'，"
            f"可用: {', '.join(lessons)}",
            file=sys.stderr,
        )
        raise SystemExit(2)

    # 课程文件名以数字开头（01.py），不是合法的 Python 标识符，
    # import 语句写不出来；import_module 接受字符串，绕过语法检查
    # 直接查找模块，这是加载"非标识符模块"的标准做法。
    lesson = import_module(f"hello_manim.{series}.{number}")

    # 课程内部的 argparse 应该只看到"属于自己的"参数：
    # 去掉 系列 + 课程编号，把程序名换成 "hello-manim calculus 03"，
    # 课程内 parser.print_help() 显示的用法就是正确的。
    sys.argv = [f"hello-manim {series} {number}"] + argv[1:]
    lesson.main()


if __name__ == "__main__":
    main()
