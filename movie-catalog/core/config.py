import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS = frozenset(
    {
        "49n6HebSj2IFY38Jhy86vg",
        "m-7cYwRXP9crTPWOHLRqgQ",
        "RuvekGOLFLxvAY8lFF7FuQ",
    }
)

USERS_DB: dict[str, str] = {
    # username: password
    "alice": "password",
    "bob": "qwerty",
}
