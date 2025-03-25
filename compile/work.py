#!/usr/bin/env python

from build_c import *
import subprocess, os
import time
import json
import logging 

log_dir = "/app/logs"
log_file = os.path.join(log_dir, "work.log")

os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=log_file, filemode="a", level=logging.DEBUG, format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)

def work(time_limit=5, runTests=True):
    logger.info("Starting work...")

    origin = os.path.dirname(os.path.realpath(__file__))

    compile_file = os.path.join(origin, "compile.sh")
    run_file = os.path.join(origin, "run.sh")
    logger.info("Created compile file and run.sh script")
    os.chmod(compile_file, 0o755)
    os.chmod(run_file, 0o755)
    logger.info("Made compile file and run.sh script executable")



    output = ""

    return_dict = {
        "compile": False,
        "run": False,
        "output": output,
        "build": False,
        "compilation_time": -1,
        "run_time": -1,
        "failed_tests": []
    }

    # build the code
    # subprocess.run(["pwd"])
    build_status = build()
    logger.info("Build status: " + str(build_status))
    if (build_status != 0):
        logger.error("Build failed!")
        return_dict["build"] = False
        return return_dict

    return_dict["build"] = True
    logger.info("Build successful!")

    # compile the code
    compilation_time_status = time.time()
    compile = subprocess.run([compile_file], cwd=origin, shell=True, capture_output=True, text=True, timeout=time_limit)
    compilation_time_endn = time.time()
    compilation_time = compilation_time_endn - compilation_time_status
    return_dict["compilation_time"] = compilation_time
    print("Compilation time: " + str(compilation_time))
    logger.info("Compilation time: " + str(compilation_time))

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
        logger.error("Compile failed!")


    # run the code if compile was successful
    if compile.returncode == 0:
        print("Compiled successfully!")
        logger.info("Compiled successfully!")

        # check if runTests is True and if not return
        if not runTests:
            return_dict["run"] = True
            return return_dict

        run_time_start = time.time()
        try:
            run = subprocess.run([run_file], cwd=origin, shell=True, capture_output=True, text=True, timeout=time_limit)
            run_time_end = time.time()
            run_time = run_time_end - run_time_start
            return_dict["run_time"] = run_time
            print("Run time: " + str(run_time))
            logger.info("Run time: " + str(run_time))

            if run.returncode == 0:
                print("Run successful!")
                logger.info("Run successful!")
                return_dict["run"] = True
                with open("output.txt", "w") as f:
                    f.write(run.stdout)
            else:
                # check which tests failed
                failed_Tests = []
                test_no = 0
                for line in run.stdout.split('\n'):
                    # print(line)
                    if "ASSERT" in line:
                        test_no += 1
                        if "FAILED" in line:
                            failed_Tests.append(test_no)
                return_dict["failed_tests"] = failed_Tests


                with open("output.txt", "w") as f:
                    f.write(run.stdout)
                    f.write(run.stderr)
                print("Run failed!")
                logger.error("Run failed!")

            return_dict["output"] += run.stdout
            return_dict["output"] += run.stderr
        except subprocess.TimeoutExpired:
            logger.error("Timed out!")
            return_dict["output"] = "Timeout"

    return return_dict


if __name__=="__main__":
    print("Building...")
    result = work()
    print(json.dumps(result, indent=2))


