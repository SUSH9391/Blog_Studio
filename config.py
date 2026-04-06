from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    database_url: str

    db_user: str = ""
    db_password: SecretStr = SecretStr("")
    db_host: str = ""
    db_port: int = 5432
    db_name: str = ""

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    max_upload_size_bytes: int = 5 * 1024 * 1024

    posts_per_page: int = 10

    reset_token_expire_minutes: int = 60

    mail_server: str = "localhost"
    mail_port: int = 587
    mail_username: str = ""
    mail_password: SecretStr = SecretStr("")
    mail_from: str = "noreply@example.com"
    mail_use_tls: bool = True



    supabase_url: str = ""
    supabase_anon_key: SecretStr = SecretStr("")
    sentry_dsn: str = ""

    @field_validator("database_url", mode="before")
    @classmethod
    def build_database_url(cls, v: str, info) -> str:
        if not v.strip():
            data = info.data
            user = data.get("db_user")
            password = data.get("db_password")
            host = data.get("db_host")
            port = data.get("db_port")
            dbname = data.get("db_name")
            if all([user, password, host, port, dbname]):
                pw = password.get_secret_value()
                return f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{dbname}?sslmode=require"
        return v


settings = Settings()  # type: ignore[call-arg] # Loaded from .env file
