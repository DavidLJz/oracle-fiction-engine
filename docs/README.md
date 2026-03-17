Here is a complete user-facing guide (formatted as a `README.md` or User Manual) that explains the philosophy, mechanics, and creative potential of the program. 

***

# 🎲 Oracle Engine: A Text-Based Adventure for Your Own Stories

Welcome to **Oracle Engine**, a terminal-based writing tool designed to break writer's block by turning your writing sessions into a responsive, semi-automated text adventure.

If you've ever enjoyed roleplaying with others (or with AI) because it keeps the momentum going, this tool is for you. Oracle Engine doesn't write the story for you; instead, it acts as a **structured source of uncertainty**. It throws constraints, random events, and character logic at you, forcing you to *react* rather than plan.

You provide the imagination. The Engine provides the spark.

---

## ⚙️ How It Works: The Core Loop

The Engine runs entirely in your terminal, acting as a Game Master for your story. Writing with the Engine follows a seamless, infinite loop:

1. **The Prompt:** The Engine's beautiful terminal interface asks what kind of turn you want to take (a random character reaction, an environmental twist, or a dive into a character's internal logic). 
2. **The Handoff:** The Engine generates a unique prompt and automatically opens it in your favorite text editor (VS Code, Vim, Notepad, Obsidian, etc.).
3. **The Reaction:** You read the prompt, write your prose directly below it, and hit save.
4. **The Stitch:** You close the editor. The Engine instantly grabs what you wrote, formats it perfectly, and appends it to an ongoing Markdown manuscript.
5. **Repeat:** The Engine asks for your next move.

---

## 🛠️ What You Need

Oracle Engine is lightweight and designed to fit into your existing workflow.

* **Python 3.8+**: The Engine is built using Python, featuring a rich, colorful terminal user interface (TUI).
* **A Text Editor:** You can configure the Engine to use literally any editor. Want a hacker-style, distraction-free environment? Use `vim` or `nano`. Prefer a GUI? Use `code --wait` (VS Code) or `notepad`.
* **A Workspace:** The Engine runs inside a local folder containing your specific story's configuration files.

---

## 📂 Managing Your Workspace

When you initialize a new story project, the Engine creates a simple, plain-text workspace. You have complete control over these files—they are designed to be easily tweaked by hand.

```text
my_story_workspace/
├── config.yaml          # Your editor choice and active settings
├── tables.yaml          # The vocabulary the Engine uses to surprise you
├── characters/          # Small files defining character brains
└── sessions/            # Where your generated story logs are safely saved
```

### 1. `tables.yaml` (The Oracle)
This file is a list of words or phrases the Engine will randomly combine. You can edit this file to perfectly match your genre. Writing a romance? Add "blushes" and "looks away." Writing sci-fi? Add "checks the scanner" and "diverts power."

### 2. `characters/` (The Character Brains)
You can create a `.yaml` file for any character. Here, you define their **Drives**. You aren't limited to specific rules—write whatever makes the character tick:

```yaml
# characters/mira.yaml
wants: Keep the ancient artifact a secret.
fear: Alex discovering the truth.
immediate_goal: Distract the guards.
secret_agenda: She is secretly working for the Emperor.
```
When a turn focuses on Mira, the Engine will randomly pull 1 or 2 of these drives and challenge you to write a response that satisfies them.

### 3. `sessions/` (Your Manuscript)
Every time you sit down to write, the Engine creates a brand new, timestamped Markdown file (e.g., `session_2026-03-16.md`). It never accidentally overwrites your past work. If you are continuing a story, it neatly pulls the last few paragraphs of your previous session so you can pick up exactly where you left off.

---

## 🎮 Playing the Game (Turn Types)

When you run the Engine, the terminal will present you with a menu of choices for the current "Turn". 

* 🎲 **[R]oll Tables:** The Engine rolls the dice on your `tables.yaml` file. It might prompt you with: *Emotion: Suspicious | Action: Changes the subject.* You must now write the prose that makes this happen.
* 🧠 **[C]haracter Logic:** The Engine picks a character from your folder, grabs their internal drives, and forces you to write their next action based *only* on those constraints.
* 🌩️ **[E]nvironment:** The world interrupts. The Engine rolls an external disturbance (e.g., *The weather changes abruptly* or *The ship's alarms sound*).
* ❓ **[?] Choose For Me:** Can't decide? Let the Engine randomly pick the turn type for you. This creates the ultimate "Text Adventure" feel, where you are completely at the mercy of the system's pacing.

---

## 🌌 Creative Uses: Hacking the Engine

Because the Engine relies entirely on plain-text files and completely ignores *what* you are writing about, it is incredibly flexible. You can bend the system to do much more than standard storytelling:

**1. GM-less Tabletop Roleplaying (Solo RPGs)**
Replace the `tables.yaml` entries with classic RPG oracle tables (like those found in *Ironsworn* or *Mythic*). Let the Engine act as your automated Game Master. Write your character's actions in the editor, and let the Engine roll the consequences.

**2. Worldbuilding & Lore Generation**
Change your character files into "Factions" or "Nations" with drives like `economic_need`, `military_strength`, and `cultural_taboo`. Change your tables to generate geopolitical events. The Engine becomes an interactive world-history simulator.

**3. Therapeutic Journaling**
Create tables filled with introspective questions, emotional states, and reflection prompts. Use the "Choose For Me" function to guide yourself through a semi-random, guided journaling session where the Engine gently pushes you to explore different aspects of your day.

**4. The Improv Timer Challenge**
Turn on the **Timer Mode** in `config.yaml`. The Engine will give you a strict time limit (e.g., 2 minutes) for every turn. If the timer runs out while you're in your editor, your terminal will chime, forcing you to finish your thought and keep the momentum flying. Perfect for beating severe writer's block.