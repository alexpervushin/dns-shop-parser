from playwright.sync_api import sync_playwright


def get_product_ids_from_url(url: str) -> list:
    product_ids = []
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        first_page = browser.new_page()
        first_page.goto(url + "?p=1")
        first_page.wait_for_selector('.catalog-product.ui-button-widget')
        total_pages = int(
            first_page.query_selector('.pagination-widget__page-link.pagination-widget__page-link_last').get_attribute(
                "href").split("p=")[-1])
        first_page.close()

        for page_number in range(1, total_pages + 1):
            current_page = browser.new_page()
            current_page.goto(url + "?p=" + str(page_number))
            current_page.wait_for_selector('.catalog-product.ui-button-widget')
            product_elements = current_page.query_selector_all('.catalog-product.ui-button-widget')
            product_ids_on_page = list(map(lambda x: x.get_attribute('data-product'), product_elements))
            product_ids.extend(product_ids_on_page)
            current_page.close()

        browser.close()

    return product_ids
