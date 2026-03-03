import os
from dotenv import load_dotenv
from fastapi import FastAPI
# Load environment variables
load_dotenv(override=True)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Travelume API", description="Backend for Travelume App")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi import Response

class CORSStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

base_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
if not os.path.exists(base_data_dir):
    os.makedirs(base_data_dir)
app.mount("/static", CORSStaticFiles(directory=base_data_dir), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to Travelume API"}

from backend.routers import auth, journals, chat, planner, trips

app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(chat.router)
app.include_router(planner.router)
app.include_router(trips.router)