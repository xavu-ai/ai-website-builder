from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Website Builder API"
    debug: bool = False
    redis_url: str = "redis://localhost:6379/0"
    max_prompt_length: int = 2000

    class Config:
        env_file = ".env"


settings = Settings()
