import questionary
import typer

BANNER_TEXT = r"""
███████╗ ██████╗ ██████╗  ██████╗ ███████╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝╚██╗██╔╝
█████╗  ██║   ██║██████╔╝██║  ███╗█████╗   ╚███╔╝ 
██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝   ██╔██╗ 
██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗██╔╝ ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""


def main(name: str = typer.Option(...), age: int = typer.Option(...)):
    print(name)
    print(age)


if __name__ == "__main__":
    import questionary

name = questionary.text("Name:").ask()

age = questionary.text("Age:").ask()

language = questionary.select(
    "Favorite language:", choices=["Python", "Java", "Go", "Rust"]
).ask()

skills = questionary.checkbox(
    "Select your skills:", choices=["Git", "Docker", "Linux", "AWS"]
).ask()

confirm = questionary.confirm("Submit?").ask()

if confirm:
    print("\nUser Information")
    print("----------------")
    print("Name:", name)
    print("Age:", age)
    print("Language:", language)
    print("Skills:", skills)
else:
    print("Cancelled")
