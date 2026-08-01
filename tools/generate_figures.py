#!/usr/bin/env python3
"""
第9章插图生成脚本
生成图9-1至图9-8，输出至 ../figures/ 目录
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import matplotlib.font_manager as fm
import numpy as np
import os

# ---- 注册中文字体 ----
font_paths = [
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]
for fp in font_paths:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        print(f"Registered: {fp}")

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUTDIR, exist_ok=True)

DPI = 200
FW, FH = 12, 6  # default figure size in inches


def save(name):
    path = os.path.join(OUTDIR, name)
    plt.tight_layout(pad=0.5)
    plt.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f"Saved: {path}")
    plt.close()


def draw_box(ax, x, y, w, h, text, color="lightblue", fontsize=9, bold=False):
    """绘制一个圆角矩形文本框"""
    weight = "bold" if bold else "normal"
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          facecolor=color, edgecolor="gray", linewidth=0.8)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, weight=weight)


def draw_arrow(ax, x1, y1, x2, y2, color="black", lw=1.2, style="->"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))


# ============================================================
# 图9-1 传统嵌入式终端与智能嵌入式系统功能层次对比
# ============================================================
def fig_9_1():
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(FW, FH * 0.75))
    fig.suptitle("图9-1  传统嵌入式终端与智能嵌入式系统功能层次对比", fontsize=13, weight="bold", y=0.98)

    # 左侧 - 传统MCU终端
    ax_l.set_xlim(0, 10)
    ax_l.set_ylim(0, 12)
    ax_l.axis("off")
    ax_l.set_title("传统MCU终端", fontsize=12, weight="bold", pad=10)

    layers_L = [("感知层", 9, "lightcoral"),
                ("↓ 模拟信号", 8, "white"),
                ("控制层\n（固化逻辑）", 6, "lightsalmon"),
                ("↓ 控制信号", 5, "white"),
                ("执行层", 3.5, "lightcoral")]
    for text, y, color in layers_L:
        h = 1.2 if "\n" not in text else 1.5
        c = color if color != "white" else "white"
        draw_box(ax_l, 1.5, y, 7, h, text, color=c, fontsize=10)
    ax_l.text(5, 1.2, "单向、固化", ha="center", fontsize=9, color="gray", style="italic")

    # 右侧 - 智能嵌入式系统
    ax_r.set_xlim(0, 10)
    ax_r.set_ylim(0, 12)
    ax_r.axis("off")
    ax_r.set_title("智能嵌入式系统", fontsize=12, weight="bold", pad=10)

    layers_R = [("感知层\n（多传感器融合）", 9.5, "lightgreen"),
                ("预处理层\n（降采样、滤波）", 7.8, "palegreen"),
                ("事件检测层\n（特征提取、状态机）", 5.8, "lightblue"),
                ("分级输出层\n（选帧、压缩、协议封装）", 3.5, "lightskyblue"),
                ("协同通信层\n（USB/WiFi/BLE，双向）", 1.2, "plum")]
    for text, y, color in layers_R:
        draw_box(ax_r, 1, y, 8, 1.5, text, color=color, fontsize=9)

    ax_r.text(5, 0.2, "双向、自适应", ha="center", fontsize=9, color="gray", style="italic")

    save("fig_9_1.png")


# ============================================================
# 图9-2 evt_sem_P4三种信息流示意图
# ============================================================
def fig_9_2():
    fig, ax = plt.subplots(figsize=(FW * 1.1, FH * 0.7))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")
    fig.suptitle("图9-2  evt_sem_P4三种信息流示意图", fontsize=13, weight="bold", y=0.98)

    channels = [
        ("数据流（RGB565帧，960×720@15fps，单向）", 6.5,
         [("传感器", 0.5), ("MIPI-CSI", 3), ("V4L2\nDMA", 5.5), ("PSRAM\n缓冲", 8),
          ("JPEG\n编码", 10.5), ("USB\nQueue", 13)]),
        ("事件流（EVTF v2+JSON边车，离散触发，单向输出）", 4,
         [("算法\n模块", 1), ("证据\n编码", 4.5), ("USB Bridge\n发送队列", 8), ("USB-Serial\nTX", 12)]),
        ("控制流（JSON指令，双向，低带宽）", 1.5,
         [("USB-Serial\nRX", 12.5), ("指令\n解析", 8), ("模块\n配置", 4), ("状态\n查询", 1)]),
    ]

    for label, y, nodes in channels:
        ax.text(0.1, y + 0.4, label, fontsize=9, va="center", weight="bold", color="darkblue")
        # channel background
        ax.axhspan(y - 0.25, y + 0.85, xmin=0.02, xmax=0.98, alpha=0.08, color="gray")
        for text, x in nodes:
            draw_box(ax, x, y, 1.8, 0.7, text, fontsize=8, color="lightyellow")
        # arrows between nodes
        positions = [x for _, x in nodes]
        for i in range(len(positions) - 1):
            x1 = positions[i] + 1.8
            x2 = positions[i + 1]
            draw_arrow(ax, x1, y + 0.35, x2 - 0.15, y + 0.35, lw=1.0)

    save("fig_9_2.png")


# ============================================================
# 图9-3 evt_sem_P4系统功能划分与外部接口框图
# ============================================================
def fig_9_3():
    fig, ax = plt.subplots(figsize=(FW * 1.15, FH * 0.9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.suptitle("图9-3  evt_sem_P4系统功能划分与外部接口框图", fontsize=13, weight="bold", y=0.98)

    # 中央系统框
    sys_rect = FancyBboxPatch((1.5, 1), 13, 8, boxstyle="round,pad=0.3",
                              facecolor="aliceblue", edgecolor="navy", linewidth=1.5, linestyle="--")
    ax.add_patch(sys_rect)
    ax.text(8, 8.6, "evt_sem_P4 视觉事件前端", ha="center", fontsize=11, weight="bold", color="navy")

    # 内部模块
    modules = [
        ("摄像头驱动\n(camera_frontend)", 2, 6.5, "lightgreen"),
        ("帧缓冲管理\n(frame_ring)", 2, 4.5, "palegreen"),
        ("算法触发器\n(algo_trigger)", 5, 6.5, "lightblue"),
        ("JPEG编码器\n(硬件加速)", 5, 4.5, "lightskyblue"),
        ("USB桥接器\n(usb_frame_bridge)", 8, 6.5, "plum"),
        ("帧导出\n(frame_export)", 8, 4.5, "thistle"),
        ("诊断模块\n(diag)", 11, 6.5, "lightyellow"),
        ("显示模块\n(display_frontend)", 11, 4.5, "wheat"),
    ]
    for text, x, y, color in modules:
        draw_box(ax, x, y, 2.5, 1.5, text, color=color, fontsize=8)

    # 外部接口标注
    # 左侧输入
    ax.text(-0.3, 6.2, "OV5645\nMIPI-CSI", ha="center", fontsize=9, weight="bold", color="darkgreen")
    draw_arrow(ax, 0.5, 6.2, 1.8, 6.8, color="darkgreen", lw=1.5)

    # 右侧输出
    ax.text(17, 7, "USB CDC-ACM\n→上位机/FS03", ha="center", fontsize=9, weight="bold", color="darkred")
    draw_arrow(ax, 14.8, 7, 16.2, 7, color="darkred", lw=1.5)
    ax.text(17, 4.5, "MIPI-DSI\n→LCD", ha="center", fontsize=9, weight="bold", color="darkred")
    draw_arrow(ax, 13.8, 5, 16.2, 4.5, color="darkred", lw=1.5)

    # 下方配置
    ax.text(8, 0.3, "Kconfig 菜单配置", ha="center", fontsize=10, weight="bold", color="purple")
    draw_arrow(ax, 8, 0.7, 8, 1.3, color="purple", lw=1.2, style="<->")

    save("fig_9_3.png")


# ============================================================
# 图9-4 ESP32-P4高速外设带宽与数据流示意图
# ============================================================
def fig_9_4():
    fig, ax = plt.subplots(figsize=(FW * 1.2, FH * 0.8))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 8)
    ax.axis("off")
    fig.suptitle("图9-4  ESP32-P4高速外设带宽与数据流示意图", fontsize=13, weight="bold", y=0.98)

    # 传感器
    draw_box(ax, 0.5, 4.8, 2.5, 1.5, "OV5645\nCMOS传感器", color="lightgreen", fontsize=9)
    ax.text(1.75, 4.5, "MIPI-CSI 2-lane\n~160Mbps", ha="center", fontsize=7, color="green")

    # SoC框
    soc = FancyBboxPatch((4, 1.5), 10, 6, boxstyle="round,pad=0.2",
                          facecolor="aliceblue", edgecolor="navy", linewidth=1.5)
    ax.add_patch(soc)
    ax.text(9, 7.1, "ESP32-P4 SoC", ha="center", fontsize=11, weight="bold", color="navy")

    # 内部路径
    draw_box(ax, 4.8, 5, 2.2, 1.2, "MIPI D-PHY\n→ DMA", color="lightcyan", fontsize=8)
    draw_box(ax, 8, 5, 2, 1.2, "PSRAM\n帧缓冲", color="lightyellow", fontsize=8)
    draw_box(ax, 11, 5, 2.2, 1.2, "JPEG硬件\n编码器", color="lightsalmon", fontsize=8)

    draw_arrow(ax, 3.2, 5.5, 4.5, 5.5, lw=1)
    draw_arrow(ax, 7.2, 5.5, 7.7, 5.5, lw=1)
    draw_arrow(ax, 10.2, 5.5, 10.7, 5.5, lw=1)

    # SoC 内部下方
    draw_box(ax, 6.5, 2.2, 2.5, 1.2, "DMA →\nUSB OTG", color="lightcyan", fontsize=8)
    draw_arrow(ax, 9, 4.8, 7.75, 3.5, lw=1, color="gray")

    # 右侧输出
    draw_arrow(ax, 14.3, 5.5, 15.5, 5.5, lw=1.5, color="darkred")
    ax.text(16.5, 5.5, "USB 2.0 HS\nCDC-ACM\n~1MB/s有效", ha="center", fontsize=8, color="darkred")

    # 上方输出
    draw_arrow(ax, 9, 7.8, 9, 8.5, lw=1.5, color="darkblue")
    ax.text(9, 8.6, "MIPI-DSI 1-lane\n720p LCD", ha="center", fontsize=8, color="darkblue")

    save("fig_9_4.png")


# ============================================================
# 图9-5 evt_sem_P4固件启动流程
# ============================================================
def fig_9_5():
    fig, ax = plt.subplots(figsize=(FW * 0.75, FH * 1.3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 22)
    ax.axis("off")
    fig.suptitle("图9-5  evt_sem_P4固件启动流程", fontsize=13, weight="bold", y=0.99)

    y = 20.5

    # ROM + Flash Bootloader
    draw_box(ax, 2.5, y, 5, 1, "ROM Bootloader → Flash Bootloader", color="lightgray", fontsize=10, bold=True)
    draw_arrow(ax, 5, y - 0.1, 5, y - 1)
    y -= 1.2

    # app_main
    draw_box(ax, 2, y, 6, 1, "app_main()", color="lightblue", fontsize=10, bold=True)
    # NVS init label
    ax.text(0.3, y + 0.3, "NVS初始化\n(含错误恢复)", fontsize=7, color="darkblue", ha="center")
    draw_arrow(ax, 5, y - 0.1, 5, y - 1)
    y -= 1.2

    # app_start
    draw_box(ax, 2, y, 6, 1, "app_start()", color="lightblue", fontsize=10, bold=True)
    y -= 1.4

    modules = [
        ("bsp_init", "板级支持包", "lightgreen", "ESP_RETURN_ON_ERROR"),
        ("frame_ring_init", "帧环形缓冲", "palegreen", "ESP_RETURN_ON_ERROR"),
        ("frame_export_init", "帧导出模块", "palegreen", "ESP_RETURN_ON_ERROR"),
        ("trigger_init", "触发器模块", "lightyellow", "ESP_RETURN_ON_ERROR"),
        ("algo_trigger_init", "算法触发器", "lightblue", "ESP_RETURN_ON_ERROR"),
        ("usb_frame_bridge_start", "USB帧桥接器", "plum", "ESP_RETURN_ON_ERROR"),
        ("camera_frontend_start", "摄像头前端", "lightsalmon", "ESP_RETURN_ON_ERROR"),
        ("display_frontend_start", "显示模块(容错)", "wheat", "手动容错(WARNING)"),
        ("diag_start", "诊断模块", "lightgray", "ESP_RETURN_ON_ERROR"),
    ]

    for func, desc, color, err in modules:
        is_display = "display" in func
        edge_style = "dashed" if is_display else "solid"
        box = FancyBboxPatch((2.5, y - 0.45), 5, 0.9, boxstyle="round,pad=0.05",
                             facecolor=color, edgecolor="gray", linewidth=0.8,
                             linestyle=edge_style)
        ax.add_patch(box)
        ax.text(3, y, func, fontsize=9, weight="bold", va="center")
        ax.text(6.5, y, desc, fontsize=8, va="center", color="dimgray")
        ax.text(9.5, y, err, fontsize=7, va="center", color="darkred", ha="right",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="mistyrose", alpha=0.7))
        if not is_display:
            draw_arrow(ax, 5, y - 0.5, 5, y - 1.0)
        else:
            ax.plot([5, 5], [y - 0.5, y - 1.0], "gray", lw=1, linestyle="dashed")
        y -= 1.0

    save("fig_9_5.png")


# ============================================================
# 图9-6 evt_sem_P4组件依赖关系图
# ============================================================
def fig_9_6():
    fig, ax = plt.subplots(figsize=(FW * 1.1, FH * 0.9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis("off")
    fig.suptitle("图9-6  evt_sem_P4组件依赖关系图", fontsize=13, weight="bold", y=0.98)

    # 按层级排列组件
    # Layer 0: bsp
    draw_box(ax, 5.5, 0.3, 3, 0.8, "bsp\n(板级支持，无依赖)", color="lightgreen", fontsize=8)

    # Layer 1: frame_ring
    draw_box(ax, 5.5, 1.8, 3, 0.8, "frame_ring\n(帧元数据环形缓冲)", color="palegreen", fontsize=8)
    draw_arrow(ax, 7, 1.2, 7, 1.65, lw=0.8)

    # Layer 2: trigger, algo_trigger, frame_export
    for i, (name, desc) in enumerate([("trigger", "触发器抽象层"),
                                       ("algo_trigger", "算法触发器"),
                                       ("frame_export", "帧导出")]):
        x = 1.5 + i * 4
        draw_box(ax, x, 3.3, 3, 0.9, f"{name}\n({desc})", color="lightyellow", fontsize=8)
        draw_arrow(ax, 7, 2.7, x + 1.5, 3.15, lw=0.5, color="gray")

    # Layer 3: usb_frame_bridge
    draw_box(ax, 1.5, 5, 3, 0.9, "usb_frame_bridge\n(USB协议栈+传输)", color="plum", fontsize=8)
    draw_arrow(ax, 7, 2.7, 3, 4.85, lw=0.5, color="gray")

    # camera_frontend (spans layers 2-3)
    draw_box(ax, 9.5, 5, 3.5, 1.5, "camera_frontend\n(摄像头采集主循环)", color="lightsalmon", fontsize=9, bold=True)
    for comp_x in [3, 7, 11]:
        draw_arrow(ax, comp_x, 4.3, 11.25, 4.85, lw=0.4, color="gray")

    # Layer 4: display_frontend
    draw_box(ax, 3.5, 7, 3, 0.9, "display_frontend\n(显示+LVGL UI)", color="wheat", fontsize=8)
    draw_arrow(ax, 5.5, 5.8, 5, 6.85, lw=0.5, color="gray")

    # Layer 5: app + diag
    draw_box(ax, 1.5, 8.5, 3, 0.9, "app\n(应用入口与编排)", color="lightblue", fontsize=9, bold=True)
    draw_box(ax, 9.5, 8.5, 3.5, 0.9, "diag\n(诊断任务，读取所有组件状态)", color="lightgray", fontsize=8)

    # 依赖箭头到 app
    for x in [3, 5, 11.25]:
        draw_arrow(ax, x, 8.0, 3, 8.35, lw=0.4, color="gray")
    # diag 读取
    for x in [3, 5.5, 7, 11.25]:
        draw_arrow(ax, x, 8.0, 11.25, 8.35, lw=0.3, color="gray", style="-")

    # 图例
    ax.text(7, 9.5, "← 箭头指向依赖方向（上层依赖下层）", fontsize=8, color="gray",
            ha="center", style="italic")

    save("fig_9_6.png")


# ============================================================
# 图9-7 单帧图像在V4L2采集管线中的生命周期
# ============================================================
def fig_9_7():
    fig, ax = plt.subplots(figsize=(FW * 1.3, FH * 0.55))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 4)
    ax.axis("off")
    fig.suptitle("图9-7  单帧图像在V4L2采集管线中的生命周期", fontsize=13, weight="bold", y=0.98)

    phases = [
        ("① 生成", 0, 3.5, "传感器曝光+读出\n~33ms", "lightcoral"),
        ("② 传输", 3.8, 2.5, "MIPI-CSI+DMA写入\n~10ms", "lightsalmon"),
        ("③ 就绪", 6.6, 1.2, "DQBUF返回\n<0.1ms", "lightgreen"),
        ("④ 消费", 8.1, 4.5, "算法处理~2ms\n+JPEG编码~20ms\n+USB入队<0.1ms", "lightblue"),
        ("⑤ 回收", 12.9, 1.2, "QBUF归还\n<0.1ms", "palegreen"),
    ]

    for label, x, w, desc, color in phases:
        rect = FancyBboxPatch((x, 1.5), w, 2, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor="gray", linewidth=1)
        ax.add_patch(rect)
        ax.text(x + w/2, 3.1, label, ha="center", fontsize=10, weight="bold")
        ax.text(x + w/2, 2.5, desc, ha="center", fontsize=8, va="center")

    # 时间轴
    ax.axhline(y=0.8, xmin=0.02, xmax=0.98, color="black", lw=1.5)
    ax.text(8, 0.3, "时间 →", ha="center", fontsize=10, weight="bold")
    for x in np.linspace(0.3, 15.5, 6):
        ax.axvline(x=x, ymin=0.18, ymax=0.22, color="black", lw=0.8)
    ax.text(0.3, 0.5, "t0", ha="center", fontsize=8)
    ax.text(15.5, 0.5, "t0 + ~65ms", ha="center", fontsize=8)

    save("fig_9_7.png")


# ============================================================
# 图9-8 evt_sem_P4数据通路各阶段过载处理策略
# ============================================================
def fig_9_8():
    fig, ax = plt.subplots(figsize=(FW * 1.3, FH * 0.65))
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 6)
    ax.axis("off")
    fig.suptitle("图9-8  evt_sem_P4数据通路各阶段过载处理策略", fontsize=13, weight="bold", y=0.98)

    stages = [
        ("① 传感器\n输出", 0.3, "lightgreen", "无过载\n固定帧率"),
        ("② V4L2 DMA\n缓冲(×6)", 2.8, "palegreen", "丢帧\n6缓冲全满\n时驱动丢弃"),
        ("③ 算法\n处理", 5.3, "lightblue", "预防性降载\n隔帧处理\n7.5fps有效"),
        ("④ JPEG\n编码", 7.8, "lightskyblue", "同步阻塞\n单帧完成\n方处理下帧"),
        ("⑤ USB证据\n队列", 10.3, "plum", "丢帧\n队列满时\n丢弃+计数"),
        ("⑥ USB\n发送", 12.8, "thistle", "选择性反压\n主机未就绪\n时阻塞等待"),
    ]

    for label, x, color, strategy in stages:
        draw_box(ax, x, 2, 2, 1.8, label, color=color, fontsize=9, bold=True)
        ax.text(x + 1, 0.6, strategy, ha="center", fontsize=8, va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="lightyellow", alpha=0.8))

        # 阶段间箭头
        if x > 1:
            prev_x = stages[stages.index((label, x, color, strategy)) - 1][1]
            ax.annotate("", xy=(x - 0.1, 2.9), xytext=(prev_x + 2.1, 2.9),
                        arrowprops=dict(arrowstyle="->", color="gray", lw=1.2))

    # 顶部数据格式标注
    formats = ["RGB565\n960×720", "RGB565\nDMA缓冲", "Gray8\n320×240", "JPEG\n640w", "EVTF v2\n+JSON", "CDC-ACM\n~1MB/s"]
    for i, (x_pos, fmt) in enumerate(zip([1.3, 3.8, 6.3, 8.8, 11.3, 13.8], formats)):
        ax.text(x_pos, 4.5, fmt, ha="center", fontsize=7, color="darkblue",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="azure", edgecolor="lightblue", alpha=0.9))

    save("fig_9_8.png")


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("Generating Chapter 9 figures...")
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    fig_9_5()
    fig_9_6()
    fig_9_7()
    fig_9_8()
    print(f"All figures saved to: {OUTDIR}")
