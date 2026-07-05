from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://f1:f1@localhost:5432/f1_race_intel"
    openf1_base_url: str = "https://api.openf1.org/v1"
    api_host: str = "0.0.0.0"
    api_port: int = 8000


settings = Settings()
