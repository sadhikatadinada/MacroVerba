import json
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.core.filesystem import ensure_directories
from src.core.database import init_db
from src.sources.rbi.scraper import fetch_rbi_policy_page, fetch_release_html
from src.sources.rbi.parser import parse_rbi_press_releases, extract_release_text

def setup_environment():
    print("Setting up MacroVerba directories...")
    ensure_directories([RAW_DATA_DIR, PROCESSED_DATA_DIR])
    init_db()
    print("Directories and Database ready.\n")

if __name__ == "__main__":
    setup_environment()
    
    metadata_path = PROCESSED_DATA_DIR / "rbi_metadata.json"
    
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            releases = json.load(f)
            
        print(f"Loaded {len(releases)} press releases from JSON.")
        
        from src.sources.rbi.scraper import fetch_release_html
        from src.sources.rbi.parser import extract_release_text
        from src.core.database import get_db_connection
        
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
                    print(f"Successfully saved to database: {release['title']}")
                except Exception as e:
                    print(f"Skipped (already exists or error): {release['title']}")
                    
        conn.close()
        print("\nDatabase operations complete.")