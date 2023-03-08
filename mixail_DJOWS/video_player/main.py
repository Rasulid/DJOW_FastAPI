from fastapi import FastAPI
import crud
from db import database, metadata, engin

app = FastAPI(docs_url="/")
app.include_router(crud.router)
app.state.database = database
metadata.create_all(engin)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
