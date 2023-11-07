import asyncio
import logging

import aiohttp
from aiohttp.client_exceptions import ContentTypeError, ClientOSError

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("debug.log"),
                              logging.StreamHandler()])


async def get_microdata(prod_ids: list, cookies: str, headers: str) -> list:
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        semaphore = asyncio.Semaphore(10)
        tasks = [fetch(session, prod_id, semaphore) for prod_id in prod_ids]
        microdata_list = await asyncio.gather(*tasks)
    return microdata_list


async def fetch(session, prod_id, semaphore):
    async with semaphore:
        while True:
            try:
                logging.info(f"Отправка запроса для продукта {prod_id}")
                async with session.get(f'https://www.dns-shop.ru/product/microdata/{prod_id}/') as response:
                    logging.info(f"Получен ответ для продукта {prod_id}. Код ответа: {response.status}")
                    response_text = await response.text()
                    logging.info(f"Текст ответа: {response_text}")
                    response_data = await response.json()

                    logging.info(f"Успешно получены данные для продукта {prod_id}")

                    data = response_data.get("data", {})
                    offers = data.get("offers", {})
                    brand = data.get("brand", {})

                    microdata = {
                        "Имя товара": data.get("name", ""),
                        "Описание товара": data.get("description", ""),
                        "Ссылка на товар": offers.get("url", ""),
                        "Цена": offers.get("price", ""),
                        "Рейтинг": "",  # Рейтинг отсутствует в ответе сервера
                        "Количество оценок": "",  # Количество оценок отсутствует в ответе сервера
                        "URL изображений": ", ".join(data.get("image", [])),
                        "Имя бренда": brand.get("name", "")
                    }
                    break

            except ContentTypeError:
                logging.error(f"ContentTypeError для продукта {prod_id}. Повторная попытка через 0.5 секунды.")
                await asyncio.sleep(0.5)
            except ClientOSError:
                logging.error(f"ClientOSError для продукта {prod_id}. Повторная попытка через 1 секунду.")
                await asyncio.sleep(1)
    logging.info(f"Возвращаемые данные для продукта {prod_id}: {microdata}")
    return microdata
