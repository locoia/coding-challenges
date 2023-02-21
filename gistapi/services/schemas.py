from dataclasses import dataclass


@dataclass
class Gist:
    id: str
    data: dict
    content: str = None
