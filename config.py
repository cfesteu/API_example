from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_URL :str
    DATE_FORMAT :str
    ORC_USERNAME : str
    ORC_PASSWORD : str
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        extra="allow"
    )


settings = Settings()

