import json
import logging
from pathlib import Path
from datetime import datetime, timezone

def get_logger(name="aavail", log_dir=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    target_dir = Path(log_dir) if log_dir else None
    target_path = target_dir / f"{name}.log" if target_dir else None

    # Avoid duplicate handlers while allowing a new target in tests.
    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler):
            existing = Path(handler.baseFilename)
            if target_path is None or existing != target_path.resolve():
                logger.removeHandler(handler)
                handler.close()

    if target_path is not None:
        target_dir.mkdir(parents=True, exist_ok=True)
        if not any(
            isinstance(h, logging.FileHandler) and Path(h.baseFilename) == target_path.resolve()
            for h in logger.handlers
        ):
            handler = logging.FileHandler(target_path, encoding="utf-8")
            handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(handler)
    elif not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

    return logger

def log_event(logger, event, **fields):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        **fields,
    }
    logger.info(json.dumps(payload, sort_keys=True))
    return payload
