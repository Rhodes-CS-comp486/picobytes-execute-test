#!/usr/bin/env 
#!/usr/bin/env python
import os
import subprocess
import signal
import time
import json
import logging
from build_c import build
import re
# Configure logging: Adjust logging level as needed.
log_dir = "/app/run_logs"
log_dir = "./"

log_file = os.path.join(log_dir, "work.log")
os.makedirs(log_dir, exist_ok=True)
class SuppressUnwantedChangeMsg(logging.Filter):
    def filter(self, record):
        return "change detected" not in record.getMessage()
streamHandler = logging.StreamHandler()
streamHandler.addFilter(SuppressUnwantedChangeMsg())
fileHandler = logging.FileHandler(log_file)
fileHandler.addFilter(SuppressUnwantedChangeMsg())
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        streamHandler,                  # Logs to the console.
        fileHandler                     # Logs to a file.
    ]
)

def parse_compile_output(compile_output):
    """
    Parse the output of the compiler.
    :param compile_output: The output of the compiler
    """
    # check for pragma poison error
    # print(compile_output)
    matches = re.findall(r'error: attempt to use poisoned "(\w+)"', compile_output)
    if matches:
        matchFormat = map(lambda x: f"Not allowed to use {x}", matches)
        return "\n".join(set(matchFormat))
    return compile_output

def valgrind_parse(valgrind_output):
    """
    Extract and clean the HEAP SUMMARY section from valgrind output.
    Removes PID prefixes, file paths, and memory addresses.
    
    :param valgrind_output: Full stderr output from valgrind.
    :return: Cleaned HEAP SUMMARY string or message if not found.
    """
    import re

    idx = valgrind_output.find("HEAP SUMMARY:")
    if idx == -1:
        return "HEAP SUMMARY not found."

    relevant = valgrind_output[idx:]
    lines = relevant.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("=="):
            parts = line.split("==", 2)
            if len(parts) == 3:
                content = parts[2].strip()
            else:
                content = line
        else:
            content = line

        # Remove memory addresses like 0x4841866
        content = re.sub(r'0x[0-9a-fA-F]+', '(address hidden)', content)

        # Remove absolute paths
        content = re.sub(r'in (/[^ ]+)', 'in (path hidden)', content)

        cleaned.append(content)

    return "\n".join(cleaned)

def parse_results(output_text, offset=0):
    """
    Parse the output of the compiler.
    :param output_text: The output of the compiler
    """
    results = []
    pattern = re.compile(r'final_c\.c:(\d+):\d+:\s+(error|warning):\s+(.*)')

    for line in output_text.splitlines():
        match = pattern.search(line)
        if match:
            line_number = int(match.group(1)) - offset
            error_message = match.group(3).strip()
            results.append((line_number, error_message))
    
    logging.info(f"Found {len(results)} errors.")
    return results

def parse_final_output(output_text, offset=0):
    """
    Parse the output of the compiler.
    :param output_text: The output of the compiler
    """
    lines = output_text.split('\n')
    parsed_lines = []
    line_pattern = re.compile(r'final_c\.c:(\d+):')

    for line in lines:
        match = line_pattern.search(line)
        if match:
            original_line_number = int(match.group(1))
            adjusted_line_number = original_line_number - offset
            line = line_pattern.sub(f'line: {adjusted_line_number}:', line)
        parsed_lines.append(line.replace('final_c.c', 'code.c'))

    return '\n'.join(parsed_lines)

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

def work(jobdir = None, time_limit=5, run_tests=True, blacklist=None, whitelist=None):
    """
    Perform the build, compile, valgrind analysis, and run test steps.

    :param jobdir: Current job's directory.
    :param time_limit: Maximum allowed time for each subprocess.
    :param run_tests: Whether to execute tests after compiling.
    :return: Dictionary with the details/results of each step.
    """
    logging.info(f"Running work.py with args: time_limit={time_limit}, run_tests={run_tests}, blacklist={blacklist}, whitelist={whitelist}")
    origin = os.path.dirname(os.path.realpath(__file__))
    logging.info(f"Working directory: {jobdir}")

    compile_file = os.path.join(origin, "compile.sh")
    run_file = os.path.join(origin, "run.sh")

    logging.info(f"Working directory: {jobdir}")
    
    # Ensure the compile and run scripts exist and are executable.
    set_executable(compile_file)
    set_executable(run_file)
    offset = 4 if blacklist else 3

    results = {
        "build": False,
        "compile": False,
        "run": False,
        "output": "",
        "compilation_time": -1,
        "run_time": -1,
        "valgrind": "",
        "formatted_response": [],
        "failed_tests": []
    }

    # Build Step
    try:
        build_status = build(jobdir, blacklist, whitelist)
        if build_status != 0:
            logging.error("Build failed. Check your build script. Aborting further steps.")
            results["output"] += "\n" + str(build_status)
            print(json.dumps(results, indent=2))
            results["output"] = parse_final_output(results["output"])
            return results
        results["build"] = True
        logging.info("Build succeeded.")
    except Exception as e:
        logging.exception(f"Exception during build: {e}")
        results["output"] += parse_final_output(results["output"])
        return results

    # Compile Step
    compile_cmd = [compile_file]
    ret_code, compile_stdout, compile_stderr, comp_time = execute(compile_cmd, cwd=jobdir, timeout=time_limit)
    results["compilation_time"] = comp_time

    if ret_code == 0:
        results["compile"] = True
        logging.info(f"Compilation succeeded in {comp_time:.2f} seconds.")
    else:
        logging.error("Compilation failed. Aborting further steps.")
        compiler_output = parse_compile_output(compile_stdout + compile_stderr)
        results["formatted_response"] = parse_results(compiler_output, offset=offset)
        results["output"] +="\n" + compiler_output
        results["output"] = parse_final_output(results["output"])
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
        results["output"] = parse_final_output(results["output"])
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
    results["output"] = parse_final_output(results["output"])
    return results

def main(jobdir=None):
    logging.info("Starting the build, compile, and test process.")
    results = work(jobdir)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

