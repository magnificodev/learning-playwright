import asyncio
from playwright.async_api import Playwright, async_playwright, Page

async def scroll_to_bottom(page: Page) -> None:
    
    product_list_height = "document.querySelector('section > .product-grid__items').scrollHeight"
    
    # Get the initial scroll height of the page
    last_height = await page.evaluate(product_list_height)
    iteration = 1

    while True:
        print(f"Scrolling page {iteration}...")

        # Scroll to the bottom of the page
        await page.evaluate(f"window.scrollTo(0, {product_list_height})")

        # Wait for the page to load additional content
        await asyncio.sleep(2)

        # Get the new scroll height and compare it with the last height
        new_height = await page.evaluate(product_list_height)
        
        print(iteration, new_height, last_height, sep=", ")
        
        if new_height == last_height:
            break  # Exit the loop if the bottom of the page is reached
        last_height = new_height
        iteration += 1

async def scrape_shoes(playwright: Playwright, url: str) -> None:
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page(viewport={"width": 1600, "height": 900})

    await page.goto(url)

    # Scrolling to the bottom of the page...
    await scroll_to_bottom(page)

    shoes_list = []

    shoe_containers = await page.query_selector_all(".product-card")

    for shoe in shoe_containers:
        shoe_name = await shoe.query_selector(".product-card__title")
        shoe_name = await shoe_name.text_content() if shoe_name else "N/A"

        shoe_price = await shoe.query_selector(".product-price")
        shoe_price = await shoe_price.text_content() if shoe_price else "N/A"

        shoe_colors = await shoe.query_selector(".product-card__product-count")
        shoe_colors = await shoe_colors.text_content() if shoe_colors else "N/A"

        shoe_status = await shoe.query_selector(".product-card__messaging")
        shoe_status = await shoe_status.text_content() if shoe_status else "N/A"

        shoe_link = await shoe.query_selector(".product-card__link-overlay")
        shoe_link = await shoe_link.get_attribute("href") if shoe_link else "N/A"

        shoe_info = {
            "name": shoe_name,
            "price": shoe_price,
            "colors": shoe_colors,
            "status": shoe_status,
            "link": shoe_link,
        }

        shoes_list.append(shoe_info)
    print(f"Total number of shoes scraped: {len(shoes_list)}")

    await browser.close()

async def main() -> None:
    async with async_playwright() as playwright:
        await scrape_shoes(
            playwright=playwright,
            url="https://www.nike.com/w/mens-lifestyle-shoes-13jrmznik1zy7ok",
        )

if __name__ == "__main__":
    asyncio.run(main())