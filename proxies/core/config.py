import os


class Settings:
    """This class represents the settings for the application."""

    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "dev")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD", "")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB", "")
    DATABASE_URI: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    MAXDBLITE_PATH: str = os.environ.get("MAXDBLITE_PATH", "/opt/GeoLite2-City.mmdb")


settings = Settings()
