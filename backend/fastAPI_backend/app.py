from contextlib import asynccontextmanager
from beanie import init_beanie

from fastapi import FastAPI
from fastapi_cors import CORS
from fastapi.middleware.cors import CORSMiddleware
from .config import BaseConfig
from motor import motor_asyncio
from mongo_backend import Compound, PreparationFormulation, MLFormulation, User

from .routers import user as user_router
from .routers import formulation as formulation_router

settings = BaseConfig()
print(settings.DB_URL, settings.DB_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]
    
    try:
        await app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
        await init_beanie(database=app.db, document_models=[Compound, PreparationFormulation, MLFormulation, User])
        print("✅ Beanie models initialized")
    except Exception as e:
        print(e)
    yield
    app.client.close()

app = FastAPI(lifespan=lifespan, root_path="/fastapi")
origins = ["*"]
# CORS(app) 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(formulation_router.router, prefix="/formulations", tags=["formulations"])

@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"message": "welcome to electrolyte formulation predict app!"}