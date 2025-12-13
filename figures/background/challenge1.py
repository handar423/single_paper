import os
import numpy as np
import matplotlib.pyplot as plt

# Ensure output directory
out_dir = "./"
os.makedirs(out_dir, exist_ok=True)

rng = np.random.default_rng(7)

# Simulated invocation demands (CPU cores, Memory GB) with three clusters
n = 240
clusters = [
    {"center": (0.3, 0.4), "scale": (0.08, 0.1),  "count": 90, "color": "#1f77b4"},
    {"center": (0.9, 1.2), "scale": (0.12, 0.18), "count": 90, "color": "#ff7f0e"},
    {"center": (1.6, 2.1), "scale": (0.15, 0.25), "count": 60, "color": "#2ca02c"},
]

xs, ys, cs = [], [], []
for c in clusters:
    x_cluster = rng.normal(c["center"][0], c["scale"][0], c["count"])
    y_cluster = rng.normal(c["center"][1], c["scale"][1], c["count"])
    xs.append(x_cluster)
    ys.append(y_cluster)
    cs.append(np.full(c["count"], c["color"], dtype=object))

x = np.concatenate(xs)
# y is generated but not used in the histogram plot; keep if needed elsewhere
y = np.clip(np.concatenate(ys), 0.15, None)

# Replace scatter/rectangles with CPU-usage histogram split by two vertical lines
fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=160)

# Histogram of CPU (vCPU): x-axis is CPU bins; y-axis is invocation frequency
bins = np.linspace(0.0, 2.4, 25)  # 24 bins across [0.0, 2.4]
counts, edges, patches = ax.hist(
    x,
    bins=bins,
    color="#8da0cb",
    alpha=0.85,
    edgecolor="white",
    linewidth=0.5,
)

# Two vertical dashed lines that split the histogram into three regions
# Choose splits to align with the three CPU-demand clusters
splits = [0.6, 1.35]
for s in splits:
    ax.axvline(s, color="black", linestyle="--", linewidth=1.2, alpha=0.9)

# --- Make the histogram bars follow a Gaussian-like shape across S/M/L ---
centers = 0.5 * (edges[:-1] + edges[1:])
bin_w = edges[1] - edges[0]

# Center the bell in the middle region and give it a spread that spans S/M/L
mu = 0.5 * (splits[0] + splits[1])  # center of middle region
sigma = (edges[-1] - edges[0]) / 6.0  # ~±3σ covers the full width

n_total = len(x)
norm_const = sigma * np.sqrt(2 * np.pi)
pdf = np.exp(-0.5 * ((centers - mu) / sigma) ** 2) / norm_const
counts_smooth = n_total * bin_w * pdf  # expected counts per bin under the Gaussian

# Override bar heights to form a Gaussian-like silhouette
for p, h in zip(patches, counts_smooth):
    p.set_height(h)

# Lightly shade the three regions and label them (S/M/L) for visual clarity
region_colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
regions = [
    (edges[0], splits[0]),
    (splits[0], splits[1]),
    (splits[1], edges[-1]),
]
labels = ["S", "M", "L"]

y_top = float(np.max(counts_smooth)) if len(counts_smooth) else 0.0
for (l, r), col, lab in zip(regions, region_colors, labels):
    ax.axvspan(l, r, color=col, alpha=0.08)
    ax.text(
        (l + r) / 2.0,
        y_top * 1.02 if y_top > 0 else 1.0,
        lab,
        ha="center",
        va="bottom",
        color=col,
        fontsize=10,
        fontweight="bold",
    )

ax.set_xlim(edges[0], edges[-1])
ax.set_ylim(0, y_top * 1.15 if y_top > 0 else 5)
ax.set_xlabel("CPU Usage")
ax.set_ylabel("Invocation frequency")
ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.5, axis="y")
ax.set_title("Invocation CPU histogram with portfolio splits")

plt.tight_layout()

out_path = os.path.join(out_dir, "challenge1_mix.pdf")
plt.savefig(out_path, dpi=160)
print(f"Saved {out_path}")