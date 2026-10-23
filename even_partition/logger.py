import logging
from typing import Any


class PartitionLogger:
    def __init__(self, name: str = "even_partition", level: int | None = None):
        self._logger = logging.getLogger(name)
        if level is not None:
            self._logger.setLevel(level)

    def debug(self, message: str, *args: Any) -> None:
        self._logger.debug(message, *args)

    def info(self, message: str, *args: Any) -> None:
        self._logger.info(message, *args)

    def warning(self, message: str, *args: Any) -> None:
        self._logger.warning(message, *args)

    def error(self, message: str, *args: Any) -> None:
        self._logger.error(message, *args)
