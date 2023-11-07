"""
Contains pydantic models for data validation and parsing.

It can also be used for ORM Integration like SQLAlchemy when required.
"""

from typing import List

from pydantic import BaseModel, HttpUrl, validator


""" Model for a file within a GitHub Gist """


class GistFile(BaseModel):
    filename: str
    type: str
    language: str
    raw_url: HttpUrl
    size: int


""" Representation of a GitHub Gist """


class Gist(BaseModel):
    url: HttpUrl
    files: dict[str, GistFile]


""" Search parameters for Gist querying """


class SearchRequest(BaseModel):
    username: str
    pattern: str

    """
    Validation to prevent empty search parameters which can lead to
    unnecessary API calls
    """

    @validator("username")
    def username_must_not_be_empty(cls, value):
        if not value or value.isspace():
            raise ValueError("Username cannot be empty or just whitespace")
        return value

    @validator("pattern")
    def pattern_must_not_be_empty(cls, value):
        if not value or value.isspace():
            raise ValueError("Pattern cannot be empty or just whitespace")
        return value


"""
Search results including the occurrence of the pattern within a user's Gists
"""


class SearchResult(BaseModel):
    status: str
    username: str
    pattern: str
    matches: List[str]
