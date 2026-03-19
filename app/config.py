from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""
    booking_api_key: str = ""
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "dev-secret-key"

    model_config = {"env_file": ".env"}


settings = Settings()
