from fastapi import APIRouter, Query

from database.history import get_history, clear_history


router = APIRouter(
    prefix="/api/history",
    tags=["History"],
)


@router.get("/")
def history(
    limit: int = Query(default=100, ge=1, le=500)
):
    return {
        "history": get_history(limit)
    }


@router.delete("/")
def delete_history():
    clear_history()

    return {
        "message": "Command history cleared"
    }