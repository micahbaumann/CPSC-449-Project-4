from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings, env_file="users/.env", extra="ignore"):
    logging_config: str

app = FastAPI()

# Example Endpoint
@app.get("/example/{ex}")
def example(ex: str):
    return []