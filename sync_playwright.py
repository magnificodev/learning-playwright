from playwright.sync_api import sync_playwright


def run(playwright, url):
    # Launch Chromium in non-headless mode (visible UI)
    browser = playwright.chromium.launch(headless=False)

    # Open a new browser page with specified dimensions
    page = browser.new_page(viewport={"width": 600, "height": 300})

    # Navigate to the given URL
    page.goto(url)

    # Get the page title
    title = page.title()

    # Close the browser
    browser.close()

    # Return the URL and title as a dictionary
    return {"url": url, "title": title}

def main():
    # Use sync_playwright to manage the Playwright instance
    with sync_playwright() as playwright:
        result = run(playwright, url="https://scrapingant.com/")
        print(result)

if __name__ == "__main__":
    main()