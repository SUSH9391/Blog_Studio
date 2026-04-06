from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )

    posts: Mapped[list[Post]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    comments: Mapped[list[Comment]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )

    reset_tokens: Mapped[list[PasswordResetToken]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @property
    def image_path(self) -> str:
        if self.image_file:
            if self.image_file.startswith("http"):
                return self.image_file
            from config import settings
            return f"{settings.supabase_url}/storage/v1/object/public/avatar/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    likes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    upvotes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    downvotes: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    media_paths: Mapped[list[str]] = mapped_column(JSON, default=list, server_default="[]")

    author: Mapped[User] = relationship(back_populates="posts")
    comments: Mapped[list[Comment]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
    )

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    post: Mapped[Post] = relationship(back_populates="comments")
    author: Mapped[User] = relationship(back_populates="comments")
    replies: Mapped[list[Comment]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    parent: Mapped[Comment | None] = relationship(
        back_populates="replies",
        remote_side=[id],
    )


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    user: Mapped[User] = relationship(back_populates="reset_tokens")