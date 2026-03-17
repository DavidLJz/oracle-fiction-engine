import click
import random
import os
import logging
from datetime import datetime
import io_manager
import generator
import ui
import editor
from models import TurnRecord

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename=os.path.join("logs", "oracle_engine.log"),
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

@click.group()
def cli():
    """Oracle Engine: A semi-automated writing adventure."""
    pass

@cli.command()
@click.option('--config', '-c', default='config.yaml', help='Path to your config.yaml file.')
@click.option('--tables', '-t', default='tables.yaml', help='Path to your tables.yaml file.')
@click.option('--chars', '-ch', default='characters.yaml', help='Path to a character or roster YAML file.')
def start(config, tables, chars):
    """Starts a new writing session.
    
    You can specify custom paths for your project files using the flags.
    Example: python main.py start --config my_custom_config.yaml
    """
    setup_logging()
    
    # Inform the user about the paths being used
    ui.display_status(f"Initializing with:")
    ui.display_status(f"  - Config: {config}")
    ui.display_status(f"  - Tables: {tables}")
    ui.display_status(f"  - Roster/Chars: {chars}")
    ui.display_status("(Use --help to see how to override these paths)\n")

    try:
        # 1. Initialize
        state = io_manager.load_workspace(config, tables, chars)
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
            
            ui.display_status(f"Opening editor...")
            # We use state.config.get('editor') but fallback to 'notepad' for Windows safety
            editor_cmd = state.config.get('editor', 'notepad')
            editor.open_in_editor(temp_file, editor_cmd)
            
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
        logging.error(f"Initialization Error: {e}")
        ui.display_error(str(e))
    except Exception as e:
        logging.exception("Unhandled Exception in main loop")
        ui.display_error(f"A fatal error occurred. Check logs/oracle_engine.log for details.\nError: {e}")

if __name__ == "__main__":
    cli()
