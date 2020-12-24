from typing import Optional
from fastapi import FastAPI

from database.main import router as crud_router

app = FastAPI()
app.include_router(crud_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
