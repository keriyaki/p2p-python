from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from ..models import File, Tag, FileTag

class SearchService:
    def __init__(self, db: Session):
        self.db = db

    def search(self, user_weight: int, q: str):
        q_like = f"%{q}%"
        # Simplified LIKE-based search; for scale use FULLTEXT
        return (
            self.db.query(File)
            .outerjoin(FileTag, File.id == FileTag.file_id)
            .outerjoin(Tag, Tag.id == FileTag.tag_id)
            .filter(File.min_role_weight <= user_weight)
            .filter(or_(File.title.like(q_like), File.description.like(q_like), Tag.name.like(q_like)))
            .group_by(File.id)
            .all()
        )