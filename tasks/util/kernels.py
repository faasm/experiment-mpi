from os.path import join
from tasks.util.env import EXAMPLES_DOCKER_DIR, PLOTS_ROOT, RESULTS_DIR

# -------------------
# All Kernels
# -------------------

KERNELS_DOCKER_DIR = join(EXAMPLES_DOCKER_DIR, "Kernels")
KERNELS_WASM_DIR = join(KERNELS_DOCKER_DIR, "build", "wasm")
KERNELS_NATIVE_DIR = join(KERNELS_DOCKER_DIR, "build", "native")

# -------------------
# MPI Kernels
# -------------------

MPI_KERNELS_FAASM_USER = "kernels-mpi"
MPI_KERNELS_FAASM_FUNCS = [
    "p2p",
    "sparse",
    "transpose",
    "reduce",
    # nstream: some spurious errors
    "nstream",
    "stencil",
]

# Experiment parameters
MPI_KERNELS_EXPERIMENT_NPROCS = [2, 4, 6, 8, 10, 12, 14, 16]

MPI_KERNELS_PLOTS_DIR = join(PLOTS_ROOT, "kernels-mpi")
MPI_KERNELS_RESULTS_DIR = join(RESULTS_DIR, "kernels-mpi")

# -------------------
# OpenMP Kernels
# -------------------

OPENMP_KERNELS_DOCKER_DIR = join(EXAMPLES_DOCKER_DIR, "Kernels")
OPENMP_KERNELS = ["global", "p2p", "sparse", "nstream", "reduce", "dgemm"]
OPENMP_KERNELS_FAASM_USER = "kernels-omp"

OPENMP_KERNELS_PLOTS_DIR = join(PLOTS_ROOT, "kernels-omp")
OPENMP_KERNELS_RESULTS_DIR = join(RESULTS_DIR, "kernels-omp")
