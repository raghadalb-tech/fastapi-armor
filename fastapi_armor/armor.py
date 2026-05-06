from fastapi import FastAPI

from .error_handler import add_exception_handlers
from .logger import setup_logger
from .sentry import init_sentry


class Armor:
    def __init__(
        self,
        app: FastAPI,
        log_file: str = "logs/app.log",
        log_max_bytes: int = 5_000_000,
        log_backup_count: int = 3,
        sentry_dsn: str = "",
        environment: str = "development",
    ):
        self.app = app
        self.logger = setup_logger(
            log_file=log_file,
            max_bytes=log_max_bytes,
            backup_count=log_backup_count,
        )
        add_exception_handlers(app=self.app, logger=self.logger)

        if sentry_dsn:
            init_sentry(dsn=sentry_dsn, environment=environment)
