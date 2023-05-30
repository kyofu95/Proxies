import os


class Settings:
    """This class represents the settings for the application."""

    DATABASE_URI: str = os.environ.get("DATABASE_URI", "")
    SECRET_KEY: str = os.environ.get("DATABASE_URI", "")


settings = Settings()
