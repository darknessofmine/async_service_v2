from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def url(self) -> str:
        return (
            "postgresql+asyncpg:"
            f"//{self.DB_USER}"
            f":{self.DB_PASS}"
            f"@{self.DB_HOST}"
            f":{self.DB_PORT}"
            f"/{self.DB_NAME}"
        )


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
