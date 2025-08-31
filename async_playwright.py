import asyncio
from playwright.async_api import async_playwright


async def run(playwright, url):
    browser = await playwright.chromium.launch(headless=False)
    
    page = await browser.new_page(viewport={"width": 1600, "height": 900})
    
    await page.goto(url)
    
    title = await page.title()
    
    await browser.close()
    
    return {"url": url, "title": title}
    

async def main():
    async with async_playwright() as playwright:
        result = await run(playwright, url="https://scrapingant.com/")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())