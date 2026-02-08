"""
Results Screen & Other Locators
"""

from selenium.webdriver.common.by import By

class ResultsLocators:
    """
    Results screen after battle completion
    """
    
    # Main results container
    RESULTS_CONTAINER = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Results screen container (e.g., div.prt-result-window)"
    )
    
    # Next/OK button to proceed
    NEXT_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Next/Continue button on results (e.g., div.btn-usual-ok)"
    )
    
    # Item/Loot list
    ITEM_LIST = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Item drops list (e.g., div.prt-result-item-list)"
    )
    
    # EXP/RP gained
    EXP_DISPLAY = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: EXP display"
    )


class QuestLocators:
    """
    Quest/Stage selection screen
    """
    
    # Quest start button
    QUEST_START_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Quest start button (e.g., div.btn-usual-ok.se-quest-start)"
    )
    
    # AP display
    AP_DISPLAY = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: AP cost display"
    )
    
    # Quest name/title
    QUEST_TITLE = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Optional: Quest name"
    )


class StoryLocators:
    """
    Story/Scene skip elements
    Replaces: story_skip coordinates
    """
    
    # Skip button
    SKIP_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Story skip button (e.g., div.btn-skip)"
    )
    
    # Skip confirmation OK
    SKIP_OK_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Skip confirmation OK (e.g., div.btn-usual-ok)"
    )
    
    # Story container (to detect we're in story)
    STORY_CONTAINER = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Story/scene container"
    )


class DialogLocators:
    """
    Common dialog/popup elements
    """
    
    # Generic OK button in popups
    POPUP_OK = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Generic popup OK button (e.g., div.btn-usual-ok)"
    )
    
    # Generic Cancel button
    POPUP_CANCEL = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Generic popup cancel (e.g., div.btn-usual-cancel)"
    )
    
    # Close button (X)
    CLOSE_BUTTON = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Close button (e.g., div.btn-close)"
    )
    
    # Error message container
    ERROR_MESSAGE = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Error message popup"
    )
    
    # Loading indicator
    LOADING_INDICATOR = (
        By.CSS_SELECTOR, 
        "PLACEHOLDER - Find: Loading spinner/indicator"
    )


# Status tracking for all locators
ALL_LOCATOR_STATUS = {
    # Results
    'RESULTS_CONTAINER': 'PENDING',
    'RESULTS_NEXT_BUTTON': 'PENDING',
    
    # Quest
    'QUEST_START_BUTTON': 'PENDING',
    
    # Story
    'STORY_SKIP_BUTTON': 'PENDING',
    'STORY_SKIP_OK': 'PENDING',
    
    # Dialogs
    'POPUP_OK': 'PENDING',
    'CLOSE_BUTTON': 'PENDING',
}
