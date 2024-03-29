from invoke import task
from os.path import join
from tasks.util.kernels import (
    KERNELS_WASM_DIR,
    MPI_KERNELS_FAASM_FUNCS,
    MPI_KERNELS_FAASM_USER,
)
from tasks.util.upload import upload_wasm


@task()
def upload(ctx):
    """
    Upload the MPI Kernels to Granny
    """
    wasm_file_details = []

    for kernel in MPI_KERNELS_FAASM_FUNCS:
        wasm_file_details.append(
            {
                "wasm_file": join(
                    KERNELS_WASM_DIR, "mpi_{}.wasm".format(kernel)
                ),
                "wasm_user": MPI_KERNELS_FAASM_USER,
                "wasm_function": kernel,
                "copies": 1,
            }
        )

    upload_wasm(wasm_file_details)
