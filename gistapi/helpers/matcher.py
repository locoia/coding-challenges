import re
import requests


def get_all_matched_gists(pattern, gists):
    matched_file_list = []
    for gist in gists:
        for k, v in gist["files"].items():
            if gist_matches_pattern(pattern, get_file_content(v["raw_url"])):
                matched_file_list.append(gist)
    return matched_file_list


def get_file_content(file_url: str):
    return requests.get(file_url).text


def gist_matches_pattern(pattern: str, gist_text: str) -> bool:
    return re.search(pattern, gist_text)
