from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.auth import AuthHandler
from models.product import Product
from scraper.storage import SQLiteStorage, StorageInterface
from scraper.cache import RedisCache, CacheInterface
from scraper.scraper import Scraper  
from scraper.notifier import NotifierInterface, ConsoleNotifier  

app = FastAPI()

# Configuration
AUTH_TOKEN = "sample_token"  # Replace with your actual token
BASE_URL = "https://dentalstall.com/shop/"

# Initialize AuthHandler
auth_handler = AuthHandler(token=AUTH_TOKEN)

# Initialize Storage
storage: StorageInterface = SQLiteStorage()

# Initialize Cache
cache: CacheInterface = RedisCache()

# Initialize Notifier
notifier: NotifierInterface = ConsoleNotifier()

class ScrapeRequest(BaseModel):
    limit: Optional[int] = None
    proxy: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "DentalStall Scraper API is running."}

@app.post("/scrape")
def scrape(request: ScrapeRequest, token: str = Depends(auth_handler.authenticate)):
    scraper = Scraper(proxy=request.proxy, cache=cache)
    scraped_products = scraper.scrape(base_url=BASE_URL, limit=request.limit)

    scraped_count = 0
    updated_count = 0
    for product in scraped_products:
        scraped_count += 1
        cached_price = cache.get_price(product.product_title)
        if cached_price is None or cached_price != product.product_price:
            storage.update_product(product)
            cache.set_price(product.product_title, product.product_price)
            updated_count += 1

    notifier.notify(scraped=scraped_count, updated=updated_count)
    return {"message": f"Scraping completed. Products scraped: {scraped_count}, Products updated: {updated_count}"}

