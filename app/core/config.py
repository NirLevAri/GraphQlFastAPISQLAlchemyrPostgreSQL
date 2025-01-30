# app/core/config.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:pass@localhost:5432/mydb")

settings = Settings()
