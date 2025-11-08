import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from api import deps
from models import Task, TaskDifficulty
from schemas.requests import CreateTaskRequest, UpdateTaskRequest
from schemas.responses import TaskResponse
from ..utils.openrouter import estimate_task_difficulty_full

router = APIRouter()


def parse_date_or_error(date_str: str) -> datetime.datetime:
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {date_str}. Expected ISO format.",
        )


def create_task_response(task: Task, task_difficulty: TaskDifficulty | None = None) -> TaskResponse:
    if not task_difficulty and task.difficulty_record:
        task_difficulty = task.difficulty_record
    return TaskResponse(
        id=str(task.id),
        name=task.name,
        description=task.description,
        due_date=task.due_date.isoformat() if task.due_date else None,
        is_completed=task.is_completed,
        diffulty_score=task_difficulty.score if task_difficulty else None,
        reasoning=task_difficulty.reasoning if task_difficulty else None,
        diffulty_estimation_time=task_difficulty.create_time.isoformat() if task_difficulty else None,
        create_time=task.create_time.isoformat(),
        update_time=task.update_time.isoformat(),
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: CreateTaskRequest, session: AsyncSession = Depends(deps.get_session)
):
    """Create a new task"""
    db_task = Task(
        name=task.name,
        description=task.description or "",
        due_date=parse_date_or_error(task.due_date) if task.due_date else None,
        is_completed=False,
        create_time=datetime.datetime.now(datetime.UTC),
        update_time=datetime.datetime.now(datetime.UTC),
    )
    session.add(db_task)
    await session.commit()
    task_difficulty = await estimate_task_difficulty_full(
        task_name=db_task.name, task_description=db_task.description
    )
    db_task.difficulty_record = TaskDifficulty(
        task_id=db_task.id,
        score=task_difficulty.difficulty_score,
        reasoning=task_difficulty.reasoning,
        create_time=datetime.datetime.now(datetime.UTC),
    )
    session.add(db_task.difficulty_record)
    await session.commit()
    return create_task_response(db_task, db_task.difficulty_record)


@router.get("/", response_model=list[TaskResponse])
async def get_tasks(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(deps.get_session)
):
    """Get all tasks"""
    tasks = await session.execute(select(Task).offset(skip).limit(limit).options(selectinload(Task.difficulty_record)))
    return [create_task_response(task) for task in tasks.scalars().all()]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, session: AsyncSession = Depends(deps.get_session)):
    """Get a specific task by ID"""
    task = await session.execute(select(Task).filter(Task.id == task_id).options(selectinload(Task.difficulty_record)))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return create_task_response(task.scalar_one())


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task: UpdateTaskRequest,
    session: AsyncSession = Depends(deps.get_session),
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
        db_task.due_date = parse_date_or_error(task.due_date)
    if task.is_completed is not None:
        db_task.is_completed = task.is_completed
    db_task.update_time = datetime.datetime.now(datetime.UTC)

    if task.difficulty_reestimate:
        task_difficulty = await estimate_task_difficulty_full(
            task_name=db_task.name, task_description=db_task.description
        )
        db_task.difficulty_record = TaskDifficulty(
            task_id=db_task.id,
            score=task_difficulty.difficulty_score,
            reasoning=task_difficulty.reasoning,
            create_time=datetime.datetime.now(datetime.UTC),
        )
        session.add(db_task.difficulty_record)

    session.add(db_task)
    await session.commit()
    return create_task_response(db_task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: AsyncSession = Depends(deps.get_session)):
    """Delete a task"""
    db_task = await session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(db_task)
    if db_task.difficulty_record:
        await session.delete(db_task.difficulty_record)
    await session.commit()
