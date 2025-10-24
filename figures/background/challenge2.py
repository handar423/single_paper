#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

OUT_DIR = "./"
os.makedirs(OUT_DIR, exist_ok=True)


def draw_eviction_amplification(out_path: str) -> None:
    """
    Left subfigure: eviction amplification when a large sandbox upscales and
    evicts many small sandboxes.
    """
    fig, ax = plt.subplots(figsize=(6, 2.4), dpi=200)

    # Node capacity as a horizontal bin (1D for clarity).
    node_w = 10.0
    node_h = 1.2
    ax.add_patch(
        Rectangle((0, 0), node_w, node_h, fill=False, lw=1.5, ec="black")
    )

    # Small sandboxes on the left.
    small_w = 1.1
    small_h = 0.9
    small_xs = [0.2, 1.5, 2.8, 4.1]
    for i, x in enumerate(small_xs):
        ax.add_patch(
            Rectangle(
                (x, 0.15), small_w, small_h, fc="#74add1", ec="#4575b4", lw=1
            )
        )
        ax.text(
            x + small_w / 2.0, 0.6, f"S{i+1}", ha="center", va="center",
            fontsize=8, color="#103b66"
        )

    # A large sandbox on the right that needs to grow.
    large_x = 6.0
    large_w = 3.0
    ax.add_patch(
        Rectangle(
            (large_x, 0.15), large_w, small_h, fc="#fdae61",
            ec="#f46d43", lw=1.2
        )
    )
    ax.text(
        large_x + large_w / 2.0, 0.6, "L", ha="center", va="center",
        fontsize=9, color="#7a2e12", fontweight="bold"
    )

    # Desired growth (dashed overlay) encroaches into small sandboxes.
    grow_w = 5.0
    ax.add_patch(
        Rectangle(
            (large_x, 0.15), grow_w, small_h, fill=False, lw=1.2,
            ls="--", ec="#d73027"
        )
    )

    # Mark evicted small sandboxes overlapped by growth area.
    overlap_x = large_x - 0.2  # growth pushes left
    for x in small_xs:
        if x + small_w > overlap_x:
            cx = x + small_w / 2.0
            cy = 0.6
            ax.text(
                cx, cy, "✕", ha="center", va="center", fontsize=12,
                color="#b2182b", fontweight="bold"
            )

    # Arrow indicating upscale growth.
    ax.add_patch(
        FancyArrow(
            large_x + large_w, 1.05, 1.6, 0.0, width=0.03,
            head_width=0.18, head_length=0.25, color="#d73027"
        )
    )
    ax.text(
        large_x + large_w + 1.9, 1.05, "Upscale", ha="left",
        va="center", fontsize=8, color="#b2182b"
    )

    ax.set_xlim(-0.2, node_w + 0.2)
    ax.set_ylim(-0.1, node_h + 0.2)
    ax.axis("off")
    ax.set_title(
        "Eviction amplification: one large upscale evicts many small pods",
        fontsize=10
    )
    fig.tight_layout(pad=0.4)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def draw_resource_stranding(out_path: str) -> None:
    """
    Right subfigure: resource stranding when placement ignores multi-resource
    balance (CPU vs. Memory).
    """
    fig, ax = plt.subplots(figsize=(3.8, 3.8), dpi=200)

    # 2D bin: CPU (x) by Memory (y). Capacity 10 x 10.
    cap = 10.0
    ax.add_patch(
        Rectangle((0, 0), cap, cap, fill=False, lw=1.5, ec="black")
    )

    # Two placed pods with different CPU:Mem ratios.
    # Pod A: CPU heavy, low memory.
    ax.add_patch(
        Rectangle(
            (0, 0), 7.0, 3.0, fc="#abd9e9", ec="#2c7bb6", lw=1.0
        )
    )
    ax.text(
        3.5, 1.5, "A", ha="center", va="center", fontsize=9,
        color="#184a74", fontweight="bold"
    )

    # Pod B: memory heavy, moderate CPU, placed on right.
    ax.add_patch(
        Rectangle(
            (7.0, 0), 2.0, 6.0, fc="#fddbc7", ec="#d6604d", lw=1.0
        )
    )
    ax.text(
        8.0, 3.0, "B", ha="center", va="center", fontsize=9,
        color="#7a2e1a", fontweight="bold"
    )

    # Stranded resources (hatched): top slab (mem left, CPU mostly used)
    ax.add_patch(
        Rectangle(
            (0, 6.0), 9.0, 4.0, fill=False, hatch="///", lw=0.0,
            ec="#969696", fc="none", alpha=0.7
        )
    )
    # Right stripe (CPU left, mem mostly used)
    ax.add_patch(
        Rectangle(
            (9.0, 0), 1.0, 6.0, fill=False, hatch="\\\\\\", lw=0.0,
            ec="#969696", fc="none", alpha=0.7
        )
    )

    # A small usable corner remains (not stranded).
    ax.add_patch(
        Rectangle(
            (9.0, 6.0), 1.0, 4.0, fill=False, lw=1.0, ec="#4d4d4d"
        )
    )
    ax.text(
        9.5, 8.0, "usable", ha="center", va="center",
        fontsize=7, color="#4d4d4d"
    )

    ax.set_xlim(0, cap)
    ax.set_ylim(0, cap)
    ax.set_xlabel("CPU")
    ax.set_ylabel("Memory")
    ax.set_xticks([0, 5, 10])
    ax.set_yticks([0, 5, 10])
    ax.set_title(
        "Resource stranding without multi-resource balance", fontsize=10
    )
    fig.tight_layout(pad=0.6)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def draw_cpu_mem_ratio_hist(out_path: str, n: int = 2000) -> None:
    """
    Extra: heterogeneous CPU:Memory ratio histogram for functions.
    Uses a synthetic mixture to emulate diverse ratios.
    """
    rng = np.random.default_rng(42)
    ratios = np.concatenate([
        rng.normal(loc=0.5, scale=0.15, size=int(n * 0.35)),  # mem-heavy
        rng.normal(loc=1.0, scale=0.20, size=int(n * 0.35)),  # balanced
        rng.normal(loc=2.0, scale=0.35, size=int(n * 0.25)),  # cpu-heavy
        rng.lognormal(mean=np.log(4.0), sigma=0.35, size=int(n * 0.05)),
    ])
    ratios = ratios[ratios > 0.02]
    ratios = np.clip(ratios, 0.05, 8.0)

    fig, ax = plt.subplots(figsize=(5.6, 3.2), dpi=200)
    bins = np.geomspace(0.05, 8.0, 40)
    ax.hist(
        ratios, bins=bins, color="#74add1", edgecolor="#2c7bb6",
        alpha=0.9
    )
    ax.set_xscale("log")
    ax.set_xlabel("CPU:Memory ratio")
    ax.set_ylabel("Frequency")
    ax.set_xticks([0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_title(
        "Heterogeneous CPU:Memory ratios across functions", fontsize=10
    )
    ax.grid(True, which="both", axis="y", ls=":", alpha=0.4)
    fig.tight_layout(pad=0.6)
    fig.savefig(out_path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def main() -> None:
    draw_eviction_amplification(
        os.path.join(OUT_DIR, "challenge2_eviction_amplification.png")
    )
    draw_resource_stranding(
        os.path.join(OUT_DIR, "challenge2_stranding.png")
    )
    # Extra histogram for the paper tail figure.
    draw_cpu_mem_ratio_hist(
        os.path.join(OUT_DIR, "cpu_mem_ratio_hist.png")
    )


if __name__ == "__main__":
    main()