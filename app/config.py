from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    db_host: str = Field(default='localhost', alias='DB_HOST')
    db_port: int = Field(default=5432, alias='DB_PORT')
    db_name: str = Field(default='expert_system', alias='DB_NAME')
    db_user: str = Field(default='postgres', alias='DB_USER')
    db_password: str = Field(default='postgres', alias='DB_PASSWORD')

    decision_threshold: float = Field(default=0.95, alias='DECISION_THRESHOLD')
    exclusion_threshold: float = Field(default=0.01, alias='EXCLUSION_THRESHOLD')

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+psycopg://{self.db_user}:{self.db_password}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )


ROOT_DIR = Path(__file__).resolve().parent.parent
settings = Settings()
