from json import loads as json_loads
from subprocess import run


def get_container_names_from_compose(compose_dir):
    json_str = (
        run(
            "docker compose ps --format json",
            capture_output=True,
            shell=True,
            check=True,
            cwd=compose_dir,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    json_dict = json_loads(json_str)
    return [c["Name"] for c in json_dict if c["Service"] == "worker"]


def get_container_ips_from_compose(compose_dir):
    container_ips = []
    container_names = get_container_names_from_compose(compose_dir)
    for c in container_names:
        ip_cmd = [
            "docker inspect -f",
            "'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}'",
            c,
        ]
        ip_cmd = " ".join(ip_cmd)
        c_ip = (
            run(
                ip_cmd,
                shell=True,
                check=True,
                cwd=compose_dir,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .strip()
        )
        container_ips.append(c_ip)
    return container_ips


def run_compose_cmd(thread_id, compose_dir, compose_cmd):
    # Note that we actually run a docker command as we specify the container
    # by name
    docker_cmd = "docker {}".format(compose_cmd)
    print("[Thread {}] {}".format(thread_id, docker_cmd))
    run(docker_cmd, shell=True, check=True, cwd=compose_dir, capture_output=True)