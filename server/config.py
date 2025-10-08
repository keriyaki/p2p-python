from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "renan#lindo"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_USER: str = "p2p"
    DB_PASS: str = "p2p"
    DB_NAME: str = "p2p"

    TRACKER_BASE: str = "http://localhost:8000/tracker"

    class Config:
        env_file = ".env"


settings = Settings()
