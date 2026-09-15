import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configurar_logging(caminho: Path) -> None:
    manipulador = RotatingFileHandler(
        caminho,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    manipulador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logging.basicConfig(level=logging.INFO, handlers=[manipulador])
