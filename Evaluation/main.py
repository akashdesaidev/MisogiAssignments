import uvicorn
from fastapi import FastAPI,UploadFile, File
from router.ingestRouter import ingestRouter
from router.queryRouter import queryRouter
import os
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(ingestRouter)
app.include_router(queryRouter)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port,reload=True)
