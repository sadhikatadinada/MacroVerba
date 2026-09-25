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
    
    soup = fetch_rbi_policy_page()
    
    rbi_html_path = RAW_DATA_DIR / "rbi" / "latest_press_releases.html"
    
    if rbi_html_path.exists():
        extracted_data = parse_rbi_press_releases(rbi_html_path)
        print(f"\nSuccessfully extracted {len(extracted_data)} press releases!")
        
        output_file = PROCESSED_DATA_DIR / "rbi_metadata.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(extracted_data, f, indent=4)
            
        print(f"Saved metadata to {output_file}")