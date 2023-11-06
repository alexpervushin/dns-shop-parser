from playwright.sync_api import sync_playwright
products_id = []

url = "https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/"

def get_products_id(url):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(url + "?p=1")
        page.wait_for_selector('.catalog-product.ui-button-widget')
        last_pos = page.query_selector('.pagination-widget__page-link.pagination-widget__page-link_last').get_attribute("href").split("p=")[-1]
        elements = page.query_selector_all('.catalog-product.ui-button-widget')
        elements = list(map(lambda x: x.get_attribute('data-product'), elements))
        products_id.extend(elements)

        if int(last_pos) > 1:
            for i in range(2, int(last_pos)+1):
                page = browser.new_page()
                page.goto(url + "?p=" + str(i))
                elements = page.query_selector_all('.catalog-product.ui-button-widget')
                elements = list(map(lambda x: x.get_attribute('data-product'), elements))
                products_id.extend(elements)

        browser.close()

    return products_id

data = get_products_id(url)

