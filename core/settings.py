from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    echo: bool = True

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    SALT: str

    transport: HTTPBearer = HTTPBearer(auto_error=False)
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl="/auth/login"
    )

    @property
    def salt(self) -> str:
        return self.SALT


class AppSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    auth: AuthSettings = AuthSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
