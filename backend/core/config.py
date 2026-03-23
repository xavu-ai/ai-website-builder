from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    APP_NAME: str = "AI Website Builder API"
    DEBUG: bool = False
    MAX_PROMPT_LENGTH: int = 2000
    REDIS_URL: str | None = None


settings = Settings()
