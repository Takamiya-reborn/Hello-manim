<div align="center">

# 🎬 Hello manim

**用 Python 制作数学动画的教程** · 深入原理 · 落到代码

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Manim](https://img.shields.io/badge/Manim-0.19%2B-FC6255?logo=manim&logoColor=white)](https://www.manim.community/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?logo=uv&logoColor=white)](https://docs.astral.sh/uv/)
[![LaTeX](https://img.shields.io/badge/LaTeX-MiKTeX%20可选-008080?logo=latex&logoColor=white)](https://miktex.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](#环境准备)
[![Calculus 图谱](https://img.shields.io/badge/calculus-课程知识图谱-2E7D32?logo=bookstack&logoColor=white)](lesson_mind/calculus-mindmap.md)
[![Linalg 图谱](https://img.shields.io/badge/linalg-课程知识图谱-1565C0?logo=bookstack&logoColor=white)](lesson_mind/linalg-mindmap.md)

一套以"深入原理、落到代码"为原则的 manim 教程，分三个系列：
**base** 讲 manim 库本身怎么用；**calculus**（高等数学）与 **linalg**（线性代数）
是面向大学生的专项实战——动画讲的是数学本身，manim 是载体。

</div>

## 课程总览

### base —— manim 基础（库的使用方法）

| 课                               | 主题         | 核心原理                                                                |
| -------------------------------- | ------------ | ----------------------------------------------------------------------- |
| [01](src/hello_manim/base/01.py) | 第一个场景   | Scene 与 Mobject 的分工；原点在中心的坐标系；质量参数只改分辨率和帧率   |
| [02](src/hello_manim/base/02.py) | 图形与排版   | 描边 vs 填充两层样式；VGroup 打包后布局；Text（Pango）不依赖 LaTeX      |
| [03](src/hello_manim/base/03.py) | 动画的本质   | 动画 = 逐帧插值；rate_func 是时间轴的形状；Transform 是形变不是位移     |
| [04](src/hello_manim/base/04.py) | 参数驱动     | ValueTracker 把变化抽象成数值；always_redraw 每帧重绘；updater 生命周期 |
| [05](src/hello_manim/base/05.py) | 坐标系与图像 | c2p/p2c 双向翻译；plot 只画显函数；get_area 与滑动切线做微积分可视化    |
| [06](src/hello_manim/base/06.py) | LaTeX 推导   | latex→dvi→dvisvgm 管线；子串拆分；TransformMatchingTex 按 token 配对    |
| [07](src/hello_manim/base/07.py) | 相机与 3D    | phi/theta 机位；环境旋转；Surface 把参数方程采样成网格面                |
| [08](src/hello_manim/base/08.py) | 工程化       | 工厂函数集中样式；自定义 Animation 保持幂等；partial movie file 缓存    |

### calculus —— 微积分：把变化"拆开"与"加回"（重构中，文案已就绪）

旧版 35 课已整体下线，新版按 [lesson_mind/calculus-mindmap.md](lesson_mind/calculus-mindmap.md)
的 8 个 Episode 重建，一集一课。总故事线不变：微分与积分互为逆运算，
地基是实数完备性，安全边界是一致收敛，高维世界同一套动作重演，
最后把这套语言推远到变换、复数与微分形式：

| 课  | 主题                                    |
| --- | --------------------------------------- |
| 01  | 从"靠近"开始——函数、极限与连续          |
| 02  | 把变化放大——导数、微分与局部线性        |
| 03  | 把变化累积回来——原函数、积分与面积      |
| 04  | 让方程自己运动——常微分方程              |
| 05  | 从平面走向空间——多元函数与局部结构      |
| 06  | 沿着曲线和曲面走——向量分析              |
| 07  | 用无限叠加逼近函数——级数与 Fourier 展开 |
| 08  | 延伸——把微积分的语言继续推远            |

### linalg —— 线性代数专项（重构中：Episode01 已就位）

旧版 8 课已整体下线，新版按 [lesson_mind/linalg-mindmap.md](lesson_mind/linalg-mindmap.md)
的 6 个 Episode 重建，叙事从"行列式在方程组里长出来"开始，而不是从定义开始。
一集成一条视频：每集一个目录 `episodeNN/`（intro + act01..actNN + main.py），
`main.py` 定义幕顺序，逐幕渲染后用 PyAV 无损拼接成单集 mp4：

| 集  | 主题                             | 状态      |
| --- | -------------------------------- | --------- |
| 01  | 从线性方程组生长出来的行列式     | ✅ 已完成 |
| 02  | 线性变换的本身——矩阵             | 待建      |
| 03  | 被变换的对象——向量               | 待建      |
| 04  | 线性方程组——从消元到结构         | 待建      |
| 05  | 特征值与特征向量——寻找变换的骨架 | 待建      |
| 06  | 二次型——把几何形状写成代数       | 待建      |

学习路线建议：先把 base 01–08 读完建立 manim 世界观（静态物体 → 时间维 →
数学表达 → 空间维 → 工程），再按需进入专项系列。专项课的注释里同时讲
"数学为什么"和"manim 怎么画"，把 base 学到的 API 放进真实教学场景。
每课文件开头的 docstring 写明了"本课要回答的问题"、"原理速览"和最短运行命令。

## 环境准备

需要 [uv](https://docs.astral.sh/uv/) 和 Python 3.13+。

安装依赖：

```bash
uv sync
```

三个可选说明：

- **LaTeX（calculus / linalg 全系列和 base 第 6 课需要）**：Windows 装
  [MiKTeX](https://miktex.org/download)，安装后重开终端；装完忘了重开也没关系，
  本项目会自动探测 MiKTeX 默认安装位置。缺了不会报错崩溃——`main()` 会
  检测并给出安装指引。首次编译公式时 MiKTeX 可能弹出补装宏包的窗口，允许即可
  （命令行下则自动安装）。
- **FFmpeg 不需要单独装**：manim 0.19 起视频编码改用内置的 PyAV，开箱即用。
- **中文字体**：专项课程大量使用中文 Text，Windows 自带微软雅黑可直接渲染；
  Linux 需要安装任意中文字体（如 `fonts-noto-cjk`）。

## 快速开始

```bash
# 打印全部系列的课程列表
uv run hello-manim

# manim 基础第 1 课：默认 480p15，几秒钟渲完
uv run hello-manim base 01

# 高等数学第 3 课：提高质量，渲完自动用系统播放器打开
uv run hello-manim calculus 03 --quality medium --preview

# 线性代数 Episode01：一集一目录，多幕渲染后自动拼接成单集（1080p30 成片）
uv run hello-manim linalg 1 --quality high

# 只重渲其中一幕再重新拼接，其余片段沿用缓存
uv run hello-manim linalg 1 --only act03

# 线性代数第 2 课（尚未就位会得到提示）；编号可以简写，"2" 会自动补齐成 "02"
uv run hello-manim linalg 2

# 只给编号、不给系列名时，默认属于 base 系列（向后兼容）
uv run hello-manim 01
```

### 渲染参数

所有课程共用同一组渲染参数：

| 参数               | 说明                                     |
| ------------------ | ---------------------------------------- |
| `--quality low`    | 480p15，默认，最快，适合学习迭代         |
| `--quality medium` | 720p30                                   |
| `--quality high`   | 1080p60，成片用（linalg 剧集为 1080p30） |
| `--preview`        | 渲染完成后用系统默认播放器打开视频       |

### 其他运行方式

每课文件也可以独立运行（两种入口共用同一个 `main()`）：

```bash
uv run python src/hello_manim/base/01.py
```

linalg 的剧集入口支持只重渲某一幕后重新拼接：

```bash
uv run python -m hello_manim.linalg.episode01.main --quality high --only act03
```

也可以直接用 manim 原生命令行渲染任一课程里的场景（场景类名见各文件）：

```bash
uv run manim -pqh src/hello_manim/base/01.py FirstScene
```

注意：原生命令行不走本项目的 `rendering.py`，但根目录的 `manim.cfg` 会把
输出同样指到 `artifacts/media/`；区别只在于它不做 `artifacts/videos/` 的归档整理。

## 目录约定

```
src/hello_manim/
  __init__.py  # hello-manim 命令行入口：系列 + 编号 调度
  base/        # manim 基础 8 课（一课一文件）
  calculus/    # 微积分专项（重构中，文案见 lesson_mind/calculus-mindmap.md）
  linalg/      # 线性代数专项：一集一目录 episodeNN/（intro + act + main.py）
  utils/       # 跨系列共用：渲染辅助、剧集拼接、旁白字幕、样式与小组件
lesson_mind/   # 重构期的新版课程文案底稿（知识图谱）
artifacts/
  media/     # manim 中间产物（partial movie files、LaTeX 缓存），删除即失去增量渲染
  videos/    # base 按系列/lessonNN/ 归档；linalg 成片为 系列/episodeNN.mp4，各幕片段在 episodeNN/segments/
```

首次渲染 manim 会自建缓存，之后增量渲染很快；想彻底重渲就删掉
`artifacts/media/`。整个 `artifacts/` 已加入 `.gitignore`。

## 常见问题

- **视频在哪？** 单场景课在 `artifacts/videos/<系列>/lessonNN/` 下，文件名即场景类名；
  linalg 剧集的成片在 `artifacts/videos/linalg/episodeNN.mp4`，各幕片段在同目录 `segments/` 下。
- **提示缺少 LaTeX？** 安装 MiKTeX 后重开终端再试；本项目也会自动探测
  MiKTeX 默认安装位置。首次编译公式 MiKTeX 可能补装宏包，允许即可。
- **直接 `python` 运行课程文件时中文输出乱码？** 重定向到文件/管道时
  Windows 默认用 GBK 编码。`hello-manim` 入口已在开头统一成 UTF-8，
  优先用它；直接运行课程文件请在真实终端里看输出。
- **渲染报错说找不到 ffmpeg？** 说明装了老版本 manim。本项目的
  `manim>=0.19` 已内置 PyAV，`uv sync` 装出来的环境不会遇到。
