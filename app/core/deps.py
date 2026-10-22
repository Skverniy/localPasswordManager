from fastapi import Depends, HTTPException, Request

from app.core.security import verify_token

COOKIE_NAME = "session_token"


def get_session_id(request: Request) -> str:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    session_id = verify_token(token)
    if not session_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return session_id


def get_encryption_key(
    request: Request,
    session_id: str = Depends(get_session_id),
) -> bytes:
    key = request.app.state.sessions.get(session_id)
    if not key:
        raise HTTPException(
            status_code=401,
            detail="Session expired — please log in again",
        )
    return key