"""
Stealth WebDriver with Anti-Detection
Makes Selenium undetectable to bot detection systems
"""

import undetected_chromedriver as uc
import random
import time
from pathlib import Path
from loguru import logger

from config.settings import PROFILES_DIR, GBF_WINDOW_WIDTH, GBF_WINDOW_HEIGHT


class StealthDriver:
    """
    Creates an undetectable WebDriver
    """
    
    @staticmethod
    def create(headless=False, profile_name="gbf_bot", window_position=None):
        """
        Create stealth WebDriver with all anti-detection measures
        
        Args:
            headless: Run without GUI (more detectable, not recommended)
            profile_name: Chrome profile name
            window_position: (x, y) tuple for window position
        
        Returns:
            WebDriver instance
        """
        logger.info("🚀 Creating Stealth WebDriver...")
        
        options = uc.ChromeOptions()
        
        # ============================================
        # Profile & Data Directory
        # ============================================
        profile_path = PROFILES_DIR / profile_name
        profile_path.mkdir(parents=True, exist_ok=True)
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument('--profile-directory=Default')
        
        # ============================================
        # User-Agent Randomization
        # ============================================
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # ============================================
        # Anti-Detection Flags
        # ============================================
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # ============================================
        # Window Settings
        # ============================================
        if not headless:
            if window_position:
                options.add_argument(f'--window-position={window_position[0]},{window_position[1]}')
            options.add_argument(f'--window-size={GBF_WINDOW_WIDTH},{GBF_WINDOW_HEIGHT}')
        else:
            # New headless mode (less detectable than old headless)
            options.add_argument('--headless=new')
            options.add_argument(f'--window-size={GBF_WINDOW_WIDTH},{GBF_WINDOW_HEIGHT}')
            logger.warning("⚠️  Headless mode enabled - may be more detectable!")
        
        # ============================================
        # Performance & Stability
        # ============================================
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # Disable images for faster loading (optional)
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        
        # ============================================
        # Create Driver
        # ============================================
        try:
            logger.info("Starting Chrome with undetected-chromedriver...")
            driver = uc.Chrome(
                options=options,
                version_main=None,  # Auto-detect Chrome version
                driver_executable_path=None,  # Auto-download driver
            )
            
            logger.success("✅ Chrome started successfully")
            
            # ============================================
            # Apply JavaScript Patches
            # ============================================
            StealthDriver._apply_stealth_patches(driver)
            
            # ============================================
            # Randomize Fingerprint
            # ============================================
            StealthDriver._randomize_fingerprint(driver)
            
            logger.success("✅ Stealth patches applied")
            
            return driver
            
        except Exception as e:
            logger.error(f"❌ Failed to create driver: {e}")
            raise
    
    @staticmethod
    def _apply_stealth_patches(driver):
        """
        Apply JavaScript patches to hide WebDriver detection
        """
        # Remove navigator.webdriver flag
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            '''
        })
        
        # Spoof Chrome object
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                window.navigator.chrome = {
                    runtime: {},
                    loadTimes: function() {},
                    csi: function() {},
                    app: {}
                };
            '''
        })
        
        # Spoof permissions
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            '''
        })
        
        # Spoof plugins (make it look like real browser)
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {
                            name: 'Chrome PDF Plugin',
                            filename: 'internal-pdf-viewer',
                            description: 'Portable Document Format'
                        },
                        {
                            name: 'Chrome PDF Viewer',
                            filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                            description: ''
                        },
                        {
                            name: 'Native Client',
                            filename: 'internal-nacl-plugin',
                            description: ''
                        }
                    ],
                });
            '''
        })
        
        # Spoof languages
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en', 'ja'],
                });
            '''
        })
        
        # Overwrite the `call` function to prevent detection
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Function.prototype.call = function() {
                    const args = Array.from(arguments);
                    if (args[0] === null && args[1] && args[1].includes && args[1].includes('webdriver')) {
                        return undefined;
                    }
                    return this.apply(...arguments);
                };
            '''
        })
    
    @staticmethod
    def _randomize_fingerprint(driver):
        """
        Randomize browser fingerprint
        """
        # Randomize viewport size (within realistic bounds)
        common_resolutions = [
            (1920, 1080),
            (1366, 768),
            (1536, 864),
            (1440, 900),
        ]
        width, height = random.choice(common_resolutions)
        
        try:
            driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
                'width': width,
                'height': height,
                'deviceScaleFactor': random.choice([1, 1.25, 1.5]),
                'mobile': False
            })
        except:
            # Some versions don't support this
            pass
        
        # Randomize timezone (use Japan timezone for GBF)
        try:
            driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
                'timezoneId': 'Asia/Tokyo'
            })
        except:
            pass
        
        # Set locale
        try:
            driver.execute_cdp_cmd('Emulation.setLocaleOverride', {
                'locale': 'en-US'
            })
        except:
            pass
    
    @staticmethod
    def warm_up(driver, logger_instance=logger):
        """
        Visit normal sites before going to game (looks more human)
        
        Args:
            driver: WebDriver instance
            logger_instance: Logger to use
        """
        logger_instance.info("🌡️  Warming up browser (visiting normal sites)...")
        
        try:
            # Visit Google first
            driver.get('https://www.google.com')
            time.sleep(random.uniform(2, 4))
            logger_instance.info("✅ Visited Google")
            
            # Maybe do a search (50% chance)
            if random.random() < 0.5:
                try:
                    search_box = driver.find_element('name', 'q')
                    search_queries = ['granblue fantasy', 'gbf wiki', 'chrome']
                    search_box.send_keys(random.choice(search_queries))
                    search_box.submit()
                    time.sleep(random.uniform(2, 5))
                    logger_instance.info("✅ Performed search (looking human)")
                except:
                    pass
            
            logger_instance.success("✅ Warm-up complete")
            
        except Exception as e:
            logger_instance.warning(f"⚠️  Warm-up failed (not critical): {e}")
