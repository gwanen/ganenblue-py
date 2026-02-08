"""
Locator Verification & Detection System
This module helps you verify that your locators work and tells you when elements are not found.

Features:
- Checks if PLACEHOLDER locators have been filled
- Tests locators against live page
- Takes screenshots when elements not found
- Provides detailed error messages
- Suggests alternative selectors
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger
from datetime import datetime
from pathlib import Path
import json

from config.settings import SCREENSHOTS_DIR, LOCATOR_VERIFICATION
from locators.battle_locators import BattleLocators, LOCATOR_STATUS as battle_status
from locators.summon_locators import SummonLocators, LOCATOR_STATUS as summon_status
from locators.other_locators import ALL_LOCATOR_STATUS


class LocatorVerifier:
    """
    Verifies locators and provides detailed feedback
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.verification_results = {}
        self.placeholder_count = 0
        self.verified_count = 0
        self.failed_count = 0
    
    def check_for_placeholders(self, locator_class):
        """
        Check if locators still have PLACEHOLDER text
        Returns: List of locator names that need to be filled
        """
        placeholder_locators = []
        
        for attr_name in dir(locator_class):
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(locator_class, attr_name)
            
            if isinstance(attr, tuple) and len(attr) == 2:
                by, selector = attr
                if 'PLACEHOLDER' in selector:
                    placeholder_locators.append(attr_name)
                    self.placeholder_count += 1
        
        return placeholder_locators
    
    def verify_all_locators(self):
        """
        Check all locators across all classes
        Returns: Detailed report
        """
        logger.info("🔍 Starting Locator Verification...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'placeholder_locators': [],
            'verification_results': {},
            'summary': {}
        }
        
        # Check Battle Locators
        logger.info("Checking Battle Locators...")
        battle_placeholders = self.check_for_placeholders(BattleLocators)
        if battle_placeholders:
            report['placeholder_locators'].extend([f"BattleLocators.{name}" for name in battle_placeholders])
        
        # Check Summon Locators
        logger.info("Checking Summon Locators...")
        summon_placeholders = self.check_for_placeholders(SummonLocators)
        if summon_placeholders:
            report['placeholder_locators'].extend([f"SummonLocators.{name}" for name in summon_placeholders])
        
        # Generate report
        if report['placeholder_locators']:
            logger.warning(f"⚠️  Found {len(report['placeholder_locators'])} PLACEHOLDER locators that need to be filled:")
            for locator in report['placeholder_locators']:
                logger.warning(f"   - {locator}")
            logger.info("\n📝 To fill these:")
            logger.info("   1. Open GBF in Chrome")
            logger.info("   2. Press F12 (DevTools)")
            logger.info("   3. Press Ctrl+Shift+C (Element Picker)")
            logger.info("   4. Click the button/element")
            logger.info("   5. Right-click highlighted HTML > Copy > Copy selector")
            logger.info("   6. Paste into the locator file")
        else:
            logger.success("✅ All locators have been filled (no PLACEHOLDERS found)")
        
        report['summary'] = {
            'total_placeholders': self.placeholder_count,
            'verified': self.verified_count,
            'failed': self.failed_count
        }
        
        return report
    
    def test_locator(self, locator_name, locator_tuple, timeout=5, required=True):
        """
        Test a single locator and provide detailed feedback
        
        Args:
            locator_name: Name of the locator (for logging)
            locator_tuple: (By.XXX, "selector")
            timeout: How long to wait for element
            required: If True, log as error; if False, log as warning
        
        Returns:
            dict with test results
        """
        by, selector = locator_tuple
        
        result = {
            'name': locator_name,
            'selector': selector,
            'by': by,
            'found': False,
            'error': None,
            'screenshot': None,
            'suggestions': []
        }
        
        # Check for PLACEHOLDER
        if 'PLACEHOLDER' in selector:
            result['error'] = "⚠️  PLACEHOLDER not filled - please add real CSS selector"
            logger.warning(f"❌ {locator_name}: {result['error']}")
            return result
        
        try:
            # Try to find element
            logger.info(f"🔍 Testing {locator_name}...")
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator_tuple))
            
            # Check if visible
            is_visible = element.is_displayed()
            
            if is_visible:
                result['found'] = True
                logger.success(f"✅ {locator_name}: FOUND and VISIBLE")
                self.verified_count += 1
            else:
                result['found'] = False
                result['error'] = "Element found but NOT VISIBLE (check display/visibility CSS)"
                logger.warning(f"⚠️  {locator_name}: {result['error']}")
                self.failed_count += 1
            
        except TimeoutException:
            result['error'] = f"Element NOT FOUND within {timeout} seconds"
            self.failed_count += 1
            
            # Take screenshot
            if LOCATOR_VERIFICATION['SCREENSHOT_ON_ERROR']:
                screenshot_path = self._take_debug_screenshot(locator_name)
                result['screenshot'] = str(screenshot_path)
            
            # Try to suggest alternatives
            result['suggestions'] = self._suggest_alternatives(selector)
            
            # Log detailed error
            log_func = logger.error if required else logger.warning
            log_func(f"❌ {locator_name}: {result['error']}")
            log_func(f"   Selector: {by} = '{selector}'")
            log_func(f"   Current URL: {self.driver.current_url}")
            
            if result['screenshot']:
                log_func(f"   Screenshot: {result['screenshot']}")
            
            if result['suggestions']:
                log_func(f"   💡 Try these alternatives:")
                for suggestion in result['suggestions']:
                    log_func(f"      - {suggestion}")
        
        except NoSuchElementException:
            result['error'] = "Element does NOT EXIST on page"
            self.failed_count += 1
            
            logger.error(f"❌ {locator_name}: {result['error']}")
            logger.error(f"   The selector '{selector}' doesn't match anything on the page")
            logger.error(f"   Current URL: {self.driver.current_url}")
            
            # Suggest checking DevTools
            logger.info(f"   💡 Debug steps:")
            logger.info(f"      1. Open DevTools (F12)")
            logger.info(f"      2. Console tab")
            logger.info(f"      3. Run: document.querySelector('{selector}')")
            logger.info(f"      4. If returns null, selector is wrong")
        
        except Exception as e:
            result['error'] = f"Unexpected error: {str(e)}"
            logger.error(f"❌ {locator_name}: {result['error']}")
        
        return result
    
    def _take_debug_screenshot(self, locator_name):
        """
        Take screenshot for debugging
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"locator_error_{locator_name}_{timestamp}.png"
        filepath = SCREENSHOTS_DIR / filename
        
        try:
            self.driver.save_screenshot(str(filepath))
            logger.info(f"📸 Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")
            return None
    
    def _suggest_alternatives(self, selector):
        """
        Suggest alternative selectors
        """
        suggestions = []
        
        # If it's a class selector
        if '.' in selector and not selector.startswith('//'):
            class_name = selector.split('.')[1].split('[')[0]
            suggestions.append(f"Try without style attribute: .{class_name}")
            suggestions.append(f"Try with partial class: [class*='{class_name}']")
        
        # If it's looking for display: block
        if "[style*='display: block']" in selector:
            base_selector = selector.split('[')[0]
            suggestions.append(f"Try without style check: {base_selector}")
            suggestions.append(f"Try with :not([style*='none']): {base_selector}:not([style*='none'])")
        
        # General suggestions
        suggestions.append("Check if element is in an iframe")
        suggestions.append("Check if element loads after page navigation")
        suggestions.append("Try using XPath instead of CSS")
        
        return suggestions
    
    def generate_report(self, output_file=None):
        """
        Generate a detailed verification report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_locators': self.placeholder_count + self.verified_count + self.failed_count,
                'placeholders': self.placeholder_count,
                'verified': self.verified_count,
                'failed': self.failed_count,
            },
            'results': self.verification_results
        }
        
        if output_file:
            output_path = Path(output_file)
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"📄 Report saved to: {output_path}")
        
        # Console summary
        logger.info("\n" + "="*60)
        logger.info("📊 LOCATOR VERIFICATION SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Locators: {report['summary']['total_locators']}")
        logger.info(f"✅ Verified:    {report['summary']['verified']}")
        logger.info(f"❌ Failed:      {report['summary']['failed']}")
        logger.info(f"⚠️  Placeholders: {report['summary']['placeholders']}")
        logger.info("="*60)
        
        if report['summary']['failed'] > 0:
            logger.warning("\n⚠️  Some locators failed verification!")
            logger.warning("Check the logs above for details and screenshots.")
        
        if report['summary']['placeholders'] > 0:
            logger.warning("\n⚠️  Some locators still have PLACEHOLDER text!")
            logger.warning("Fill them in before running the bot.")
        
        if report['summary']['verified'] == report['summary']['total_locators']:
            logger.success("\n🎉 All locators verified successfully!")
        
        return report


class SmartElementFinder:
    """
    Enhanced element finding with automatic retries and detailed logging
    """
    
    def __init__(self, driver, logger_instance=None):
        self.driver = driver
        self.logger = logger_instance or logger
    
    def find_element(self, locator_tuple, timeout=10, required=True, element_name="Element"):
        """
        Find element with detailed error reporting
        
        Args:
            locator_tuple: (By.XXX, "selector")
            timeout: How long to wait
            required: If True, raise exception; if False, return None
            element_name: Human-readable name for logging
        
        Returns:
            WebElement or None
        """
        by, selector = locator_tuple
        
        # Check for PLACEHOLDER
        if 'PLACEHOLDER' in selector:
            error_msg = f"❌ Cannot find {element_name}: Locator has PLACEHOLDER text! Please update the locator in locators/ directory."
            self.logger.error(error_msg)
            if required:
                raise ValueError(error_msg)
            return None
        
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator_tuple))
            
            if not element.is_displayed():
                self.logger.warning(f"⚠️  {element_name} found but NOT VISIBLE")
                if required:
                    wait.until(EC.visibility_of_element_located(locator_tuple))
            
            self.logger.debug(f"✅ Found: {element_name}")
            return element
            
        except TimeoutException:
            error_msg = f"❌ {element_name} NOT FOUND within {timeout}s\n"
            error_msg += f"   Locator: {by} = '{selector}'\n"
            error_msg += f"   Current URL: {self.driver.current_url}\n"
            error_msg += f"\n   💡 Debug steps:\n"
            error_msg += f"      1. Open GBF and navigate to this screen\n"
            error_msg += f"      2. Open DevTools (F12) > Console\n"
            error_msg += f"      3. Run: document.querySelector('{selector}')\n"
            error_msg += f"      4. If null, the selector is wrong - update it in locators/\n"
            
            self.logger.error(error_msg)
            
            if required:
                raise NoSuchElementException(error_msg)
            return None
        
        except Exception as e:
            self.logger.error(f"❌ Unexpected error finding {element_name}: {e}")
            if required:
                raise
            return None
    
    def is_element_visible(self, locator_tuple, timeout=2, element_name="Element"):
        """
        Check if element is visible (non-blocking)
        
        Returns: bool
        """
        try:
            element = self.find_element(locator_tuple, timeout=timeout, required=False, element_name=element_name)
            if element:
                return element.is_displayed()
            return False
        except:
            return False
