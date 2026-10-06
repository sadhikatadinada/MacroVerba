import sys
import json
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.core.filesystem import ensure_directories
from src.core.database import get_db_connection

# RBI Imports
from src.sources.rbi.scraper import fetch_release_html
from src.sources.rbi.parser import extract_release_text

# Fed Imports
from src.sources.fed.scraper import fetch_fed_press_releases, fetch_fed_release_html
from src.sources.fed.parser import parse_fed_press_releases, extract_fed_release_text

def setup_environment():
    """Initialize the base project directories."""
    ensure_directories([RAW_DATA_DIR, PROCESSED_DATA_DIR])

def update_rbi():
    """Runs the data extraction pipeline for the Reserve Bank of India."""
    print("--- Running RBI Pipeline ---")
    metadata_path = PROCESSED_DATA_DIR / "rbi_metadata.json"
    
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            releases = json.load(f)
            
        print(f"Loaded {len(releases)} press releases. Updating database...")
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for release in releases:
            html = fetch_release_html(release["link"])
            if html:
                text = extract_release_text(html)
                try:
                    cursor.execute('''
                        INSERT INTO documents (institution, title, url, content)
                        VALUES (?, ?, ?, ?)
                    ''', ("RBI", release["title"], release["link"], text))
                    conn.commit()
                except Exception:
                    pass
                    
        conn.close()
        print("RBI pipeline complete.")

def update_fed():
    """Runs the data extraction pipeline for the Federal Reserve."""
    print("--- Running Federal Reserve Pipeline ---")
    soup = fetch_fed_press_releases()
    
    fed_html_path = RAW_DATA_DIR / "fed" / "latest_fed_releases.html"
    
    if fed_html_path.exists():
        releases = parse_fed_press_releases(fed_html_path)
        print(f"\nSuccessfully extracted {len(releases)} press releases. Updating database...")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for release in releases:
            html = fetch_fed_release_html(release["link"])
            if html:
                text = extract_fed_release_text(html)
                try:
                    cursor.execute('''
                        INSERT INTO documents (institution, title, url, content)
                        VALUES (?, ?, ?, ?)
                    ''', ("Fed", release["title"], release["link"], text))
                    conn.commit()
                    print(f"Successfully saved to database: {release['title']}")
                except Exception:
                    print(f"Skipped (already exists): {release['title']}")
                    
        conn.close()
        print("Federal Reserve pipeline complete.")

if __name__ == "__main__":
    setup_environment()
    
    if len(sys.argv) > 1:
        target_bank = sys.argv[1].lower()
        
        if target_bank == "rbi":
            update_rbi()
        elif target_bank == "fed":
            update_fed()
        else:
            print(f"Unknown institution: {target_bank}. Please use 'rbi' or 'fed'.")
    else:
        print("Please specify an institution. Example: python3 main.py fed")