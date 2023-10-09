import logging

from rich.console import Console
from rich.logging import RichHandler
import rich.traceback

FORMAT = "%(message)s"
console = Console(width=200, color_system="standard", force_terminal=False)

logging.basicConfig(
    level=logging.NOTSET,
    datefmt="%X",
    format=FORMAT,
    handlers=[
        RichHandler(
            rich_tracebacks=True,
            markup=True,
            tracebacks_width=80,
            locals_max_length=80,
            locals_max_string=120,
            level="INFO",
            console=console,
            tracebacks_show_locals=True,
        )
    ],
)

rich.traceback.install(console=console, show_locals=False)



logger = logging.getLogger()

