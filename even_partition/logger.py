import logging


class PartitionLogger:
    def __init__(self, name="even_partition"):
        self._logger = logging.getLogger(name)

    def debug(self, message, *args):
        self._logger.debug(message, *args)

    def info(self, message, *args):
        self._logger.info(message, *args)

    def warning(self, message, *args):
        self._logger.warning(message, *args)
