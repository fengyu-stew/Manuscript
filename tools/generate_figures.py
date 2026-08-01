#!/usr/bin/env python3
"""
第9章插图生成脚本 v2
修复：图9-2文字重叠、图9-3底部空白、图9-4标注重叠、图9-5箭头、图9-6排版
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm
import numpy as np
import os, sys

# ---- 中文字体 ----
for fp in ["C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/msyh.ttc"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

DPI = 200
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
os.makedirs(OUTDIR, exist_ok=True)


def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none", pad_inches=0.15)
    print(f"Saved: {path}")
    plt.close(fig)


def box(ax, x, y, w, h, text, color="#E8F0FE", fontsize=8, bold=False, edgecolor="#888888", lw=0.6):
    """绘制圆角文本框，返回矩形patch"""
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                       facecolor=color, edgecolor=edgecolor, linewidth=lw, zorder=2)
    ax.add_patch(r)
    wt = "bold" if bold else "normal"
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize, weight=wt, zorder=3)


def arrow(ax, x1, y1, x2, y2, color="#555555", lw=1.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, connectionstyle="arc3,rad=0"))


def arrow_down(ax, x, y1, y2, color="#555555", lw=1.0):
    arrow(ax, x, y1, x, y2, color, lw)


def arrow_right(ax, x1, x2, y, color="#555555", lw=1.0):
    arrow(ax, x1, y, x2, y, color, lw)


# ============================================================
# 图9-1 功能层次对比 — 完全还原用户选中的v1原版
# ============================================================
def fig_9_1():
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(13, 7.5))
    fig.suptitle("图9-1  传统嵌入式终端与智能嵌入式系统功能层次对比", fontsize=13, weight="bold", y=0.98)

    # 左侧 - 传统MCU终端
    ax_l.set_xlim(0, 10)
    ax_l.set_ylim(0, 12)
    ax_l.axis("off")
    ax_l.set_title("传统MCU终端", fontsize=12, weight="bold", pad=10)

    layers_L = [("感知层", 9, "#F1948A"),
                ("↓ 模拟信号", 8, "white"),
                ("控制层\n（固化逻辑）", 6, "#F5B7B1"),
                ("↓ 控制信号", 5, "white"),
                ("执行层", 3.5, "#F1948A")]
    for text, y, color in layers_L:
        h = 1.2 if "\n" not in text else 1.5
        c = color if color != "white" else "white"
        box(ax_l, 1.5, y, 7, h, text, color=c, fontsize=10)
    ax_l.text(5, 1.2, "单向、固化", ha="center", fontsize=9, color="gray", style="italic")

    # 右侧 - 智能嵌入式系统
    ax_r.set_xlim(0, 10)
    ax_r.set_ylim(0, 12)
    ax_r.axis("off")
    ax_r.set_title("智能嵌入式系统", fontsize=12, weight="bold", pad=10)

    layers_R = [("感知层\n（多传感器融合）", 9.5, "#D5F5E3"),
                ("预处理层\n（降采样、滤波）", 7.8, "#ABEBC6"),
                ("事件检测层\n（特征提取、状态机）", 5.8, "#AED6F1"),
                ("分级输出层\n（选帧、压缩、协议封装）", 3.5, "#85C1E9"),
                ("协同通信层\n（USB/WiFi/BLE，双向）", 1.2, "#D7BDE2")]
    for text, y, color in layers_R:
        box(ax_r, 1, y, 8, 1.5, text, color=color, fontsize=9)

    ax_r.text(5, 0.2, "双向、自适应", ha="center", fontsize=9, color="gray", style="italic")

    save(fig, "fig_9_1.png")


# ============================================================
# 图9-2 三种信息流 — 修复文字与模块重叠
# ============================================================
def fig_9_2():
    fig, ax = plt.subplots(figsize=(16, 5.5))
    ax.set_xlim(-3.2, 16); ax.set_ylim(0, 10.5); ax.axis("off")
    ax.set_title("图9-2  evt_sem_P4三种信息流示意图", fontsize=13, weight="bold", y=0.96)

    # 三条通道，y坐标拉开距离
    channels = [
        ("数据流", "（RGB565，960×720@15fps，单向）",
         7.5, "#FFF9C4",
         [("传感器", 1.2), ("MIPI-CSI", 4.0), ("V4L2 DMA", 6.8), ("PSRAM\n帧缓冲", 9.6), ("JPEG编码", 12.4)]),
        ("事件流", "（EVTF v2+JSON，离散触发，单向）",
         4.5, "#E1F5FE",
         [("算法\n模块", 1.2), ("证据\n编码", 4.5), ("USB Bridge\n发送队列", 7.8), ("USB-Serial\nTX", 11.5)]),
        ("控制流", "（JSON指令，双向，低带宽）",
         1.5, "#FCE4EC",
         [("USB-Serial\nRX", 11.5), ("指令\n解析", 8.0), ("模块\n配置", 4.5), ("状态\n查询", 1.2)]),
    ]

    for ch_name, ch_desc, ch_y, ch_color, nodes in channels:
        # 通道背景色带
        ax.axhspan(ch_y - 0.5, ch_y + 1.0, xmin=0.04, xmax=0.97, alpha=0.12, color=ch_color, zorder=0)
        # 通道标签放在左侧空白区，不与模块重叠
        ax.text(-2.8, ch_y + 0.6, ch_name, fontsize=10, weight="bold", color="#1A5276", va="center")
        ax.text(-2.8, ch_y + 0.1, ch_desc, fontsize=7, color="#555555", va="center")
        # 模块
        for txt, nx in nodes:
            box(ax, nx, ch_y + 0.05, 2.0, 0.9, txt, fontsize=8)
        # 模块间箭头
        xs = [p[1] for p in nodes]
        for i in range(len(xs)-1):
            arrow_right(ax, xs[i]+2.05, xs[i+1]-0.05, ch_y+0.5, "#666", 0.8)

    save(fig, "fig_9_2.png")


# ============================================================
# 图9-3 系统功能框图 — 缩小图高，消除底部空白
# ============================================================
def fig_9_3():
    fig, ax = plt.subplots(figsize=(15, 6.5))
    ax.set_xlim(-1, 17); ax.set_ylim(-0.5, 9.5); ax.axis("off")
    ax.set_title("图9-3  evt_sem_P4系统功能划分与外部接口框图", fontsize=13, weight="bold", y=0.97)

    # 中央虚线框
    sys_r = FancyBboxPatch((1.5, 0.8), 13, 7.8, boxstyle="round,pad=0.25",
                           facecolor="#EBF5FB", edgecolor="#1A5276", linewidth=1.2, linestyle="--", zorder=0)
    ax.add_patch(sys_r)
    ax.text(8, 8.3, "evt_sem_P4 视觉事件前端", ha="center", fontsize=11, weight="bold", color="#1A5276")

    # 内部模块 — 3行×3列布局
    mods = [
        (2.0, 6.3, 3.5, 1.4, "摄像头驱动\n(camera_frontend)", "#D5F5E3"),
        (6.5, 6.3, 3.5, 1.4, "算法触发器\n(algo_trigger)", "#AED6F1"),
        (11.0, 6.3, 3.0, 1.4, "USB桥接器\n(usb_frame_bridge)", "#D7BDE2"),
        (2.0, 4.2, 3.5, 1.4, "帧缓冲管理\n(frame_ring)", "#ABEBC6"),
        (6.5, 4.2, 3.5, 1.4, "JPEG编码器\n(硬件加速)", "#85C1E9"),
        (11.0, 4.2, 3.0, 1.4, "帧导出\n(frame_export)", "#E8DAEF"),
        (2.0, 2.1, 3.5, 1.4, "触发器\n(trigger)", "#FCF3CF"),
        (6.5, 2.1, 3.5, 1.4, "诊断模块\n(diag)", "#FDEBD0"),
        (11.0, 2.1, 3.0, 1.4, "显示模块\n(display_frontend)", "#FADBD8"),
    ]
    for x, y, w, h, txt, c in mods:
        box(ax, x, y, w, h, txt, color=c, fontsize=8, bold=True)

    # 左侧输入
    ax.text(-0.2, 5.0, "OV5645\nMIPI-CSI", ha="center", fontsize=9, weight="bold", color="#196F3D")
    arrow(ax, 0.3, 5.0, 1.8, 5.0, "#196F3D", 1.3)

    # 右侧输出
    ax.text(16.3, 7.0, "USB CDC-ACM\n → 上位机/FS03", ha="center", fontsize=9, weight="bold", color="#922B21")
    arrow(ax, 14.6, 7.0, 15.8, 7.0, "#922B21", 1.3)
    ax.text(16.3, 4.0, "MIPI-DSI\n → LCD", ha="center", fontsize=9, weight="bold", color="#922B21")
    arrow(ax, 14.3, 2.8, 15.8, 3.5, "#922B21", 1.3)

    # 下方配置
    ax.text(8, 0.2, "Kconfig 配置系统", ha="center", fontsize=10, weight="bold", color="#6C3483")
    ax.annotate("", xy=(8, 1.8), xytext=(8, 0.6),
                arrowprops=dict(arrowstyle="<->", color="#6C3483", lw=1.2))

    save(fig, "fig_9_3.png")


# ============================================================
# 图9-4 高速外设数据流 — 修复标注重叠
# ============================================================
def fig_9_4():
    fig, ax = plt.subplots(figsize=(16, 6.5))
    ax.set_xlim(-1, 18); ax.set_ylim(0, 10.5); ax.axis("off")
    ax.set_title("图9-4  ESP32-P4高速外设带宽与数据流示意图", fontsize=13, weight="bold", y=0.97)

    # 传感器 — 左侧
    box(ax, 0.5, 3.8, 2.8, 1.6, "OV5645\nCMOS传感器", color="#D5F5E3", fontsize=9, bold=True)
    # 带宽标注放在传感器下方
    ax.text(1.9, 3.3, "MIPI-CSI 2-lane\n数据率≈160Mbps", ha="center", fontsize=7, color="#1E8449",
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2))

    # SoC框
    r = FancyBboxPatch((4.5, 1.5), 9.5, 7.0, boxstyle="round,pad=0.2",
                       facecolor="#EBF5FB", edgecolor="#1A5276", linewidth=1.3, zorder=0)
    ax.add_patch(r)
    ax.text(9.25, 8.1, "ESP32-P4 SoC", ha="center", fontsize=11, weight="bold", color="#1A5276")

    # SoC内部模块
    box(ax, 5.2, 5.5, 2.2, 1.2, "MIPI D-PHY\n→ DMA", color="#FCF3CF", fontsize=8)
    box(ax, 8.2, 5.5, 2.0, 1.2, "PSRAM\n帧缓冲", color="#FDEBD0", fontsize=8)
    box(ax, 11.0, 5.5, 2.3, 1.2, "JPEG硬件\n编码器", color="#FADBD8", fontsize=8)

    arrow_right(ax, 7.45, 8.1, 6.1, "#555", 0.8)
    arrow_right(ax, 10.25, 11.0, 6.1, "#555", 0.8)

    # USB输出路径
    box(ax, 6.8, 2.8, 2.5, 1.2, "DMA → USB OTG", color="#FCF3CF", fontsize=8)
    arrow(ax, 9.25, 5.4, 8.0, 4.1, "#888", 0.6)

    # 传感器→SoC箭头
    arrow(ax, 3.5, 4.6, 4.3, 4.6, "#1E8449", 1.2)

    # 右侧输出 — USB
    arrow(ax, 14.2, 6.1, 15.8, 6.1, "#922B21", 1.3)
    ax.text(17.0, 6.1, "USB 2.0 HS\nCDC-ACM\n有效≈1MB/s", ha="center", fontsize=8, color="#922B21",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"))

    # 上方输出 — DSI (降低位置确保可见)
    arrow(ax, 9.25, 8.6, 9.25, 9.4, "#1A5276", 1.2)
    ax.text(9.25, 10.0, "MIPI-DSI 1-lane，720p LCD", ha="center", fontsize=8, color="#1A5276",
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="#AED6F1", pad=3))

    save(fig, "fig_9_4.png")


# ============================================================
# 图9-5 启动流程 — 修复箭头，增大间距
# ============================================================
def fig_9_5():
    fig, ax = plt.subplots(figsize=(10, 13))
    ax.set_xlim(0, 12); ax.set_ylim(0, 24); ax.axis("off")
    ax.set_title("图9-5  evt_sem_P4固件启动流程", fontsize=13, weight="bold", y=0.99)

    y = 22.5
    mid_x = 6.0
    BOX_H = 0.8  # 模块框高度
    GAP = 0.4    # 框间额外间距（箭头长度）

    # ROM Bootloader
    box(ax, mid_x-2.5, y, 5, BOX_H, "ROM Bootloader → Flash Bootloader", color="#D5D8DC", fontsize=10, bold=True)
    arrow_down(ax, mid_x, y, y - GAP)
    y = y - GAP

    # app_main
    box(ax, mid_x-2.5, y - BOX_H, 5, BOX_H, "app_main()", color="#AED6F1", fontsize=10, bold=True)
    ax.text(0.8, y - BOX_H/2, "NVS初始化\n(含错误恢复)", fontsize=7, color="#1A5276", ha="center")
    arrow_down(ax, mid_x, y - BOX_H, y - BOX_H - GAP)
    y = y - BOX_H - GAP

    # app_start
    box(ax, mid_x-2.5, y - BOX_H, 5, BOX_H, "app_start()", color="#AED6F1", fontsize=10, bold=True)
    arrow_down(ax, mid_x, y - BOX_H, y - BOX_H - GAP)
    y = y - BOX_H - GAP

    mods = [
        ("bsp_init", "板级支持包", "#D5F5E3"),
        ("frame_ring_init", "帧环形缓冲", "#ABEBC6"),
        ("frame_export_init", "帧导出模块", "#82E0AA"),
        ("trigger_init", "触发器模块", "#FCF3CF"),
        ("algo_trigger_init", "算法触发器", "#AED6F1"),
        ("usb_frame_bridge_start", "USB帧桥接器", "#D7BDE2"),
        ("camera_frontend_start", "摄像头前端", "#F5B7B1"),
        ("display_frontend_start", "显示模块 (容错)", "#FADBD8"),
        ("diag_start", "诊断模块", "#D5D8DC"),
    ]

    for i, (func, desc, color) in enumerate(mods):
        is_disp = "display" in func
        is_last = (i == len(mods) - 1)
        ls = "dashed" if is_disp else "solid"

        # 框：左下角 (mid_x-3.5, y - BOX_H)
        r = FancyBboxPatch((mid_x-3.5, y - BOX_H), 7, BOX_H, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor="#888", linewidth=0.7, linestyle=ls, zorder=2)
        ax.add_patch(r)
        ax.text(mid_x-3.0, y - BOX_H/2, func, fontsize=9, weight="bold", va="center", zorder=3)
        ax.text(mid_x+0.8, y - BOX_H/2, desc, fontsize=8, va="center", color="#555", zorder=3)

        # 错误处理策略
        if is_disp:
            err_txt = "手动容错\n(WARNING)"
            err_bg = "#FDEBD0"
        else:
            err_txt = "ESP_RETURN_\nON_ERROR"
            err_bg = "#FADBD8"
        ax.text(10.8, y - BOX_H/2, err_txt, fontsize=6.5, va="center", ha="center", color="#922B21",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=err_bg, alpha=0.8, edgecolor="none"), zorder=3)

        # 箭头：从框底到下一框顶（最后一个模块后不画箭头）
        if not is_last:
            if not is_disp:
                arrow(ax, mid_x, y - BOX_H, mid_x, y - BOX_H - GAP)
            else:
                ax.plot([mid_x, mid_x], [y - BOX_H, y - BOX_H - GAP], color="#888", lw=0.8, linestyle="dashed")
            y = y - BOX_H - GAP

    save(fig, "fig_9_5.png")


# ============================================================
# 图9-6 组件依赖图 — 重修分层布局
# ============================================================
def fig_9_6():
    fig, ax = plt.subplots(figsize=(14, 8.5))
    ax.set_xlim(0, 16); ax.set_ylim(0, 13); ax.axis("off")
    ax.set_title("图9-6  evt_sem_P4组件依赖关系图（箭头指向被依赖方）", fontsize=12, weight="bold", y=0.98)

    # 分层坐标 (layer, y)
    layers = {
        "L0": 1.0,   # bsp
        "L1": 3.0,   # frame_ring
        "L2": 5.2,   # trigger, algo_trigger, frame_export
        "L3": 7.4,   # usb_frame_bridge, camera_frontend
        "L4": 9.6,   # display_frontend
        "L5": 11.8,   # app, diag
    }

    # 画层级背景线
    for name, ly in layers.items():
        ax.axhline(y=ly, xmin=0.02, xmax=0.98, color="#CCCCCC", lw=0.5, linestyle="dotted", zorder=0)
        ax.text(0.15, ly-0.3, name, fontsize=7, color="#AAAAAA")

    # 各层组件 (name, desc, x, y, w, h, color)
    comps = [
        # L0
        ("bsp", "板级支持包", 5.5, layers["L0"]-0.3, 5, 0.8, "#D5F5E3"),
        # L1
        ("frame_ring", "帧元数据环形缓冲", 5.5, layers["L1"]-0.3, 5, 0.8, "#ABEBC6"),
        # L2
        ("trigger", "触发器抽象层", 1.5, layers["L2"]-0.3, 3.5, 0.8, "#FCF3CF"),
        ("algo_trigger", "算法触发器", 6.25, layers["L2"]-0.3, 3.5, 0.8, "#AED6F1"),
        ("frame_export", "帧导出模块", 11.0, layers["L2"]-0.3, 3.5, 0.8, "#FCF3CF"),
        # L3
        ("usb_frame_bridge", "USB协议栈与传输", 5.5, layers["L3"]-0.3, 5, 0.8, "#D7BDE2"),
        ("camera_frontend", "摄像头采集主循环", 1.5, layers["L3"]+0.5, 4, 1.2, "#F5B7B1"),
        # L4
        ("display_frontend", "显示与LVGL UI", 5.5, layers["L4"]-0.3, 5, 0.8, "#FADBD8"),
        # L5
        ("app", "应用入口与编排", 2.5, layers["L5"]-0.3, 4.5, 0.8, "#AED6F1"),
        ("diag", "诊断任务(读取所有组件)", 9.0, layers["L5"]-0.3, 5.5, 0.8, "#D5D8DC"),
    ]

    # 组件位置映射
    cpos = {}  # name -> (cx, top, bottom)
    for name, desc, x, y, w, h, color in comps:
        box(ax, x, y, w, h, f"{name}\n({desc})", color=color, fontsize=7.5, bold=("app" in name or "bsp" in name))
        cpos[name] = (x + w/2, y+h, y)  # cx, top, bottom

    # 画依赖箭头 (从上层指向下层，从调用中点向下)
    def dep_arrow(caller, callee, lw=0.6):
        if caller in cpos and callee in cpos:
            cx, _, cbot = cpos[caller]
            _, ctop, _ = cpos[callee]
            arrow(ax, cx, cbot, cpos[callee][0], ctop, "#888888", lw)

    dep_arrow("bsp", "frame_ring")  # bsp被frame_ring依赖... wait
    # 实际上 frame_ring 不依赖 bsp，但 bsp 是先决条件。让我画 frame_ring 依赖链路。

    # 正确的依赖关系：
    # L1 ← L0: 无（bsp无依赖）
    # L2 ← L1: trigger, algo_trigger, frame_export 都依赖 frame_ring
    dep_arrow("trigger", "frame_ring")
    dep_arrow("algo_trigger", "frame_ring")
    dep_arrow("frame_export", "frame_ring")

    # L3 ← L1: usb_frame_bridge 依赖 frame_ring
    dep_arrow("usb_frame_bridge", "frame_ring")

    # L3 camera_frontend 依赖很多
    for callee in ["frame_ring", "trigger", "algo_trigger", "frame_export", "usb_frame_bridge"]:
        dep_arrow("camera_frontend", callee)

    # L4 ← L2: display_frontend 依赖 algo_trigger
    dep_arrow("display_frontend", "algo_trigger")

    # L5 app 依赖 camera_frontend, display_frontend, ...
    for callee in ["camera_frontend", "display_frontend"]:
        dep_arrow("app", callee)

    # diag 读取所有组件
    for callee in ["bsp", "frame_ring", "trigger", "algo_trigger", "frame_export",
                    "usb_frame_bridge", "camera_frontend", "display_frontend"]:
        arrow(ax, cpos["diag"][0], cpos["diag"][2], cpos[callee][0], cpos[callee][1], "#CCBBBB", 0.4)

    save(fig, "fig_9_6.png")


# ============================================================
# 图9-7 帧生命周期 — 保持良好
# ============================================================
def fig_9_7():
    fig, ax = plt.subplots(figsize=(16, 3.5))
    ax.set_xlim(0, 17); ax.set_ylim(0, 5); ax.axis("off")
    ax.set_title("图9-7  单帧图像在V4L2采集管线中的生命周期", fontsize=13, weight="bold", y=0.95)

    phases = [
        ("① 生成\n传感器曝光+读出\n≈33ms", 0.3, 3.3, "#F5B7B1"),
        ("② 传输\nMIPI-CSI+DMA\n≈10ms", 3.9, 2.5, "#F0B27A"),
        ("③ 就绪\nDQBUF返回\n<0.1ms", 6.7, 1.4, "#82E0AA"),
        ("④ 消费\n算法处理≈2ms\n+JPEG编码≈20ms\n+USB入队<0.1ms", 8.4, 4.3, "#AED6F1"),
        ("⑤ 回收\nQBUF归还\n<0.1ms", 13.0, 1.4, "#A9DFBF"),
    ]

    for txt, x, w, c in phases:
        r = FancyBboxPatch((x, 1.5), w, 2.2, boxstyle="round,pad=0.12",
                           facecolor=c, edgecolor="#888", linewidth=0.8)
        ax.add_patch(r)
        ax.text(x+w/2, 3.15, txt, ha="center", fontsize=8.5, va="center")

    # 时间轴
    ax.axhline(y=0.7, xmin=0.02, xmax=0.98, color="#333", lw=1.5)
    ax.text(8.5, 0.15, "时间 →", ha="center", fontsize=10, weight="bold")
    for i, (x_pos, label) in enumerate([(0.3, "t0"), (16.3, "t0 + ~65ms")]):
        ax.axvline(x=x_pos+0.15, ymin=0.12, ymax=0.18, color="#333", lw=0.8)
        ax.text(x_pos, 0.55, label, ha="center", fontsize=8)

    save(fig, "fig_9_7.png")


# ============================================================
# 图9-8 过载策略 — 保持良好
# ============================================================
def fig_9_8():
    fig, ax = plt.subplots(figsize=(17, 5))
    ax.set_xlim(0, 18.5); ax.set_ylim(0, 7); ax.axis("off")
    ax.set_title("图9-8  evt_sem_P4数据通路各阶段过载处理策略", fontsize=13, weight="bold", y=0.96)

    stages = [
        ("① 传感器\n输出", 0.5, "#D5F5E3", "无过载\n固定帧率"),
        ("② V4L2 DMA\n缓冲（×6）", 3.2, "#ABEBC6", "丢帧\n6缓冲全满\n时驱动丢弃"),
        ("③ 算法\n处理", 5.9, "#AED6F1", "预防性降载\n隔帧处理\n7.5fps有效"),
        ("④ JPEG\n编码", 8.6, "#85C1E9", "同步阻塞\n单帧完成\n方处理下帧"),
        ("⑤ USB证据\n队列", 11.3, "#D7BDE2", "丢帧\n队列满时\n丢弃+计数"),
        ("⑥ USB\n发送", 14.0, "#E8DAEF", "选择性反压\n主机未就绪\n时阻塞等待"),
    ]

    for txt, x, c, strat in stages:
        box(ax, x, 2.2, 2.4, 1.6, txt, color=c, fontsize=9, bold=True)
        ax.text(x+1.2, 0.5, strat, ha="center", fontsize=7.5, va="center",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF9E7", edgecolor="#DDDDDD", alpha=0.9))
        # 阶段间箭头
        if x > 2:
            ax.annotate("", xy=(x-0.15, 3.0), xytext=(x-1.3, 3.0),
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.1))

    # 数据格式标注
    fmt_labels = ["RGB565\n960×720", "DMA\n缓冲", "Gray8\n320×240", "JPEG\n640w", "EVTF v2\n+JSON", "CDC-ACM\n≈1MB/s"]
    for i, (x_pos, lbl) in enumerate(zip([1.7, 4.4, 7.1, 9.8, 12.5, 15.2], fmt_labels)):
        ax.text(x_pos, 4.6, lbl, ha="center", fontsize=7.2, color="#1A5276",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#EBF5FB", edgecolor="#AED6F1", alpha=0.9))

    save(fig, "fig_9_8.png")


# ============================================================
if __name__ == "__main__":
    print("Generating Chapter 9 figures (v2)...")
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    fig_9_5()
    fig_9_6()
    fig_9_7()
    fig_9_8()
    print("Done.")
