import asyncio
import aiohttp
from aiohttp.client_exceptions import ContentTypeError, ClientOSError

async def get_microdata(prod_ids: list, cookies: str, headers: str) -> list:
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        tasks = [fetch(session, prod_id) for prod_id in prod_ids]
        microdata_list = await asyncio.gather(*tasks)
    return microdata_list

async def fetch(session, prod_id):
    while True:
        try:
            async with session.post(f'https://www.dns-shop.ru/product/microdata/{prod_id}/') as response:
                response_data = await response.json()
                break

        except ContentTypeError:
            await asyncio.sleep(0.5)
        except ClientOSError:
            await asyncio.sleep(1)

    response_data = response_data["data"]

    aggregate_rating = response_data.get("aggregateRating", {})
    offers = response_data.get("offers", {})

    microdata = {
        "Имя товара": response_data.get("name", ""),
        "Описание товара": response_data.get("description", ""),
        "Ссылка на товар": offers.get("url", ""),
        "Цена": offers.get("price", ""),
        "Рейтинг": aggregate_rating.get("ratingValue", ""),
        "Количество оценок": aggregate_rating.get("reviewCount", ""),
        "URL изображений": response_data.get("image", ""),
        "Имя бренда": response_data.get("brand", "")
    }
    return microdata
