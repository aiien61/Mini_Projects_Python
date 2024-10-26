from dataclasses import dataclass

@dataclass
class Post:
    id: int
    title: str
    subtitle: str
    body: str