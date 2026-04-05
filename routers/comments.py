from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

import models
from auth import CurrentUser
from database import get_db
from schemas import CommentCreate, CommentResponse

router = APIRouter()

@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    # Verify post exists
    post_result = await db.execute(select(models.Post).where(models.Post.id == post_id))
    if not post_result.scalars().first():
        raise HTTPException(status_code=404, detail="Post not found")
        
    # If parent_id provided, verify comment exists and belongs to same post
    if comment.parent_id:
        parent_result = await db.execute(select(models.Comment).where(models.Comment.id == comment.parent_id))
        parent_comment = parent_result.scalars().first()
        if not parent_comment or parent_comment.post_id != post_id:
            raise HTTPException(status_code=400, detail="Invalid parent comment")

    new_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user.id,
        parent_id=comment.parent_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment, attribute_names=["author"])
    return new_comment

@router.get("", response_model=list[CommentResponse])
async def get_comments(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.Comment)
        .options(selectinload(models.Comment.author))
        .where(models.Comment.post_id == post_id)
        .order_by(models.Comment.date_posted.asc())
    )
    comments = result.scalars().all()
    return comments
