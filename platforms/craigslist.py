import requests
from bs4 import BeautifulSoup
from typing import List
import time
import urllib.parse
from protocols.ucp import UCPProduct
from .base import BasePlatform

class CraigslistPlatform(BasePlatform):
    def __init__(self, region: str = "sfbay"):
        self.region = region
        self.base_url = f"https://{self.region}.craigslist.org"

    def search_items(self, query: str, limit: int = 5) -> List[UCPProduct]:
        print(f"Searching Craigslist ({self.region}) for: {query}")
        search_url = f"{self.base_url}/search/sss?query={urllib.parse.quote(query)}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        products = []
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Craigslist recently updated their DOM. Let's try multiple common selectors.
            results = soup.select('li.cl-search-result') or soup.select('li.result-row')

            for result in results[:limit]:
                try:
                    title_elem = result.select_one('.cl-app-anchor.posting-title') or result.select_one('.result-title')
                    if not title_elem:
                        continue

                    title = title_elem.text.strip()
                    url = title_elem.get('href', '')
                    if not url.startswith('http'):
                        url = f"https://{self.region}.craigslist.org" + url

                    price_elem = result.select_one('.priceinfo') or result.select_one('.result-price')
                    price = price_elem.text.strip() if price_elem else "N/A"

                    product_id = url.split('/')[-1].replace('.html', '')

                    products.append(UCPProduct(
                        id=product_id,
                        title=title,
                        price=price,
                        url=url,
                        attributes={"platform": "craigslist"}
                    ))
                except Exception as e:
                    print(f"Error parsing result: {e}")
        except Exception as e:
            print(f"Error fetching Craigslist: {e}")

        # Fallback to mock data to ensure the rest of the agent flow can be demonstrated
        # if Craigslist blocks the request or changes its DOM
        if not products:
            print("Failed to scrape live results (likely blocked). Using mock data for demonstration.")
            timestamp = int(time.time())
            products.append(UCPProduct(
                id=f"mock_{query.replace(' ', '_')}_{timestamp}_1",
                title=f"Used {query.capitalize()} in good condition",
                price="$450",
                url=f"https://{self.region}.craigslist.org/mock/{timestamp}_1.html",
                attributes={"platform": "craigslist_mock"}
            ))

        return products

    def send_message(self, product_url: str, message_content: str, dry_run: bool = True) -> bool:
        if dry_run:
            print(f"\n[DRY RUN] Would send message to {product_url}:\n{message_content}\n")
            return True
        else:
            print(f"\n[LIVE RUN - NOT IMPLEMENTED] Real messaging requires Playwright/Puppeteer and evasion.")
            print(f"Target: {product_url}\nMessage:\n{message_content}\n")
            return False
