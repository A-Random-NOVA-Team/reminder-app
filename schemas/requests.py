from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str


class UserLoginRequest(BaseRequest):
    email: EmailStr
    password: str


class UserLogoutRequest(BaseRequest):
    refresh_token: str


class CreateTaskRequest(BaseRequest):
    name: str
    description: str | None = None
    due_date: str | None = None


class UpdateTaskRequest(BaseRequest):
    name: str | None = None
    description: str | None = None
    difficulty_reestimate: bool | None = None
    due_date: str | None = None
    is_completed: bool | None = None


class DeleteTaskRequest(BaseRequest):
    task_id: str
