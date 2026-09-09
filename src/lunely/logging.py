import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(server_name: str):
    return logging.getLogger(f"[Lunely][{server_name}]")


logger = get_logger("Lunely")


def log_info(message: str, tag: str | None = None, server_name: str = "Lunely") -> None:
    target_logger = get_logger(server_name)
    if tag:
        target_logger.info(f"[{tag}] {message}")
    else:
        target_logger.info(message)


def log_warning(message: str, tag: str | None = None, server_name: str = "Lunely") -> None:
    target_logger = get_logger(server_name)
    if tag:
        target_logger.warning(f"[{tag}] {message}")
    else:
        target_logger.warning(message)


def log_error(message: str, tag: str | None = None, server_name: str = "Lunely") -> None:
    target_logger = get_logger(server_name)
    if tag:
        target_logger.error(f"[{tag}] {message}")
    else:
        target_logger.error(message)


def log_critical(message: str, tag: str | None = None, server_name: str = "Lunely") -> None:
    target_logger = get_logger(server_name)
    if tag:
        target_logger.critical(f"[{tag}] {message}")
    else:
        target_logger.critical(message)