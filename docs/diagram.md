Here is the revised flow diagram showing the new startup routine and the immutable session handling.

```mermaid
flowchart TD
    %% Styling
    classDef file fill:#2b2d31,stroke:#8aadf4,stroke-width:2px,color:#fff;
    classDef process fill:#2b2d31,stroke:#a6da95,stroke-width:2px,color:#fff;
    classDef user fill:#2b2d31,stroke:#ed8796,stroke-width:2px,color:#fff;

    %% --- STARTUP PHASE ---
    subgraph Startup [Startup Routine]
        direction TB
        Boot{CLI Starts}:::process
        CharSelect[Load Characters:\n1. Entire Folder\n2. Roster YAML\n3. Manual / Skip]:::user
        CharFiles[/"characters/*.yaml"/]:::file
        OldSession[("Previous Session\n(session_OLD.md)")]:::file
        InitSession["Create New Session File\n(Fetch context if continuing)"]:::process
        NewSession[("New Session Log\n(session_NEW.md)")]:::file
        
        Boot --> CharSelect
        CharFiles -.-> CharSelect
        CharSelect --> InitSession
        OldSession -.->|Extracts last 3 turns| InitSession
        InitSession -->|Creates| NewSession
    end

    %% --- CORE LOOP PHASE ---
    subgraph CoreLoop ["Prompt-Edit-Log" Loop]
        direction TB
        MainMenu{"Turn Type Menu:\n[R]oll Tables\n[C]haracter Logic\n[E]nvironment\n Choose For Me"}:::process
        GenTemp["Generate Prompts\n& Add Delimiter"]:::process
        TempFile[/"Temporary File\n(.turn.md)"/]:::file
        Editor["User writes prose\nin $EDITOR"]:::user
        Parse["CLI Parses File\n(Extracts text)"]:::process
        
        MainMenu -->|System decides if | GenTemp
        GenTemp -->|Creates/Overwrites| TempFile
        TempFile -->|Opens in| Editor
        Editor -->|Saves & Closes| Parse
    end

    %% Connections between phases
    Startup --> MainMenu
    Parse -->|Appends blockquote + prose| NewSession
    Parse -->|Loop repeats| MainMenu
```

By decoupling characters into their own files and isolating sessions by timestamp, the system acts much more like a true project manager or "game engine" while keeping the data format incredibly simple to edit by hand. 