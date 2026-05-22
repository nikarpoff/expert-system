from pathlib import Path

from loguru import logger


def configure_logger() -> None:
    logs_dir = Path('logs')
    logs_dir.mkdir(exist_ok=True)
    logger.remove()
    logger.add(logs_dir / 'expert_system.log', rotation='1 MB', retention=10, enqueue=True)
    logger.add(lambda m: print(m, end=''))
