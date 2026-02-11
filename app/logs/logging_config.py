import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

LOG_DIR = (Path(os.getenv("LOG_PATH", "log")) / "").resolve()
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "backend")


class Logger:
    """Factory for module loggers that write to a shared file with a uniform format."""

    def __init__(self, name: str, level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        if self._logger.handlers:
            self._logger.setLevel(level)
            return

        self._logger.setLevel(level)
        self._logger.propagate = False

        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{LOG_FILE_NAME}.log"

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",  datefmt='%m/%d/%Y %I:%M:%S')

        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger
