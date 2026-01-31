#настройки
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/bookstore"
    secret_key: str = "6Ty18bTOf"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 15

    app_name: str = "BookStoreApishka"
    debug: bool = True
    
    #pagina
    default_page_size: int = 20
    max_page_size: int = 100

    model_config = ConfigDict(
        env_file = ".env",
        extra="ignore"
    )

settings = Settings()