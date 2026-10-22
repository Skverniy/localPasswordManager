from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.crypto import decrypt, encrypt
from app.core.deps import get_encryption_key
from app.database import get_db
from app.models.vault_item import VaultItem
from app.schemas.vault import (
    RevealResponse,
    VaultItemCreate,
    VaultItemResponse,
    VaultItemUpdate,
)

router = APIRouter(prefix="/api/vault", tags=["vault"])


def _to_response(item: VaultItem, key: bytes) -> VaultItemResponse:
    return VaultItemResponse(
        id=item.id,
        title=item.title,
        username=item.username,
        url=item.url,
        notes=decrypt(key, item.encrypted_notes),
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.get("/items", response_model=List[VaultItemResponse])
def list_items(
    db: Session = Depends(get_db),
    key: bytes = Depends(get_encryption_key),
) -> List[VaultItemResponse]:
    items = db.query(VaultItem).order_by(VaultItem.title.asc()).all()
    return [_to_response(it, key) for it in items]


@router.post("/items", response_model=VaultItemResponse, status_code=201)
def create_item(
    body: VaultItemCreate,
    db: Session = Depends(get_db),
    key: bytes = Depends(get_encryption_key),
) -> VaultItemResponse:
    item = VaultItem(
        title=body.title,
        username=body.username,
        url=body.url,
        encrypted_password=encrypt(key, body.password),
        encrypted_notes=encrypt(key, body.notes),
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_response(item, key)


@router.post("/items/{item_id}/reveal", response_model=RevealResponse)
def reveal_item(
    item_id: int,
    db: Session = Depends(get_db),
    key: bytes = Depends(get_encryption_key),
) -> RevealResponse:
    item = db.query(VaultItem).filter(VaultItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    try:
        return RevealResponse(password=decrypt(key, item.encrypted_password))
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


@router.put("/items/{item_id}", response_model=VaultItemResponse)
def update_item(
    item_id: int,
    body: VaultItemUpdate,
    db: Session = Depends(get_db),
    key: bytes = Depends(get_encryption_key),
) -> VaultItemResponse:
    item = db.query(VaultItem).filter(VaultItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    if body.title is not None:
        item.title = body.title
    if body.username is not None:
        item.username = body.username
    if body.url is not None:
        item.url = body.url
    if body.notes is not None:
        item.encrypted_notes = encrypt(key, body.notes)
    if body.password is not None:
        item.encrypted_password = encrypt(key, body.password)

    db.commit()
    db.refresh(item)
    return _to_response(item, key)


@router.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    key: bytes = Depends(get_encryption_key),
) -> dict:
    item = db.query(VaultItem).filter(VaultItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"success": True}