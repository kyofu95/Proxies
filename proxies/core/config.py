import os


class Settings:
    """This class represents the settings for the application."""

    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "dev")
    DATABASE_URI: str = os.environ.get("DATABASE_URI", "")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    MAXDBLITE_PATH: str = os.environ.get("MAXDBLITE_PATH", "")


settings = Settings()
