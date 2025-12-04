from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Union


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., description="MySQL/MariaDB connection string")

    # Application
    APP_NAME: str = Field(default="Media Manager API", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # CORS
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default="http://localhost:5173,http://localhost:3000",
        description="Allowed CORS origins (comma-separated in .env)"
    )

    # Upload
    UPLOAD_DIR: str = Field(default="./media", description="Directory for uploaded files")
    MAX_FILE_SIZE: int = Field(default=104857600, description="Max file size in bytes (100MB)")
    ALLOWED_EXTENSIONS: Union[str, List[str]] = Field(
        default="image/jpeg,image/png,image/gif,image/webp,video/mp4,video/webm,video/quicktime",
        description="Allowed MIME types (comma-separated in .env)"
    )

    # Security
    SECRET_KEY: str = Field(..., description="Secret key for security")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_allowed_extensions(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding="utf-8"
    )


settings = Settings()

