#!/usr/bin/env 
#!/usr/bin/env python
import os
import subprocess
import signal
import time
import json
import logging
from build_c import build

# Configure logging: Adjust logging level as needed.
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def valgrind_parse(valgrind_output):
    """
    Extract the HEAP SUMMARY from a valgrind output.
    
    :param valgrind_output: The full stderr output from valgrind.
    :return: A substring beginning from "HEAP SUMMARY:" or the original output if not found.
    """
    idx = valgrind_output.find("HEAP SUMMARY:")
    return valgrind_output[idx:] if idx != -1 else valgrind_output

def execute(command, cwd=None, timeout=5):
    """
    Execute a command with a timeout, returning its output details.
    
    :param command: A list containing the command and its arguments.
    :param cwd: The directory in which to run the command.
    :param timeout: Timeout value in seconds.
    :return: Tuple (returncode, stdout, stderr, elapsed_time).
    """
    start_time = time.time()
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd,
            preexec_fn=os.setsid
        )
        stdout, stderr = process.communicate(timeout=timeout)
        elapsed_time = time.time() - start_time
        return process.returncode, stdout, stderr, elapsed_time
    except subprocess.TimeoutExpired:
        # Kill process tree if timeout is reached.
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        stdout, stderr = process.communicate()
        elapsed_time = time.time() - start_time
        logging.error(f"Command {' '.join(command)} timed out after {timeout} seconds.")
        stderr = f"Command time out after {timeout} seconds."
        return process.returncode, stdout, stderr, elapsed_time
    except Exception as e:
        elapsed_time = time.time() - start_time
        logging.exception(f"Error executing command {' '.join(command)}: {e}")
        return -1, "", str(e), elapsed_time

def set_executable(path):
    """
    Ensure that the file at 'path' is executable.
    
    :param path: The file path.
    """
    if os.path.exists(path):
        os.chmod(path, 0o755)
        logging.debug(f"Set executable permissions for {path}.")
    else:
        logging.warning(f"File {path} does not exist.")

def work(jobdir, time_limit=5, run_tests=True):
    """
    Perform the build, compile, valgrind analysis, and run test steps.

    :param jobdir: Current job's directory.
    :param time_limit: Maximum allowed time for each subprocess.
    :param run_tests: Whether to execute tests after compiling.
    :return: Dictionary with the details/results of each step.
    """
    origin = os.path.dirname(os.path.realpath(__file__))
    logging.info(f"Working directory: {jobdir}")

    compile_file = os.path.join(origin, "compile.sh")
    run_file = os.path.join(origin, "run.sh")
    
    # Ensure the compile and run scripts exist and are executable.
    set_executable(compile_file)
    set_executable(run_file)

    results = {
        "build": False,
        "compile": False,
        "run": False,
        "output": "",
        "compilation_time": -1,
        "run_time": -1,
        "valgrind": "",
        "failed_tests": []
    }

    # Build Step
    try:
        build_status = build(jobdir)
        if build_status != 0:
            logging.error("Build failed. Check your build script. Aborting further steps.")
            return results
        results["build"] = True
        logging.info("Build succeeded.")
    except Exception as e:
        logging.exception(f"Exception during build: {e}")
        return results

    # Compile Step
    compile_cmd = [compile_file]
    ret_code, compile_stdout, compile_stderr, comp_time = execute(compile_cmd, cwd=jobdir, timeout=time_limit)
    results["compilation_time"] = comp_time
    results["output"] += compile_stdout + compile_stderr

    if ret_code == 0:
        results["compile"] = True
        logging.info(f"Compilation succeeded in {comp_time:.2f} seconds.")
    else:
        logging.error("Compilation failed. Aborting further steps.")
        return results

    # Valgrind Analysis Step: Only performed if code.out exists.
    code_out_path = os.path.join(jobdir, "code.out")
    if os.path.exists(code_out_path):
        valgrind_cmd = ["valgrind", "--tool=memcheck", "--leak-check=yes", "--track-origins=yes", "./code.out"]
        try:
            ret_valgrind, _, valgrind_stderr, _ = execute(valgrind_cmd, cwd=jobdir, timeout=time_limit)
            if ret_valgrind == 0:
                logging.info("Valgrind analysis completed successfully.")
            else:
                logging.warning("Valgrind reported issues during analysis.")
            results["valgrind"] = valgrind_parse(valgrind_stderr)
        except Exception as e:
            logging.exception("Valgrind analysis failed.")
            results["valgrind"] = f"Valgrind error: {e}"
    else:
        logging.error("code.out not found. Skipping valgrind analysis.")
        results["valgrind"] = "code.out not found."

    # Test Execution Step (if enabled)
    if not run_tests:
        results["run"] = True
        return results

    run_cmd = [run_file]
    ret_run, run_stdout, run_stderr, run_time = execute(run_cmd, cwd=jobdir, timeout=time_limit)
    results["run_time"] = run_time
    results["output"] += run_stdout

    if ret_run == 0:
        results["run"] = True
        logging.info(f"Test execution succeeded in {run_time:.2f} seconds.")
        try:
            with open(os.path.join(jobdir, "output.txt"), "w") as f:
                f.write(run_stdout)
        except Exception as e:
            logging.exception("Error writing test output to file.")
    else:
        logging.error("Test execution failed. Analyzing output for failed tests.")
        # Identify tests as failed if the output contains both 'ASSERT' and 'FAILED'
        results["output"] += "\n" + run_stderr
        failed_tests = [i for i, line in enumerate(run_stdout.splitlines(), start=1)
                        if "ASSERT" in line and "FAILED" in line]
        results["failed_tests"] = failed_tests
        try:
            with open(os.path.join(jobdir, "output.txt"), "w") as f:
                f.write(run_stdout)
        except Exception as e:
            logging.exception("Error writing test output to file.")
    return results

def main(jobdir):
    logging.info("Starting the build, compile, and test process.")
    results = work(jobdir)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

