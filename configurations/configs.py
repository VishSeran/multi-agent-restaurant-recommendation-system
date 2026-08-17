from pathlib import Path
from typing import Optional

from configurations.logger import get_logger

logger = get_logger("configs")

GROQ_MODEL = "llama-3.1-8b-instant"

Base_dir = Path.cwd().resolve()

