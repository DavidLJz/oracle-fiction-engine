from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Character:
    name: str
    drives: Dict[str, str] = field(default_factory=dict)

@dataclass
class TurnRecord:
    timestamp: datetime
    turn_type: str
    system_prompt: str
    user_prose: str

@dataclass
class AppState:
    config: Dict[str, any]
    tables: Dict[str, List[str]]
    characters: Dict[str, Character]
    session_file_path: Optional[str] = None
    history: List[TurnRecord] = field(default_factory=list)
