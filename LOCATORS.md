# 🔍 How to Find and Fill Locators

This guide shows you **step-by-step** how to find element locators in Granblue Fantasy and fill them into the bot.

## 📋 Table of Contents

1. [What Are Locators?](#what-are-locators)
2. [Step-by-Step: Finding Locators](#step-by-step-finding-locators)
3. [Testing Your Locators](#testing-your-locators)
4. [Common Locator Patterns](#common-locator-patterns)
5. [Troubleshooting](#troubleshooting)

---

## What Are Locators?

**Locators** are CSS selectors or XPath expressions that tell Selenium which element to interact with.

**Old Way (AHK):** Scan screen for `fa_button.png` image  
**New Way (Python):** Find element with `div.btn-auto` CSS selector

### Advantages:
- ✅ 100x faster
- ✅ Works when UI changes
- ✅ No need for screenshots
- ✅ More reliable

---

## Step-by-Step: Finding Locators

### Example: Finding the Full Auto Button

#### Step 1: Open GBF and Navigate to Battle

1. Open Chrome
2. Go to `https://game.granbluefantasy.jp/`
3. Navigate to any quest
4. Start a battle

#### Step 2: Open Chrome DevTools

Press **F12** or **Ctrl+Shift+I**

You'll see something like this:

```
┌─────────────────────────────────────┐
│      Your Game Window               │
│                                     │
│  [Attack] [Full Auto]               │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│      DevTools Panel                 │
│  Elements | Console | Network       │
│                                     │
│  <html>                             │
│    <body>                           │
│      <div class="game">             │
│        ...                          │
└─────────────────────────────────────┘
```

#### Step 3: Activate Element Picker

Press **Ctrl+Shift+C** or click the "Select an element" button (top-left of DevTools)

Your cursor will change to a crosshair 🎯

#### Step 4: Click the Full Auto Button

Move your cursor over the Full Auto button in the game and **click it**.

DevTools will highlight the HTML for that button:

```html
<div class="btn-auto lis-auto" style="display: block;">
  <div class="btn-auto-inner">
    <div class="txt-btn-auto">Full Auto</div>
  </div>
</div>
```

#### Step 5: Copy the Selector

**Right-click** the highlighted HTML in DevTools  
→ **Copy**  
→ **Copy selector**

You'll get something like:
```
#game > div.prt-battle > div.btn-auto
```

**OR** you can write your own simpler selector:
```
div.btn-auto
```

#### Step 6: Paste into Locator File

Open `locators/battle_locators.py` and replace:

```python
# BEFORE:
FULL_AUTO_BUTTON = (
    By.CSS_SELECTOR, 
    "PLACEHOLDER"
)

# AFTER:
FULL_AUTO_BUTTON = (
    By.CSS_SELECTOR, 
    "div.btn-auto[style*='display: block']"
)
```

**Why `[style*='display: block']`?**  
This ensures the button is visible. Hidden buttons have `display: none`.

---

## Testing Your Locators

### Method 1: DevTools Console

1. **Open Console tab** in DevTools (not Elements)
2. **Type this command**:
   ```javascript
   document.querySelector("div.btn-auto[style*='display: block']")
   ```
3. **Press Enter**

**Results:**
- ✅ Returns `<div class="btn-auto">...`: **GOOD!** Locator works
- ❌ Returns `null`: **BAD!** Locator is wrong

### Method 2: Bot Verification

Run the bot with verification enabled:

```bash
python main.py --verify-locators
```

The bot will test ALL locators and tell you which ones don't work.

---

## Common Locator Patterns

### Pattern 1: Simple Class

```python
# Element: <div class="btn-attack"></div>
ATTACK_BUTTON = (By.CSS_SELECTOR, "div.btn-attack")
```

### Pattern 2: Multiple Classes

```python
# Element: <div class="btn-usual-ok se-ok"></div>
OK_BUTTON = (By.CSS_SELECTOR, "div.btn-usual-ok.se-ok")
#                              Note the dot between classes ^^
```

### Pattern 3: Class + Visibility Check

```python
# Only find if visible (display: block)
FULL_AUTO = (By.CSS_SELECTOR, "div.btn-auto[style*='display: block']")
```

### Pattern 4: Partial Class Match

```python
# Element: <div class="lis-supporter-12345"></div>
# The number changes, so use partial match:
SUMMON_ITEM = (By.CSS_SELECTOR, "[class*='lis-supporter']")
```

### Pattern 5: XPath for Text

```python
# Find element containing specific text
DIALOG = (By.XPATH, "//div[contains(text(), 'Character Defeated')]")
```

### Pattern 6: Parent > Child

```python
# Find child inside specific parent
BUTTON = (By.CSS_SELECTOR, "div.prt-battle > div.btn-auto")
#                          Parent        ^  Child
```

---

## Locator Priority Guide

### ✅ GOOD Locators (Recommended)

```python
# 1. Unique class name
"div.btn-auto"

# 2. Unique ID (if stable)
"#attack-button"

# 3. Data attributes
"[data-action='attack']"

# 4. Combination of stable classes
"div.prt-battle div.btn-auto"
```

### ⚠️ OKAY Locators (Use Carefully)

```python
# Class with visibility check
"div.btn-auto[style*='display']"

# Partial class match
"[class*='supporter']"

# nth-child (brittle, can break if UI changes)
"div.button-list > div:nth-child(2)"
```

### ❌ BAD Locators (Avoid)

```python
# Too generic (matches multiple elements)
"div"
"button"
".btn"

# Dynamic IDs (change every session)
"#prt-12345"
"#supporter-67890"

# Too specific (breaks if anything changes)
"html > body > div:nth-child(3) > div:nth-child(5) > div > button"
```

---

## Troubleshooting

### Problem: `null` in Console Test

**Cause:** Selector doesn't match any element

**Solutions:**
1. Make sure you're on the right page (battle screen, summon screen, etc.)
2. Check spelling and syntax:
   - `div.btn-auto` ✅
   - `div btn-auto` ❌ (missing dot)
   - `div..btn-auto` ❌ (double dot)
3. Inspect the element again - HTML might have changed

### Problem: Multiple Elements Found

**Cause:** Selector is too generic

**Solution:** Make it more specific:

```python
# Too generic (finds 10 buttons):
"div.btn"

# More specific (finds 1 button):
"div.prt-battle div.btn-auto"
```

### Problem: Element Not Visible

**Cause:** Element exists but is hidden

**Solution:** Add visibility check:

```python
# Before (finds hidden elements too):
"div.btn-auto"

# After (only finds visible):
"div.btn-auto[style*='display: block']"
```

### Problem: Selector Works in Console But Not in Bot

**Cause:** Timing issue - element loads after page loads

**Solution:** Increase timeout in code:

```python
# In page object class:
element = self.wait.until(
    EC.visibility_of_element_located(locator),
    timeout=10  # Wait up to 10 seconds
)
```

---

## Required Locators Checklist

Before running the bot, fill in these:

### Battle Screen (`battle_locators.py`)
- [ ] `FULL_AUTO_BUTTON` - Full Auto button
- [ ] `ATTACK_BUTTON` - Attack button
- [ ] `CANCEL_BUTTON` - Back/Cancel button
- [ ] `SALUTE_DIALOG` - Character defeat popup
- [ ] `ELIXIR_BUTTON` - Revive button
- [ ] `REJOIN_BUTTON` - Rejoin battle button

### Summon Screen (`summon_locators.py`)
- [ ] `AUTO_SELECT_BUTTON` - Auto-select summon
- [ ] `OK_BUTTON` - Confirm selection
- [ ] `SCROLL_CONTAINER` - Summon list scroll area

### Other Screens (`other_locators.py`)
- [ ] `RESULTS_NEXT_BUTTON` - Continue after battle
- [ ] `QUEST_START_BUTTON` - Start quest
- [ ] `STORY_SKIP_BUTTON` - Skip story
- [ ] `STORY_SKIP_OK` - Confirm skip

---

## Example: Complete Workflow

Let's find the **Attack Button** from start to finish:

1. **Open GBF** → Navigate to any battle
2. **Press F12** → Open DevTools
3. **Press Ctrl+Shift+C** → Activate element picker
4. **Click Attack button** → DevTools highlights HTML
5. **Check the HTML**:
   ```html
   <div class="btn-attack-start display-on">
     <div class="txt-attack">Attack</div>
   </div>
   ```
6. **Write selector**:
   ```python
   ATTACK_BUTTON = (By.CSS_SELECTOR, "div.btn-attack-start.display-on")
   ```
7. **Test in Console**:
   ```javascript
   document.querySelector("div.btn-attack-start.display-on")
   // Returns: <div class="btn-attack-start display-on">...</div>
   // ✅ WORKS!
   ```
8. **Paste into file** → `locators/battle_locators.py`
9. **Mark as verified**:
   ```python
   LOCATOR_STATUS = {
       'ATTACK_BUTTON': 'VERIFIED',  # ✅ Done!
   }
   ```

Repeat for all buttons!

---

## Tips & Tricks

### Tip 1: Use Simple Selectors

Simpler is better:
```python
# Good:
"div.btn-auto"

# Overcomplicated:
"html body div#game div.prt-wrapper div.prt-battle div.btn-auto"
```

### Tip 2: Check for Dynamic Classes

Some games add random numbers to classes:
```html
<!-- Bad: Number changes -->
<div class="supporter-item-12345">

<!-- Good: Stable class -->
<div class="supporter-item" data-id="12345">
```

Use `[class*='supporter-item']` for partial match.

### Tip 3: Save Screenshots

When element picker is active, take a screenshot! Helps remember where elements are.

### Tip 4: Document Your Locators

Add comments:
```python
# Location: Bottom-left during battle
# Appears: Only when battle is ready
FULL_AUTO_BUTTON = (By.CSS_SELECTOR, "div.btn-auto[style*='display']")
```

---

## Next Steps

1. ✅ Fill in ALL required locators
2. ✅ Test each one in DevTools Console
3. ✅ Run bot verification: `python main.py --verify-locators`
4. ✅ Fix any failed locators
5. ✅ Start the bot!

**Need help?** Check the error logs in `data/logs/` - they'll tell you exactly which locator failed and why.
