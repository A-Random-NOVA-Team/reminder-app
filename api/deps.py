from collections.abc import AsyncGenerator

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core import database_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with database_session.get_async_session() as session:
        yield session
