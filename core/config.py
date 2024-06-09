from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


load_dotenv()


class Settings(BaseSettings):

    BOT_TOKEN: str
    # WEBHOOK_URL: str = ''
    # REDIS_HOST: str = 'redis'
    # REDIS_PORT: int = 6379
    # REDIS_PASSWORD: str
    # REDIS_DB: int = 0
    # LOG_LEVEL: str = ''
    BOT_BACKEND_HOST: str
    RETRY_COUNT: int = 3


settings = Settings()
