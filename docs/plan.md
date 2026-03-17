# Structured Uncertainty: A DIY "Text Adventure" Writing System

Based on the philosophy outlined in [`idea0.md`](#original-idea), the core goal is to build a "structured source of uncertainty" that forces the writer to react, bypassing writer's block without needing an AI to generate the actual prose. 

Here is a brainstormed feature set for this CLI-based "text adventure" writing system:

### 1. The Core Loop: The "Prompt-Edit-Log" Engine
The heart of the system is a strict turn-based state machine that alternatingly hands control between the system's random generation and the user's prose creation.
*   **The Oracle Prompt:** The CLI rolls on predefined tables and presents a generic situation (e.g., `Emotion: Suspicious | Action: Avoids question`).
*   **The Decision Interface:** The user is presented with a fast CLI menu: `[Accept (Enter)] [Reroll (R)] [Custom Override (C)]`. 
*   **Seamless Editor Handoff:** Once accepted, the CLI generates a temporary text file pre-filled with the generic prompt (e.g., *"Character B reacts suspiciously and avoids the question by..."*) and opens it in the user's preferred text editor. The CLI pauses and waits.
*   **The Stitcher:** When the user saves and closes the editor, the CLI automatically reads the written prose, appends it to the master story file, and moves to the next phase (e.g., generating a consequence).

### 2. Deep Editor Customization
To ensure the system feels native to the user's workflow, the text entry method must be highly configurable.
*   **`$EDITOR` Agnostic:** Supports terminal-based editors (`vim`, `nano`, `emacs`) for a distraction-free, hacker-style workflow, or GUI editors (`code --wait`, `notepad`, `obsidian`) for a richer writing environment.
*   **Template Injection:** Users can define how the temporary files are formatted. For example, injecting Markdown headers, character names, or previous context into the top of the temporary file so the user doesn't lose their place while writing.

### 3. Dynamic, Pluggable "Oracle Tables"
The system knows nothing about the story; it only knows grammar and contextually linked vocabulary.
*   **YAML/JSON Table Definitions:** Users can create custom files defining their own themes. A sci-fi project might use different action verbs than a fantasy romance. 
*   **Multi-Axis Rolling:** Instead of just one table, the CLI can roll across several to create complex constraints. (e.g., Rolling on *Emotion*, *Action*, and *Information Revealed* simultaneously).
*   **Contextual Weighting:** (Optional advanced feature) If a previous roll resulted in "Hostile," the next table roll could slightly favor "Escalation" or "Defensive" nouns to maintain a natural flow.

### 4. The "Character Brain" Tracker
Implementing the psychological constraints mentioned in the document.
*   **Character Profiles:** Users can define basic metadata for characters via the CLI: `Wants`, `Fears`, `Misunderstandings`.
*   **Constraint Injection:** Instead of a random roll, the CLI will occasionally insert a character's internal logic as the prompt: *"Character B must react to this. How does their response highlight their fear of [X]?"*

### 5. Time-Pressure Mode ("Improv Engine")
To replicate the fast-paced, non-stop momentum of roleplaying with an AI or another person.
*   **Configurable Timers:** The user can set a turn limit (e.g., 2 minutes). 
*   **CLI Countdown:** While the editor is open, a visible timer could run in the background CLI window. If the timer expires, the CLI could trigger a bell/alert, forcing the user to wrap up the sentence and save, preventing over-planning.

### 6. "Consequence & Twist" Injection
To prevent the story from becoming just a predictable back-and-forth conversation.
*   **The Environment Die:** Every few turns, the CLI rolls on a "Disturbance" table to force an external event. (e.g., *"Just as Character A finishes speaking, a random disturbance occurs: [Weather Changes / Someone Enters / Object Breaks]. Describe it:"*).

### 7. Session & Output Management
*   **Chronological Transcript:** The system maintains a continuous markdown file of the session, stitching together the user's written entries seamlessly.
*   **Undo/Rewind:** A simple command (`/undo`) to scrap the last turn, delete the generated text, and re-roll the prompt if the user realizes they wrote themselves into a corner.
*   **Script vs. Prose Export Modes:** The ability to export the final log either as a raw back-and-forth transcript (like a chat log) or stripped of the CLI prompts so it reads like a standard prose document.
 
## File Formats & I/O Mechanics

You are absolutely right to nail down the file formats and I/O structures before touching any code. A system like this lives or dies by how frictionless its data handling is.

YAML for configuration and tables, and Markdown for the output/session logs, is the perfect stack. It’s human-readable, easily parsed, and natively supported by almost all text editors.

Here is a proposed architectural standard for the file formats and I/O mechanics:

### 1. Output Format: The Session Log (`session.md`)
The goal here is twofold: it needs to be readable as a story right now, but also structurally predictable so the CLI can parse it (for features like `/undo` or "Export as Pure Prose").

**Distinguishing System vs. User:**
We should use **Markdown Blockquotes (`>`)** for all system-generated prompts, metadata, and timestamps. This visually separates the "game engine" from the "story," and makes it trivial to strip out the system text later if you want a clean manuscript.

**Example Structure:**
```markdown
---
session_start: 2026-03-16T10:00:00Z
theme: sci-fi-mystery
---

> **[10:05 AM] Roll:** Emotion: Suspicious | Action: Avoids question
> *Prompt: Mira reacts suspiciously and avoids the question...*

Mira narrowed her eyes, stepping back from the console. "I don't know what you're talking about," she lied, her hands slipping into her pockets to hide the trembling.

> **[10:07 AM] Turn:** Environment Disturbance
> *Prompt: A sudden external event interrupts the scene...*

The ship groaned as the hyperdrive spun down abruptly, plunging the corridor into emergency red lighting.
```
*   **Frontmatter:** Stores session metadata.
*   **System blocks:** Always start with `>`. Includes a timestamp, the mechanical roll, and the narrative prompt.
*   **User prose:** Standard, unformatted text.

### 2. The Input Mechanism: The Temporary Editor File (`.turn.md`)
**Special Consideration for Input:** When the CLI hands off control to your editor (`vim`, `VS Code`, etc.), you need to see the prompt, maybe the last few lines of the story for context, and have a clear place to write. 

However, we don't want the prompt saved twice in the main log. We need a **delimiter**.

**Example Temporary File (`.turn.md`):**
```markdown
> LAST TURN:
> Alex: "You lied to me about the artifact."
> 
> CURRENT PROMPT: Emotion: Suspicious
> Mira reacts suspiciously to Alex's accusation.
> 
> --- WRITE BELOW THIS LINE (Do not delete this line) ---

[Your cursor starts here...]
```
**How it works:** When you save and close the editor, the CLI reads this temporary file, splits the text at `--- WRITE BELOW THIS LINE ---`, discards the top half, and appends only your new writing to `session.md`.

### 3. Data Tables Format (`tables.yaml`)
To make the "Oracle" a glorified, customizable rice doll, the tables need to be as flat and simple as possible so you can write your own easily.

```yaml
# tables.yaml
tables:
  emotion:
    - dismissive
    - sarcastic
    - suspicious
    - supportive
    - hostile
    - evasive
  action:
    - speaks aggressively
    - avoids the question
    - changes the subject
    - reveals a minor clue
    - tries to leave the scene
  environment_disturbance:
    - weather changes abruptly
    - a loud noise interrupts
    - a new character enters
```
*   **Consideration:** By keeping it simple, the CLI just does a random `choice()` from a specific list. Users can create `fantasy-tables.yaml` or `cyberpunk-tables.yaml` and load them at will.

### 4. System Configuration & "Character Brains" (`config.yaml`)
This handles the CLI state, editor preferences, and the constraints mentioned in the document.

```yaml
# config.yaml
settings:
  editor_command: "code --wait"  # or "vim", "nano"
  turn_timer_seconds: 120        # Set to 0 to disable the improv timer
  active_tables: "tables.yaml"

characters:
  Mira:
    wants: "Keep the artifact a secret"
    fear: "Alex discovering the truth"
    misunderstanding: "Believes Alex already knows everything"
  Alex:
    wants: "Find out what happened to the artifact"
    fear: "Being betrayed again"
    misunderstanding: "Believes Mira is working for the enemy"
```
**Special Input Consideration for Characters:** If the CLI decides to trigger a "Character Brain" turn instead of a random roll, it parses this config. The temporary editor file (`.turn.md`) would then look like this:

```markdown
> CHARACTER LOGIC FOR: Mira
> Wants: Keep the artifact a secret
> Fear: Alex discovering the truth
> 
> PROMPT: How does Mira respond, driven by her fear?
> --- WRITE BELOW THIS LINE ---
```

### Summary of the I/O Flow:
1. CLI reads `config.yaml` and `tables.yaml`.
2. CLI prompts you in the terminal: `[R]oll / [C]haracter Logic / [E]nvironment`
3. CLI generates `.turn.md` with context, prompts, and a delimiter.
4. CLI opens `.turn.md` in `$EDITOR` and waits.
5. You write below the delimiter, save, and close.
6. CLI parses `.turn.md`, formats it with blockquote timestamps, and appends it to `session.md`.
7. Loop repeats.

Does this data structure align with how you envision interacting with the system?

## Refining the Architecture with Your Rules

These are excellent architectural refinements. Moving towards immutable, timestamped session files and modularizing the characters makes the system much more robust and safer for long-term writing projects.

Here is the updated architectural standard incorporating your rules:

### 1. File & Folder Structure
Instead of a flat directory, the system should expect (or create) a structured workspace:

```text
workspace/
├── config.yaml          # Core settings (editor, timers, paths)
├── tables.yaml          # The random generation tables
├── characters/          # Independent character files
│   ├── team_a_characters.yaml
│   └── team_b_characters.yaml
├── rosters/             # Master files combining various characters/tables
│   └── artifact_arc.yaml
└── sessions/            # Immutable session logs
    ├── session_20260315_1430.md
    └── session_20260316_1000.md
```

### 2. Character Data & Loading Routine
Character files like `characters/team_a_characters.yaml` remain extremely simple:
```yaml
characters:
 Mira:
  - wants: Keep the artifact a secret
  - fear: Alex discovering the truth
  - misunderstanding: Believes Alex already knows

 Alden:
  - wants: Prove his worth to the team
  - fear: Being left behind
  - misunderstanding: Thinks Mira is hiding something from him
```

**Startup Routine:**
When the CLI boots, it runs a pre-flight sequence:
1. **Character Intake:** The CLI prompts: `How would you like to load characters?`
   * `[1] Load all from /characters folder`
   * `[2] Load from a Master Roster YAML` (reads a file that points to specific characters and tables)
   * `[3] Select manually` (opens a quick CLI checklist)
   * `[4] Skip` (run purely on generic random tables)
2. **Session Initialization:**
   * The system looks at the `sessions/` directory.
   * If older sessions exist, it asks: `Continue from previous session? [Y/n]`.
   * If `Y`, it grabs the last ~3 turns (or ~50 lines) from the most recent file.
   * It **always** creates a fresh file: `sessions/session_YYYYMMDD_HHMMSS.md`.
   * It injects the grabbed context at the top of the new file as a blockquote (e.g., `> --- Previously ---`).

### 3. The Turn Menu ("Choose for Me")
The core loop menu is expanded to fulfill the "hybrid system" philosophy perfectly:
* `[R]oll Table` (Standard Emotion/Action/Information)
* `[C]haracter Logic` (Forces a response based on Wants/Fears)
* `[E]nvironment` (External disturbance)
* `[?] Random / Choose for me` (The CLI rolls a weighted die behind the scenes to pick one of the three options above, taking the decision-making burden completely off the user).

### Updated Architecture Flowchart

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
    subgraph CoreLoop [The "Prompt-Edit-Log" Loop]
        direction TB
        MainMenu{"Turn Type Menu:\n[R]oll Tables\n[C]haracter Logic\n[E]nvironment\n[?] Choose For Me"}:::process
        GenTemp["Generate Prompts\n& Add Delimiter"]:::process
        TempFile[/"Temporary File\n(.turn.md)"/]:::file
        Editor["User writes prose\nin $EDITOR"]:::user
        Parse["CLI Parses File\n(Extracts text)"]:::process
        
        MainMenu -->|System decides if [?]| GenTemp
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

Are we aligned on these mechanics? If so, we are in a great position to start discussing the CLI implementation stack (e.g., Python vs Node, CLI rendering libraries, etc.).

## Dynamic Character Models & Flexible Constraints

You make an excellent point. You are completely right to catch that. 

While `@idea0.md` specifically lists *wants, fears, and misunderstandings*, it presents them as an example of a technique ("You ask three questions..."). Hardcoding the `Character` struct to *only* those three fields would betray the flexibility of the system. 

What if a user is writing a mystery and wants their character constraints to be `secret`, `motive`, and `alibi`? Or a military sci-fi where the drives are `duty`, `current_orders`, and `loyalty`?

Using "sane defaults" but allowing free-form definition is the perfect solution.

### The Updated Dynamic Character Model

Instead of hardcoded attributes, we treat the character's internal logic as a flexible dictionary of **Drives**.

#### 1. The YAML Structure
The user can define whatever keys they want. The system doesn't care what the keys are called; it just uses them to inject constraints.

```yaml
characters:
  Mira:
    # Sane defaults (from the original idea)
    wants: Keep the artifact a secret
    fear: Alex discovering the truth
    misunderstanding: Believes Alex already knows
    # Custom user-defined drives
    secret_agenda: Wants to steal the ship
    immediate_goal: Distract the guards

  Guard_NPC:
    orders: Do not let anyone through
    boredom_level: Extremely high
```

#### 2. The Updated Internal Structure
The internal model simply absorbs whatever key-value pairs the user provides.

```typescript
struct Character {
    name: String
    drives: Map<String, String>  // Flexible dictionary of constraint keys to values
}
```

#### 3. How this changes the "Character Logic" Turn
When the CLI rolls a "Character Logic" turn, instead of statically printing the same three questions every time, it can dynamically pick from the character's defined drives. 

For example, the engine could randomly select 2 drives from the character's dictionary to form the prompt:

> **CHARACTER LOGIC FOR: Mira**
> *   **Fear**: Alex discovering the truth
> *   **Immediate Goal**: Distract the guards
> 
> **PROMPT**: How does Mira respond, constrained by these two factors?

This creates an incredibly powerful "hybrid system" (as mentioned in the document). It keeps the internal logic consistent but introduces **combinatorial uncertainty** by forcing the writer to combine different internal drives on each turn.

### Moving Forward

With the file formats, execution loops, and dynamic internal structures defined, we have a complete, robust design document for this "Text-Based Adventure Engine for Writers."

The next logical step is deciding **what language/tech stack to build this in**. 

Given that it's a CLI tool that needs to spawn external editor processes (`$EDITOR`), parse YAML/Markdown, and handle interactive menus, the most common choices are:

1.  **Python** (using `rich` for beautiful terminal UI and `InquirerPy` for menus). *Pros: Easiest to prototype, native YAML/OS handling.*
2.  **Node.js / TypeScript** (using `inquirer` and `chalk`). *Pros: Great if you prefer JS/TS ecosystem.*
3.  **Go or Rust** (using `bubbletea` or `ratatui`). *Pros: Compiles to a single, lightning-fast binary. No need for the user to install Python/Node to run it.*

Do you have a preference for the tech stack, or should we start drafting the initialization code in one of these?