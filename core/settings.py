from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    url: str = f"sqlalchemy+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    echo: bool = True

    model_config = SettingsConfigDict(env_file=".env")


class AppSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
