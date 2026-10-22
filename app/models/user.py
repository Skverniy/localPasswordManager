from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    salt = Column(LargeBinary, nullable=False)      # Argon2 salt (16 bytes)
    password_hash = Column(String, nullable=False)  # sha256(derived_key).hex()
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)