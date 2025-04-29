import asyncio
import os
import json
import logging
from work import work
import redis.asyncio as aioredis
import threading
from pathlib import Path
import shutil
import concurrent.futures
import functools
import sys
from concurrent.futures.process import BrokenProcessPool


def run_with_timeout(timeout, function, *args, **kwargs):
    result = {"response": None}
    print("Running with timeout of {} seconds".format(timeout))
    def run():
        try:
            result["response"] = function(*args, **kwargs)
        except Exception as e:
            result["response"] = {"error": str(e)}
    thread = threading.Thread(target=run)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        result["response"] = {"error": "Total Timeout exceeded!!!"}
    return result["response"]

async def process_job(r, job, executor):

    job_data = job
    job_id = job_data["id"]
    code = job_data["code"]
    tests = job_data["tests"]
    total_timeout = job_data["timeout"]
    per_test_timeout = job_data["per_test_timeout"]
    whitelisted = job_data["whitelisted"]
    blacklisted = job_data["blacklisted"]
    jobdir = f"/jobs/{job_id}"
    jobpath = Path(jobdir)
    jobpath.parent.mkdir(parents=True, exist_ok=True)
    os.makedirs(jobdir, exist_ok=True)
    try:

        isopath1 = jobpath / "tempC.c"
        isopath2 = jobpath / "tempTest.c"

        with open(isopath1, "w", encoding="utf-8") as f:
                f.write(code)
        if tests is not None:
                with open(isopath2, "w", encoding="utf-8") as f:
                    f.write(tests)
        else:
                with open(isopath2, "w", encoding="utf-8") as f:
                    f.write("")
        loop = asyncio.get_event_loop()
        work_task = functools.partial(work,
    jobdir=jobdir,
    time_limit=per_test_timeout,
    blacklist=blacklisted,
    whitelist=whitelisted)
        try:
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    executor,
                    work_task
                ),
                timeout=total_timeout
            )
        except (
                BrokenProcessPool, RuntimeError):
            logging.error(f"[{job_id}] Fatal: Executor pool became unusable. Exiting worker.",
                          exc_info=True)
            sys.exit(1)
        except asyncio.TimeoutError:
            logging.warning(f"Job {job_id} timed out after {total_timeout} seconds")
            response = {"error": f"Total Timeout exceeded ({total_timeout}s)!!!"}

        if response is not None:
            await r.rpush(f"result:{job_id}", json.dumps(response))
        else:
            # Fallback error if response somehow wasn't set (shouldn't happen with current logic)
            await r.rpush(f"result:{job_id}", json.dumps({"error": "Unknown processing issue"}))
    except Exception as e:
        # This block catches exceptions *before* or *after* the executor call
        # (e.g., failure during file writing, directory creation/removal)
        logging.error(f"Job {job_id} setup/cleanup error: {e}", exc_info=True)
        # Attempt to push an error result for this job ID if possible
        error_response = {"error": f"Setup/Cleanup error: {e}"}
        try:
            await r.rpush(f"result:{job_id}", json.dumps(error_response))
        except Exception as redis_e:
            logging.error(f"Failed to push error result for job {job_id}: {redis_e}", exc_info=True)
    finally:
        if jobpath.exists():
            shutil.rmtree(jobdir)





async def worker():
    logging.basicConfig(filename = "/run_logs/worker.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    r = aioredis.Redis(host='redis', port=6379, decode_responses=True)
    logging.info("Worker connecting to Redis...")
    executor = concurrent.futures.ProcessPoolExecutor()
    logging.info("Executor created")
    try:
        while True:
            try:
                job = await r.blpop("job_queue")
                job_data_str = job[1]
                job_data = json.loads(job_data_str)
                job_id = job_data["id"]
                await process_job(r, job_data, executor)
            except (
            BrokenProcessPool, RuntimeError):
                logging.error(f"[{job_id}] Fatal: Executor pool became unusable. Exiting worker.",
                              exc_info=True)
                sys.exit(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
    finally:
        executor.shutdown(wait=True)
        await r.close()

if __name__ == "__main__":
    asyncio.run(worker())