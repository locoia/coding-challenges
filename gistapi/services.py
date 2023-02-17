import requests
import re


def list_content(url: str) -> str:
    response = requests.get(url)
    return response.text


def search_pattern(url: str, pattern: str) -> bool:
    content = list_content(url)
    return re.search(pattern, content)
