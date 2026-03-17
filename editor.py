import subprocess
import os

def open_in_editor(file_path: str, editor_command: str) -> None:
    """
    Opens the specified file in the user's preferred editor.
    Expects editor_command to be something like 'vim', 'nano', or 'code --wait'.
    """
    try:
        # Split command for subprocess (handles 'code --wait' etc)
        cmd = editor_command.split()
        cmd.append(file_path)
        
        # We use shell=True on Windows often for better command resolution
        # but here we'll try a direct call first.
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f"Error opening editor: {e}")
        # Fallback to a very basic input if editor fails
        input("Press Enter once you have manually edited the file...")
