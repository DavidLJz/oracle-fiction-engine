import pytest
import os
import yaml
from io_manager import load_characters, prepare_temp_file, parse_and_cleanup_temp_file, DELIMITER

def test_load_characters_single_file(tmp_path):
    char_file = tmp_path / "chars.yaml"
    data = {
        "characters": {
            "Hero": {"want": "peace"},
            "Villain": {"want": "chaos"}
        }
    }
    char_file.write_text(yaml.dump(data))
    
    chars = load_characters(str(char_file))
    assert len(chars) == 2
    assert "Hero" in chars
    assert "Villain" in chars
    assert chars["Hero"].drives["want"] == "peace"

def test_load_characters_with_includes(tmp_path):
    roster_file = tmp_path / "roster.yaml"
    inc_file = tmp_path / "included.yaml"
    
    inc_data = {
        "characters": {
            "Sidekick": {"fear": "darkness"}
        }
    }
    inc_file.write_text(yaml.dump(inc_data))
    
    roster_data = {
        "include": ["included.yaml"],
        "characters": {
            "Main": {"want": "glory"}
        }
    }
    roster_file.write_text(yaml.dump(roster_data))
    
    chars = load_characters(str(roster_file))
    
    assert len(chars) == 2
    assert "Main" in chars
    assert "Sidekick" in chars

def test_load_characters_circular_dependency(tmp_path):
    file_a = tmp_path / "a.yaml"
    file_b = tmp_path / "b.yaml"
    
    file_a.write_text(yaml.dump({"include": ["b.yaml"], "characters": {"A": {}}}))
    file_b.write_text(yaml.dump({"include": ["a.yaml"], "characters": {"B": {}}}))
    
    # Should not infinite loop
    chars = load_characters(str(file_a))
    assert len(chars) == 2
    assert "A" in chars
    assert "B" in chars

def test_temp_file_lifecycle(tmp_path):
    prompt = "This is a prompt\nLine 2"
    
    # 1. Prepare
    temp_path_str = prepare_temp_file(prompt, root_dir=str(tmp_path))
    assert os.path.exists(temp_path_str)
    
    with open(temp_path_str, 'r') as f:
        content = f.read()
    
    assert "This is a prompt" in content
    assert DELIMITER in content
    
    # Simulate user writing
    with open(temp_path_str, 'a') as f:
        f.write("And here is the user's beautiful prose.")
        
    # 2. Parse and Cleanup
    prose = parse_and_cleanup_temp_file(temp_path_str)
    
    assert prose == "And here is the user's beautiful prose."
    assert not os.path.exists(temp_path_str)
