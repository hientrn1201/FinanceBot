from pydantic_settings import BaseSettings


class Settings(BaseSettings, extra="allow"):
    app_name: str = "Awesome API"

    class Config:
        env_file = ".env"
