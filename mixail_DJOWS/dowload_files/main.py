from fastapi import FastAPI
import crud
app = FastAPI(docs_url='/')
app.include_router(crud.router)

