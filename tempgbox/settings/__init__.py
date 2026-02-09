import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

debug_value = os.getenv("DEBUG", "true").strip().lower()
is_debug = debug_value in {"1", "true", "yes", "on"}

if is_debug:
    from .dev import *  # noqa: F401,F403
else:
    from .production import *  # noqa: F401,F403