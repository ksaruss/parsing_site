from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Store:
    site: str
    name: str
    rating: float
    price: float
    bonus: float


options = webdriver.ChromeOptions()
options.add_argument('start-maximized')


driver = webdriver.Chrome()

driver.get(
    'https://megamarket.ru/catalog/details/i-pda-huawei-mna-lx9-8-256gb-rococo-pe-100051189354/#?details_block=prices&related_search=p60%20pro')

r = driver.page_source

soup = BeautifulSoup(r, 'lxml')

block = soup.find('div', {'class': 'product-offers product-offers_no-border pdp-prices__offers'})

list_store: list[Store] = []

for i in block.find_all('div', {'class': 'product-offer product-offer_with-payment-method'}):
    name_store = i.find('span', {'class': 'pdp-merchant-rating-block__merchant-name'}).text
    rating_store = float(i.find('span', {'class': 'pdp-merchant-rating-block__rating'}).text)
    price_store = float(i.find('span', {'class': 'product-offer-price__amount'}).text.replace(' ', '').replace('₽', ''))
    bonus_store = float(i.find('span', {'class': 'bonus-amount'}).text.replace(' ', ''))

    # print({'name_store': name_store, 'rating_store': rating_store,
    #        'price_store': price_store, 'discount_store': bonus_store})

    list_store.append(Store(site='megamarket', name=name_store, rating=rating_store,
                            price=price_store, bonus=bonus_store))


def filter_store(price, max_price):
    store_list = []
    for store in list_store:
        if store.price > price[0] or store.price < price[1]:
            if store.price - store.bonus <= max_price:
                store_list.append(store)
    return store_list


print(filter_store((30000, 70000), 60000))
