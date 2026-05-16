"""Configuration management for Sauti ya Mwananchi."""

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Cloud
    google_cloud_project: str = Field(default="sauti-ya-mwananchi")
    google_cloud_location: str = Field(default="us-central1")
    google_genai_use_vertexai: bool = Field(default=True)
    
    # Africa's Talking
    at_username: str = Field(default="sandbox")
    at_api_key: str = Field(default="")
    at_environment: str = Field(default="sandbox")
    
    # Vertex AI Search
    civic_datastore_id: str = Field(default="")
    
    # Security
    phone_hash_salt: str = Field(default="sauti-salt-2026")
    
    # App
    log_level: str = Field(default="INFO")
    port: int = Field(default=8080)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def get_settings() -> Settings:
    """Dependency for retrieving settings."""
    return Settings()
