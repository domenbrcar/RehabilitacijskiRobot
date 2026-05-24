import os
from pathlib import Path


os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parent / ".mplconfig"))

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "trajectories"
FIG = ROOT / "report" / "figures"
ARCHIVE = next(ROOT.glob("RehabilitacijskiRobot-*"), None)


TRAJECTORIES = [
    ("Premik", "premik_v1.npz"),
    ("Zogica 1", "zogica_1.npz"),
    ("Zogica 2", "zogica_2.npz"),
    ("Zogica 3", "zogica_3.npz"),
]

CMP_FILES = [
    ("Premik", "cmp_premik_v1.npz"),
    ("Zogica 1 naprej", "cmp_zogica_1_naprej.npz"),
    ("Zogica 1 nazaj", "cmp_zogica_1_nazaj.npz"),
    ("Zogica 2 naprej", "cmp_zogica_2_naprej.npz"),
    ("Zogica 2 nazaj", "cmp_zogica_2_nazaj.npz"),
    ("Zogica 3 naprej", "cmp_zogica_3_naprej.npz"),
    ("Zogica 3 nazaj", "cmp_zogica_3_nazaj.npz"),
]


def load_npz(path):
    return np.load(path, allow_pickle=True)


def savefig(name):
    FIG.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIG / name, bbox_inches="tight")
    plt.close()


def plot_trajectory_summary():
    names, samples, durations = [], [], []
    for label, filename in TRAJECTORIES:
        d = load_npz(DATA / filename)
        t = np.asarray(d["tt"]).reshape(-1)
        names.append(label)
        samples.append(len(t))
        durations.append(float(t[-1] - t[0]))

    x = np.arange(len(names))
    width = 0.38

    fig, ax1 = plt.subplots(figsize=(6.4, 3.0))
    ax2 = ax1.twinx()
    ax1.bar(x - width / 2, samples, width, color="0.25", label="st. vzorcev")
    ax2.bar(x + width / 2, durations, width, color="0.70", edgecolor="0.20", label="trajanje")
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=15, ha="right")
    ax1.set_ylabel("Stevilo vzorcev")
    ax2.set_ylabel("Trajanje [s]")
    ax1.grid(axis="y", color="0.85", linewidth=0.6)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", frameon=False)
    savefig("povzetek_trajektorij.pdf")


def plot_joint_trajectories():
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.8), sharex=False)
    styles = ["-", "--", "-.", ":", (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (1, 1))]

    for ax, (label, filename) in zip(axes.ravel(), TRAJECTORIES):
        d = load_npz(DATA / filename)
        t = np.asarray(d["tt"]).reshape(-1)
        q = np.asarray(d["qt"])
        for j in range(q.shape[1]):
            ax.plot(t - t[0], q[:, j], linestyle=styles[j], linewidth=0.9, color=str(0.15 + 0.1 * j),
                    label=f"q{j + 1}")
        ax.set_title(label, fontsize=9)
        ax.set_xlabel("t [s]")
        ax.set_ylabel("q [rad]")
        ax.grid(True, color="0.88", linewidth=0.5)

    axes[0, 0].legend(ncol=4, fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(1.1, 1.35))
    fig.tight_layout()
    savefig("trajektorije_sklepi.pdf")


def plot_cmp_norms():
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    styles = ["-", "--", ":", "-.", (0, (5, 1)), (0, (3, 1, 1, 1)), (0, (1, 1))]
    for i, (label, filename) in enumerate(CMP_FILES):
        d = load_npz(DATA / filename)
        t = np.asarray(d["t_cmp"]).reshape(-1)
        tau = np.asarray(d["tau_cmp"])
        norm = np.linalg.norm(tau, axis=1)
        ax.plot(t - t[0], norm, linestyle=styles[i], color=str(0.1 + 0.1 * i), linewidth=1.0, label=label)
    ax.set_xlabel("t [s]")
    ax.set_ylabel(r"$\|\tau_\mathrm{CMP}\|$ [Nm]")
    ax.grid(True, color="0.88", linewidth=0.5)
    ax.legend(ncol=2, fontsize=7, frameon=False)
    savefig("cmp_norme.pdf")


def plot_cmp_directions():
    pairs = [
        ("Zogica 1", "cmp_zogica_1_naprej.npz", "cmp_zogica_1_nazaj.npz"),
        ("Zogica 2", "cmp_zogica_2_naprej.npz", "cmp_zogica_2_nazaj.npz"),
        ("Zogica 3", "cmp_zogica_3_naprej.npz", "cmp_zogica_3_nazaj.npz"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.45), sharey=True)
    for ax, (label, fwd, back) in zip(axes, pairs):
        for filename, style, txt in [(fwd, "-", "naprej"), (back, "--", "nazaj")]:
            d = load_npz(DATA / filename)
            tau = np.asarray(d["tau_cmp"])
            s = np.linspace(0.0, 100.0, tau.shape[0])
            ax.plot(s, np.linalg.norm(tau, axis=1), style, color="0.15", linewidth=1.0, label=txt)
        ax.set_title(label, fontsize=9)
        ax.set_xlabel("potek giba [%]")
        ax.grid(True, color="0.88", linewidth=0.5)
    axes[0].set_ylabel(r"$\|\tau_\mathrm{CMP}\|$ [Nm]")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    savefig("cmp_smeri.pdf")


def plot_load_pilot():
    if ARCHIVE is None:
        return
    base = ARCHIVE / "RehabilitacijskiRobot"
    candidates = list(base.glob("*OŠ/ostale_trajektorije"))
    if not candidates:
        return
    data_dir = candidates[0]

    labels, no_load_dur, load_dur, no_load_speed, load_speed = [], [], [], [], []
    for i in range(2, 6):
        plain = data_dir / f"trajektorija_{i}.npz"
        loaded = data_dir / f"trajektorija_{i}_teza.npz"
        if not plain.exists() or not loaded.exists():
            continue
        d0 = load_npz(plain)
        d1 = load_npz(loaded)
        t0 = np.asarray(d0["tt"]).reshape(-1)
        t1 = np.asarray(d1["tt"]).reshape(-1)
        dq0 = np.asarray(d0["dqt"])
        dq1 = np.asarray(d1["dqt"])
        labels.append(str(i))
        no_load_dur.append(float(t0[-1] - t0[0]))
        load_dur.append(float(t1[-1] - t1[0]))
        no_load_speed.append(float(np.max(np.linalg.norm(dq0, axis=1))))
        load_speed.append(float(np.max(np.linalg.norm(dq1, axis=1))))

    if not labels:
        return

    x = np.arange(len(labels))
    width = 0.36
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7))
    axes[0].bar(x - width / 2, no_load_dur, width, color="0.25", label="brez obremenitve")
    axes[0].bar(x + width / 2, load_dur, width, color="0.75", edgecolor="0.20", label="z obremenitvijo")
    axes[0].set_ylabel("Trajanje [s]")
    axes[0].set_xlabel("pilotni par")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].grid(axis="y", color="0.88", linewidth=0.5)

    axes[1].bar(x - width / 2, no_load_speed, width, color="0.25")
    axes[1].bar(x + width / 2, load_speed, width, color="0.75", edgecolor="0.20")
    axes[1].set_ylabel(r"max $\|\dot{q}\|$ [rad/s]")
    axes[1].set_xlabel("pilotni par")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].grid(axis="y", color="0.88", linewidth=0.5)

    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    savefig("obremenitev_pilot.pdf")


def main():
    plot_trajectory_summary()
    plot_joint_trajectories()
    plot_cmp_norms()
    plot_cmp_directions()
    plot_load_pilot()


if __name__ == "__main__":
    main()
