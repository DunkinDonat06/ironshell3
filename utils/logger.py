import logging
import os

def setup_logger(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, "ironshell.log")
    logger = logging.getLogger("ironshell")
    logger.setLevel(logging.INFO)
    # Очищаем старые хендлеры для предотвращения дублирования логов при повторных вызовах
    logger.handlers = []
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger