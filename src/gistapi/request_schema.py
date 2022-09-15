import typing

from pydantic import BaseModel, Field


class Base(BaseModel):
    ...


class Payload(Base):
    username: str
    pattern: str


class Args(Base):
    per_page: int = 10
    page: int = 1


class RequestSchema(Base):
    payload: Payload
    args: Args


class Paging(Base):
    total: int
    per_page: int = 10
    page: int = 1


class ResponseSchema(Base):
    status: str
    username: str
    pattern: str
    matches: typing.List[str] = Field(default=list)
    pagination: Paging
