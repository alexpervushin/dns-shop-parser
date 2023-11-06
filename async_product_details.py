import asyncio
import json

import aiohttp
from bs4 import BeautifulSoup


async def get_product_details(params_list: list, cookies: str, headers: str) -> list:
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        fetch_tasks = [fetch_product_data(session, params) for params in params_list]
        product_details_list = await asyncio.gather(*fetch_tasks)
    return product_details_list


async def fetch_product_data(session, params):
    async with session.post(
            'https://www.dns-shop.ru/catalog/product/get-product-characteristics-actual/',
            params=params,
    ) as response:
        response_text = await response.text()

    html_content = json.loads(response_text)["html"]
    soup = BeautifulSoup(html_content, 'html.parser')

    characteristic_groups = soup.find_all(class_="product-characteristics__group")

    product_data = {}

    for group in characteristic_groups:
        group_data = {}
        specs_in_group = group.find_all(class_="product-characteristics__spec")
        group_title = group.find(class_="product-characteristics__group-title").get_text(strip=True).replace(u'\xa0',
                                                                                                             u' ')
        for spec in specs_in_group:
            spec_title = spec.find(class_="product-characteristics__spec-title").get_text(strip=True).replace(u'\xa0',
                                                                                                              u' ')
            spec_value = spec.find(class_="product-characteristics__spec-value").get_text(strip=True).replace(u'\xa0',
                                                                                                              u' ')
            group_data.update({spec_title: spec_value})
        product_data.update({group_title: group_data})

    return product_data
