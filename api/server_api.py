from fastapi import FastAPI
from pydantic import BaseModel
import subprocess



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
        subprocess.run(["python3", "save_as_text.py", item.code, item.tests], check = True)
        return {"success": True}
    except subprocess.CalledProcessError as e:
        return {"success": False}