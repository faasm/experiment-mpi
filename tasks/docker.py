from invoke import task
from os.path import join
from subprocess import run
from tasks.util.env import (
    ACR_NAME,
    FAABRIC_EXP_IMAGE_NAME,
    PROJ_ROOT,
    get_version,
)

OPENMPI_IMAGE_NAME = "openmpi"


def _get_docker_tag(img_name):
    ver = get_version()
    return "{}/{}:{}".format(ACR_NAME, img_name, ver)


def _do_container_build(name, nocache=False, push=False):
    tag_name = _get_docker_tag(name)

    if nocache:
        no_cache_str = "--no-cache"
    else:
        no_cache_str = ""

    dockerfile = join(PROJ_ROOT, "docker", "{}.dockerfile".format(name))

    build_cmd = [
        "docker build",
        no_cache_str,
        "-t {}".format(tag_name),
        "-f {}".format(dockerfile),
        ".",
    ]
    build_cmd = " ".join(build_cmd)

    print(build_cmd)
    run(build_cmd, shell=True, check=True, env={"DOCKER_BUILDKIT": "1"})

    if push:
        _do_push(name)


def _do_push(name):
    tag_name = _get_docker_tag(name)

    cmd = "docker push {}".format(tag_name)
    print(cmd)
    run(cmd, shell=True, check=True)


@task(iterable=["c"])
def build(ctx, c, nocache=False, push=False):
    """
    Build containers for faabric exp: `openmpi` and `faabric-experiments`
    """
    for ctr in c:
        if ctr == "openmpi":
            img_name = OPENMPI_IMAGE_NAME
        elif ctr == "faabric-experiments":
            img_name = FAABRIC_EXP_IMAGE_NAME
        else:
            print("Unrecognised container name: {}".format(ctr))
            raise RuntimeError("Unrecognised container name")

        _do_container_build(img_name, nocache=nocache, push=push)


@task(iterable=["c"])
def push(ctx, c):
    """
    Push containers for faabric exp: `openmpi` and `faabric-experiments`
    """
    for ctr in c:
        if ctr == "openmpi":
            img_name = OPENMPI_IMAGE_NAME
        elif ctr == "faabric-experiments":
            img_name = FAABRIC_EXP_IMAGE_NAME
        else:
            print("Unrecognised container name: {}".format(ctr))
            raise RuntimeError("Unrecognised container name")

        _do_push(img_name)
