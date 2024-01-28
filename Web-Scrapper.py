import requests
from bs4 import BeautifulSoup
import csv
import random
import time
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def scrape_eCommerce_website(url, num_pages=5):
    headers = {'User-Agent': get_random_user_agent()}
    all_products = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}/page/{page}" if page > 1 else url
        response = requests.get(page_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_containers = soup.find_all('div', class_='product-container')

            for product in product_containers:
                product_info = {
                    'Name': product.find('h2', class_='product-title').text.strip(),
                    'Price': product.find('span', class_='price').text.strip(),
                    'Rating': product.find('span', class_='rating').text.strip(),
                    'Availability': product.find('span', class_='availability').text.strip()
                }
                all_products.append(product_info)

            # This aspect is to introduce a random delay to avoid being blocked by the website
            time.sleep(random.uniform(1, 3))
        else:
            print(f"Failed to retrieve data from {page_url}. Status Code: {response.status_code}")

    return all_products

def save_to_csv(data, filename='scraped_data.csv'):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Rating', 'Availability']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Writing the headers
            writer.writeheader()

            # Writing the data
            for product in data:
                writer.writerow(product)

        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

if __name__ == '__main__':
    ecommerce_url = 'https://amazon.co.uk'
    scraped_data = scrape_eCommerce_website(ecommerce_url, num_pages=5)
    save_to_csv(scraped_data)
