from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API JEC/Krona Futsal"
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/jec_krona"

    class Config:
        env_file = ".env" 

settings = Settings()