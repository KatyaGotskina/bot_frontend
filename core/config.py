from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    BOT_TOKEN: str
    WEBHOOK_URL: str
    BOT_BACKEND_HOST: str
    RETRY_COUNT: int = 3
    AUTH_KEY: str
    LOG_LEVEL: str


settings = Settings()
