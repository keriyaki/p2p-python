from fastapi import APIRouter, HTTPException
from typing import List
from ..db import db_session
from ..services.search_service import SearchService
from ..security import decode_token
from ..models import User
from ..schemas import SearchQuery, FileOut

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/", response_model=List[FileOut])
def search(body: SearchQuery, authorization: str):
    token = authorization.replace("Bearer ", "")
    with db_session() as db:
        sub = decode_token(token)
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.get(User, int(sub))
        files = SearchService(db).search(user.role.weight, body.q)
        return [{
            "id": f.id,
            "title": f.title,
            "size_bytes": f.size_bytes,
            "min_role_weight": f.min_role_weight,
            "info_hash": f.path_hash,
            "tags": []
        } for f in files]