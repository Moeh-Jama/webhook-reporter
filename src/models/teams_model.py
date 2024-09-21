
from dataclasses import dataclass, field, fields
from typing import Any, Dict, List, Optional

@dataclass
class Item:
    type: str = field(init=False)

    def __post_init__(self):
        self.type = self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        def convert_value(value: Any) -> Any:
            if isinstance(value, Item):
                return value.to_dict()
            elif isinstance(value, list):
                return [convert_value(item) for item in value if item is not None]
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items() if v is not None}
            else:
                return value

        return {
            field.name: convert_value(getattr(self, field.name))
            for field in fields(self)
                if getattr(self, field.name) is not None
        }

@dataclass
class TextBlock(Item):
    text: str
    wrap: bool
    size: Optional[str] = None
    weight: Optional[str] = None
    spacing: Optional[str] = None
    horizontalAlignment: Optional[str] = None

@dataclass
class Image(Item):
    url: str
    size: str
    altText: str

@dataclass
class Column(Item):
    width: Optional[str] = None
    items: Optional[List[Item]] = field(default_factory=list)

@dataclass
class ColumnSet(Item):
    columns: List[Column]

@dataclass
class Container(Item):
    items: Optional[List[Item]] = field(default_factory=list)