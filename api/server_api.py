from fastapi import FastAPI
from pydantic import BaseModel
import json
import uvicorn
import uuid
import asyncio
import redis.asyncio as aioredis

class TimeoutError(Exception):
    pass


class Item(BaseModel):
    code : str
    tests : str | None = None
    timeout : int = 15
    perTestTimeout : int = 5
    whitelisted: list[str] | None = None
    blacklisted: list[str] | None = None

app = FastAPI()
r = aioredis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/")
def root():
    return {"message": "Hello World"}

#json has to be formatted in a specific way to work
#newlines (\n) are escaped as \\n
#double quotes (") inside the string are escaped as \"
@app.post("/submit")
async def better_submit(item : Item):
    print(item)
    print(item.timeout)

    job_id = str(uuid.uuid4())
    jobdir = f"/jobs/{job_id}"

    job_data = {
        "id": job_id,
        "code": item.code,
        "tests": item.tests,
        "timeout": item.timeout,
        "per_test_timeout": item.perTestTimeout,
        "whitelisted": item.whitelisted,
        "blacklisted": item.blacklisted
    }

    await r.rpush("job_queue", json.dumps(job_data))

    timeout_seconds = 30
    poll_interval = 0.2  # 200ms between checks
    elapsed = 0

    while elapsed < timeout_seconds:
        result_name, result_json = await r.blpop(f"result:{job_id}")
        print(result_json)
        if result_json:
            await r.delete(f"result:{job_id}")  # Optional cleanup
            return json.loads(result_json)

        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    return "Timeout Error"



@app.post("/encoded")
def decode_and_write(item: Item):
    return "Wowza"


if __name__ == "__main__":
    uvicorn.run("server_api:app", host="0.0.0.0", port=5000, reload=True)
