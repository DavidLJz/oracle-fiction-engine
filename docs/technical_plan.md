# Oracle Engine: Technical Specification

## 1. Architectural Overview

The Oracle Engine is a terminal-based Python application. To maintain a "silly simple" codebase while adhering to SOLID principles, the architecture strictly separates concerns into discrete layers:

1.  **Presentation Layer (`ui.py`, `cli.py`)**: Handles all user input and terminal formatting using `rich` and `click`. It knows nothing about how prompts are generated or files are saved.
2.  **Application / Logic Layer (`engine.py`, `generator.py`)**: The "Game Master." Manages the state, rolls on tables, selects character drives, and constructs the text prompts.
3.  **Infrastructure / I/O Layer (`io_manager.py`, `editor.py`)**: Handles all side effects. Reads YAML, parses Markdown, appends to the session file, and spawns the subprocess for the user's text editor.

### Tech Stack
*   **Language**: Python 3.8+
*   **CLI Framework**: `click` (for command routing like `oracle start` or `oracle init`)
*   **TUI Framework**: `rich` (for rendering panels, colors, and menus)
*   **Data Parsing**: `PyYAML` (for reading configuration and tables)

---

## 2. Core Data Models (`models.py`)

Using Python `dataclasses`, we define the internal memory structures. These contain no logic, only data.

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Character:
    name: str
    drives: Dict[str, str]  # e.g., {"fear": "...", "wants": "..."}

@dataclass
class TurnRecord:
    timestamp: datetime
    turn_type: str          # "ROLL", "CHARACTER", "ENVIRONMENT"
    system_prompt: str
    user_prose: str

@dataclass
class AppState:
    config: Dict[str, str]
    tables: Dict[str, List[str]]
    characters: Dict[str, Character]
    session_file_path: str
    history: List[TurnRecord]
```

---

## 3. Module Breakdown & Responsibilities

### `cli.py` (Entrypoint)
Uses `click` to define the command-line interface.
*   `init()`: Scaffolds a new workspace (creates folders, default `config.yaml`, `tables.yaml`).
*   `start()`: Bootstraps the `AppState`, creates the new session file, and enters the main game loop.

### `ui.py` (Presentation)
Exclusively handles `rich` console outputs and input prompts.
*   `display_welcome(session_file: str)`: Shows the startup banner.
*   `prompt_turn_menu() -> str`: Renders the `[R]oll, [C]haracter, [E]nvironment, [?] Random` menu and returns the user's choice.
*   `display_system_prompt(prompt: str)`: Prints the generated prompt to the terminal before the editor opens.
*   `display_error(msg: str)`: Formats and prints errors gracefully.

### `generator.py` (Domain Logic)
Pure functions that take data models and return formatted prompt strings. 
*   `generate_table_roll(tables: Dict) -> str`: Randomly selects items from the loaded tables and constructs a prompt string.
*   `generate_character_logic(characters: Dict) -> str`: Randomly selects a character, picks 1-2 drives, and constructs a constraint prompt.
*   `generate_environment_twist(tables: Dict) -> str`: Selects an external disturbance prompt.

### `editor.py` (Infrastructure)
Handles the OS-level interaction with the user's text editor.
*   `open_in_editor(filepath: str, editor_cmd: str) -> None`: Uses `subprocess.run` to open the file and block execution until the user closes the editor.

### `io_manager.py` (Data Persistence)
Handles all disk operations. Isolates file system side-effects from the rest of the app.
*   `load_workspace() -> AppState`: Reads `config.yaml`, `tables.yaml`, and the `characters/` directory. Returns the populated state object.
*   `init_new_session(previous_session_path: Optional[str]) -> str`: Creates a new timestamped Markdown file. If a previous session exists, extracts the last N lines and prepends them.
*   `prepare_temp_file(prompt: str) -> str`: Creates `.turn.md`, writes the prompt and the `--- WRITE BELOW THIS LINE ---` delimiter.
*   `parse_and_cleanup_temp_file(filepath: str) -> str`: Reads `.turn.md`, extracts everything below the delimiter, deletes the temp file, and returns the raw user prose.
*   `append_to_session(session_path: str, record: TurnRecord)`: Formats the record (adding `>` blockquotes to the system prompt) and appends it to the master session Markdown file.

---

## 4. The Execution Flow (The Main Loop)

Once `cli.py:start()` is called, the loop looks like this:

1.  **Initialize**: `io_manager` loads files into `AppState`. It creates a new timestamped `session.md`.
2.  **Menu**: `ui` prompts the user for the turn type.
3.  **Generate**: Based on the choice, `generator` builds a `system_prompt` string.
4.  **Prep File**: `io_manager` writes the `system_prompt` and delimiter to `.turn.md`.
5.  **Edit**: `editor` opens `.turn.md` via subprocess and halts the loop.
6.  **Parse**: User saves and closes. `io_manager` reads the new prose and deletes `.turn.md`.
7.  **Record**: A `TurnRecord` is created and appended to `AppState.history`.
8.  **Save**: `io_manager.append_to_session()` writes the formatted turn to the permanent Markdown log.
9.  **Repeat**: Return to Step 2.

## 5. SOLID Principles Applied
*   **Single Responsibility**: Formatting terminal output (`ui.py`) is entirely separate from formatting text files (`io_manager.py`).
*   **Open/Closed**: New turn types (e.g., "Combat Turn") can be added by creating a new function in `generator.py` and adding an option in `ui.py`, without touching the core file-saving or editor logic.
*   **Dependency Inversion**: High-level modules (`cli.py`) rely on abstractions (the pure functions in `generator.py` and `io_manager.py`) rather than hardcoded global states. State is passed down explicitly via the `AppState` object.