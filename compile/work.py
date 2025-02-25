#!/usr/bin/env python

from build_c import *
import subprocess, os
import time

def work():
    # os.chmod("./compile.sh", 0o755)
    # os.chmod("./run.sh", 0o755)
    #

    output = ""

    compile_successful = False
    run_successful = False
    compilation_time = -1
    run_time = -1

    subprocess.run(["pwd"])
    build_status = build()
    if (build_status != 0):
        print("Build failed!")
        exit(1)


    compilation_time_status = time.time()
    compile = subprocess.run(["./compile.sh"], shell=True, capture_output=True, text=True)
    compilation_time_endn = time.time()
    compilation_time = compilation_time_endn - compilation_time_status
    print("Compilation time: " + str(compilation_time))

    output += compile.stdout
    output += compile.stderr
    if compile.returncode == 0:
        compile_successful = True
        with open("output.txt", "w") as f:
            f.write(compile.stdout)
    else:
        with open("output.txt", "w") as f:
            f.write(compile.stdout)
            f.write(compile.stderr)
        print("Compile failed!")

    if compile.returncode == 0:
        print(compile)
        print("Compiled successfully!")

        run_time_start = time.time()
        run = subprocess.run(["./run.sh"], shell=True, capture_output=True, text=True)
        run_time_end = time.time()
        run_time = run_time_end - run_time_start
        print("Run time: " + str(run_time))

        if run.returncode == 0:
            run_successful = True
            with open("output.txt", "w") as f:
                f.write(run.stdout)
        else:
            with open("output.txt", "w") as f:
                f.write(run.stdout)
                f.write(run.stderr)
            print("Run failed!")

        output += run.stdout
        output += run.stderr

        print("Run successfull!")

    return {
        "compile": compile_successful,
        "run": run_successful,
        "output": output,
        "compilation_time": compilation_time,
        "run_time": run_time
    }


if __name__=="__main__":
    print("Building...")
    print(work())


