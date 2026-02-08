"""
Logging Configuration
Replaces: Log() function from AHK
"""

from loguru import logger
import sys
from pathlib import Path
from datetime import datetime

from config.settings import LOGS_DIR, LOG_LEVEL, LOG_FORMAT, LOG_ROTATION, LOG_RETENTION


def setup_logger():
    """
    Configure loguru logger for bot
    """
    # Remove default logger
    logger.remove()
    
    # Console output (colored, formatted)
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=True
    )
    
    # File output (all logs)
    log_file = LOGS_DIR / f"bot_{datetime.now().strftime('%Y-%m-%d')}.log"
    logger.add(
        log_file,
        format=LOG_FORMAT,
        level="DEBUG",
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip"
    )
    
    # Error-only log file
    error_log = LOGS_DIR / "errors.log"
    logger.add(
        error_log,
        format=LOG_FORMAT,
        level="ERROR",
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION
    )
    
    logger.info("✅ Logger initialized")
    logger.info(f"📁 Log directory: {LOGS_DIR}")
    
    return logger


# Initialize on import
setup_logger()
