from dataclasses import dataclass, field
from typing import Dict, Any, Literal
from uuid import uuid4
from broverse.utils import get_timestamp

@dataclass
class Context:
    context: str
    id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    type: Literal["document"] = "document"
    # created_at: str = field(default_factory=get_timestamp)
