#!/usr/bin/env python

from build_c import *
import subprocess, os

def main():
    os.chmod("./compile.sh", 0o755)
    os.chmod("./run.sh", 0o755)

    build()
    compile = subprocess.run(["./compile.sh"])

    if (compile.returncode != 0):
        print("Compile failed:")
        print(compile.stderr)
        exit(1)
    print("Compiled successfully!")

    run = subprocess.run(["./run.sh "], capture_output=True)
    if (run.returncode != 0):
        print("Run failed:")
        print(run.stderr)
        exit(1)
    print("Run successfull!")


if __name__=="__main__":
    main()


