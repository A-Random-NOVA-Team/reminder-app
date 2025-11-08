import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from api import deps
from schemas.requests import CreateTaskRequest, UpdateTaskRequest
from schemas.responses import TaskResponse
from models import Task

router = APIRouter()


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: CreateTaskRequest, session: AsyncSession = Depends(deps.get_session)):
    """Create a new task"""
    db_task = Task(
        name=task.name,
        description=task.description,
        due_date=task.due_date,
        is_completed=False,
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc),
    )
    session.add(db_task)
    await session.commit()
    return db_task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(deps.get_session)):
    """Get all tasks"""
    tasks = await session.execute(select(Task).offset(skip).limit(limit))
    return tasks.scalars().all()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, session: AsyncSession = Depends(deps.get_session)):
    """Get a specific task by ID"""
    task = await session.execute(select(Task).filter(Task.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int, task: UpdateTaskRequest, session: AsyncSession = Depends(deps.get_session)
):
    """Update a task"""
    db_task = await session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.name is not None:
        db_task.name = task.name
    if task.description is not None:
        db_task.description = task.description
    if task.due_date is not None:
        db_task.due_date = datetime.datetime.fromisoformat(task.due_date)
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed
    db_task.update_time = datetime.datetime.now(datetime.timezone.utc)

    session.add(db_task)
    await session.commit()
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: AsyncSession = Depends(deps.get_session)):
    """Delete a task"""
    db_task = await session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(db_task)
    await session.commit()
    return None
