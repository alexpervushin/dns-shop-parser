import logging

from playwright.async_api import async_playwright

URL = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug.log"),
                              logging.StreamHandler()])


async def get_request_data():
    cookies = {}
    headers = {}

    def get_response_headers(response):
        nonlocal headers
        headers = response.headers
        logging.info(f"Получены headers: {headers}")

    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        page.on("response", get_response_headers)
        await page.goto(URL)
        await page.wait_for_selector('.products-page__list')
        cookies_list = await context.cookies()
        await browser.close()

    for c in cookies_list:
        cookies.update({c["name"]: c["value"]})
    logging.info(f"Получены cookies: {cookies}")
    return cookies, headers
