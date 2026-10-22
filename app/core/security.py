from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.config import settings

ALGORITHM = "HS256"


def create_token(session_id: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.session_ttl_minutes)
    payload = {"sub": session_id, "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None