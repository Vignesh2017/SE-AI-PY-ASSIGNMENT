from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    # Open browser
    browser = p.chromium.launch(headless=False)

    # Create page
    page = browser.new_page()

    # Open Cricbuzz
    page.goto(
        "https://www.cricbuzz.com/",
        wait_until="domcontentloaded"
    )

    # Wait for page
    page.wait_for_timeout(3000)

    # Screenshot before clicking
    page.screenshot(
        path="playwright_cricbuzz_before.png",
        full_page=True
    )

    # Find Live Scores link
    live_scores = page.get_by_text("Live Scores", exact=True).first

    # Check whether Playwright found it
    print("Live Scores count:", page.get_by_text("Live Scores", exact=True).count())

    # Click Live Scores
    live_scores.click()

    # Wait for navigation
    page.wait_for_load_state("domcontentloaded")

    # Wait a little for the page to render
    page.wait_for_timeout(3000)

    # Print current URL
    print("Current URL:", page.url)

    # Screenshot after navigation
    page.screenshot(
        path="playwright_cricbuzz_after.png",
        full_page=True
    )

    print("Run completed!")
    print("Screenshot saved as playwright_cricbuzz_after.png")

    # Keep browser open
    page.wait_for_timeout(5000)

    browser.close()