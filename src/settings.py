from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    aoc_cookie: str
    year: int

    class Config:
        env_file = ".env"
