import random
from typing import Dict, List
from models import Character

def generate_table_roll(tables: Dict[str, List[str]]) -> str:
    """Combines random rolls from available tables into a prompt."""
    results = []
    # Pick a few common axes if they exist
    for key in ["emotion", "action", "information"]:
        if key in tables:
            results.append(f"{key.capitalize()}: {random.choice(tables[key])}")
    
    if not results:
        # Fallback if specific keys aren't found
        key = random.choice(list(tables.keys()))
        results.append(f"{key.capitalize()}: {random.choice(tables[key])}")
        
    return " | ".join(results)

def generate_character_logic(characters: Dict[str, Character]) -> str:
    """Picks a character and 1-2 of their drives to form a constraint prompt."""
    if not characters:
        return "No characters loaded. Roll on a table instead."
    
    char_name = random.choice(list(characters.keys()))
    char = characters[char_name]
    
    if not char.drives:
        return f"{char_name} has no defined drives. How do they react naturally?"
    
    # Pick 1-2 random drives
    num_drives = min(len(char.drives), random.randint(1, 2))
    keys = random.sample(list(char.drives.keys()), num_drives)
    
    constraints = [f"{k.capitalize()}: {char.drives[k]}" for k in keys]
    prompt = f"CHARACTER LOGIC FOR: {char_name}\n" + "\n".join([f"* {c}" for c in constraints])
    return prompt

def generate_environment_twist(tables: Dict[str, List[str]]) -> str:
    """Picks a random disturbance from the environment table."""
    key = "environment_disturbance"
    if key in tables:
        return f"ENVIRONMENT TWIST: {random.choice(tables[key])}"
    return "A sudden change in the atmosphere catches everyone off guard."
