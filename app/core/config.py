from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    APP_NAME: str = "ExcuseSense AI"
    APP_ENV: str = "development"
    APP_VERSION: str = "2.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./excusesense.db"
    
    # ML Artifacts
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    MODEL_PATH: str = "model.pkl"
    VECTORIZER_PATH: str = "vectorizer.pkl"
    METRICS_PATH: str = "metrics.txt"
    DATASET_PATH: str = "leave_applications.csv"
    
    # CORS
    CORS_ORIGINS: Union[str, List[str]] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def get_model_path(self) -> str:
        if os.path.isabs(self.MODEL_PATH):
            return self.MODEL_PATH
        return os.path.join(self.BASE_DIR, self.MODEL_PATH)

    def get_vectorizer_path(self) -> str:
        if os.path.isabs(self.VECTORIZER_PATH):
            return self.VECTORIZER_PATH
        return os.path.join(self.BASE_DIR, self.VECTORIZER_PATH)

    def get_metrics_path(self) -> str:
        if os.path.isabs(self.METRICS_PATH):
            return self.METRICS_PATH
        return os.path.join(self.BASE_DIR, self.METRICS_PATH)

    def get_dataset_path(self) -> str:
        if os.path.isabs(self.DATASET_PATH):
            return self.DATASET_PATH
        return os.path.join(self.BASE_DIR, self.DATASET_PATH)

settings = Settings()
