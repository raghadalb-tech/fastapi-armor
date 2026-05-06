import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    log_file: str = "logs/app.log",
    max_bytes: int = 5_000_000,
    backup_count: int = 3,
) -> logging.Logger:
    logger = logging.getLogger("fastapi_armor")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = RotatingFileHandler(
        filename=log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
