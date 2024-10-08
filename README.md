markdown
Copy code
# DentalStall Scraper Tool

## Overview

A FastAPI-based tool to scrape product information from [DentalStall](https://dentalstall.com/shop/). It extracts product names, prices, and image URLs, stores them in a SQLite database, caches the data, and upon re-scraping, only stores new data and updates existing entries based on cache status. It also provides notifications upon completion.

## Features

- Scrape product details from multiple pages with optional limits.
- Supports proxy settings for scraping.
- Stores data in a SQLite database with easy extensibility for other storage methods.
- Notifies via console output after scraping.
- Implements type validation, retry mechanisms, authentication, and caching using Redis.
- Modular and extensible design using Object-Oriented Design principles and the Strategy Pattern.

## Setup

1. **Clone the Repository**

   ```bash
   git clone git@github.com:Pinakee15/scaping_app.git
   cd scaping_app
2. ** Create a virtual env and a .env file
   ```bash
   python3 -m venv {your env name}
   // Put the following in .env file 
   AUTH_TOKEN={your key}   

3. Install & run redis if not already
   ```bash
   brew install redis
   brew services start redis
4. **Install Dependencies and run server
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload

5. Run the curl request and put limit, token & proxy accordingly
   ```bash
   curl -X POST "http://127.0.0.1:8000/scrape" \
     -H "Content-Type: application/json" \
     -H "token: securetoken12345" \
     -d '{"limit":3, "proxy":"http://user:pass@proxyserver:port"}'
6. Check you redis and sqlite db for the data
   ```bash
   redis-cli
   KEYS *

   sqlite3 products.db
7. Try different limit param and see that only the new or exiting product with
   new value are updated in the db 



   
    