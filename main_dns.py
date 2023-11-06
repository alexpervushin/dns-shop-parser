from microdata import get_microdata
import asyncio
from prod_data import get_prod_data


cookies = {
    '_csrf': '3b5b377a269c13de8db6fe053835116dee3907d403125c6266ef0f533a5e90e3a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22rEF2yn1xE8Q6OtSRLd9mOC06hL6z7X05%22%3B%7D',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.dns-shop.ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76',
    'X-CSRF-Token': 'DlyfQd_oGMWfwBi3ou7ldWsZ3HpVmytn06Xs2YxB9DR8GdlzpoYpvdr4SYHtmrYnJ33lFxrYG1G76dqjuxnEAQ==',
    'X-Requested-With': 'XMLHttpRequest',
    'content-type': 'application/x-www-form-urlencoded',
    'sec-ch-ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

prod_id = ['96b1191c-6692-11eb-a218-00155d03332b', '5a7b4c6d-0bc3-11ec-a2b0-00155dfc8232', 'fba07f27-6a91-11e7-8fd0-00155d03330d', '975c271b-a778-11e9-a20b-00155df1b805', '4e2d2342-ce28-11e5-bc54-00155d033307', '7fbad683-6ef1-11ed-905e-00155d8ed20b', '8d99fc81-ddcf-11ec-a28c-00155dd2ff41', 'debd0785-ad35-11e6-83a6-00155d03330d', '34addc53-49e6-11e4-8326-005056a4699b', '8c12d3e8-2d96-11ec-8f06-00155d8ed20b', '9a003379-891d-11ea-a20f-00155d03332b', '3bfb3d23-637c-11e6-9e70-001e6728a5a4', '1e0ad304-e08a-4294-a69a-0c0d3b23473b', '5522f160-5e6d-11ee-914d-00155d8ed20b', '246b8ebd-54e1-11e8-9dc5-00155d03330d', 'dffe1d26-6ba0-11e8-9547-00155d03330d', 'c2583706-c212-4e3b-8fc2-8eb8a1c6009f', '1f48fe4d-3928-11e7-939d-00155d03330d']

params = {
    'id': prod_id,
}

result = asyncio.run(get_microdata(prod_id, cookies, headers))
print(result)
# print(get_prod_data(params, cookies, headers))

