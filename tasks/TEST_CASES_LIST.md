# Test Cases List

Quick reference list of all test cases in the simAPy framework, organized by category.

## Table of Contents

1. [Navigation Tests](#navigation-tests)
2. [Content Validation Tests](#content-validation-tests)
3. [Navigation Layout Tests](#navigation-layout-tests)
4. [Trading Functionality Tests](#trading-functionality-tests)

---

## Navigation Tests

**File:** `tests/ui/test_navigation.py`  
**Class:** `TestNavigation`

- **TC-NAVIGATION-002:** About Us page navigation via dropdown links
- **TC-NAVIGATION-003:** Trade page navigation via dropdown links
- **TC-NAVIGATION-004:** Features page navigation via dropdown links
- **TC-NAVIGATION-005:** Support page navigation via dropdown links

---

### Content Validation Tests

**File:** `tests/ui/test_content_validation.py`  
**Class:** `TestContentValidation`

- **TC-CONTENT-CORE-001:** Hero banner appears in the top section of the page
- **TC-CONTENT-CORE-002:** Marketing banners appear at the page bottom
- **TC-CONTENT-CORE-003:** Download section links correctly to App Store and Google Play
- **TC-CONTENT-CORE-004:** Download section content
- **TC-CONTENT-CORE-005:** About Us → Why Multibank page renders all expected components with correct text

---

### Navigation Layout Tests

**File:** `tests/ui/test_navigation_layout.py`  
**Class:** `TestNavigationLayout`

- **TC-NAV-CORE-001:** Top navigation menu displays correctly with all expected options
- **TC-NAV-CORE-002:** Navigation items are functional and link to appropriate destinations
- **TC-NAV-CORE-003:** Navigation menu responsiveness

---

### Trading Functionality Tests

**File:** `tests/ui/test_trading_functionality.py`  
**Class:** `TestTradingFunctionality`

- **TC-TRADE-CORE-001:** Spot trading section displays trading pairs across different categories
- **TC-TRADE-CORE-002:** Trading pair data structure and presentation is correct
- **TC-TRADE-CORE-003:** Trading pair filtering and sorting
- **TC-TRADE-CORE-004:** Trading pair interaction - Market data buttons display and interaction

---

## Summary

| Category | Test Cases | File |
|----------|-----------|------|
| **Navigation** | 4 | `test_navigation.py` |
| **Content Validation** | 5 | `test_content_validation.py` |
| **Navigation Layout** | 3 | `test_navigation_layout.py` |
| **Trading Functionality** | 4 | `test_trading_functionality.py` |
| **Total** | **16** | **4 files** |

