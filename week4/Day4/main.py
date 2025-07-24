from fastapi import FastAPI
from routes import ingest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingest"])