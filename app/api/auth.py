import secrets as py_secrets
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session

from app.config import settings
from app.core.crypto import (
    derive_key,
    generate_salt,
    key_verify_hash,
)
from app.core.deps import COOKIE_NAME
from app.core.limiter import limiter
from app.core.security import create_token, verify_token
from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    SetupRequest,
    StatusResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/status", response_model=StatusResponse)
def status(db: Session = Depends(get_db)) -> StatusResponse:
    return StatusResponse(initialized=db.query(User).count() > 0)


@router.post("/setup", response_model=AuthResponse)
@limiter.limit("3/minute")
def setup(
    request: Request,
    body: SetupRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    if db.query(User).count() > 0:
        raise HTTPException(status_code=400, detail="Already initialized")

    salt = generate_salt()
    key = derive_key(body.master_password, salt)
    db.add(User(salt=salt, password_hash=key_verify_hash(key)))
    db.commit()
    return AuthResponse(success=True, message="Setup complete")


@router.post("/login", response_model=AuthResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    body: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> AuthResponse:
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="Not initialized")

    key = derive_key(body.master_password, user.salt)
    if not py_secrets.compare_digest(key_verify_hash(key), user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid master password")

    session_id = uuid.uuid4().hex
    request.app.state.sessions[session_id] = key
    token = create_token(session_id)

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="strict",
        secure=False,  # local HTTP; set True behind TLS
        max_age=settings.session_ttl_minutes * 60,
        path="/",
    )
    return AuthResponse(success=True, message="Logged in")


@router.post("/logout", response_model=AuthResponse)
def logout(request: Request, response: Response) -> AuthResponse:
    token = request.cookies.get(COOKIE_NAME)
    if token:
        sid = verify_token(token)
        if sid:
            request.app.state.sessions.pop(sid, None)
    response.delete_cookie(COOKIE_NAME, path="/")
    return AuthResponse(success=True, message="Logged out")