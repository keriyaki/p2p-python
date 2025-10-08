from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..db import db_session
from ..models import User, File
from ..schemas import FileIn, FileOut
from ..services.file_service import FileService
from ..security import decode_token

router = APIRouter(prefix="/files", tags=["files"])

# Helper to get current user

def get_user(db: Session, token: str) -> User:
    sub = decode_token(token)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, int(sub))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=FileOut)
def create(file: FileIn, authorization: str):
    token = authorization.replace("Bearer ", "")
    with db_session() as db:
        user = get_user(db, token)
        # info_hash/size deverão vir do cliente após criar torrent
        f = FileService(db).create(user, file.title, file.description, file.min_role_weight, file.tags, info_hash="pending", size_bytes=0)
        return {"id": f.id, "title": f.title, "size_bytes": f.size_bytes, "min_role_weight": f.min_role_weight, "info_hash": f.path_hash, "tags": file.tags}

@router.get("/", response_model=List[FileOut])
def list_all(authorization: str):
    token = authorization.replace("Bearer ", "")
    with db_session() as db:
        user = get_user(db, token)
        files = FileService(db).list_visible(user.role.weight)
        out = []
        for f in files:
            out.append({
                "id": f.id,
                "title": f.title,
                "size_bytes": f.size_bytes,
                "min_role_weight": f.min_role_weight,
                "info_hash": f.path_hash,
                "tags": []
            })
        return out