from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.auth import AuthHandler

app = FastAPI()

AUTH_TOKEN = "sample_token" 

auth_handler = AuthHandler(token=AUTH_TOKEN)

class ScrapeRequest(BaseModel):
    limit: Optional[int] = None
    proxy: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Scraper API is running."}

@app.post("/scrape")
def scrape(request: ScrapeRequest, token: str = Depends(auth_handler.authenticate)):
    return {"message": "Scraping endpoint reached."}

