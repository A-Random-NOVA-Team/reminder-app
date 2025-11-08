from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int


class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr


class TaskResponse(BaseResponse):
    id: str
    name: str
    description: str | None
    due_date: str | None
    is_completed: bool
    diffulty_score: int | None = None
    reasoning: str | None = None
    diffulty_estimation_time: str | None = None
    create_time: str
    update_time: str
