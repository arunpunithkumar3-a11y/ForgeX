from questionary import Style
from rich.theme import Theme

# Rich Console Theme (supporting hex colors)
FORGEX_THEME = Theme(
    {
        "banner": "bold #875fdf",
        "brand": "bold #875fdf",
        "accent": "bold #00d7ff",
        "success": "#00ff87",
        "success_bold": "bold #00ff87",
        "error": "#ff5f87",
        "error_bold": "bold #ff5f87",
        "warning": "#ffaf5f",
        "warning_bold": "bold #ffaf5f",
        "info": "#5f87ff",
        "info_bold": "bold #5f87ff",
        "muted": "#8a8a8a",
        "muted_bold": "bold #8a8a8a",
    }
)

# Questionary Style
QUESTIONARY_STYLE = Style(
    [
        ("qmark", "fg:#875fdf bold"),  # question mark symbol
        ("question", "bold fg:#ffffff"),  # question text
        ("answer", "fg:#00ff87 bold"),  # answer text (once selected)
        ("pointer", "fg:#00d7ff bold"),  # pointer arrow in list select
        ("highlighted", "fg:#00d7ff bold"),  # choice text currently hovered/focused
        ("selected", "fg:#00ff87 bold"),  # selected checkbox choice
        ("separator", "fg:#8a8a8a"),  # separator lines
        ("instruction", "fg:#8a8a8a italic"),  # keyboard instructions
        ("text", "fg:#ffffff"),  # input text for fields
        ("disabled", "fg:#5f5f5f italic"),  # disabled items
    ]
)
