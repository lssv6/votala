import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install

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

install(console=console, show_locals=True)

logger = logging.getLogger("votala")
