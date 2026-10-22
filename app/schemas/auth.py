from pydantic import BaseModel, Field


class SetupRequest(BaseModel):
    master_password: str = Field(..., min_length=8, max_length=256)


class LoginRequest(BaseModel):
    master_password: str = Field(..., min_length=1, max_length=256)


class AuthResponse(BaseModel):
    success: bool
    message: str = ""


class StatusResponse(BaseModel):
    initialized: bool