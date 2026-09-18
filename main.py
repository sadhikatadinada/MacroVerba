from config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.core.filesystem import ensure_directories

from src.sources.rbi.scraper import fetch_rbi_policy_page

def setup_environment():
    print("Setting up MacroVerba directories....")
    ensure_directories([RAW_DATA_DIR, PROCESSED_DATA_DIR])
    print("Directories ready!")
    
if __name__ == "__main__":
    setup_environment()
    
    soup = fetch_rbi_policy_page()
    if soup:
        print("Page title found:", soup.title.string)