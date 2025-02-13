from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import json
from pathlib import Path
import uvicorn

directory = Path("to_execute")
directory.mkdir(parents=True, exist_ok=True)
filepath1 = directory / "code.c"
filepath2 = directory / "tests.c"

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



if __name__ == "__main__":
    uvicorn.run("server_api:app", host="127.0.0.1", port=5000, reload=True)