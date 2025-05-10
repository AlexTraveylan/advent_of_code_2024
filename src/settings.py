from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aoc_cookie: str
    year: int
    openai_api_key: str

    class Config:
        env_file = ".env"
