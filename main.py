"""
GBF Bot - Main Entry Point
Python + Selenium Edition with Page Object Model

Usage:
    python main.py                    # Normal start
    python main.py --verify-locators  # Test locators only
    python main.py --help             # Show help
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from utils.logger import setup_logger
from antidetection.stealth import StealthDriver
from utils.locator_verification import LocatorVerifier

# Import locator classes
from locators.battle_locators import BattleLocators
from locators.summon_locators import SummonLocators
from locators.other_locators import ResultsLocators, QuestLocators, StoryLocators


def verify_locators_only():
    """
    Run locator verification without starting the bot
    Useful for testing after filling in locators
    """
    logger.info("="*60)
    logger.info("🔍 LOCATOR VERIFICATION MODE")
    logger.info("="*60)
    logger.info("")
    logger.info("This will test all your locators against a live GBF page.")
    logger.info("Make sure:")
    logger.info("  1. Chrome is installed")
    logger.info("  2. You've filled in locators (replaced PLACEHOLDER)")
    logger.info("  3. You're logged into GBF")
    logger.info("")
    
    input("Press Enter when ready to start Chrome...")
    
    # Create stealth driver
    logger.info("\n🚀 Starting Chrome...")
    driver = StealthDriver.create(headless=False)
    
    try:
        # Navigate to GBF
        logger.info("📍 Navigating to GBF...")
        driver.get('https://game.granbluefantasy.jp/')
        
        logger.info("\n⏳ Waiting for you to navigate to a battle screen...")
        logger.info("   Please:")
        logger.info("   1. Log in if needed")
        logger.info("   2. Navigate to any quest")
        logger.info("   3. Start a battle")
        logger.info("   4. Wait until you see the Attack/Full Auto buttons")
        logger.info("")
        
        input("Press Enter when you're in battle...")
        
        # Create verifier
        verifier = LocatorVerifier(driver)
        
        # Check for placeholders first
        logger.info("\n" + "="*60)
        logger.info("STEP 1: Checking for PLACEHOLDER text...")
        logger.info("="*60)
        
        report = verifier.verify_all_locators()
        
        if report['placeholder_locators']:
            logger.warning(f"\n⚠️  Found {len(report['placeholder_locators'])} locators with PLACEHOLDER text!")
            logger.warning("You need to fill these in before the bot will work.")
            logger.warning("\nSee: docs/LOCATORS.md for detailed instructions")
        else:
            logger.success("\n✅ No PLACEHOLDER text found - all locators filled!")
        
        # Ask if user wants to test locators
        if report['placeholder_locators']:
            logger.info("\n⚠️  Cannot test locators until PLACEHOLDERs are filled.")
        else:
            logger.info("\n" + "="*60)
            logger.info("STEP 2: Testing locators on live page...")
            logger.info("="*60)
            
            input("\nPress Enter to test battle locators...")
            
            # Test battle locators
            logger.info("\n🎮 Testing Battle Locators...")
            verifier.test_locator("FULL_AUTO_BUTTON", BattleLocators.FULL_AUTO_BUTTON)
            verifier.test_locator("ATTACK_BUTTON", BattleLocators.ATTACK_BUTTON)
            verifier.test_locator("CANCEL_BUTTON", BattleLocators.CANCEL_BUTTON, required=False)
            
            logger.info("\n⏸️  To test other screens, navigate to them now.")
            logger.info("   Press Ctrl+C when done testing.")
            
            # Keep browser open for manual testing
            input("\nPress Enter to close browser...")
        
    except KeyboardInterrupt:
        logger.info("\n⏸️  Verification stopped by user")
    except Exception as e:
        logger.error(f"\n❌ Error during verification: {e}")
    finally:
        driver.quit()
        logger.info("\n✅ Browser closed")


def start_bot():
    """
    Start the actual bot (GUI + automation)
    """
    logger.info("="*60)
    logger.info("🎮 GBF BOT STARTING")
    logger.info("="*60)
    
    # Check if locators are filled
    logger.info("\n🔍 Checking locators...")
    
    # Quick check for PLACEHOLDER text
    from locators.battle_locators import BattleLocators
    
    fa_locator = BattleLocators.FULL_AUTO_BUTTON[1]
    if "PLACEHOLDER" in fa_locator:
        logger.error("\n❌ LOCATORS NOT FILLED!")
        logger.error("You still have PLACEHOLDER text in your locators.")
        logger.error("\nPlease:")
        logger.error("  1. Read: docs/LOCATORS.md")
        logger.error("  2. Fill in locators in locators/ directory")
        logger.error("  3. Run: python main.py --verify-locators")
        logger.error("\nExiting...")
        sys.exit(1)
    
    logger.success("✅ Locators appear to be filled")
    
    # Import GUI and bot core (only after locator check)
    logger.info("\n📦 Loading bot modules...")
    
    try:
        # This would import your actual bot implementation
        # from core.bot import GBFBot
        # from gui.main_window import BotGUI
        
        logger.info("✅ Modules loaded")
        
        # Start GUI
        logger.info("\n🖥️  Starting GUI...")
        logger.info("⚠️  GUI implementation coming soon!")
        logger.info("\nFor now, use --verify-locators to test your setup.")
        
        # TODO: Implement actual bot
        # bot = GBFBot()
        # gui = BotGUI(bot)
        # gui.start()
        
    except ImportError as e:
        logger.error(f"❌ Failed to import modules: {e}")
        logger.error("Make sure all dependencies are installed:")
        logger.error("  pip install -r requirements.txt")
        sys.exit(1)


def main():
    """
    Main entry point with argument parsing
    """
    parser = argparse.ArgumentParser(
        description='GBF Bot - Automated quest farming with anti-detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py                    # Start bot with GUI
  python main.py --verify-locators  # Test locators only
  python main.py --help             # Show this help

Before first run:
  1. Fill in locators (see docs/LOCATORS.md)
  2. Configure quest URL in config/bot_settings.json
  3. Run verification to test locators
  4. Start the bot!

Documentation:
  README.md         - Quick start guide
  docs/LOCATORS.md  - How to find element locators
  
For help: Check logs in data/logs/
        '''
    )
    
    parser.add_argument(
        '--verify-locators',
        action='store_true',
        help='Test locators without starting bot'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode (not recommended - more detectable)'
    )
    
    args = parser.parse_args()
    
    # Display banner
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║         🎮 Granblue Fantasy Bot v3.0 🎮              ║
    ║              Python + Selenium Edition                ║
    ║                                                       ║
    ║         Page Object Model Architecture                ║
    ║         Full Anti-Detection Measures                  ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    if args.verify_locators:
        verify_locators_only()
    else:
        start_bot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n⏸️  Bot stopped by user (Ctrl+C)")
        logger.info("Goodbye! 👋")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"❌ Fatal error: {e}")
        sys.exit(1)
