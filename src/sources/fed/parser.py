from bs4 import BeautifulSoup
from pathlib import Path

def parse_fed_press_releases(file_path: Path) -> list[dict]:
    """Parses the saved Fed HTML file to extract titles and links."""
    print(f"Parsing {file_path.name}...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
    releases = []
    
    for link in soup.find_all("a"):
        href = link.get("href", "")
        
        if "/newsevents/pressreleases/" in href.lower() and href.endswith(".htm"):
            title = link.get_text(strip=True)
            
            if not title or title.lower() == "html":
                continue
                
            full_url = f"https://www.federalreserve.gov{href}" if href.startswith("/") else href
            
            if not any(r['link'] == full_url for r in releases):
                releases.append({
                    "title": title,
                    "link": full_url
                })
                
    return releases

def extract_fed_release_text(html: str) -> str:
    """Extracts the main paragraph text from a Fed press release HTML."""
    soup = BeautifulSoup(html, "html.parser")
    
    paragraphs = soup.find_all("p")
    
    text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
    return "\n\n".join(text_blocks)