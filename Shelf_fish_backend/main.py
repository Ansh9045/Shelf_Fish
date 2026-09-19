from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import init_db
from database.router import router as item_router
from auth.router import router as auth_router
from detections.router import router as detection_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App started")
    await init_db()
    yield
    print("App closed")


app = FastAPI(title= "Shelf-fish" ,lifespan=lifespan)

app.include_router(item_router)
app.include_router(auth_router)
app.include_router(detection_router)

@app.get("/")
def read_root():
    return {"Hello":"World"}