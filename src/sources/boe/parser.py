from bs4 import BeautifulSoup
from pathlib import Path

def parse_boe_press_releases(file_path: Path) -> list[dict]:
    """
    Bypasses BoE's JavaScript UI by explicitly targeting the 
    2021-2023 inflation shock monetary policy summaries.
    """
    print("Bypassing JS UI: Injecting 2021-2023 BoE MPC archive...")
    
    meetings = [
        ("December 2021", "2021/december-2021"),
        ("February 2022", "2022/february-2022"),
        ("May 2022", "2022/may-2022"),
        ("August 2022", "2022/august-2022"),
        ("November 2022", "2022/november-2022"),
        ("February 2023", "2023/february-2023"),
        ("May 2023", "2023/may-2023"),
        ("August 2023", "2023/august-2023"),
        ("November 2023", "2023/november-2023"),
    ]
    
    releases = []
    for title_date, url_path in meetings:
        releases.append({
            "title": f"BoE Monetary Policy Summary - {title_date}",
            "link": f"https://www.bankofengland.co.uk/monetary-policy-summary-and-minutes/{url_path}"
        })
        
    return releases

def extract_boe_release_text(html: str) -> str:
    """Extracts the main paragraph text from a BoE HTML document."""
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    text_blocks = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
    return "\n\n".join(text_blocks)