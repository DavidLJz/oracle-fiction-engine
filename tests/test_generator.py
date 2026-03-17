import pytest
from models import Character
from generator import generate_table_roll, generate_character_logic, generate_environment_twist

def test_generate_table_roll_common_axes():
    tables = {
        "emotion": ["happy", "sad"],
        "action": ["jumps", "runs"],
        "information": ["secret", "clue"]
    }
    result = generate_table_roll(tables)
    
    # Should contain all three common axes
    assert "Emotion:" in result
    assert "Action:" in result
    assert "Information:" in result
    assert " | " in result

def test_generate_table_roll_fallback():
    tables = {
        "weather": ["rain", "sun"],
        "location": ["forest", "cave"]
    }
    result = generate_table_roll(tables)
    
    # Since common axes aren't present, it should pick one random key as fallback
    assert ("Weather:" in result) or ("Location:" in result)

def test_generate_character_logic_no_chars():
    assert generate_character_logic({}) == "No characters loaded. Roll on a table instead."

def test_generate_character_logic_no_drives():
    chars = {"Bob": Character(name="Bob", drives={})}
    result = generate_character_logic(chars)
    assert "Bob has no defined drives" in result

def test_generate_character_logic_with_drives():
    chars = {
        "Alice": Character(name="Alice", drives={"want": "gold", "fear": "spiders", "goal": "escape"})
    }
    result = generate_character_logic(chars)
    
    assert "CHARACTER LOGIC FOR: Alice" in result
    assert "* Want: gold" in result or "* Fear: spiders" in result or "* Goal: escape" in result
    # It should pick 1 to 2 drives
    assert result.count("*") in [1, 2]

def test_generate_environment_twist():
    tables = {"environment_disturbance": ["earthquake"]}
    result = generate_environment_twist(tables)
    assert "ENVIRONMENT TWIST: earthquake" in result

def test_generate_environment_twist_fallback():
    result = generate_environment_twist({})
    assert "A sudden change in the atmosphere" in result
