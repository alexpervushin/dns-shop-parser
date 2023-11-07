import asyncio

import aiohttp
from bs4 import BeautifulSoup


async def get_total_pages(session):
    async with session.get('https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p=1') as response:
        soup = BeautifulSoup(await response.text(), 'html.parser')
        total_pages = int(
            soup.find(class_='pagination-widget__page-link pagination-widget__page-link_last').get("href").split("p=")[
                -1])
    return total_pages


async def get_products_id(cookies: str, headers: str) -> list:
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        semaphore = asyncio.Semaphore(10)
        total_pages = await get_total_pages(session)
        pages = list(range(1, total_pages + 1))
        tasks = [fetch(session, page, semaphore) for page in pages]
        products_id_list = await asyncio.gather(*tasks)
    return products_id_list


async def fetch(session, page, semaphore):
    async with semaphore:
        async with session.get(f'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?p={page}/') as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
            elements = soup.find_all(class_='catalog-product ui-button-widget')
            elements = list(map(lambda x: x.get("data-product"), elements))

    return elements
