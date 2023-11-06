import requests
from bs4 import BeautifulSoup
import json


def get_prod_data(params: str, cookies: str, headers: str) -> dict:
    response = requests.post(
        'https://www.dns-shop.ru/catalog/product/get-product-characteristics-actual/',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    html_content = json.loads(response.text)["html"]
    soup = BeautifulSoup(html_content, 'html.parser')

    groups = soup.find_all(class_="product-characteristics__group")

    data = {}

    for group in groups:
        group_data = {}
        spec_in_group = group.find_all(class_="product-characteristics__spec")
        group_title = group.find(class_="product-characteristics__group-title").get_text(strip=True).replace(u'\xa0',
                                                                                                             u' ')
        for spec in spec_in_group:
            spec_title = spec.find(class_="product-characteristics__spec-title").get_text(strip=True).replace(u'\xa0',
                                                                                                              u' ')
            spec_value = spec.find(class_="product-characteristics__spec-value").get_text(strip=True).replace(u'\xa0',
                                                                                                              u' ')
            group_data.update({spec_title: spec_value})
        data.update({group_title: group_data})

    return data
