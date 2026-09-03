from urllib.parse import urlparse
import socket
import requests
from bs4 import BeautifulSoup

class ScrapeTool:
    def __init__(self):
        pass

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "scrape_url",
                    "description": "Fetch a webpage and extract its text content. Useful for reading articles, documentation, or extracting data from a specific website.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL of the website to scrape."
                            }
                        },
                        "required": ["url"]
                    }
                }
            }
        ]

    def scrape_url(self, url: str) -> dict:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            # SSRF Protection: Ensure we don't scrape internal IPs or localhosts
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            try:
                ip_addr = socket.gethostbyname(hostname)
                if ip_addr.startswith("127.") or ip_addr.startswith("10.") or ip_addr.startswith("192.168.") or ip_addr.startswith("172.") or ip_addr == "169.254.169.254" or ip_addr == "0.0.0.0":
                    return {"ok": False, "message": "Scrape failed: Internal or reserved IPs are not allowed."}
            except Exception:
                pass # If DNS resolution fails, requests will catch it anyway

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text, stripping out script and style tags
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=' ', strip=True)

            # Truncate text if it's excessively long to avoid blowing up context windows
            max_length = 15000
            if len(text) > max_length:
                text = text[:max_length] + "... (truncated)"

            return {"ok": True, "text": text}
        except Exception as e:
            return {"ok": False, "message": f"Scrape failed: {str(e)}"}
