from glob import glob
from invoke import task
from matplotlib.pyplot import hlines, savefig, subplots
from numpy import arange
from os import makedirs
from os.path import join
from pandas import read_csv
from tasks.util.env import PLOTS_ROOT, PROJ_ROOT


ALL_WORKLOADS = ["compute", "network"]


def _read_results():
    results_dir = join(PROJ_ROOT, "results", "migration")
    result_dict = {}

    for csv in glob(join(results_dir, "migration_*.csv")):
        workload = csv.split("_")[-1].split(".")[0]
        if workload not in ALL_WORKLOADS:
            continue

        results = read_csv(csv)
        groupped_results = results.groupby("Check", as_index=False)

        if workload not in result_dict:
            result_dict[workload] = {}

        result_dict[workload] = {
            "checks": groupped_results.mean()["Check"].to_list(),
            "mean": groupped_results.mean()["Time"].to_list(),
            "sem": groupped_results.sem()["Time"].to_list(),
        }

    return result_dict


@task(default=True)
def plot(ctx):
    """
    Plot migration figure
    """
    migration_results = _read_results()

    do_plot("compute", migration_results)
    do_plot("network", migration_results)


def do_plot(workload, migration_results):
    plots_dir = join(PLOTS_ROOT, "migration")
    makedirs(plots_dir, exist_ok=True)
    out_file = join(plots_dir, "migration_speedup_{}.pdf".format(workload))
    fig, ax = subplots(figsize=(3, 2))
    xs = [0, 2, 4, 6, 8]
    xticks = arange(1, 6)
    width = 0.5
    idx_ref = migration_results[workload]["checks"].index(10)
    ys = []
    for x in xs:
        idx_granny = migration_results[workload]["checks"].index(x)
        ys.append(
            float(
                migration_results[workload]["mean"][idx_ref]
                / migration_results[workload]["mean"][idx_granny]
            )
        )

    ax.bar(
        xticks,
        ys,
        width,
        label=workload,
        edgecolor="black",
    )

    # Aesthetics
    ax.set_ylabel("Speed-up \n [No mig. / mig.]")
    ax.set_xlabel("% of execution when to migrate")
    ax.set_xticks(xticks)
    ax.set_xticklabels(["1 VM", "20", "40", "60", "80"])
    xlim_left = 0.5
    xlim_right = 5.5
    ax.set_xlim(left=xlim_left, right=xlim_right)

    if workload == "all-to-all":
        ax.text(
            xticks[0] - 0.1,
            1.5,
            "{:.1f}".format(ys[0]),
            rotation="vertical",
            fontsize=6,
            bbox={
                "boxstyle": "Square, pad=0.2",
                "edgecolor": "black",
                "facecolor": "white",
            },
        )
        ax.set_ylim(bottom=0, top=6)
    else:
        ax.set_ylim(bottom=0)

    hlines(1, xlim_left, xlim_right, linestyle="dashed", colors="red")
    fig.tight_layout()
    savefig(out_file, format="pdf")  # , bbox_inches="tight")
    print("Plot saved to: {}".format(out_file))
