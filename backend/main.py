from fastapi import FastAPI
from pydantic import BaseModel

from terminal.executor import execute_command


app = FastAPI(
    title="AI-Powered Terminal",
    version="1.0.0",
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