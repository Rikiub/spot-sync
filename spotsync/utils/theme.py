from rich.theme import Theme
from rich.console import Console

theme = Theme({
	"error": "bold red",
	"warning": "red",

    "high": "bold yellow",
	"low": "bold italic cyan",
    "choices": "bold magenta",
    "success": "bold italic green",

    "enumerate": "magenta",
    "item": "blue",
    "object": "green",

    "spotdl_log": "green"
})
console = Console(theme=theme)

print = console.print
input = console.input