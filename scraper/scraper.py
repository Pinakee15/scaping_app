import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from models.product import Product
import time

BASE_URL = "https://dentalstall.com/shop/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/85.0.4183.102 Safari/537.36"
}

class Scraper:
    def __init__(self, proxy: Optional[str] = None, retries: int = 3, backoff: int = 2):
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.retries = retries
        self.backoff = backoff

    def get_soup(self, url: str) -> Optional[BeautifulSoup]:
        """Fetches the content at the given URL and returns a BeautifulSoup object."""
        attempt = 0
        while attempt < self.retries:
            try:
                # response = requests.get(url, headers=HEADERS, proxies=self.proxy, timeout=10)
                response = requests.get(url, headers=HEADERS, timeout=10)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}. Retrying in {self.backoff} seconds...")
                time.sleep(self.backoff)
                attempt += 1
        print(f"Failed to fetch {url} after {self.retries} attempts.")
        return None

    def extract_products(self, soup: BeautifulSoup) -> List[Product]:
        """Extracts product information from the BeautifulSoup object."""
        products = []

        product_items = soup.find_all('li', class_='product')

        for item in product_items:
            product = {}

            title_tag = item.find('h2', class_='woo-loop-product__title')
            if title_tag and title_tag.find('a'):
                product['Title'] = title_tag.find('a').get_text(strip=True)
                product['Product URL'] = title_tag.find('a')['href']
            else:
                product['Title'] = None
                product['Product URL'] = None

            img_tag = item.find('div', class_='mf-product-thumbnail').find('img')
            if img_tag:
                product['Image URL'] = img_tag.get('src') or img_tag.get('data-lazy-src')
            else:
                product['Image URL'] = None


            price_ins = item.find('ins')
            if price_ins:
                price_tag = price_ins.find('span', class_='woocommerce-Price-amount amount')
            else:
                price_tag = item.find('span', class_='woocommerce-Price-amount amount')
            
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                price_numeric = ''.join(c for c in price_text if (c.isdigit() or c == '.' or c == ','))
                price_numeric = price_numeric.replace(',', '')
                try:
                    product['Price'] = float(price_numeric)
                except ValueError:
                    product['Price'] = 0.0
            else:
                product['Price'] = 0.0
            
            if product['Title'] and product['Image URL']:                
                product_model = Product(
                    product_title=product['Title'],
                    product_price=product['Price'],
                    path_to_image=product['Image URL']
                )
                products.append(product_model)                

        return products

    def scrape_all_pages(self, base_url: str, limit: Optional[int] = None) -> List[Product]:
        """Scrapes all product pages by navigating through pagination."""
        all_products = []
        current_page = 1

        while True:
            if limit and current_page > limit:
                break
            print(f"Scraping page {current_page}...")
            url = f"{base_url}"
            if current_page > 1:
                url = f"{base_url}page/{current_page}/"
            
            soup = self.get_soup(url)            
            if not soup:
                break
            products = self.extract_products(soup)          
            if not products:
                print("No more products found. Ending scrape.")
                break

            all_products.extend(products)
            current_page += 1

        return all_products

