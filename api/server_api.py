from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import tempfile
import json



class Item(BaseModel):
    code : str
    tests : str | None = ""

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/submit")
def submit(item : Item ):
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as temp_file:
            json.dump(item.model_dump(), temp_file)  # Fix: Use model_dump(), NOT model_dump_json()
            temp_file_name = temp_file.name

        result = subprocess.run(
            ["python3", "save_as_text.py"],
            stdin=open(temp_file_name, "r"),
            check=True,
            capture_output=True,
            text=True
        )

        return {"success": True, "output": result.stdout}

    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}