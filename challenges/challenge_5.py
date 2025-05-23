import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

async def fetch_url(session, url):
    print(f"Fetching {url}")
    start_time = time.time()
    try:
        async with session.get(url) as response:
            html = await response.text()
            duration = time.time() - start_time
            print(f"Fetched {url} in {duration:.2f} seconds")
            return {
                "url": url,
                "status": response.status,
                "content_length": len(html),
                "duration": duration,
                "html": html
            }
    except Exception as e:
        duration = time.time() - start_time
        print(f"Error fetching {url}: {e} after {duration:.2f} seconds")
        return {
            "url": url,
            "status": "error",
            "error_message": str(e),
            "duration": duration
        }

async def extract_title(html_data):
    url = html_data["url"]
    if html_data.get("status") == "error":
        return {"url": url, "title": "N/A (Error)", "links_count": 0}
    
    soup = BeautifulSoup(html_data["html"], 'html.parser')
    title = soup.title.text if soup.title else "No title found"
    links = soup.find_all('a')
    
    return {
        "url": url,
        "title": title,
        "links_count": len(links)
    }

async def scrape_website(url):
    async with aiohttp.ClientSession() as session:
        html_data = await fetch_url(session, url)
        metadata = await extract_title(html_data)
        return metadata

async def scrape_all_websites(urls):
    start_time = time.time()
    tasks = [scrape_website(url) for url in urls]
    results = await asyncio.gather(*tasks)
    total_time = time.time() - start_time
    
    print(f"\nAll URLs scraped in {total_time:.2f} seconds")
    return results

if __name__ == "__main__":
    urls_to_scrape = [
        "https://www.python.org",
        "https://docs.python.org",
        "https://pypi.org",
        "https://www.djangoproject.com",
        "https://fastapi.tiangolo.com",
        "https://www.postgresql.org",
        "https://www.mongodb.com",
        "https://redis.io",
        "https://github.com",
        "https://stackoverflow.com"
    ]
    
    results = asyncio.run(scrape_all_websites(urls_to_scrape))
    
    print("\nResults:")
    for result in results:
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Links Count: {result['links_count']}")
        print("-" * 50)