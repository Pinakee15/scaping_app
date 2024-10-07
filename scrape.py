import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://dentalstall.com/shop/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/85.0.4183.102 Safari/537.36"
}

def get_soup(url):
    """Fetches the content at the given URL and returns a BeautifulSoup object."""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status() 
    return BeautifulSoup(response.text, 'html.parser')

def extract_products(soup):
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
        
        desc_tag = item.find('div', class_='woocommerce-product-details__short-description')
        if desc_tag:
            product['Description'] = desc_tag.get_text(strip=True)
        else:
            product['Description'] = None

        price_tag = item.find('span', class_='woocommerce-Price-amount')
        if price_tag:
            product['Price'] = price_tag.get_text(strip=True)
        else:
            product['Price'] = None
        
        discount_tag = item.find('span', class_='onsale')
        if discount_tag:
            product['Discount'] = discount_tag.get_text(strip=True)
        else:
            product['Discount'] = None

        products.append(product)
    
    return products

def scrape_all_pages():
    """Scrapes all product pages by navigating through pagination."""
    all_products = []
    current_page = 1
    
    while current_page < 4:
        print(f"Scraping page {current_page}...")
        url = f"{BASE_URL}page/{current_page}/"
        soup = get_soup(url)
        products = extract_products(soup)
        
        if not products:
            print("No more products found. Ending scrape.")
            break
        
        all_products.extend(products)
        current_page += 1        
    
    return all_products

def save_to_csv(products, filename='products.csv'):
    """Saves the list of products to a CSV file."""
    keys = products[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)
    print(f"Saved {len(products)} products to {filename}")

if __name__ == "__main__":
    try:
        products = scrape_all_pages()
        if products:
            save_to_csv(products)
        else:
            print("No products were scraped.")
    except Exception as e:
        print(f"An error occurred: {e}")
