"""
Global Settings & Constants
Replaces: config.ahk global variables
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
PROFILES_DIR = BASE_DIR / "profiles"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, SCREENSHOTS_DIR, PROFILES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Bot Settings (replaces AHK config)
SETTINGS_FILE = CONFIG_DIR / "bot_settings.json"
MAIN_LOOP_DELAY = 0.3  # seconds
BATTLE_TIMEOUT = 30    # seconds
ATTACK_TIMEOUT = 100   # seconds
RESULT_TIMEOUT = 60    # seconds
SUMMON_SCROLL_MAX = 5

# Window Settings
GBF_WINDOW_WIDTH = 700
GBF_WINDOW_HEIGHT = 1080

# Click Variance
CLICK_VARIANCE = 5  # pixels
IMAGE_VARIANCE = 50  # Not used anymore (we use locators now!)

# URL Patterns (replaces searchBattle, searchResults, etc.)
URL_PATTERNS = {
    'battle': '#raid',
    'results': 'result',
    'scene': 'scene',
    'stage': 'stage',
    'summon': 'supporter',
    'quest': '#quest',
    'coop': '#coopraid',
    'coop_join': '#coopraid/offer',
    'coop_room': '#coopraid/room',
    'mypage': '#mypage'
}

# Anti-Detection Settings
SAFETY_CONFIG = {
    'MAX_SESSION_DURATION': int(os.getenv('MAX_SESSION_DURATION', 14400)),  # 4 hours
    'MIN_BREAK_DURATION': int(os.getenv('MIN_BREAK_DURATION', 600)),        # 10 min
    'BREAK_FREQUENCY': int(os.getenv('BREAK_FREQUENCY', 3600)),             # Every hour
    'MIN_CLICK_DELAY': float(os.getenv('MIN_CLICK_DELAY', 0.5)),            # 500ms
    'MAX_CLICK_DELAY': float(os.getenv('MAX_CLICK_DELAY', 2.0)),            # 2s
    'RANDOM_VARIANCE': 0.3,                                                  # 30% variance
    'ENABLE_FATIGUE': os.getenv('ENABLE_FATIGUE', 'true').lower() == 'true',
    'SOLVE_CAPTCHA_MANUAL': True,
}

# Locator Verification Settings
LOCATOR_VERIFICATION = {
    'VERIFY_ON_START': os.getenv('VERIFY_LOCATORS_ON_START', 'true').lower() == 'true',
    'SCREENSHOT_ON_ERROR': os.getenv('SCREENSHOT_ON_ERROR', 'true').lower() == 'true',
    'MAX_FIND_ATTEMPTS': 3,
    'RETRY_DELAY': 1.0,  # seconds
}

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
LOG_ROTATION = "500 MB"
LOG_RETENTION = "7 days"
