# file: plot_usage_variation.py
# Purpose: Reproduce the two-panel figure:
# (a) Histogram of per-invocation CPU usage for a single function
# (b) Distribution of per-function standard deviation of CPU usage across many functions
#
# Usage:
#   python plot_usage_variation.py
#
# Notes:
# - This script generates synthetic data to illustrate the figure.
# - If you have real data, replace the synthetic generation with your arrays and call `plot_figure(...)`.

import os
import numpy as np
import matplotlib.pyplot as plt

RNG_SEED = 2025

def synth_single_function_cpu_usage(n=5000, rng=None):
    """
    Simulate per-invocation CPU usage for a single function.
    We use a mixture to reflect heterogeneous execution paths (heavy tails + multi-modality).
    Returns:
        cpu (np.ndarray): shape (n,), nonnegative usage values.
    """
    if rng is None:
        rng = np.random.default_rng(RNG_SEED)

    # Mixture of log-normal components (nonnegative) to induce a broad, possibly multi-modal distribution
    weights = np.array([0.55, 0.30, 0.15])
    comps_mu = np.array([-1.1, -0.1, 0.6])   # log-space means
    comps_sigma = np.array([0.35, 0.25, 0.40])

    z = rng.choice(len(weights), size=n, p=weights)
    cpu = rng.lognormal(mean=comps_mu[z], sigma=comps_sigma[z])
    return cpu


def synth_many_functions_std(num_functions=400, min_inv=300, max_inv=4000, rng=None):
    """
    Simulate many functions, each with its own invocation-level CPU usage distribution.
    We compute the per-function standard deviation, then return the list of stds.
    Returns:
        stds (np.ndarray): shape (num_functions,)
    """
    if rng is None:
        rng = np.random.default_rng(RNG_SEED + 1)

    stds = []
    for _ in range(num_functions):
        n_i = rng.integers(min_inv, max_inv + 1)

        # Randomize each function's "base" scale and variability
        # - base_scale controls the overall magnitude (mean) of usage
        # - var_scale controls variability; use a lognormal to ensure most > 0 but with a long tail
        base_scale = rng.lognormal(mean=-0.4, sigma=0.5)  # typical means around e.g., 0.6–1.5 in linear space
        var_scale = rng.lognormal(mean=-1.0, sigma=0.6)   # many low-variance, some high-variance functions

        # With some probability, give the function a multi-modal profile
        if rng.random() < 0.35:
            weights = np.array([0.65, 0.35])
            # Components scaled from the base_scale; variability modulated by var_scale
            mu1 = np.log(max(1e-6, 0.6 * base_scale))
            mu2 = np.log(max(1e-6, 1.6 * base_scale))
            sigma1 = 0.25 + 0.6 * var_scale
            sigma2 = 0.30 + 0.8 * var_scale

            z = rng.choice([0, 1], size=n_i, p=weights)
            cpu_i = np.empty(n_i)
            cpu_i[z == 0] = rng.lognormal(mean=mu1, sigma=sigma1, size=(z == 0).sum())
            cpu_i[z == 1] = rng.lognormal(mean=mu2, sigma=sigma2, size=(z == 1).sum())
        else:
            mu = np.log(max(1e-6, base_scale))
            sigma = 0.25 + 0.9 * var_scale
            cpu_i = rng.lognormal(mean=mu, sigma=sigma, size=n_i)

        stds.append(cpu_i.std(ddof=1))

    return np.array(stds)


def plot_figure(single_cpu, per_function_stds, save_path="./usage_variation.pdf"):
    """
    Plot the two-panel figure:
      (a) Per-invocation CPU usage histogram (single function)
      (b) Histogram of per-function standard deviations across many functions
    """
    dirpath = os.path.dirname(save_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    plt.style.use("seaborn-v0_8-whitegrid")
    # Use Arial font globally and increase font sizes
    plt.rcParams["font.family"] = "Arial"
    plt.rcParams["font.size"] = 16
    plt.rcParams["axes.labelsize"] = 18
    plt.rcParams["xtick.labelsize"] = 15
    plt.rcParams["ytick.labelsize"] = 15
    plt.rcParams["legend.fontsize"] = 15

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), constrained_layout=True)
    fig.set_constrained_layout_pads(w_pad=0.08, h_pad=0.08, wspace=0.08, hspace=0.08)

    # Panel (a): single function per-invocation CPU usage
    ax = axes[0]
    ax.hist(single_cpu, bins="fd", color="#4C72B0", alpha=0.9, density=True, edgecolor="white", linewidth=0.3)
    ax.set_xlabel("CPU usage")
    ax.set_ylabel("Density")
    # Label (a), centered below the axis (outside)
    # ax.text(
    #     0.5, -0.30, "(a) FUNC-A Per-invocation CPU usage",
    #     transform=ax.transAxes, ha="center", va="top",
    #     fontsize=16, fontweight="bold", clip_on=False
    # )

    # Panel (b): distribution of per-function std of CPU usage
    ax = axes[1]
    ax.hist(per_function_stds, bins="fd", color="#55A868", alpha=0.9, density=True, edgecolor="white", linewidth=0.3)
    ax.set_xlabel("Standard deviation of CPU usage")
    ax.set_ylabel("Density")
    # Label (b), centered below the axis (outside)
    # ax.text(
    #     0.5, -0.30, "(b) Distribution of per-function std",
    #     transform=ax.transAxes, ha="center", va="top",
    #     fontsize=16, fontweight="bold", clip_on=False
    # )

    # Optional: tidy x-lims to focus on the bulk mass
    xmax_a = np.quantile(single_cpu, 0.995)
    axes[0].set_xlim(left=0, right=xmax_a)
    xmax_b = np.quantile(per_function_stds, 0.995)
    axes[1].set_xlim(left=0, right=xmax_b)

    # Save without suptitle
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Saved figure to: {save_path}")


def main():
    rng = np.random.default_rng(RNG_SEED)
    single_cpu = synth_single_function_cpu_usage(n=6000, rng=rng)
    per_function_stds = synth_many_functions_std(num_functions=500, min_inv=300, max_inv=5000, rng=rng)
    plot_figure(single_cpu, per_function_stds)

if __name__ == "__main__":
    main()