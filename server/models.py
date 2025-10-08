from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, BigInteger,
    UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .db import Base

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    weight: Mapped[int] = mapped_column(Integer, default=10, nullable=False)  # higher = more power

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    ratio_target: Mapped[float] = mapped_column(Integer, default=50)  # store as percent (e.g., 50)
    role = relationship(Role)

class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    path_hash: Mapped[str] = mapped_column(String(64), unique=True)  # infohash
    size_bytes: Mapped[int] = mapped_column(BigInteger, default=0)
    min_role_weight: Mapped[int] = mapped_column(Integer, default=10)  # who can see
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)

class FileTag(Base):
    __tablename__ = "file_tags"
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)

class UserStat(Base):
    __tablename__ = "user_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bytes_up: Mapped[int] = mapped_column(BigInteger, default=0)
    bytes_down: Mapped[int] = mapped_column(BigInteger, default=0)

class Peer(Base):
    __tablename__ = "peers"
    id: Mapped[int] = mapped_column(primary_key=True)
    info_hash: Mapped[str] = mapped_column(String(64), index=True)
    peer_id: Mapped[str] = mapped_column(String(64))
    ip: Mapped[str] = mapped_column(String(64))
    port: Mapped[int] = mapped_column(Integer)
    last_seen: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("info_hash", "peer_id", name="uix_peer"),)

# Optional FULLTEXT index DDL (execute once in DB):
# ALTER TABLE files ADD FULLTEXT idx_full (title, description);
# CREATE TABLE tag_search AS SELECT f.id, GROUP_CONCAT(t.name SEPARATOR ' ') keywords FROM files f
#   JOIN file_tags ft ON f.id=ft.file_id JOIN tags t ON t.id=ft.tag_id GROUP BY f.id;
# Or perform JOIN-based filtering in queries.