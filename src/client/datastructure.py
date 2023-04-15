from dataclasses import dataclass
@dataclass
class NotebookItem:
    id: int
    name: str
    pages: list[dict()]

@dataclass
class PageItem:
    id: int
    name: str