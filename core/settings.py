from pathlib import Path

from fastapi.security import HTTPBearer, OAuth2PasswordBearer

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    @property
    def url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class FastMailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class JWTSettings(BaseModel):
    private_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key: Path = BASE_DIR / "certs" / "jwt-public.pem"

    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    reset_password_expire_minutes: int = 10
    verification_expire_minutes: int = 10


class AuthSettings(BaseSettings):
    HASH_SALT: str

    transport: HTTPBearer = HTTPBearer(auto_error=False)
    oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(
        tokenUrl="/auth/login"
    )

    jwt: JWTSettings = JWTSettings()

    @property
    def salt(self) -> str:
        return self.HASH_SALT

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class AppSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True

    @property
    def domain(self) -> str:
        return f"{self.port}:{self.host}"


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    auth: AuthSettings = AuthSettings()
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    mail: FastMailSettings = FastMailSettings()


settings = Settings()
