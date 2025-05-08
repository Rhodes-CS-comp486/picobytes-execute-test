import subprocess


def build_images():
    subprocess.run(["docker","build","-t","picobytes:api", "./api"])
    subprocess.run(["docker", "build", "-t", "picobytes:compile", "./compile"])

def apply_yaml():
    subprocess.run(["kubectl", "delete", "-f", "./kubernetes-setup"])
    subprocess.run(["kubectl", "apply", "-f", "./kubernetes-setup"])


if __name__ == "__main__":
    build_images()
    apply_yaml()