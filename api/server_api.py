from base64 import b64decode
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import json
from pathlib import Path
import uvicorn
import base64
import os
import logging
import sys
import threading

class TimeoutError(Exception):
    pass

def run_with_timeout(timeout, function, *args, **kwargs):
    result = {"response": None}
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

parent = Path(__file__).parent.parent
compile_location = parent / "compile"
tempC_location = compile_location / "tempC.c"
tempTest_location = compile_location / "tempTest.c"
sys.path.append(str(compile_location))

TOTAL_TIMEOUT = 10 # seconds

from work import work

directory = Path("../")
directory.mkdir(parents=True, exist_ok=True)
#filepath1 = "../compile/tempC.c"
#filepath2 = "../compile/tempTest.c"
# filepath1 = directory / "compile" /"tempC.c"
# filepath2 = directory / "compile" / "tempTest.c"
filepath3 = directory / "dcode.c"
filepath4 = directory / "dtests.c"



filepath1 = tempC_location
filepath2 = tempTest_location

logLocation = parent / "logs"

logging.basicConfig(filename=str( logLocation ) , filemode="a", level=logging.DEBUG, format='%(asctime)s %(message)s')

class Item(BaseModel):
    code : str
    tests : str | None = None

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

#json has to be formatted in a specific way to work
#newlines (\n) are escaped as \\n
#double quotes (") inside the string are escaped as \"
@app.post("/submit")
def better_submit(item : Item):
    with open(filepath1, "w", encoding="utf-8") as f:
        f.write(item.code)
    if item.tests is not None:
        with open(filepath2, "w", encoding="utf-8") as f:
            f.write(item.tests)
    else:
        with open(filepath2, "w", encoding="utf-8") as f:
            f.write("")

    response = run_with_timeout(TOTAL_TIMEOUT, work);
    return response

@app.post("/encoded")
def decode_and_write(item: Item):
    dcode = b64decode(item.code).decode("utf-8")
    with filepath3.open( "w", encoding="utf-8") as f:
        f.write(dcode)
    if item.tests is not None:
        dtests = b64decode(item.tests).decode("utf-8")
        with filepath4.open( "w", encoding="utf-8") as f:
            f.write(dtests)
    else:
        with filepath4.open( "w", encoding="utf-8") as f:
            f.write("")

if __name__ == "__main__":
    uvicorn.run("server_api:app", host="0.0.0.0", port=5000, reload=True)
