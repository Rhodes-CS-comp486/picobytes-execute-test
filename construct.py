import subprocess


def build_images():
    subprocess.run(["docker","build","-t","picobytes:api2", "./api"])
    subprocess.run(["docker", "build", "-t", "worker", "./compile"])

def apply_yaml():
    subprocess.run(["kubectl", "apply", "-f", "./kubernetes-setup"])


if __name__ == "__main__":
    build_images()
    apply_yaml()