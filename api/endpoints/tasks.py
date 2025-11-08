import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api import deps
from models import Task, TaskDifficulty
from schemas.requests import CreateTaskRequest, UpdateTaskRequest
from schemas.responses import TaskResponse

from ..utils.datetime import add_timezone_to_datetime, parse_date_or_error
from ..utils.openrouter import TaskDifficultySchema, estimate_task_difficulty_full

router = APIRouter()


async def run_estimate_task_difficulty(
    task: Task) -> TaskDifficultySchema:
    if task.due_date is not None:
        due_date = add_timezone_to_datetime(task.due_date)
        created = add_timezone_to_datetime(task.create_time)
        deadline_str = f"{due_date - created}"
    else:
        deadline_str = None
    return await estimate_task_difficulty_full(
        task_name=task.name, task_description=task.description, task_deadline=deadline_str
    )

def create_task_response(task: Task, task_difficulty: TaskDifficulty | None = None) -> TaskResponse:
    return TaskResponse(
        id=str(task.id),
        name=task.name,
        description=task.description,
        due_date=task.due_date.isoformat() if task.due_date else None,
        is_completed=task.is_completed,
        difficulty_score=task_difficulty.score if task_difficulty else None,
        reasoning=task_difficulty.reasoning if task_difficulty else None,
        difficulty_estimation_time=task_difficulty.create_time.isoformat() if task_difficulty else None,
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
    task_difficulty = await run_estimate_task_difficulty(db_task)
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
    exclude_completed: bool = False, skip: int = 0, limit: int = 100, session: AsyncSession = Depends(deps.get_session)
):
    """Get all tasks"""
    query = select(Task).offset(skip).limit(limit).options(selectinload(Task.difficulty_record))
    if exclude_completed:
        query = query.filter(Task.is_completed == False)
    tasks = await session.execute(query)
    result = []
    for task in tasks.scalars().all():
        difficulty_record = task.difficulty_record
        result.append(create_task_response(task, difficulty_record))
    return result


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
        task_difficulty = await run_estimate_task_difficulty(db_task)
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
