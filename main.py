from fastapi import FastAPI
from os import getenv
app = FastAPI()
#configuration of the app
app.title="GLOB-DATA"

@app.get("/")
def read_root():
    return {"Hello": getenv("PGADMIN_DEFAULT_EMAIL")}
