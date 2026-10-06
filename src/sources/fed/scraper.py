import requests
from bs4 import BeautifulSoup
from config import RAW_DATA_DIR
import time

def fetch_fed_press_releases():
    """Fetches the latest press releases from the Federal Reserve."""
    url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Politely fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            fed_raw_dir = RAW_DATA_DIR / "fed"
            fed_raw_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = fed_raw_dir / "latest_fed_releases.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                
            print(f"Successfully saved Fed raw HTML to {file_path}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to connect to Fed. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection failed for {url}. Error: {e}")
        return None
    
def fetch_fed_release_html(url: str) -> str | None:
    """Politely fetches the HTML of a single Fed press release."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Politely fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            time.sleep(2)
            return response.text
        else:
            print(f"Failed to fetch {url}. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection failed or timed out for {url}. Skipping.")
        return None