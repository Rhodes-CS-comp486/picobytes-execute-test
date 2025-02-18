from base64 import b64decode

from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import json
from pathlib import Path
import uvicorn
import base64

directory = Path("to_execute")
directory.mkdir(parents=True, exist_ok=True)
filepath1 = directory / "code.c"
filepath2 = directory / "tests.c"
filepath3 = directory / "ecode.c"
filepath4 = directory / "etests.c"

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
    with filepath1.open( "w", encoding="utf-8") as f:
        f.write(item.code)
    if item.tests is not None:
        with filepath2.open( "w", encoding="utf-8") as f:
            f.write(item.tests)
    else:
        with filepath2.open( "w", encoding="utf-8") as f:
            f.write("")
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
    uvicorn.run("server_api:app", host="127.0.0.1", port=5000, reload=True)