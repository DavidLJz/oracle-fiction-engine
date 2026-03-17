import click
import random
from datetime import datetime
import io_manager
import generator
import ui
import editor
from models import TurnRecord

@click.group()
def cli():
    """Oracle Engine: A semi-automated writing adventure."""
    pass

@cli.command()
def start():
    """Starts a new writing session in the current directory."""
    try:
        # 1. Initialize
        state = io_manager.load_workspace()
        state.session_file_path = io_manager.init_new_session()
        
        ui.display_welcome(state.session_file_path)
        
        # 2. Main Loop
        while True:
            turn_type = ui.prompt_turn_menu()
            
            if turn_type == 'q':
                ui.display_status("Farewell, Author.")
                break
            
            # Handle Random Choice
            actual_type = turn_type
            if turn_type == '?':
                actual_type = random.choice(['r', 'c', 'e'])
                ui.display_status(f"The Oracle chooses: {actual_type.upper()}")

            # 3. Generate Prompt
            prompt = ""
            label = ""
            if actual_type == 'r':
                prompt = generator.generate_table_roll(state.tables)
                label = "TABLE ROLL"
            elif actual_type == 'c':
                prompt = generator.generate_character_logic(state.characters)
                label = "CHARACTER LOGIC"
            elif actual_type == 'e':
                prompt = generator.generate_environment_twist(state.tables)
                label = "ENVIRONMENT TWIST"

            # 4. Preparation & Editing
            ui.display_system_prompt(prompt)
            temp_file = io_manager.prepare_temp_file(prompt)
            
            ui.display_status(f"Opening {state.config.get('editor', 'editor')}...")
            editor.open_in_editor(temp_file, state.config.get('editor', 'notepad'))
            
            # 5. Parse & Save
            prose = io_manager.parse_and_cleanup_temp_file(temp_file)
            
            if not prose:
                ui.display_error("No text detected. Turn skipped.")
                continue
                
            record = TurnRecord(
                timestamp=datetime.now(),
                turn_type=label,
                system_prompt=prompt,
                user_prose=prose
            )
            
            io_manager.append_to_session(state.session_file_path, record)
            state.history.append(record)
            ui.display_status("Turn recorded successfully.")

    except FileNotFoundError as e:
        ui.display_error(f"Workspace not initialized correctly. Missing: {e.filename}")
    except Exception as e:
        ui.display_error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    cli()
