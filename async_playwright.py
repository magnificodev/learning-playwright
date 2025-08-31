import asyncio
from playwright.async_api import Playwright, async_playwright


async def run(playwright: Playwright, url: str):
    # Launch Chromium in non-headless mode (visible UI)
    browser = await playwright.chromium.launch(headless=False)

    # Open a new browser page with specified dimensions
    page = await browser.new_page(viewport={"width": 1600, "height": 900})

    # Navigate to the given URL
    await page.goto(url)

    # Add a sleep to ensure the page is fully loaded
    await asyncio.sleep(3)  # Wait for 3 seconds

    # Take a screenshot
    await page.screenshot(path="visible_part.png", full_page=True)

    # Close the browser
    await browser.close()


async def main():
    # Use async_playwright to manage the Playwright instance
    async with async_playwright() as playwright:
        await run(playwright, url="https://playwright.dev/")


if __name__ == "__main__":
    asyncio.run(main())
