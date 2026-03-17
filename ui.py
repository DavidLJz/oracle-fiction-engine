from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from typing import Optional

console = Console()

def display_welcome(session_file: str):
    console.print(Panel.fit(
        "[bold cyan]ORACLE ENGINE[/bold cyan]\n"
        "[italic]Your structured source of uncertainty[/italic]",
        border_style="blue"
    ))
    console.print(f"Logging to: [green]{session_file}[/green]\n")

def prompt_turn_menu() -> str:
    choices = {
        "r": "Roll Table",
        "c": "Character Logic",
        "e": "Environment Twist",
        "?": "Random Choice",
        "q": "Quit"
    }
    
    console.print("[bold]Select Turn Type:[/bold]")
    for key, val in choices.items():
        console.print(f"  [[cyan]{key}[/cyan]] {val}")
    
    return Prompt.ask("Choose", choices=list(choices.keys()), default="?")

def display_system_prompt(prompt: str):
    console.print(Panel(prompt, title="[bold yellow]System Prompt[/bold yellow]", border_style="yellow"))

def display_status(msg: str):
    console.print(f"[italic white]{msg}[/italic white]")

def display_error(msg: str):
    console.print(f"[bold red]ERROR:[/bold red] {msg}")
