import asyncio

from products_id import get_products_id
from request_data import get_request_data


async def main():
    cookies, headers = await get_request_data()
    products_id_list = await get_products_id(cookies, headers)
    print(products_id_list)


if __name__ == "__main__":
    asyncio.run(main())
