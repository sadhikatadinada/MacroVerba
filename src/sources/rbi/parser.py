from bs4 import BeautifulSoup
from pathlib import Path

def parse_rbi_press_releases(file_path: Path) -> list[dict]:
    """Parses the saved RBI HTML file to extract titles and links."""
    print(f"Parsing {file_path.name}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
    releases = []
    
    for link in soup.find_all("a"):
        href = link.get("href", "")
        
        if "prid=" in href.lower():
            title = link.get_text(strip=True)
            full_url = f"https://rbi.org.in/Scripts/{href}" if not href.startswith("http") else href
            
            releases.append({
                "title": title,
                "link": full_url
            })
            
    return releases