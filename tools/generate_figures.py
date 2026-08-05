#!/usr/bin/env python3
"""
v3 — 放大所有图片尺寸与字体，解决 Word 中显示过小的问题
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm
import numpy as np
import os

for fp in ["C:/Windows/Fonts/simhei.ttf", "C:/Windows/Fonts/simsun.ttc", "C:/Windows/Fonts/msyh.ttc"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "SimSun"]
plt.rcParams["axes.unicode_minus"] = False

DPI = 300
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
os.makedirs(OUTDIR, exist_ok=True)

# 全局字体放大：box 默认正文从 8pt 提到 12pt
FONT = 12
FONT_SMALL = 10
FONT_TINY = 9

def save(fig, name):
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", edgecolor="none", pad_inches=0.15)
    print(f"Saved: {path}")
    plt.close(fig)

def box(ax, x, y, w, h, text, color="#E8F0FE", fontsize=FONT, bold=False, edgecolor="#888888", lw=0.6):
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                       facecolor=color, edgecolor=edgecolor, linewidth=lw, zorder=2)
    ax.add_patch(r)
    wt = "bold" if bold else "normal"
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize, weight=wt, zorder=3)

def arrow(ax, x1, y1, x2, y2, color="#555555", lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw, connectionstyle="arc3,rad=0"))

def arrow_down(ax, x, y1, y2, color="#555555", lw=1.2):
    arrow(ax, x, y1, x, y2, color, lw)

def bi_arrow(ax, x1, y1, x2, y2, color="#555555", lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<->", color=color, lw=lw, connectionstyle="arc3,rad=0"))

# ============================================================
# 图9-1
# ============================================================
def fig_9_1():
    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(20, 11))
    ax_l.set_xlim(0, 10); ax_l.set_ylim(0, 12); ax_l.axis("off")
    ax_l.set_title("传统MCU终端", fontsize=18, weight="bold", pad=14)
    layers_L = [("感知层", 9, "#F1948A"),
                ("↓ 模拟信号", 8, "white"),
                ("控制层\n（固化逻辑）", 6, "#F5B7B1"),
                ("↓ 控制信号", 5, "white"),
                ("执行层", 3.5, "#F1948A")]
    for text, y, color in layers_L:
        h = 1.5 if "\n" not in text else 2.0
        c = color if color != "white" else "white"
        box(ax_l, 1.5, y, 7, h, text, color=c, fontsize=14)
    ax_l.text(5, 1.2, "单向、固化", ha="center", fontsize=12, color="gray", style="italic")

    ax_r.set_xlim(0, 10); ax_r.set_ylim(0, 12); ax_r.axis("off")
    ax_r.set_title("智能嵌入式系统", fontsize=18, weight="bold", pad=14)
    layers_R = [("感知层\n（多传感器融合）", 9.5, "#D5F5E3"),
                ("预处理层\n（降采样、滤波）", 7.8, "#ABEBC6"),
                ("事件检测层\n（特征提取、状态机）", 5.8, "#AED6F1"),
                ("分级输出层\n（选帧、压缩、协议封装）", 3.5, "#85C1E9"),
                ("协同通信层\n（USB/WiFi/BLE，双向）", 1.2, "#D7BDE2")]
    for text, y, color in layers_R:
        box(ax_r, 1, y, 8, 1.8, text, color=color, fontsize=13)
    ax_r.text(5, 0.2, "双向、自适应", ha="center", fontsize=12, color="gray", style="italic")
    save(fig, "fig_9_1.png")

# ============================================================
# 图9-2
# ============================================================
def fig_9_2():
    fig, ax = plt.subplots(figsize=(22, 8))
    ax.set_xlim(-3.5, 16); ax.set_ylim(0, 10.5); ax.axis("off")
    channels = [
        ("数据流", "（RGB565，960×720@15fps，单向）", 7.5, "#FFF9C4", "L→R",
         [("传感器", 1.2), ("MIPI-CSI", 4.0), ("V4L2 DMA", 6.8), ("PSRAM\n帧缓冲", 9.6), ("JPEG编码", 12.4)]),
        ("事件流", "（EVTF v2+JSON，离散触发，单向）", 4.5, "#E1F5FE", "L→R",
         [("算法\n模块", 1.2), ("证据\n编码", 4.5), ("USB Bridge\n发送队列", 7.8), ("USB-Serial\nTX", 11.5)]),
        ("控制流", "（JSON指令，双向←→，低带宽）", 1.5, "#FCE4EC", "R↔L",
         [("USB-Serial\nRX", 11.5), ("指令\n解析", 8.0), ("模块\n配置", 4.5), ("状态\n查询", 1.2)]),
    ]
    for ch_name, ch_desc, ch_y, ch_color, direction, nodes in channels:
        ax.axhspan(ch_y - 0.6, ch_y + 1.2, xmin=0.04, xmax=0.97, alpha=0.12, color=ch_color, zorder=0)
        ax.text(-3.0, ch_y + 0.8, ch_name, fontsize=14, weight="bold", color="#1A5276", va="center")
        ax.text(-3.0, ch_y + 0.2, ch_desc, fontsize=10, color="#555555", va="center")
        for txt, nx in nodes:
            box(ax, nx, ch_y + 0.05, 2.2, 1.1, txt, fontsize=11)
        xs = [p[1] for p in nodes]
        is_bidi = (direction == "R↔L")
        for i in range(len(xs) - 1):
            if is_bidi:
                bi_arrow(ax, xs[i] - 0.05, ch_y + 0.6, xs[i+1] + 2.25, ch_y + 0.6, "#666", 1.4)
            elif direction == "L→R":
                arrow(ax, xs[i] + 2.25, ch_y + 0.6, xs[i+1] - 0.05, ch_y + 0.6, "#666", 1.4)
            else:
                arrow(ax, xs[i] - 0.05, ch_y + 0.6, xs[i+1] + 2.25, ch_y + 0.6, "#666", 1.4)
    save(fig, "fig_9_2.png")

# ============================================================
# 图9-3
# ============================================================
def fig_9_3():
    fig, ax = plt.subplots(figsize=(20, 9))
    ax.set_xlim(-1, 17); ax.set_ylim(-0.5, 9.5); ax.axis("off")
    sys_r = FancyBboxPatch((1.5, 0.8), 13, 7.8, boxstyle="round,pad=0.25",
                           facecolor="#EBF5FB", edgecolor="#1A5276", linewidth=1.5, linestyle="--", zorder=0)
    ax.add_patch(sys_r)
    ax.text(8, 8.3, "evt_sem_P4 视觉事件前端", ha="center", fontsize=15, weight="bold", color="#1A5276")
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
        box(ax, x, y, w, h, txt, color=c, fontsize=11, bold=True)
    ax.text(-0.2, 5.0, "OV5645\nMIPI-CSI", ha="center", fontsize=12, weight="bold", color="#196F3D")
    arrow(ax, 0.3, 5.0, 1.8, 5.0, "#196F3D", 1.8)
    ax.text(16.3, 7.0, "USB CDC-ACM\n → 上位机/FS03", ha="center", fontsize=12, weight="bold", color="#922B21")
    arrow(ax, 14.6, 7.0, 15.8, 7.0, "#922B21", 1.8)
    ax.text(16.3, 4.0, "MIPI-DSI\n → LCD", ha="center", fontsize=12, weight="bold", color="#922B21")
    arrow(ax, 14.3, 2.8, 15.8, 3.5, "#922B21", 1.8)
    ax.text(8, 0.2, "Kconfig 配置系统", ha="center", fontsize=13, weight="bold", color="#6C3483")
    ax.annotate("", xy=(8, 1.8), xytext=(8, 0.6),
                arrowprops=dict(arrowstyle="<->", color="#6C3483", lw=1.5))
    save(fig, "fig_9_3.png")

# ============================================================
# 图9-4
# ============================================================
def fig_9_4():
    fig, ax = plt.subplots(figsize=(22, 9))
    ax.set_xlim(-1, 18); ax.set_ylim(0, 10.5); ax.axis("off")
    box(ax, 0.5, 3.8, 3.0, 1.8, "OV5645\nCMOS传感器", color="#D5F5E3", fontsize=13, bold=True)
    ax.text(2.0, 3.3, "MIPI-CSI 2-lane\n数据率≈160Mbps", ha="center", fontsize=10, color="#1E8449",
            bbox=dict(facecolor="white", alpha=0.85, edgecolor="none", pad=2))
    r = FancyBboxPatch((4.5, 1.5), 9.5, 7.0, boxstyle="round,pad=0.2",
                       facecolor="#EBF5FB", edgecolor="#1A5276", linewidth=1.5, zorder=0)
    ax.add_patch(r)
    ax.text(9.25, 8.1, "ESP32-P4 SoC", ha="center", fontsize=15, weight="bold", color="#1A5276")
    box(ax, 5.2, 5.5, 2.2, 1.4, "MIPI D-PHY\n→ DMA", color="#FCF3CF", fontsize=11)
    box(ax, 8.2, 5.5, 2.0, 1.4, "PSRAM\n帧缓冲", color="#FDEBD0", fontsize=11)
    box(ax, 11.0, 5.5, 2.3, 1.4, "JPEG硬件\n编码器", color="#FADBD8", fontsize=11)
    arrow(ax, 7.45, 6.2, 8.1, 6.2, "#555", 1.2)
    arrow(ax, 10.25, 6.2, 11.0, 6.2, "#555", 1.2)
    box(ax, 6.8, 2.8, 2.5, 1.4, "DMA → USB OTG", color="#FCF3CF", fontsize=11)
    arrow(ax, 9.25, 5.4, 8.0, 4.3, "#888", 1.0)
    arrow(ax, 3.5, 4.7, 4.3, 4.7, "#1E8449", 1.5)
    arrow(ax, 14.2, 6.2, 15.8, 6.2, "#922B21", 1.5)
    ax.text(17.0, 6.2, "USB 2.0 HS\nCDC-ACM\n有效≈1MB/s", ha="center", fontsize=11, color="#922B21",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"))
    arrow(ax, 9.25, 8.6, 9.25, 9.4, "#1A5276", 1.5)
    ax.text(9.25, 9.7, "MIPI-DSI 1-lane，720p LCD", ha="center", fontsize=11, color="#1A5276",
            bbox=dict(facecolor="white", alpha=0.9, edgecolor="#AED6F1", pad=3))
    save(fig, "fig_9_4.png")

# ============================================================
# 图9-5 (已有较大尺寸，维持)
# ============================================================
def fig_9_5():
    fig, ax = plt.subplots(figsize=(14, 13))
    ax.set_xlim(0, 12); ax.set_ylim(8, 24); ax.axis("off")
    y = 22.5; mid_x = 6.0; BOX_H = 1.0; GAP = 0.5
    box(ax, mid_x-2.5, y, 5, BOX_H, "ROM Bootloader → Flash Bootloader", color="#D5D8DC", fontsize=13, bold=True)
    arrow_down(ax, mid_x, y, y - GAP)
    y = y - GAP
    box(ax, mid_x-2.5, y - BOX_H, 5, BOX_H, "app_main()", color="#AED6F1", fontsize=13, bold=True)
    ax.text(0.8, y - BOX_H/2, "NVS初始化\n(含错误恢复)", fontsize=10, color="#1A5276", ha="center")
    arrow_down(ax, mid_x, y - BOX_H, y - BOX_H - GAP)
    y = y - BOX_H - GAP
    box(ax, mid_x-2.5, y - BOX_H, 5, BOX_H, "app_start()", color="#AED6F1", fontsize=13, bold=True)
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
        is_disp = "display" in func; is_last = (i == len(mods) - 1)
        ls = "dashed" if is_disp else "solid"
        r = FancyBboxPatch((mid_x-3.5, y - BOX_H), 7, BOX_H, boxstyle="round,pad=0.05",
                           facecolor=color, edgecolor="#888", linewidth=0.8, linestyle=ls, zorder=2)
        ax.add_patch(r)
        ax.text(mid_x-3.0, y - BOX_H/2, func, fontsize=12, weight="bold", va="center", zorder=3)
        ax.text(mid_x+0.8, y - BOX_H/2, desc, fontsize=10, va="center", color="#555", zorder=3)
        err_txt = "手动容错\n(WARNING)" if is_disp else "ESP_RETURN_\nON_ERROR"
        err_bg = "#FDEBD0" if is_disp else "#FADBD8"
        ax.text(10.8, y - BOX_H/2, err_txt, fontsize=9, va="center", ha="center", color="#922B21",
                bbox=dict(boxstyle="round,pad=0.2", facecolor=err_bg, alpha=0.8, edgecolor="none"), zorder=3)
        if not is_last:
            if not is_disp:
                arrow(ax, mid_x, y - BOX_H, mid_x, y - BOX_H - GAP)
            else:
                ax.plot([mid_x, mid_x], [y - BOX_H, y - BOX_H - GAP], color="#888", lw=1.0, linestyle="dashed")
            y = y - BOX_H - GAP
    save(fig, "fig_9_5.png")

# ============================================================
# 图9-6
# ============================================================
def fig_9_6():
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.set_xlim(0, 16); ax.set_ylim(0, 11); ax.axis("off")
    layers = [
        ("L0: 板级支持", 0.8, ["bsp"], "#D5F5E3"),
        ("L1: 帧元数据", 2.3, ["frame_ring"], "#ABEBC6"),
        ("L2: 触发与导出", 3.8, ["trigger", "algo_trigger", "frame_export"], "#FCF3CF"),
        ("L3: 协议与采集", 5.3, ["usb_frame_bridge", "camera_frontend"], "#AED6F1"),
        ("L4: 显示", 6.8, ["display_frontend"], "#FADBD8"),
        ("L5: 应用与诊断", 8.3, ["app", "diag"], "#D5D8DC"),
    ]
    for label, y, comps, color in layers:
        n = len(comps); total_w = 12; box_w = total_w / n - 0.5; box_h = 0.8
        for i, cname in enumerate(comps):
            x = 2.0 + i * (total_w / n)
            box(ax, x, y, box_w, box_h, cname, color=color, fontsize=12, bold=(cname in ["app", "camera_frontend"]))
        ax.text(0.3, y + box_h/2, label, fontsize=10, color="#888", va="center")
    # 依赖箭头
    arrow(ax, 8, 3.5, 8, 2.9, "#4A90D9", 2.0)
    arrow(ax, 5, 5.0, 5, 4.4, "#4A90D9", 2.0)
    arrow(ax, 3.2, 5.0, 10, 2.9, "#4A90D9", 1.8)
    arrow(ax, 8, 6.5, 10, 4.4, "#4A90D9", 1.8)
    arrow(ax, 5, 8.0, 7, 5.9, "#4A90D9", 1.8)
    arrow(ax, 8, 8.0, 8, 7.4, "#4A90D9", 1.8)
    for txt, xp, yp in [("L2依赖L1", 9.8, 3.1), ("L3依赖L1+L2", 6.5, 4.7),
                          ("camera_frontend\n→L1+L2", 9.0, 5.9), ("L5依赖L3+L4", 9.0, 7.3)]:
        ax.text(xp, yp, txt, fontsize=10, color="#4A90D9", style="italic")
    ax.text(13.5, 8.8, "diag: 只读读取\n所有组件状态",
            fontsize=9, color="#B03A2E", ha="center", style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FADBD8", edgecolor="#E6B0AA", alpha=0.9))
    save(fig, "fig_9_6.png")

# ============================================================
# 图9-7
# ============================================================
def fig_9_7():
    fig, ax = plt.subplots(figsize=(22, 5))
    ax.set_xlim(0, 17); ax.set_ylim(0, 5); ax.axis("off")
    phases = [
        ("① 生成\n传感器曝光+读出\n≈33ms", 0.3, 3.3, "#F5B7B1"),
        ("② 传输\nMIPI-CSI+DMA\n≈10ms", 3.9, 2.5, "#F0B27A"),
        ("③ 就绪\nDQBUF返回\n<0.1ms", 6.7, 1.4, "#82E0AA"),
        ("④ 消费\n算法处理≈2ms\n+JPEG编码≈20ms\n+USB入队<0.1ms", 8.4, 4.3, "#AED6F1"),
        ("⑤ 回收\nQBUF归还\n<0.1ms", 13.0, 1.4, "#A9DFBF"),
    ]
    for txt, x, w, c in phases:
        r = FancyBboxPatch((x, 1.5), w, 2.5, boxstyle="round,pad=0.12",
                           facecolor=c, edgecolor="#888", linewidth=1.0)
        ax.add_patch(r)
        ax.text(x+w/2, 3.3, txt, ha="center", fontsize=12, va="center")
    ax.axhline(y=0.7, xmin=0.02, xmax=0.98, color="#333", lw=2.0)
    ax.text(8.5, 0.15, "时间 →", ha="center", fontsize=14, weight="bold")
    ax.text(0.3, 0.55, "t0", ha="center", fontsize=11)
    ax.text(16.3, 0.55, "t0 + ~65ms", ha="center", fontsize=11)
    save(fig, "fig_9_7.png")

# ============================================================
# 图9-8
# ============================================================
def fig_9_8():
    fig, ax = plt.subplots(figsize=(22, 6.5))
    ax.set_xlim(0, 18.5); ax.set_ylim(0, 7); ax.axis("off")
    stages = [
        ("① 传感器\n输出", 0.5, "#D5F5E3", "无过载\n固定帧率"),
        ("② V4L2 DMA\n缓冲（×6）", 3.2, "#ABEBC6", "丢帧\n6缓冲全满\n时驱动丢弃"),
        ("③ 算法\n处理", 5.9, "#AED6F1", "预防性降载\n隔帧处理\n7.5fps有效"),
        ("④ JPEG\n编码", 8.6, "#85C1E9", "同步阻塞\n单帧完成\n方处理下帧"),
        ("⑤ USB证据\n队列", 11.3, "#D7BDE2", "丢帧\n队列满时\n丢弃+计数"),
        ("⑥ USB\n发送", 14.0, "#E8DAEF", "选择性反压\n主机未就绪\n时阻塞等待"),
    ]
    for txt, x, c, strat in stages:
        box(ax, x, 2.2, 2.6, 1.8, txt, color=c, fontsize=12, bold=True)
        ax.text(x+1.3, 0.5, strat, ha="center", fontsize=10, va="center",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF9E7", edgecolor="#DDDDDD", alpha=0.9))
        if x > 2:
            ax.annotate("", xy=(x-0.15, 3.1), xytext=(x-1.3, 3.1),
                        arrowprops=dict(arrowstyle="->", color="#888", lw=1.5))
    fmt_labels = ["RGB565\n960×720", "DMA\n缓冲", "Gray8\n320×240", "JPEG\n640w", "EVTF v2\n+JSON", "CDC-ACM\n≈1MB/s"]
    for x_pos, lbl in zip([1.8, 4.5, 7.2, 9.9, 12.6, 15.3], fmt_labels):
        ax.text(x_pos, 4.8, lbl, ha="center", fontsize=10, color="#1A5276",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#EBF5FB", edgecolor="#AED6F1", alpha=0.9))
    save(fig, "fig_9_8.png")

# ============================================================
# 图9-9 FSM四态转移图
# ============================================================
def fig_9_9():
    fig, ax = plt.subplots(figsize=(18, 10))
    ax.set_xlim(0, 16); ax.set_ylim(0, 12); ax.axis("off")

    # 四个状态框 (name, x, y, color)
    states = [
        ("F0_IDLE\n空闲态", 1, 7, "#D5F5E3"),
        ("F1_CANDIDATE\n候选态", 7, 7, "#FCF3CF"),
        ("F2_TRIGGERED\n触发态", 7, 2, "#FADBD8"),
        ("F5_COOLDOWN\n冷却态", 1, 2, "#E8DAEF"),
    ]
    for name, x, y, c in states:
        box(ax, x, y, 4.5, 2.0, name, color=c, fontsize=14, bold=True, lw=1.2)

    # 转移箭头
    # F0→F1: candidate=true
    arrow(ax, 5.6, 8.5, 6.8, 8.5, "#1A5276", 1.5)
    ax.text(6.2, 9.1, "candidate", fontsize=11, color="#1A5276", ha="center", weight="bold")
    # F1→F2: shadow_trigger=true
    arrow(ax, 9.3, 6.8, 9.3, 4.2, "#922B21", 1.5)
    ax.text(9.9, 5.5, "shadow_trigger", fontsize=11, color="#922B21", ha="center", weight="bold")
    # F1→F0: !candidate
    arrow(ax, 9.3, 8.2, 5.6, 8.2, "#888", 1.2)
    ax.text(7.5, 8.6, "!candidate", fontsize=10, color="#888", ha="center")
    # F2→F5: quiet>=8
    arrow(ax, 5.6, 2.5, 6.8, 2.5, "#1A5276", 1.5)
    ax.text(6.2, 3.1, "quiet_frames≥8", fontsize=11, color="#1A5276", ha="center", weight="bold")
    # F5→F0: cooldown_end
    arrow(ax, 3.3, 2.2, 3.3, 6.8, "#1A5276", 1.5)
    ax.text(2.4, 4.5, "cooldown=0", fontsize=11, color="#1A5276", ha="center", weight="bold")
    # F0→F2 (直接触发，跳过candidate)
    ax.annotate("", xy=(10.8, 3.5), xytext=(5.0, 7.5),
                arrowprops=dict(arrowstyle="->", color="#F39C12", lw=1.2, connectionstyle="arc3,rad=0.3"))
    ax.text(11.5, 5.5, "直接触发\n(罕见)", fontsize=9, color="#F39C12", ha="center", style="italic")

    # warmup标注
    ax.text(0.5, 9.5, "预热30帧\n(warmup)", fontsize=10, color="#888", ha="center", style="italic",
            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none"))
    arrow(ax, 1.5, 9.3, 3.0, 8.8, "#888", 0.8)

    ax.set_title("事件检测有限状态机（FSM）状态转移", fontsize=16, weight="bold", pad=12, color="#1A5276")
    save(fig, "fig_9_9.png")

# ============================================================
# 图9-10 滑动窗口投票示意
# ============================================================
def fig_9_10():
    fig, ax = plt.subplots(figsize=(18, 7))
    ax.set_xlim(0, 18); ax.set_ylim(0, 8); ax.axis("off")
    ax.set_title("滑动窗口投票机制（WINDOW_SIZE=5, WINDOW_HITS=3）", fontsize=16, weight="bold", pad=12, color="#1A5276")

    # 示例帧序列：0,1,1,0,1,1,1,1,0,1
    frames = [0, 1, 1, 0, 1, 1, 1, 1, 0, 1]
    for i, val in enumerate(frames):
        x = 1.5 + i * 1.5
        c = "#82E0AA" if val == 1 else "#F5B7B1"
        box(ax, x, 5.5, 1.2, 1.0, str(val), color=c, fontsize=14, bold=True)
        ax.text(x+0.6, 5.0, f"f{i}", ha="center", fontsize=9, color="#555")

    # 窗口标注
    # 时刻5 (i=5): 帧2-6 = [1,0,1,1,1] → hits=4 ≥ 3 → 触发
    # 时刻6 (i=6): 帧3-7 = [0,1,1,1,1] → hits=4 ≥ 3
    windows = [(5, 3, 8, "✓ 4≥3\n触发!"), (6, 4, 8, "✓ 4≥3\n保持")]
    for w_end, w_start, y_pos, label in windows:
        x0 = 1.5 + w_start * 1.5 - 0.3
        x1 = 1.5 + w_end * 1.5 + 0.9
        r = FancyBboxPatch((x0, 4.0), x1-x0, 0.8, boxstyle="round,pad=0.05",
                           facecolor="none", edgecolor="#E74C3C", linewidth=2.0, linestyle="dashed")
        ax.add_patch(r)
        ax.text((x0+x1)/2, 4.4, label, ha="center", fontsize=11, color="#E74C3C", weight="bold")

    # 图例
    ax.text(1.5, 3.0, "1 = 候选帧（candidate=true）", fontsize=11, color="#1E8449")
    ax.text(1.5, 2.3, "0 = 非候选帧", fontsize=11, color="#922B21")
    ax.text(1.5, 1.6, "虚线框 = 滑动窗口（5帧），框内1的个数≥3时触发事件", fontsize=11, color="#E74C3C")

    save(fig, "fig_9_10.png")

# ============================================================
# 图9-11 EVTF v1/v2帧结构对比
# ============================================================
def fig_9_11():
    """EVTF帧结构对比 — 宽幅单行布局，v1上 v2下，字段清晰可读"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(26, 12))
    fig.subplots_adjust(hspace=0.6)

    # === v1: 12 fields in one row ===
    ax1.set_xlim(0, 28); ax1.set_ylim(0, 7); ax1.axis("off")
    ax1.set_title("EVTF v1 帧结构（32字节固定帧头 + RGB565图像载荷 + 可选JSON拖车）",
                  fontsize=16, weight="bold", pad=10, color="#1A5276")

    v1 = [
        ("magic\n4B", 0.5, "#FCF3CF"), ("version\n2B", 2.5, "#FCF3CF"), ("hdr_size\n2B", 4.0, "#FCF3CF"),
        ("flags\n4B", 5.7, "#AED6F1"), ("frame_id\n4B", 7.8, "#FCF3CF"), ("timestamp\n4B", 10.0, "#FCF3CF"),
        ("width\n2B", 12.2, "#FCF3CF"), ("height\n2B", 13.5, "#FCF3CF"), ("fourcc\n4B", 15.0, "#FCF3CF"),
        ("stride\n4B", 17.2, "#FCF3CF"), ("payload_len\n4B", 19.5, "#FCF3CF"), ("checksum\n4B", 21.8, "#AED6F1"),
    ]
    for txt, x, c in v1:
        box(ax1, x, 3.8, 1.8, 1.6, txt, color=c, fontsize=10, bold=True, lw=0.6)
    # 分隔线 + 载荷/拖车标注
    ax1.axvline(x=24.2, ymin=0.2, ymax=0.85, color="#555", lw=1.5, linestyle="dotted")
    r1 = FancyBboxPatch((24.8, 4.0), 2.5, 1.2, boxstyle="round,pad=0.05",
                         facecolor="#D5F5E3", edgecolor="#888", linewidth=0.8)
    ax1.add_patch(r1); ax1.text(26.05, 4.6, "RGB565\n载荷", ha="center", fontsize=11, weight="bold")
    r2 = FancyBboxPatch((24.8, 2.4), 2.5, 1.2, boxstyle="round,pad=0.05",
                         facecolor="#E8DAEF", edgecolor="#888", linewidth=0.8, linestyle="dashed")
    ax1.add_patch(r2)
    ax1.text(26.05, 3.0, "JSON\n拖车", ha="center", fontsize=10, color="#7D3C98", weight="bold")
    ax1.text(24.5, 1.8, "(flags bit0=1时存在)", ha="center", fontsize=9, color="#7D3C98", style="italic")
    ax1.text(0.5, 2.5, "← 帧头 32B", fontsize=11, color="#555", style="italic")

    # === v2: two rows of fields ===
    ax2.set_xlim(0, 28); ax2.set_ylim(0, 8); ax2.axis("off")
    ax2.set_title("EVTF v2 帧结构（52字节扩展帧头 + JPEG图像载荷 + JSON边车）",
                  fontsize=16, weight="bold", pad=10, color="#1A5276")

    # Row 1: first 8 fields (v1-compatible portion)
    v2_r1 = [
        ("magic\n4B", 0.5, "#FCF3CF"), ("version\n2B", 2.5, "#FCF3CF"), ("hdr_size\n2B", 4.0, "#FCF3CF"),
        ("flags\n4B", 5.7, "#AED6F1"), ("src_frame\n4B", 7.8, "#FCF3CF"), ("image_id\n4B", 10.0, "#D5F5E3"),
        ("event_id\n4B", 12.2, "#D5F5E3"), ("timestamp\n4B", 14.5, "#FCF3CF"),
    ]
    for txt, x, c in v2_r1:
        box(ax2, x, 5.5, 1.8, 1.4, txt, color=c, fontsize=10, bold=True, lw=0.6)

    # Row 2: remaining 10 fields (v2 extensions)
    v2_r2 = [
        ("src_w\n2B", 0.5, "#FCF3CF"), ("src_h\n2B", 1.8, "#FCF3CF"), ("src_fourcc\n4B", 3.2, "#FCF3CF"),
        ("img_w\n2B", 5.5, "#FCF3CF"), ("img_h\n2B", 6.8, "#FCF3CF"),
        ("fmt\n2B", 8.2, "#AED6F1"), ("role\n2B", 9.5, "#AED6F1"),
        ("img_bytes\n4B", 11.0, "#D5F5E3"), ("side_bytes\n4B", 13.3, "#E8DAEF"),
        ("img_csum\n4B", 15.6, "#AED6F1"), ("side_csum\n4B", 18.0, "#AED6F1"),
    ]
    for txt, x, c in v2_r2:
        box(ax2, x, 3.0, 1.8, 1.4, txt, color=c, fontsize=9, bold=True, lw=0.6)

    # 分隔线 + JPEG/Sidecar
    ax2.axvline(x=20.5, ymin=0.15, ymax=0.9, color="#555", lw=1.5, linestyle="dotted")
    r3 = FancyBboxPatch((21.0, 5.6), 3.0, 1.2, boxstyle="round,pad=0.05",
                         facecolor="#D5F5E3", edgecolor="#888", linewidth=0.8)
    ax2.add_patch(r3); ax2.text(22.5, 6.2, "JPEG载荷", ha="center", fontsize=11, weight="bold")
    r4 = FancyBboxPatch((21.0, 3.0), 3.0, 1.2, boxstyle="round,pad=0.05",
                         facecolor="#E8DAEF", edgecolor="#888", linewidth=0.8, linestyle="dashed")
    ax2.add_patch(r4)
    ax2.text(22.5, 3.6, "JSON边车", ha="center", fontsize=10, color="#7D3C98", weight="bold")

    ax2.text(0.5, 1.2, "← 帧头 52B (Row1: 24B + Row2: 28B)", fontsize=11, color="#555", style="italic")

    # 图例
    for i, (label, x, c) in enumerate([("固定帧头字段", 0.8, "#FCF3CF"), ("校验/标志字段", 5.5, "#AED6F1"),
                          ("v2新增字段", 10.5, "#D5F5E3"), ("JSON/元数据", 15.5, "#E8DAEF")]):
        box(ax2, x, 0.3, 2.2, 0.6, "", color=c, fontsize=6, lw=0.3)
        ax2.text(x+2.5, 0.6, label, fontsize=10, va="center", color="#555")

    save(fig, "fig_9_11.png")

# ============================================================
if __name__ == "__main__":
    print("Generating Chapter 9 figures (v3 — large)...")
    fig_9_1()
    fig_9_2()
    fig_9_3()
    fig_9_4()
    fig_9_5()
    fig_9_6()
    fig_9_7()
    fig_9_8()
    fig_9_9()
    fig_9_10()
    fig_9_11()
    print("Done.")
