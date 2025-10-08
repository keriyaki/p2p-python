from fastapi import APIRouter, HTTPException
from ..db import db_session
from ..services.stats_service import StatsService
from ..security import decode_token

router = APIRouter(prefix="/stats", tags=["stats"])

@router.post("/upload")
def add_upload(bytes: int, authorization: str):
    token = authorization.replace("Bearer ", "")
    with db_session() as db:
        sub = decode_token(token)
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        StatsService(db).add_upload(int(sub), bytes)
        return {"ok": True}

@router.post("/download")
def add_download(bytes: int, authorization: str):
    token = authorization.replace("Bearer ", "")
    with db_session() as db:
        sub = decode_token(token)
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        StatsService(db).add_download(int(sub), bytes)
        return {"ok": True}