from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from websocket_routes import router as websocket_router
from catalog import CatalogManager
from utils import ConnectionManager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Change to domains if you deploy this to production
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket_router)


CatalogManager.initialize()
ConnectionManager.initialize()