from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_ENV: str = "local"
    APP_NAME: str = "HRadar Chatbot"

    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    RELEVANCE_THRESHOLD: float = 0.45

    # MongoDB
    MONGO_URI: str
    MONGO_DB: str

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC: str = "document.index"
    KAFKA_GROUP_ID: str = "hr-chatbot-indexer"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
