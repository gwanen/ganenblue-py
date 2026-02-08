"""
Battle Screen Element Locators
Replaces: fa_button.png, attack_button.png, salute.png, etc.

HOW TO FIND LOCATORS:
1. Open GBF in Chrome
2. Press F12 (DevTools)
3. Press Ctrl+Shift+C (Element Picker)
4. Click on the button/element you want
5. In DevTools, right-click the highlighted HTML > Copy > Copy selector
6. Paste it below, replacing the PLACEHOLDER

EXAMPLE:
If you see: <div class="btn-auto lis-auto" style="display: block;"></div>
Your locator: (By.CSS_SELECTOR, "div.btn-auto[style*='display: block']")

TIPS:
- Use classes that are unique (btn-auto, not just btn)
- Avoid dynamic IDs (prt-12345 changes)
- Use [style*='display'] to check visibility
- Test locators in DevTools Console: document.querySelector("your.selector")
"""

from selenium.webdriver.common.by import By

class BattleLocators:
    """
    Battle screen element locators
    These replace image files from AHK version
    """
    
    # ============================================
    # MAIN BATTLE BUTTONS
    # ============================================
    
    # Replaces: fa_button.png
    # Location: Bottom left area during battle
    # What it looks like: Blue "Full Auto" or "フルオート" button
    FULL_AUTO_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Full Auto button (e.g., div.btn-auto)"
    )
    
    # Replaces: attack_button.png
    # Location: Bottom center during battle
    # What it looks like: Large orange/red "Attack" button
    ATTACK_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Attack button (e.g., div.btn-attack-start)"
    )
    
    # Replaces: cancel_button.png
    # Location: Next to Attack button
    # What it looks like: Gray "Back" or "Cancel" button
    CANCEL_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Cancel/Back button (e.g., div.btn-cancel)"
    )
    
    # ============================================
    # CHARACTER DEFEAT DIALOG
    # ============================================
    
    # Replaces: salute.png (character defeated popup)
    # Location: Center of screen when character dies
    # What it looks like: Dialog box with character portrait and options
    SALUTE_DIALOG = (
        By.XPATH, 
        "PLACEHOLDER - Find: Character defeated dialog (e.g., //div[contains(@class, 'pop-usual')])"
    )
    
    # Elixir/Revive button inside defeat dialog
    ELIXIR_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Full Elixir button in defeat dialog (e.g., div.btn-use-full-elixir)"
    )
    
    # Withdraw button (if you don't want to revive)
    WITHDRAW_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Withdraw/Give up button (e.g., div.btn-usual-cancel)"
    )
    
    # ============================================
    # DISCONNECTION / REJOIN
    # ============================================
    
    # Replaces: rejoin_button.png
    # Location: Appears when connection lost
    # What it looks like: "Rejoin Battle" or "再参戦" button
    REJOIN_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Rejoin battle button (e.g., div.btn-usual-ok.rejoin)"
    )
    
    # ============================================
    # BATTLE STATE INDICATORS
    # ============================================
    
    # Turn counter (e.g., "Turn 3")
    TURN_COUNTER = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Turn number display (e.g., div.txt-turn-count)"
    )
    
    # HP bar (to check if battle is still active)
    ENEMY_HP_BAR = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Enemy HP bar (e.g., div.prt-gauge-hp)"
    )
    
    # Your party HP
    PARTY_HP_BAR = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Your party HP (e.g., div.prt-party-gauge)"
    )
    
    # Battle menu button (to verify we're in battle)
    BATTLE_MENU = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Battle menu button (e.g., div.btn-menu)"
    )

    # ============================================
    # OPTIONAL: ADVANCED FEATURES
    # ============================================
    
    # Character skill buttons (if implementing skill usage)
    CHAR_SKILL_1 = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: Character 1 skill button"
    )
    
    # Summon button
    SUMMON_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: Summon button during battle"
    )


# ============================================
# LOCATOR STATUS TRACKING
# ============================================
# Mark which locators you've filled in:
LOCATOR_STATUS = {
    'FULL_AUTO_BUTTON': 'PENDING',      # Change to 'VERIFIED' when tested
    'ATTACK_BUTTON': 'PENDING',
    'CANCEL_BUTTON': 'PENDING',
    'SALUTE_DIALOG': 'PENDING',
    'ELIXIR_BUTTON': 'PENDING',
    'REJOIN_BUTTON': 'PENDING',
    'TURN_COUNTER': 'PENDING',
    'ENEMY_HP_BAR': 'PENDING',
}
