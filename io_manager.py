import os
import yaml
from datetime import datetime
from typing import Dict, List, Optional
from models import AppState, Character, TurnRecord

DELIMITER = "--- WRITE BELOW THIS LINE (Do not delete this line) ---"

def load_workspace(config_path: str = "config.yaml", tables_path: str = "tables.yaml", char_dir: str = "characters") -> AppState:
    """Loads config, tables, and characters from the specified paths."""
    # Load Config
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}

    # Load Tables
    if not os.path.exists(tables_path):
        raise FileNotFoundError(f"Tables file not found at: {tables_path}")
    with open(tables_path, 'r') as f:
        loaded = yaml.safe_load(f) or {}
        tables = loaded.get('tables', {})

    # Load Characters
    if not os.path.exists(char_dir):
        raise FileNotFoundError(f"Characters directory not found at: {char_dir}")
    characters = {}
    for filename in os.listdir(char_dir):
        if filename.endswith(".yaml"):
            with open(os.path.join(char_dir, filename), 'r') as f:
                data = yaml.safe_load(f) or {}
                chars_in_file = data.get('characters', {})
                for name, drives in chars_in_file.items():
                    characters[name] = Character(name=name, drives=drives)

    return AppState(config=config, tables=tables, characters=characters)

def init_new_session(root_dir: str = ".") -> str:
    """Creates a new timestamped session file and handles context carry-over."""
    sessions_dir = os.path.join(root_dir, "sessions")
    os.makedirs(sessions_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(sessions_dir, f"session_{timestamp}.md")
    
    # Context Carry-over Logic
    previous_context = ""
    existing_sessions = sorted([f for f in os.listdir(sessions_dir) if f.endswith(".md")])
    if existing_sessions:
        last_session = os.path.join(sessions_dir, existing_sessions[-1])
        with open(last_session, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Grab last 20 lines as context
            previous_context = "".join(lines[-20:])
    
    with open(session_path, 'w', encoding='utf-8') as f:
        f.write(f"--- SESSION START: {datetime.now().isoformat()} ---\n\n")
        if previous_context:
            f.write("> ### Previously...\n")
            for line in previous_context.splitlines():
                f.write(f"> {line}\n")
            f.write("\n---\n\n")
            
    return session_path

def prepare_temp_file(prompt: str, root_dir: str = ".") -> str:
    temp_path = os.path.join(root_dir, ".turn.md")
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(f"> CURRENT PROMPT:\n")
        for line in prompt.splitlines():
            f.write(f"> {line}\n")
        f.write(f"\n{DELIMITER}\n\n")
    return temp_path

def parse_and_cleanup_temp_file(temp_path: str) -> str:
    if not os.path.exists(temp_path):
        return ""
    
    with open(temp_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prose = ""
    if DELIMITER in content:
        prose = content.split(DELIMITER)[-1].strip()
    
    os.remove(temp_path)
    return prose

def append_to_session(session_path: str, record: TurnRecord):
    with open(session_path, 'a', encoding='utf-8') as f:
        f.write(f"\n> **[{record.timestamp.strftime('%H:%M:%S')}] {record.turn_type}**\n")
        for line in record.system_prompt.splitlines():
            f.write(f"> {line}\n")
        f.write("\n")
        f.write(record.user_prose)
        f.write("\n\n---\n")
