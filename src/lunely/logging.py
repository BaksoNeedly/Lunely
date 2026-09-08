import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("[Lunely]")
def log_info(message: str, tag: str | None = None) -> None:
    logger.info(message) if not tag else logger.info(f"[{tag}] {message}")


def log_warning(message: str) -> None:
    logger.warning(message)


def log_error(message: str) -> None:
    logger.error(message)


def log_critical(message: str) -> None:
    logger.critical(message)