from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import File, Tag, FileTag, User

class FileService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, creator: User, title: str, description: str, min_role_weight: int, tags: list[str], info_hash: str, size_bytes: int):
        f = File(title=title, description=description, min_role_weight=min_role_weight, created_by=creator.id, path_hash=info_hash, size_bytes=size_bytes)
        self.db.add(f)
        self.db.flush()
        tag_objs = []
        for name in tags:
            t = self.db.query(Tag).filter_by(name=name).first()
            if not t:
                t = Tag(name=name)
                self.db.add(t)
                self.db.flush()
            tag_objs.append(t)
        for t in tag_objs:
            self.db.add(FileTag(file_id=f.id, tag_id=t.id))
        return f

    def list_visible(self, user_weight: int):
        return self.db.query(File).filter(File.min_role_weight <= user_weight).all()