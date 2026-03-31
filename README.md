# 植物大战僵尸 (Python/Pygame)

## 1. How to Run

### 环境要求
- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

### 启动步骤

#### 方法一：常规方式（需安装 Python）
1. **安装依赖**
   请在项目根目录下运行以下命令安装游戏所需的 Pygame 库：
   ```bash
   pip install -r backend/requirements.txt
   ```

2. **启动游戏**
   运行以下命令开始游戏：
   ```bash
   python backend/main.py
   ```

#### 方法二：免安装便携版 (Embedded Python)
无需手动安装 Python 和依赖，直接运行脚本即可自动构建并启动环境。

- **Windows 用户**: 双击运行 `run.bat`
- **Git Bash / Linux 用户**: 运行 `./run.sh`

> **注意**: 首次运行会自动下载 Python 环境（约 10MB）并安装依赖，请保持网络连接。后续运行无需联网。

## 2. Services

- **backend**: 核心游戏程序
  - 这是一个基于 Python 和 Pygame 开发的桌面单机游戏应用。
  - 代码位于 `backend/` 目录下，包含所有游戏逻辑与资源。

## 3. 测试账号

本项目为单机游戏，无需登录账号，直接运行即可体验。

## 4. 题目内容

使用 Python 语言开发的一个植物大战僵尸游戏。

---

## 项目介绍

这是一个使用 Pygame 开发的植物大战僵尸复刻版。

### 游戏操作
- **鼠标左键**: 选择植物卡片 / 放置植物 / 收集阳光
- **鼠标右键**: 取消选择植物
- **ESC**: 取消选择植物
- **P**: 暂停/继续游戏
- **R**: 重新开始游戏

### 包含植物
- 向日葵
- 豌豆射手
- 寒冰射手
- 坚果墙
- 樱桃炸弹

### 包含僵尸
- 普通僵尸
- 路障僵尸
- 铁桶僵尸

### 项目结构

```
pvz_game/
├── backend/                # 核心后端代码目录
│   ├── entities/           # 游戏实体模块
│   │   ├── plants.py       # 植物类定义 (向日葵、豌豆射手等)
│   │   ├── zombies.py      # 僵尸类定义 (普通、路障、铁桶僵尸)
│   │   ├── projectiles.py  # 投射物逻辑 (豌豆子弹等)
│   │   └── sun.py          # 阳光收集机制
│   ├── config.py           # 全局配置 (屏幕尺寸、颜色、帧率等)
│   ├── game_state.py       # 游戏状态管理 (主循环、波次控制)
│   ├── logger.py           # 日志模块
│   ├── main.py             # 程序入口
│   ├── ui.py               # 界面渲染 (按钮、血条、面板)
│   └── requirements.txt    # 项目依赖清单
├── .gitignore              # Git 忽略文件配置
└── README.md               # 项目说明文档
```
