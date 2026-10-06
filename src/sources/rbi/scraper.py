import requests
from bs4 import BeautifulSoup
from config import RAW_DATA_DIR
import time

def fetch_rbi_policy_page():
    
    url = "https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    print(f"Fetching data from {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("Successfully connected to RBI!")
        
        rbi_raw_dir = RAW_DATA_DIR / "rbi"
        rbi_raw_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = rbi_raw_dir / "latest_press_releases.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Saved raw HTML to {file_path}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print(f"Failed to connect. Status code: {response.status_code}")
        return None
    
def fetch_release_html(url: str) -> str | None:
    """Politely fetches the HTML of a single RBI press release."""
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
        print(f"Connection failed or timed out for {url}. Skipping to next.")
        return None