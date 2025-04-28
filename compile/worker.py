import asyncio
import os
import json
import logging
from work import work
import redis.asyncio as aioredis
import threading
from pathlib import Path
import shutil

class TimeoutError(Exception):
    pass

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

async def process_job(r, job):

    job_data = json.loads(job[1])  # job is a tuple, with [0] being the queue and [1] the data
    job_id = job_data["id"]
    code = job_data["code"]
    tests = job_data["tests"]
    timeout = job_data["timeout"]
    per_test_timeout = job_data["per_test_timeout"]
    whitelisted = job_data["whitelisted"]
    blacklisted = job_data["blacklisted"]
    jobdir = f"/jobs/{job_id}"
    jobpath = Path(jobdir)
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
        response = run_with_timeout(timeout, work, jobdir=jobdir, time_limit=per_test_timeout,
                                        blacklist=blacklisted,
                                        whitelist=whitelisted)
        await r.rpush(f"result:{job_id}", json.dumps(response))
    finally:
        shutil.rmtree(jobdir)





async def worker():
    r = aioredis.Redis(host='redis', port=6379, decode_responses=True)
    while True:
        try:
            job = await r.blpop("job_queue")
            await process_job(r, job)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(worker())