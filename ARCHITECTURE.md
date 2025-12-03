# Architecture Design & Rationale

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Architectural Principles](#architectural-principles)
- [Framework Structure](#framework-structure)
- [Design Decisions](#design-decisions)
- [Key Patterns](#key-patterns)
- [Technology Choices](#technology-choices)
- [Trade-offs](#trade-offs)

---

## Core Philosophy

### Simplicity at the Core, Strong Features on Top

The fundamental architectural decision for simAPy is to **keep the core simple** while providing **strong features** that enhance developer productivity and test reliability. This philosophy drives every architectural choice we make.

### The Playwright-First Approach

**Key Decision:** Use Playwright's official APIs directly without creating unnecessary wrapper layers.

**Rationale:**
- Playwright is a mature, well-designed framework with excellent APIs
- Wrappers add abstraction layers that:
  - Hide Playwright's powerful features
  - Create maintenance burden
  - Introduce bugs and inconsistencies
  - Make debugging harder
  - Require developers to learn both Playwright AND our wrapper
- Direct usage means:
  - Developers can leverage Playwright's full feature set
  - Documentation and examples from Playwright directly apply
  - Easier debugging with Playwright's built-in tools
  - Less code to maintain
  - Faster adoption for developers already familiar with Playwright

**What We DON'T Do:**
```python
# ❌ Anti-pattern: Wrapping Playwright's Page object
class CustomPage:
    def __init__(self, playwright_page):
        self._page = playwright_page
    
    def click(self, selector):
        # Unnecessary wrapper that adds no value
        self._page.click(selector)
    
    def fill(self, selector, text):
        # Another wrapper that hides Playwright features
        self._page.fill(selector, text)
```

**What We DO:**
```python
# ✅ Direct usage: Use Playwright's Page and Locator directly
class BasePage:
    def __init__(self, page: Page):
        self.page = page  # Direct reference to Playwright Page
    
    def goto(self, url: str, **kwargs):
        # Thin convenience layer that uses Playwright's built-in methods
        self.page.goto(url, **kwargs)
```

---

## Architectural Principles

### 1. **Direct Playwright Usage**
- Use Playwright's `Page`, `Locator`, and `expect` APIs directly
- Leverage Playwright's auto-waiting and built-in retries
- Use Playwright's official best practices

### 2. **Minimal Abstraction**
- Only add abstractions that provide real value
- Prefer composition over inheritance
- Keep abstractions thin and transparent

### 3. **Separation of Concerns**
- **Page Objects**: Encapsulate page-specific logic and locators
- **Components**: Reusable UI components (Navigation, Trading Section, etc.)
- **Utilities**: Cross-cutting concerns (waiting, retry, logging)
- **Fixtures**: Test setup and configuration
- **Tests**: Business logic validation

### 4. **Test Data Externalization**
- All test data in YAML files
- No hard-coded values in tests
- Environment-specific configurations

### 5. **Explicit Over Implicit**
- Clear, readable test code
- Explicit waits using Playwright's `expect` API
- Explicit error handling and logging

---

## Framework Structure

```
simAPy/
├── tests/
│   ├── pages/              # Page Object Model
│   │   ├── basepage.py     # Base page with common navigation
│   │   └── multibank/      # Application-specific pages
│   │       ├── homepage.py
│   │       ├── aboutuspage.py
│   │       └── components/ # Reusable UI components
│   │           ├── navigation.py
│   │           ├── tradingsection.py
│   │           └── ...
│   ├── fixtures/           # Pytest fixtures
│   │   ├── playwright.py   # Browser/page fixtures
│   │   ├── configload.py   # Configuration loading
│   │   └── testdata.py     # Test data loading
│   ├── utils/              # Utility modules
│   │   ├── wait.py         # Wait utilities (thin wrappers)
│   │   ├── retry.py        # Retry decorators
│   │   ├── logging/        # Logging framework
│   │   └── exceptions.py   # Custom exceptions
│   ├── ui/                 # Test files
│   │   ├── test_navigation.py
│   │   ├── test_trading.py
│   │   └── test_content_validation.py
│   └── data/               # Test data (YAML)
│       ├── navigation_test_data.yaml
│       ├── trading_test_data.yaml
│       └── content_test_data.yaml
├── configs/                # Environment configurations
│   ├── dev.yaml
│   ├── stage.yaml
│   └── prod.yaml
└── tasks/                  # Additional tasks (e.g., Task 2)
    └── task2_character_frequency.py
```

---

## Design Decisions

### Decision 1: Page Object Model (POM) with Components

**Decision:** Use Page Object Model with component-based architecture.

**Rationale:**
- **Maintainability**: UI changes require updates in one place
- **Reusability**: Components can be shared across pages
- **Readability**: Tests read like user stories
- **Scalability**: Easy to add new pages and components

**Implementation:**
```python
# Base page uses Playwright Page directly
class BasePage:
    def __init__(self, page: Page):
        self.page = page  # Direct Playwright Page reference

# Page objects inherit from BasePage
class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Components use Playwright Locators directly
        self.navigation = NavigationComponent(page)
        self.trading_section = TradingSectionComponent(page)

# Components encapsulate related UI elements
class NavigationComponent:
    def __init__(self, page: Page):
        self.page = page
        # Direct Playwright locators
        self.nav_container = page.locator("header, nav, [role='banner']").first
        self.markets_link = page.get_by_role("link", name="Markets")
```

**Benefits:**
- Clear separation between pages and components
- Components can be tested independently
- Easy to compose complex pages from simple components

---

### Decision 2: Direct Playwright Locator Usage

**Decision:** Use Playwright's locator API directly without custom selector builders.

**Rationale:**
- Playwright's locator API is powerful and expressive
- Supports multiple selector strategies (CSS, XPath, text, role, test-id)
- Built-in auto-waiting eliminates flakiness
- No need to reinvent the wheel

**Implementation:**
```python
# ✅ Direct Playwright locators
class NavigationComponent:
    def __init__(self, page: Page):
        # Use Playwright's role-based locators (recommended)
        self.markets_link = page.get_by_role("link", name="Markets", exact=True)
        self.login_link = page.get_by_role("link", name="Log In", exact=True)
        
        # Use test-id when available (best practice)
        self.logo_link = page.get_by_test_id("logo")
        
        # Use CSS/XPath when needed
        self.nav_container = page.locator("header, nav, [role='banner']").first
```

**Why Not Custom Selector Builders?**
- Adds unnecessary complexity
- Hides Playwright's powerful features
- Requires maintaining selector syntax
- Developers need to learn our syntax instead of Playwright's

---

### Decision 3: Playwright's `expect` API for Assertions

**Decision:** Use Playwright's `expect` API instead of custom assertion libraries.

**Rationale:**
- Playwright's `expect` has built-in auto-waiting
- Reduces flakiness by waiting for conditions automatically
- Consistent with Playwright's design philosophy
- No need for separate assertion library

**Implementation:**
```python
from playwright.sync_api import expect

# ✅ Use Playwright's expect API
def test_navigation(self, page, config):
    homepage = TestHelper.navigate_to_homepage(page, config)
    
    # Auto-waits for element to be visible
    expect(homepage.navigation.nav_container).to_be_visible()
    
    # Auto-waits for URL to match
    expect(page).to_have_url(re.compile(".*market.*"))
    
    # Auto-waits for text content
    expect(homepage.navigation.markets_link).to_have_text("Markets")
```

**Benefits:**
- No need for explicit waits before assertions
- More reliable tests
- Cleaner test code
- Leverages Playwright's built-in retry logic

---

### Decision 4: Thin Utility Wrappers

**Decision:** Create minimal utility functions only when they add value.

**Rationale:**
- Some operations benefit from slight abstraction
- Utilities should be thin wrappers around Playwright APIs
- Only create utilities that:
  - Improve readability
  - Add domain-specific logic
  - Provide consistent error handling
  - Don't hide Playwright features

**Implementation:**
```python
# ✅ Thin wrapper that adds value (error handling + logging)
def wait_for_dropdown(page: Page, dropdown_locator: Locator, timeout: int = 5000):
    """Wait for dropdown with custom error handling"""
    try:
        # Still uses Playwright's expect API directly
        expect(dropdown_locator).to_be_visible(timeout=timeout)
        return dropdown_locator
    except PlaywrightTimeoutError as e:
        # Add custom error with context
        raise ElementNotFoundError(f"Dropdown not found: {e}") from e

# ❌ Unnecessary wrapper that hides Playwright
def click_element(locator):
    """Don't do this - just use locator.click() directly"""
    locator.click()
```

**When to Create Utilities:**
- ✅ Error handling and logging
- ✅ Domain-specific operations
- ✅ Retry logic for flaky operations
- ✅ Test data transformations

**When NOT to Create Utilities:**
- ❌ Simple Playwright operations (click, fill, etc.)
- ❌ Selector building (use Playwright's locators)
- ❌ Basic assertions (use Playwright's expect)

---

### Decision 5: Mixins for Code Reuse

**Decision:** Use Python mixins to share common functionality across page objects.

**Rationale:**
- Avoids deep inheritance hierarchies
- Promotes composition over inheritance
- Allows selective feature inclusion
- Keeps code DRY without coupling

**Implementation:**
```python
# Mixin provides reusable functionality
class ContentPageMixin:
    """Mixin for pages with content validation"""
    
    page: Page  # Type hint for mixin compatibility
    page_heading: Locator
    
    def get_page_heading(self, timeout: int = 5000) -> str:
        # Uses Playwright APIs directly
        self.page_heading.wait_for(state="visible", timeout=timeout)
        return self.page_heading.inner_text()

# Page objects use mixins for composition
class AboutUsPage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    def __init__(self, page: Page):
        super().__init__(page)
        # Direct Playwright locators
        self.page_heading = page.locator('h1, [role="heading"]').first
```

**Benefits:**
- Reusable functionality without inheritance chains
- Pages can pick and choose features
- Easy to test mixins independently
- Clear separation of concerns

---

### Decision 6: External Test Data (YAML)

**Decision:** Store all test data in YAML files, separate from test code.

**Rationale:**
- **Maintainability**: Update test data without touching code
- **Reusability**: Same data can be used across multiple tests
- **Clarity**: Tests focus on logic, not data
- **Flexibility**: Easy to create environment-specific data

**Implementation:**
```yaml
# tests/data/navigation_test_data.yaml
navigation:
  expected_items:
    - Markets
    - Log In
    - Sign Up
  url_patterns:
    markets: ".*market.*"
```

```python
# Test uses external data
def test_navigation(self, page, config, test_data):
    nav_data = test_data["navigation"]
    expected_items = nav_data["expected_items"]
    
    for item in expected_items:
        assert item in nav_items
```

**Benefits:**
- Non-developers can update test data
- Easy to create data-driven tests
- Environment-specific configurations
- Version control friendly

---

### Decision 7: Configuration Management

**Decision:** Multi-environment configuration with YAML files and environment variables.

**Rationale:**
- Support multiple environments (dev, stage, prod)
- Environment variables for sensitive data
- YAML for structured configuration
- Easy to switch environments

**Implementation:**
```yaml
# configs/dev.yaml
MultiBank:
  base_url: ${MULTIBANK_BASE_URL:https://trade.multibank.io}
  element_visibility_timeout: ${MULTIBANK_ELEMENT_VISIBILITY_TIMEOUT:2000}

Playwright:
  viewport:
    width: 1920
    height: 1080
  navigation_timeout: ${PLAYWRIGHT_NAVIGATION_TIMEOUT:30000}
```

**Benefits:**
- Environment-specific settings
- Secure handling of sensitive data
- Easy configuration updates
- Supports CI/CD pipelines

---

### Decision 8: Retry Mechanism as Decorators

**Decision:** Implement retry logic as Python decorators, not as wrapper methods.

**Rationale:**
- Clean, declarative syntax
- Reusable across different operations
- Doesn't interfere with Playwright's built-in retries
- Easy to apply selectively

**Implementation:**
```python
# Retry decorator for flaky operations
@retry_element_interaction(max_attempts=3, delay=0.5)
def click_markets(self, timeout: int = 10000):
    """Click Markets link with retry"""
    # Uses Playwright's API directly
    self.markets_nav_link.wait_for(state="visible", timeout=timeout)
    self.markets_nav_link.click()
```

**Benefits:**
- Declarative retry logic
- Works with Playwright's built-in retries
- Easy to configure per method
- Doesn't hide Playwright features

---

## Key Patterns

### Pattern 1: Direct Playwright API Usage

**Pattern:** Use Playwright's APIs directly in page objects and components.

```python
class NavigationComponent:
    def __init__(self, page: Page):
        self.page = page
        # Direct Playwright locators
        self.markets_link = page.get_by_role("link", name="Markets")
    
    def click_markets(self):
        # Direct Playwright method
        self.markets_link.click()
```

**Why:** No abstraction layer means full access to Playwright's features.

---

### Pattern 2: Component-Based Page Objects

**Pattern:** Compose pages from reusable components.

```python
class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Compose from components
        self.navigation = NavigationComponent(page)
        self.trading_section = TradingSectionComponent(page)
        self.marketing_banners = MarketingBannersComponent(page)
```

**Why:** Promotes reusability and maintainability.

---

### Pattern 3: Mixins for Shared Functionality

**Pattern:** Use mixins to share functionality without deep inheritance.

```python
class AboutUsPage(BasePage, ContentPageMixin, SubPageNavigationMixin):
    # Inherits navigation from BasePage
    # Gets content validation from ContentPageMixin
    # Gets sub-page navigation from SubPageNavigationMixin
```

**Why:** Flexible composition without inheritance chains.

---

### Pattern 4: Fixture-Based Configuration

**Pattern:** Use pytest fixtures for test setup and configuration.

```python
@pytest.fixture(scope="session")
def config():
    """Load configuration once per test session"""
    return load_config()

@pytest.fixture
def test_data(config):
    """Load test data per test"""
    return load_test_data(config)
```

**Why:** Clean separation of concerns and efficient resource management.

---

### Pattern 5: Data-Driven Tests

**Pattern:** Externalize test data and use parametrization.

```python
@pytest.mark.parametrize("sub_page_name", ["Why Multibank?", "Global Presence"])
def test_navigation(self, page, config, test_data, sub_page_name):
    # Test logic uses parametrized data
    homepage.navigation.click_about_us_item(sub_page_name)
```

**Why:** Reduces code duplication and enables easy test expansion.

---

## Technology Choices

### Playwright

**Why Playwright?**
- Modern, fast, and reliable
- Excellent API design
- Built-in auto-waiting
- Cross-browser support
- Active development and community
- Great documentation

**How We Use It:**
- Direct API usage (no wrappers)
- Leverage auto-waiting and retries
- Use official best practices
- Follow Playwright's recommended patterns

---

### pytest

**Why pytest?**
- Industry standard for Python testing
- Excellent fixture system
- Rich plugin ecosystem
- Great for parallel execution
- Clear test output

**How We Use It:**
- Fixtures for setup/teardown
- Markers for test categorization
- Parametrization for data-driven tests
- Plugins for Playwright integration

---

### Allure Reporting

**Why Allure?**
- Rich, interactive reports
- Screenshot and video attachments
- Test history and trends
- Integration with CI/CD
- Industry standard

**How We Use It:**
- Custom decorators for attachments
- Screenshot on failure
- Test categorization
- Historical reporting

---

### YAML for Configuration

**Why YAML?**
- Human-readable
- Supports complex data structures
- Easy to edit
- Widely used in DevOps
- Good tooling support

**How We Use It:**
- Test data files
- Environment configurations
- Easy to version control

---

## Trade-offs

### Trade-off 1: Direct Playwright Usage vs. Custom Wrappers

**Chosen:** Direct Playwright Usage

**Pros:**
- Full access to Playwright features
- Easier debugging
- Less code to maintain
- Faster developer onboarding
- Better documentation support

**Cons:**
- Developers need Playwright knowledge
- Less "framework-specific" abstraction

**Rationale:** The benefits far outweigh the costs. Playwright's API is well-designed and doesn't need wrapping.

---

### Trade-off 2: Component-Based vs. Flat Page Objects

**Chosen:** Component-Based Architecture

**Pros:**
- Better code organization
- Reusable components
- Easier maintenance
- Scales well

**Cons:**
- Slightly more complex structure
- More files to manage

**Rationale:** The organizational benefits and reusability justify the added structure.

---

### Trade-off 3: YAML vs. JSON vs. Python for Test Data

**Chosen:** YAML

**Pros:**
- Human-readable
- Supports comments
- Easy to edit
- Good for complex structures

**Cons:**
- Requires YAML parser
- Less type-safe than Python

**Rationale:** YAML's readability and editability make it ideal for test data that non-developers may need to update.

---

### Trade-off 4: Mixins vs. Deep Inheritance

**Chosen:** Mixins

**Pros:**
- Flexible composition
- Avoids deep inheritance
- Selective feature inclusion
- Better testability

**Cons:**
- Multiple inheritance complexity
- Type hints can be tricky

**Rationale:** Mixins provide flexibility without the complexity of deep inheritance hierarchies.

---

## Conclusion

The architecture of simAPy is built on a simple principle: **use Playwright directly and add only what's necessary**. This approach:

1. **Keeps the core simple** - No unnecessary abstractions
2. **Provides strong features** - Utilities and patterns that add real value
3. **Leverages Playwright's power** - Full access to Playwright's features
4. **Maintains clarity** - Code is easy to understand and debug
5. **Scales well** - Architecture supports growth without complexity

By avoiding unnecessary wrappers and abstractions, we've created a framework that is:
- **Easy to learn** - Developers familiar with Playwright can start immediately
- **Easy to maintain** - Less code means fewer bugs
- **Easy to extend** - Clear patterns for adding new features
- **Production-ready** - Reliable, scalable, and maintainable

This architecture demonstrates that **simplicity and power are not mutually exclusive** - by using Playwright's excellent APIs directly and adding only what's needed, we've created a framework that is both simple and feature-rich.

