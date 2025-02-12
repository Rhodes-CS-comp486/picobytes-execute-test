from fastapi import FastAPI
from pydantic import BaseModel



class Item(BaseModel):
    code : str
    tests : str | None = None

app = FastAPI()



@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/submit")
def submit(item : Item ):
    return {"code":item.code,"tests":item.tests}