import requests
import time
from bs4 import BeautifulSoup
from config import RAW_DATA_DIR

def fetch_boe_press_releases():
    """Fetches the Bank of England monetary policy summaries."""
    url = "https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/monetary-policy-summary-and-minutes"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Politely fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            boe_raw_dir = RAW_DATA_DIR / "boe"
            boe_raw_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = boe_raw_dir / "latest_boe_releases.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                
            print(f"Successfully saved BoE raw HTML to {file_path}")
            return BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"Failed to connect to BoE. Status: {response.status_code}")
            return None
    except Exception as e:
        print(f"Connection failed for {url}. Error: {e}")
        return None

def fetch_boe_release_html(url: str) -> str | None:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    print(f"Politely fetching {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            time.sleep(2)
            return response.text
        return None
    except Exception:
        print(f"Connection failed or timed out for {url}. Skipping.")
        return None