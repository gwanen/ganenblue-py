# 🎮 Granblue Fantasy Bot - Python Edition

A sophisticated automation bot for Granblue Fantasy using Selenium WebDriver with **Page Object Model** architecture and **full anti-detection** measures.

## ✨ Key Features

- ✅ **No Image Recognition** - Uses DOM element locators (faster, more reliable)
- ✅ **Mouse Freedom** - Your mouse is free to use while bot runs
- ✅ **Anti-Detection** - Undetected ChromeDriver + human behavior simulation
- ✅ **Page Object Model** - Professional, maintainable architecture
- ✅ **Locator Verification** - Tells you when elements aren't found
- ✅ **Smart GUI** - Clean interface with real-time statistics
- ✅ **Human Behavior** - Random delays, fatigue simulation, breaks
- ✅ **Multi-Tasking** - Run on second monitor or minimized

## 📋 Requirements

- Python 3.11+
- Chrome browser (latest version)
- Windows/Mac/Linux

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Fill in Locators (IMPORTANT!)

**Before running the bot, you MUST fill in the element locators:**

1. Open GBF in Chrome
2. Press `F12` (open DevTools)
3. Press `Ctrl+Shift+C` (element picker)
4. Click on a button (e.g., Full Auto button)
5. In DevTools, right-click the highlighted HTML > **Copy > Copy selector**
6. Open `locators/battle_locators.py`
7. Replace `PLACEHOLDER` with your copied selector

**Example:**

```python
# Before (PLACEHOLDER):
FULL_AUTO_BUTTON = (By.CSS_SELECTOR, "PLACEHOLDER")

# After (real selector):
FULL_AUTO_BUTTON = (By.CSS_SELECTOR, "div.btn-auto[style*='display: block']")
```

**Required Locators to Fill:**

- `locators/battle_locators.py` - Full Auto, Attack, Elixir, Rejoin buttons
- `locators/summon_locators.py` - Auto-select, OK button
- `locators/other_locators.py` - Results, Quest start, Story skip

### 3. Configure Quest URL

Edit `config/bot_settings.json`:

```json
{
  "quest_url": "https://game.granbluefantasy.jp/#quest/supporter/940331/3"
}
```

### 4. Run the Bot

```bash
python main.py
```

## 📁 Project Structure

```
gbf-bot/
├── main.py                     # Start here!
├── config/
│   ├── settings.py             # Global settings
│   └── bot_settings.json       # Your quest URL, preferences
├── locators/                   # ⚠️ FILL THESE IN!
│   ├── battle_locators.py      # Battle screen elements
│   ├── summon_locators.py      # Summon selection
│   └── other_locators.py       # Results, quest, story
├── pages/                      # Page Object classes
│   ├── battle_page.py          # Battle interactions
│   └── summon_page.py          # Summon selection
├── handlers/                   # Business logic
│   ├── battle_handler.py       # Battle automation
│   └── summon_handler.py       # Summon handling
├── antidetection/              # Anti-bot measures
│   └── stealth.py              # Undetected ChromeDriver
├── utils/                      # Utilities
│   ├── human_simulator.py      # Human-like behavior
│   ├── locator_verification.py # Element detection
│   └── logger.py               # Logging system
└── data/
    ├── logs/                   # Bot logs
    └── screenshots/            # Error screenshots
```

## 🔍 How to Find Element Locators

### Method 1: Chrome DevTools (Recommended)

1. **Open GBF in Chrome**
2. **Press F12** to open DevTools
3. **Press Ctrl+Shift+C** (Element Picker)
4. **Click on the button** you want to find (e.g., Attack button)
5. In DevTools, the HTML will be highlighted
6. **Right-click** the highlighted HTML
7. **Copy > Copy selector**
8. **Paste into locator file**

### Method 2: Console Testing

Test your selector in Console:

```javascript
// In DevTools Console tab:
document.querySelector("div.btn-auto")  // Should return the element
```

If it returns `null`, your selector is wrong!

### Example Selectors

```python
# Button with specific class
ATTACK_BUTTON = (By.CSS_SELECTOR, "div.btn-attack-start")

# Button that's visible (has display: block)
FULL_AUTO_BUTTON = (By.CSS_SELECTOR, "div.btn-auto[style*='display: block']")

# Using XPath for text content
DIALOG = (By.XPATH, "//div[contains(text(), 'Character Defeated')]")

# Class with partial match
SUMMON = (By.CSS_SELECTOR, "[class*='supporter-item']")
```

## ⚙️ Configuration

### Anti-Detection Settings

Edit `.env` or `config/settings.py`:

```python
# Safety limits (prevents ban)
MAX_SESSION_DURATION = 14400  # 4 hours max
MIN_BREAK_DURATION = 600      # 10 min breaks
BREAK_FREQUENCY = 3600        # Every hour
MIN_CLICK_DELAY = 0.5         # 500ms minimum between clicks
MAX_CLICK_DELAY = 2.0         # 2s maximum
```

### Window Position

Run on second monitor:

```json
{
  "window_position": [1920, 0]  // X, Y coordinates
}
```

## 🛡️ Anti-Detection Features

### What Makes This Bot Undetectable?

1. **Undetected ChromeDriver** - Bypasses `navigator.webdriver` detection
2. **Human Behavior Simulation**:
   - Random delays (not fixed 300ms)
   - Variable click positions (not center)
   - Occasional mouse movements
   - Fatigue simulation (slower over time)
   - Mandatory breaks
3. **Fingerprint Randomization**:
   - Randomized User-Agent
   - Variable viewport sizes
   - Realistic timezone
4. **Pattern Avoidance**:
   - No 24/7 farming
   - Session duration limits
   - Varied action timing

### Safety Best Practices

✅ **DO:**
- Run 4-6 hours max per session
- Take breaks every hour
- Use visible window (not headless)
- Vary quest types occasionally
- Manually play sometimes

❌ **DON'T:**
- Run 24/7
- Click faster than 200ms
- Farm same quest 1000+ times
- Ignore CAPTCHAs
- Use headless mode

## 🐛 Troubleshooting

### "Element NOT FOUND"

**Problem:** Bot can't find a button

**Solution:**
1. Check the locator file (e.g., `battle_locators.py`)
2. Make sure you replaced `PLACEHOLDER` with real selector
3. Test selector in DevTools Console:
   ```javascript
   document.querySelector("your.selector.here")
   ```
4. If `null`, get new selector using Element Picker

### "PLACEHOLDER not filled"

**Problem:** You haven't filled in the locators

**Solution:**
1. Read "How to Find Element Locators" above
2. Fill in ALL required locators
3. Test each one in DevTools

### Bot clicks but nothing happens

**Problem:** Element found but not clickable

**Solution:**
1. Element might be loading - increase timeout
2. Element might be covered - check z-index
3. Try clicking parent element
4. Check if element is in an iframe

### Chrome driver version mismatch

**Problem:** ChromeDriver version doesn't match Chrome

**Solution:**
- `undetected-chromedriver` handles this automatically
- If still failing, update Chrome to latest version

## 📊 Monitoring

### View Logs

```bash
# All activity
tail -f data/logs/bot_2024-XX-XX.log

# Errors only
tail -f data/logs/errors.log
```

### Statistics

The GUI shows real-time:
- Battles completed
- Errors encountered
- Current status
- Session duration

## 🎯 Battle Modes

### Full Auto Mode
Bot clicks **Full Auto** button and waits

### Semi Auto Mode
Bot clicks **Attack** button each turn (not Full Auto)

Toggle in GUI or config:
```json
{
  "battle_mode": "full_auto"  // or "semi_auto"
}
```

## 🔄 vs AutoHotkey Version

| Feature | AHK (Old) | Python (New) |
|---------|-----------|--------------|
| Mouse | ❌ Blocked | ✅ Free |
| Method | Image files | DOM locators |
| Speed | Slow (image scan) | Fast (direct) |
| Reliability | 90% (UI changes break) | 99% (stable) |
| Headless | ❌ No | ✅ Yes |
| Multi-window | Difficult | Easy |
| Debugging | Hard | DevTools |

## 🤝 Contributing

Found a bug or want to improve? 

1. Test your locators thoroughly
2. Document any changes
3. Follow existing code style

## ⚠️ Disclaimer

This bot is for **educational purposes only**. Use at your own risk. Botting may violate the game's Terms of Service and could result in account suspension or ban.

## 📚 Additional Resources

- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [CSS Selectors Guide](https://www.w3schools.com/cssref/css_selectors.asp)
- [XPath Tutorial](https://www.w3schools.com/xml/xpath_intro.asp)
- [Chrome DevTools Guide](https://developer.chrome.com/docs/devtools/)

## 🆘 Getting Help

1. **Check logs** in `data/logs/`
2. **Test locators** in DevTools Console
3. **Read error messages** - they tell you what's wrong
4. **Check screenshots** in `data/screenshots/` (taken on errors)

---

**Ready to start? Fill in the locators and run `python main.py`!** 🚀
