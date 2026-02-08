"""
Summon Selection Screen Locators
Replaces: summon.png, select_party_auto_select.png, ok_button.png

HOW TO FIND THESE:
1. Navigate to summon selection screen in GBF
2. Open DevTools (F12)
3. Use Element Picker (Ctrl+Shift+C)
4. Click on each button/element
5. Copy the selector and paste below
"""

from selenium.webdriver.common.by import By

class SummonLocators:
    """
    Summon selection screen locators
    """
    
    # ============================================
    # AUTO-SELECT BUTTON
    # ============================================
    
    # Replaces: select_party_auto_select.png
    # Location: Bottom left of summon selection screen
    # What it looks like: "Auto Select" or "おまかせ選択" button
    AUTO_SELECT_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Auto-select summon button (e.g., div.btn-auto-select)"
    )
    
    # ============================================
    # CONFIRMATION BUTTON
    # ============================================
    
    # Replaces: ok_button.png (for summon/party confirmation)
    # Location: Bottom right when summon is selected
    # What it looks like: Blue "OK" or "決定" button
    OK_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: OK/Confirm button (e.g., div.btn-usual-ok)"
    )
    
    # ============================================
    # SUMMON LIST
    # ============================================
    
    # Container for the list of summons
    SUMMON_LIST_CONTAINER = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Summon list container (e.g., div.prt-supporter-list)"
    )
    
    # Individual summon items in the list
    SUMMON_ITEM = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Individual summon item (e.g., div.lis-supporter)"
    )
    
    # Scrollable area
    SCROLL_CONTAINER = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Scrollable summon area (e.g., div.prt-supporter-scroll)"
    )
    
    # ============================================
    # PARTY CONFIRMATION
    # ============================================
    
    # Party selection screen (before summon)
    PARTY_OK_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Party confirmation OK button (e.g., div.btn-usual-ok.se-ok)"
    )
    
    # Party list
    PARTY_LIST = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: Party list container"
    )


# Status tracking
LOCATOR_STATUS = {
    'AUTO_SELECT_BUTTON': 'PENDING',
    'OK_BUTTON': 'PENDING',
    'SUMMON_LIST_CONTAINER': 'PENDING',
    'SCROLL_CONTAINER': 'PENDING',
}
