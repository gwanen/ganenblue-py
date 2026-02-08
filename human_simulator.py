"""
Human Behavior Simulation
Makes bot actions look like a real human player
"""

import random
import time
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from loguru import logger

from config.settings import SAFETY_CONFIG


class HumanBehavior:
    """
    Simulates human-like behavior to avoid detection
    """
    
    @staticmethod
    def human_delay(min_ms=100, max_ms=500, distribution='normal'):
        """
        Random delay with realistic distribution
        
        Args:
            min_ms: Minimum delay in milliseconds
            max_ms: Maximum delay in milliseconds
            distribution: 'uniform' or 'normal' (normal is more human-like)
        """
        if distribution == 'normal':
            # Normal distribution is more realistic (most delays near middle)
            mean = (min_ms + max_ms) / 2
            std_dev = (max_ms - min_ms) / 6  # 99.7% within range
            delay_ms = np.random.normal(mean, std_dev)
            delay_ms = np.clip(delay_ms, min_ms, max_ms)
        else:
            delay_ms = random.uniform(min_ms, max_ms)
        
        time.sleep(delay_ms / 1000)
    
    @staticmethod
    def human_click(driver, element, variance=10):
        """
        Click like a human (not always center of element)
        
        Args:
            driver: WebDriver instance
            element: WebElement to click
            variance: Pixel variance from center
        """
        try:
            # Get element size and check if it's visible
            if not element.is_displayed():
                logger.warning("⚠️  Trying to click invisible element")
                return False
            
            size = element.size
            
            # Calculate offset (not always center)
            # Humans tend to click slightly off-center
            max_offset_x = min(variance, size['width'] // 3)
            max_offset_y = min(variance, size['height'] // 3)
            
            offset_x = int(np.random.normal(0, max_offset_x / 2))
            offset_y = int(np.random.normal(0, max_offset_y / 2))
            
            # Clamp to element bounds
            offset_x = np.clip(offset_x, -size['width']//2 + 5, size['width']//2 - 5)
            offset_y = np.clip(offset_y, -size['height']//2 + 5, size['height']//2 - 5)
            
            # Move to element with curve
            actions = ActionChains(driver)
            actions.move_to_element_with_offset(element, offset_x, offset_y)
            
            # Small pause before clicking (humans don't instant-click)
            HumanBehavior.human_delay(50, 200)
            
            actions.click()
            actions.perform()
            
            logger.debug(f"✅ Human click at offset ({offset_x}, {offset_y})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Human click failed: {e}")
            # Fallback to regular click
            try:
                element.click()
                return True
            except:
                return False
    
    @staticmethod
    def human_scroll(driver, direction='down', amount=None, element=None):
        """
        Scroll like a human (variable speed, multiple steps)
        
        Args:
            driver: WebDriver instance
            direction: 'up' or 'down'
            amount: Pixels to scroll (random if None)
            element: Specific element to scroll (None for window)
        """
        if amount is None:
            amount = random.randint(100, 500)
        
        scroll_amount = amount if direction == 'down' else -amount
        
        # Humans don't scroll in one smooth motion
        steps = random.randint(2, 5)
        scroll_per_step = scroll_amount // steps
        
        for i in range(steps):
            if element:
                driver.execute_script(
                    f"arguments[0].scrollTop += {scroll_per_step};", 
                    element
                )
            else:
                driver.execute_script(f"window.scrollBy(0, {scroll_per_step});")
            
            # Variable delay between scroll steps
            HumanBehavior.human_delay(50, 150)
        
        logger.debug(f"✅ Scrolled {direction} {amount}px in {steps} steps")
    
    @staticmethod
    def random_mouse_movement(driver, small_movement=True):
        """
        Occasionally move mouse randomly (humans don't leave cursor perfectly still)
        
        Args:
            driver: WebDriver instance
            small_movement: If True, small movements; if False, larger
        """
        if random.random() < 0.3:  # 30% chance to move
            actions = ActionChains(driver)
            
            if small_movement:
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-30, 30)
            else:
                x_offset = random.randint(-200, 200)
                y_offset = random.randint(-100, 100)
            
            try:
                actions.move_by_offset(x_offset, y_offset)
                actions.perform()
                logger.debug(f"✅ Random mouse movement: ({x_offset}, {y_offset})")
            except:
                pass  # Movement might fail, that's okay
    
    @staticmethod
    def reading_pause(min_sec=0.5, max_sec=2.0):
        """
        Simulate reading/thinking time before action
        """
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        logger.debug(f"✅ Reading pause: {delay:.2f}s")
    
    @staticmethod
    def typo_simulation(text):
        """
        Simulate occasional typos when typing (then correct them)
        Returns: Modified text with typo chance
        """
        if random.random() < 0.05:  # 5% typo chance
            # Add random character, then backspace
            typo_char = random.choice('abcdefghijklmnopqrstuvwxyz')
            return text + typo_char + '\b'
        return text
    
    @staticmethod
    def occasional_mistake():
        """
        Returns True if bot should make a "mistake" (misclick, then correct)
        """
        return random.random() < 0.03  # 3% chance


class TimingVariation:
    """
    Adds realistic timing variations and fatigue simulation
    """
    
    def __init__(self):
        self.start_time = time.time()
        self.action_count = 0
        self.last_break_time = time.time()
        self.action_history = []
    
    def get_delay(self, action_type='normal'):
        """
        Get delay with variation based on action type and fatigue
        
        Args:
            action_type: 'click', 'battle', 'reading', 'summon', etc.
        
        Returns:
            float: Delay in seconds
        """
        # Base delays for different action types
        delay_ranges = {
            'click': (SAFETY_CONFIG['MIN_CLICK_DELAY'], SAFETY_CONFIG['MAX_CLICK_DELAY']),
            'battle': (0.3, 0.8),
            'reading': (1.0, 3.0),
            'summon': (0.5, 1.5),
            'results': (0.8, 2.0),
            'navigation': (0.4, 1.0),
        }
        
        min_delay, max_delay = delay_ranges.get(action_type, (0.3, 0.8))
        
        # Get fatigue factor
        fatigue = self._calculate_fatigue()
        
        # Apply variance
        variance = SAFETY_CONFIG['RANDOM_VARIANCE']
        base_delay = random.uniform(min_delay, max_delay)
        delay_with_fatigue = base_delay * fatigue
        
        # Add random variance
        final_delay = delay_with_fatigue * random.uniform(1 - variance, 1 + variance)
        
        # Record action
        self.action_count += 1
        self.action_history.append({
            'time': time.time(),
            'type': action_type,
            'delay': final_delay
        })
        
        # Keep history limited (last 100 actions)
        if len(self.action_history) > 100:
            self.action_history.pop(0)
        
        logger.debug(f"⏱️  {action_type} delay: {final_delay:.2f}s (fatigue: {fatigue:.2f}x)")
        
        return final_delay
    
    def _calculate_fatigue(self):
        """
        Calculate fatigue factor (humans slow down over time)
        
        Returns:
            float: Multiplier (1.0 = normal, 1.2 = 20% slower)
        """
        if not SAFETY_CONFIG['ENABLE_FATIGUE']:
            return 1.0
        
        # Calculate session duration in hours
        session_duration = time.time() - self.start_time
        hours = session_duration / 3600
        
        # Add 5% slowdown per hour (up to 25% after 5 hours)
        fatigue = min(1.25, 1.0 + (hours * 0.05))
        
        # Add action count factor (slow down after many actions)
        if self.action_count > 500:
            action_fatigue = 1.0 + ((self.action_count - 500) / 10000)
            fatigue *= min(1.1, action_fatigue)
        
        return fatigue
    
    def should_take_break(self):
        """
        Determine if it's time for a break
        
        Returns:
            tuple: (should_break: bool, break_duration: float)
        """
        current_time = time.time()
        time_since_break = current_time - self.last_break_time
        
        # Mandatory break every BREAK_FREQUENCY seconds
        if time_since_break >= SAFETY_CONFIG['BREAK_FREQUENCY']:
            duration = self._get_break_duration('scheduled')
            logger.info(f"⏸️  Scheduled break time ({time_since_break/60:.1f} min since last break)")
            return True, duration
        
        # Random micro-breaks (bathroom, drink water, etc.)
        if random.random() < 0.001:  # 0.1% per action
            duration = self._get_break_duration('micro')
            logger.info(f"⏸️  Taking random micro-break")
            return True, duration
        
        # Session duration limit
        session_duration = current_time - self.start_time
        if session_duration >= SAFETY_CONFIG['MAX_SESSION_DURATION']:
            duration = self._get_break_duration('long')
            logger.warning(f"⏸️  Maximum session duration reached ({session_duration/3600:.1f} hours)")
            return True, duration
        
        return False, 0
    
    def _get_break_duration(self, break_type):
        """
        Get break duration based on type
        
        Returns:
            float: Duration in seconds
        """
        durations = {
            'micro': random.uniform(30, 120),       # 30s - 2min
            'short': random.uniform(300, 600),      # 5-10min
            'scheduled': random.uniform(600, 1200), # 10-20min
            'long': random.uniform(1800, 3600),     # 30-60min
        }
        
        return durations.get(break_type, 600)
    
    def record_break(self):
        """
        Record that a break was taken
        """
        self.last_break_time = time.time()
        logger.info("✅ Break recorded")
    
    def get_session_stats(self):
        """
        Get current session statistics
        
        Returns:
            dict: Session stats
        """
        session_duration = time.time() - self.start_time
        time_since_break = time.time() - self.last_break_time
        
        return {
            'session_duration_hours': session_duration / 3600,
            'total_actions': self.action_count,
            'time_since_break_minutes': time_since_break / 60,
            'current_fatigue': self._calculate_fatigue(),
            'actions_per_hour': self.action_count / (session_duration / 3600) if session_duration > 0 else 0
        }
