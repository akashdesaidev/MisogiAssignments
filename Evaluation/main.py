import uvicorn
from fastapi import FastAPI,UploadFile, File
from router.ingestRouter import ingestRouter
from router.queryRouter import queryRouter

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(ingestRouter)
app.include_router(queryRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
