#!/usr/bin/env python

from build_c import *
import subprocess, os
import time

def work():
    os.chmod("./compile.sh", 0o755)
    os.chmod("./run.sh", 0o755)


    output = ""

    return_dict = {
        "compile": False,
        "run": False,
        "output": output,
        "build": False,
        "compilation_time": -1,
        "run_time": -1
    }

    # build the code
    subprocess.run(["pwd"])
    build_status = build()
    if (build_status != 0):
        print("Build failed!")
        return_dict["build"] = False
        return return_dict

    build_successful = True

    # compile the code
    compilation_time_status = time.time()
    compile = subprocess.run(["./compile.sh"], shell=True, capture_output=True, text=True, timeout=5)
    compilation_time_endn = time.time()
    compilation_time = compilation_time_endn - compilation_time_status
    return_dict["compilation_time"] = compilation_time
    print("Compilation time: " + str(compilation_time))

    return_dict["output"] += compile.stdout
    return_dict["output"] += compile.stderr
    if compile.returncode == 0:
        return_dict["compile"] = True
        with open("output.txt", "w") as f:
            f.write(compile.stdout)
    else:
        with open("output.txt", "w") as f:
            f.write(compile.stdout)
            f.write(compile.stderr)
        print("Compile failed!")


    # run the code if compile was successful
    if compile.returncode == 0:
        print(compile)
        print("Compiled successfully!")

        run_time_start = time.time()
        try:
            run = subprocess.run(["./run.sh"], shell=True, capture_output=True, text=True, timeout=5)
            run_time_end = time.time()
            run_time = run_time_end - run_time_start
            return_dict["run_time"] = run_time
            print("Run time: " + str(run_time))

            if run.returncode == 0:
                return_dict["run"] = True
                with open("output.txt", "w") as f:
                    f.write(run.stdout)
            else:
                with open("output.txt", "w") as f:
                    f.write(run.stdout)
                    f.write(run.stderr)
                print("Run failed!")

            return_dict["output"] += run.stdout
            return_dict["output"] += run.stderr
            print("Run successfull!")
        except subprocess.TimeoutExpired:
            return_dict["output"] = "Timeout"

    return return_dict


if __name__=="__main__":
    print("Building...")
    print(work())


