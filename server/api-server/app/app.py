from fastapi import FastAPI
from app.routes import command
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "*",
    "http://localhost:3000",
]

app = FastAPI(
    title="C2 - API Server",
    description="API Server for C2 Executor",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Deepak Navaria",
        "email": "dnavaria15+github@gmail.com",
    },

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health-check")
def health_check():
    return {"status": "ok"}


app.include_router(command.router, prefix="/api/v1/command", tags=["command"])
