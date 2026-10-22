from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    db_path: str = "/app/data/vault.db"
    jwt_secret: str = ""
    session_ttl_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

if not settings.jwt_secret:
    settings.jwt_secret = secrets.token_hex(32)
    print(
        "[config] JWT_SECRET not set — generated random value. "
        "Sessions will not survive a restart."
    )