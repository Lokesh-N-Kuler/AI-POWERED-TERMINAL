from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from terminal.executor import execute_command
from contextlib import asynccontextmanager

from database.database import init_database
from routes.history import router as history_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield


app = FastAPI(
    title="AI-Powered Terminal",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CommandRequest(BaseModel):
    command: str
    shell: str = "powershell"
    cwd: str | None = None


@app.get("/")
def root():
    return {
        "message": "AI-Powered Terminal backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/terminal/execute")
def execute(request: CommandRequest):

    result = execute_command(
        command=request.command,
        shell_type=request.shell,
        cwd=request.cwd,
    )

    return result

app.include_router(history_router)
