# Hello manim —— 用 Python 制作数学动画的教程

一套以"深入原理、落到代码"为原则的 manim 教程，分三个系列：
**base** 讲 manim 库本身怎么用；**calculus**（高等数学）与 **linalg**（线性代数）
是面向大学生的专项实战——动画讲的是数学本身，manim 是载体。

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

### calculus —— 高等数学专项（大学完整课程）

| 课                                   | 主题             | 可视化亮点                                        |
| ------------------------------------ | ---------------- | ------------------------------------------------- |
| [01](src/hello_manim/calculus/01.py) | 函数与极限       | 数列点列收敛；ε-δ 带联动；无穷小阶的快慢对比      |
| [02](src/hello_manim/calculus/02.py) | 重要极限与连续性 | (1+1/n)ⁿ 逼近 e；单位圆夹逼证 sin x/x；三类间断点 |
| [03](src/hello_manim/calculus/03.py) | 导数             | 割线滑向切线；导函数是"斜率函数"；链式法则分色    |
| [04](src/hello_manim/calculus/04.py) | 中值定理与应用   | 罗尔水平切线；拉格朗日割线平移；单调区间与洛必达  |
| [05](src/hello_manim/calculus/05.py) | 不定积分         | 原函数族平移；凑微分的颜色对应；分部积分逐步推导  |
| [06](src/hello_manim/calculus/06.py) | 定积分           | 黎曼矩形收敛；变上限积分同步生长；圆盘法体积      |
| [07](src/hello_manim/calculus/07.py) | 微分方程         | 斜率场贴合解曲线；积分因子；三种阻尼解曲线对比    |
| [08](src/hello_manim/calculus/08.py) | 多元函数微分学   | 3D 曲面切片求偏导；切平面近似；梯度垂直等高线     |
| [09](src/hello_manim/calculus/09.py) | 二重积分         | 曲顶柱体；扫描条带做累次积分；极坐标 dA=r dr dθ   |
| [10](src/hello_manim/calculus/10.py) | 无穷级数         | 正方形对分拼 1；判别法卡片；泰勒多项式逐阶贴合    |

### linalg —— 线性代数专项（大学完整课程，几何优先）

| 课                                 | 主题               | 可视化亮点                                      |
| ---------------------------------- | ------------------ | ----------------------------------------------- |
| [01](src/hello_manim/linalg/01.py) | 向量与线性组合     | 首尾相接加法；标量滑动的组合；张成空间塌缩      |
| [02](src/hello_manim/linalg/02.py) | 矩阵即线性变换     | 网格整体变形；列 = 基向量落点；基变换           |
| [03](src/hello_manim/linalg/03.py) | 矩阵乘法           | 两步复合 vs 一步；AB≠BA 的网格对比              |
| [04](src/hello_manim/linalg/04.py) | 行列式             | 正方形变平行四边形；压扁到直线；定向翻转        |
| [05](src/hello_manim/linalg/05.py) | 逆、列空间与秩     | 逆 = 撤销变换；落点被压到直线；核收缩到原点     |
| [06](src/hello_manim/linalg/06.py) | 方程组与高斯消元   | 解 = 直线交点；增广矩阵逐步消元；三种解的情形   |
| [07](src/hello_manim/linalg/07.py) | 点积、叉积与正交化 | 投影图解；平行四边形面积；Gram-Schmidt 逐步     |
| [08](src/hello_manim/linalg/08.py) | 特征值与特征向量   | 不变方向的向量；旋转无实特征值；对角化 = 纯缩放 |

学习路线建议：先把 base 01–08 读完建立 manim 世界观（静态物体 → 时间维 →
数学表达 → 空间维 → 工程），再按需进入专项系列。专项课的注释里同时讲
"数学为什么"和"manim 怎么画"，把 base 学到的 API 放进真实教学场景。
每课文件开头的 docstring 写明了"本课要回答的问题"、"原理速览"和最短运行命令。

## 环境准备

需要 [uv](https://docs.astral.sh/uv/) 和 Python 3.13+。安装 uv：

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

然后安装依赖：

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

# 线性代数第 8 课；编号可以简写，"8" 会自动补齐成 "08"
uv run hello-manim linalg 8

# 只给编号、不给系列名时，默认属于 base 系列（向后兼容）
uv run hello-manim 01
```

### 渲染参数

所有课程共用同一组渲染参数：

| 参数               | 说明                               |
| ------------------ | ---------------------------------- |
| `--quality low`    | 480p15，默认，最快，适合学习迭代   |
| `--quality medium` | 720p30                             |
| `--quality high`   | 1080p60，成片用                    |
| `--preview`        | 渲染完成后用系统默认播放器打开视频 |

### 其他运行方式

每课文件也可以独立运行（两种入口共用同一个 `main()`）：

```bash
uv run python src/hello_manim/calculus/03.py
```

也可以直接用 manim 原生命令行渲染任一课程里的场景（场景类名见各文件）：

```bash
uv run manim -pqh src/hello_manim/calculus/03.py SlopeIsDerivative
```

注意：原生命令行不走本项目的 `rendering.py`，输出会落在 manim 默认的
`media/` 目录，而不是 `artifacts/`。

## 目录约定

```
src/hello_manim/
  __init__.py  # hello-manim 命令行入口：系列 + 编号 调度
  rendering.py # 所有系列共用的渲染辅助（质量、产物目录、LaTeX 探测）
  base/        # manim 基础 8 课
  calculus/    # 高等数学专项 10 课
  linalg/      # 线性代数专项 8 课
artifacts/
  media/     # manim 中间产物（partial movie files、LaTeX 缓存），删除即失去增量渲染
  videos/    # 最终视频，按 系列/课 分目录：base/lesson01、calculus/lesson03 ...
```

首次渲染 manim 会自建缓存，之后增量渲染很快；想彻底重渲就删掉
`artifacts/media/`。整个 `artifacts/` 已加入 `.gitignore`。

## 常见问题

- **视频在哪？** `artifacts/videos/<系列>/lessonNN/` 下，文件名即场景类名。
- **提示缺少 LaTeX？** 安装 MiKTeX 后重开终端再试；本项目也会自动探测
  MiKTeX 默认安装位置。首次编译公式 MiKTeX 可能补装宏包，允许即可。
- **直接 `python` 运行课程文件时中文输出乱码？** 重定向到文件/管道时
  Windows 默认用 GBK 编码。`hello-manim` 入口已在开头统一成 UTF-8，
  优先用它；直接运行课程文件请在真实终端里看输出。
- **渲染报错说找不到 ffmpeg？** 说明装了老版本 manim。本项目的
  `manim>=0.19` 已内置 PyAV，`uv sync` 装出来的环境不会遇到。
