import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_mode = os.getenv("APP_ENV", "dev")
env_file = ".env.test" if env_mode == "test" else ".env"

class Settings(BaseSettings):

    SECRET_KEY_ACCESS: str
    SECRET_KEY_REFRESH: str
    SECRET_KEY_VERIFY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    VERIFY_TOKEN_EXPIRES: int

    CLIENT_HOST_PROTOCOL: str 
    CLIENT_HOST: str 
    CLIENT_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=env_file,
        extra="ignore"
    )


settings = Settings()