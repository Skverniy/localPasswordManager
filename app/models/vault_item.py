from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    username = Column(String, default="", nullable=False)
    url = Column(String, default="", nullable=False)
    encrypted_password = Column(Text, nullable=False)
    encrypted_notes = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )