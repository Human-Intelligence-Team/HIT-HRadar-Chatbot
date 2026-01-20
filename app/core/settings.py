from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # ===== App =====
    APP_NAME: str = "HRadar Chatbot"
    APP_ENV: str = "local"

    # ===== OpenAI =====
    OPENAI_API_KEY: str

    # ===== MongoDB =====
    MONGO_URI: str
    MONGO_DB: str = "hradar_chatbot"

    # ===== App =====
    APP_ENV: str = "local"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()
