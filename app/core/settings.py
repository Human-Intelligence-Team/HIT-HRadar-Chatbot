from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_ENV: str = "local"
    APP_NAME: str = "HRadar Chatbot"

    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    RELEVANCE_THRESHOLD: float = 0.6

    # MongoDB
    MONGO_URI: str
    MONGO_DB: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()