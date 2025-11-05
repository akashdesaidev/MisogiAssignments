import uvicorn
from fastapi import FastAPI
from router.adminrouter import router as admin

app = FastAPI()

app.include_router(admin)

@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
