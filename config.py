import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = Field(default=os.getenv("BASE_URL", ""))
    admin_username: str = Field(default=os.getenv("ADMIN_USERNAME", ""))
    admin_password: str = Field(default=os.getenv("ADMIN_PASSWORD", ""))
    is_mobile: bool = Field(default=False)
    latitude: float = Field(default=48.9)
    longitude: float = Field(default=2.4)
    db_path: str = Field(default="")
    bob_username: str = Field(default="bob")
    bob_password: str = Field(default=os.getenv("ADMIN_PASSWORD", "password"))

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


settings = Settings()
