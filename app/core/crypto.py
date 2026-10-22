"""Argon2id KDF + AES-256-GCM encrypt/decrypt."""

import base64
import hashlib
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Argon2id parameters (RFC 9106 recommended for "second" mode)
ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 65536  # 64 MiB
ARGON2_PARALLELISM = 4
ARGON2_HASH_LEN = 32  # 256 bit AES key


def generate_salt() -> bytes:
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=ARGON2_HASH_LEN,
        type=Type.ID,
    )


def key_verify_hash(key: bytes) -> str:
    """Cheap verifier stored in DB — safe because key already derived via Argon2."""
    return hashlib.sha256(key).hexdigest()


def encrypt(key: bytes, plaintext: str) -> str:
    if not plaintext:
        return ""
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
    return base64.b64encode(nonce + ct).decode("ascii")


def decrypt(key: bytes, blob: str) -> str:
    if not blob:
        return ""
    raw = base64.b64decode(blob.encode("ascii"))
    nonce, ct = raw[:12], raw[12:]
    pt = AESGCM(key).decrypt(nonce, ct, None)
    return pt.decode("utf-8")