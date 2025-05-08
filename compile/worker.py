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

NUM_WORKERS = os.cpu_count()

async def process_job(r, job, executor):

    job_data = job
    job_id = job_data["id"]
    code = job_data["code"]
    tests = job_data["tests"]
    total_timeout = job_data["timeout"]
    per_test_timeout = job_data["per_test_timeout"]
    whitelisted = job_data["whitelisted"]
    blacklisted = job_data["blacklisted"]
    jobdir = f"/tmp/jobs/{job_id}"
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

            await r.rpush(f"result:{job_id}", json.dumps({"error": "Unknown processing issue"}))
    except Exception as e:

        logging.error(f"Job {job_id} setup/cleanup error: {e}", exc_info=True)
        error_response = {"error": f"Setup/Cleanup error: {e}"}
        try:
            await r.rpush(f"result:{job_id}", json.dumps(error_response))
        except Exception as redis_e:
            logging.error(f"Failed to push error result for job {job_id}: {redis_e}", exc_info=True)
    finally:
        if jobpath.exists():
            shutil.rmtree(jobdir)


async def job_consumer(r, executor, worker_id):
    logging.info(f"Worker-{worker_id} started")
    while True:
        try:
            job = await r.blpop("job_queue")
            job_data_str = job[1]
            job_data = json.loads(job_data_str)
            await process_job(r, job_data, executor)
        except (BrokenProcessPool, RuntimeError):
            logging.error(f"Worker-{worker_id}: Executor pool unusable. Exiting.", exc_info=True)
            sys.exit(1)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.error(f"Worker-{worker_id} unexpected error: {e}", exc_info=True)

async def worker():
    logging.basicConfig(
        filename="/run_logs/worker.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    r = aioredis.Redis(host='redis', port=6379, decode_responses=True)
    logging.info("Connected to Redis")
    executor = concurrent.futures.ProcessPoolExecutor()

    try:
        consumers = [
            asyncio.create_task(job_consumer(r, executor, i))
            for i in range(NUM_WORKERS)
        ]
        await asyncio.gather(*consumers)
    finally:
        executor.shutdown(wait=True)
        await r.close()

if __name__ == "__main__":
    asyncio.run(worker())