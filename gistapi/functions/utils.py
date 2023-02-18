# Created by elvinmirzazada at 15:09 18/02/2023 using PyCharm
"""
Helper functions
"""
import re
import requests


def iterate_over_gist(url: str) -> str:
    """
    Generator for creating iterator over each requested gist

    Args:
    url (string): the url to gists

    Returns:
        yield each line as str
    """
    with requests.get(url, stream=True, timeout=15) as response:
        response.raise_for_status()
        for chunk in response.iter_lines(chunk_size=9600):
            yield chunk.decode('utf-8')


def search_pattern(url: str, pattern: str) -> bool:
    """
    Iterate over the gist and search the given pattern

    Args:
    url (string): the url to gists
    pattern (string): searching pattern

    Returns:
    bool: if pattern exists in content
    """
    for content in iterate_over_gist(url):
        if re.search(pattern, content):
            return True
    return False
