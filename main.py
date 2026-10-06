import json
from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.core.filesystem import ensure_directories
from src.sources.rbi.scraper import fetch_rbi_policy_page
from src.sources.rbi.parser import parse_rbi_press_releases

def setup_environment():
    print("Setting up MacroVerba directories...")
    ensure_directories([RAW_DATA_DIR, PROCESSED_DATA_DIR])
    print("Directories ready.\n")

if __name__ == "__main__":
    setup_environment()
    
    metadata_path = PROCESSED_DATA_DIR / "rbi_metadata.json"
    
    if metadata_path.exists():
        with open(metadata_path, "r", encoding="utf-8") as f:
            releases = json.load(f)
            
        print(f"Loaded {len(releases)} press releases from JSON.")
        
        from src.sources.rbi.scraper import fetch_release_html
        from src.sources.rbi.parser import extract_release_text
        
        for release in releases[:3]:
            html = fetch_release_html(release["link"])
            if html:
                print(f"Successfully downloaded: {release['title']}")
                
                text = extract_release_text(html)
                snippet = text[:200].replace("\n", " ")
                print(f"Preview: {snippet}...\n")