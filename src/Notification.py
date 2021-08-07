import re
import requests
import threading
import json
import logging
from bs4 import BeautifulSoup
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)


class NotifyThread(threading.Thread):

    def __init__(self, dispatcher, user_data_path):

        threading.Thread.__init__(self)

        self.dispatcher = dispatcher

        with open(user_data_path, 'r') as json_file:
            self.user_data = json.load(json_file)

        self.chat_id = self.user_data["chat_id"]
        self.prods = self.user_data['prods']
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

        # run local
        # opts = Options()
        # opts.headless = True
        # self.driver = webdriver.Firefox(firefox_options=opts)
        # self.WebWait = WebDriverWait(self.driver, 30)


    def run(self) -> None:

        logger.info(threading.currentThread().name + ' start working')

        if_momo = False
        for prod in self.prods:

            new_prod_price = self.get_new_price(prod['url'])
            # if prod['store'] == 'momoshop':
            #     if_momo = True

            if not new_prod_price:
                re_msg = f'[{prod["name"]}]({prod["url"]})無法查到最新價格，麻煩點一下看一下囉'
                context = CallbackContext(self.dispatcher)
                context.bot.send_message(self.chat_id, re_msg, parse_mode='MarkdownV2', disable_notification=True)

            elif new_prod_price < prod['price']:
                prod['price'] = new_prod_price
                context = CallbackContext(self.dispatcher)
                re_msg = f'[{prod["name"]}]({prod["url"]})現在特價{str(prod["price"])}元'
                context.bot.send_message(self.chat_id, re_msg, parse_mode='MarkdownV2')

            elif new_prod_price > prod['price']:
                prod['price'] = new_prod_price

        self.write_back()
        logger.info(threading.currentThread().name + ' finish work')

    def get_new_price(self, url):

        new_prod_price = None

        if '24h.pchome' in url:
            # new_prod_price = self.WebWait.until(
            #     EC.visibility_of_element_located(
            #         (By.XPATH, "//span[@class='price']/span[@id='PriceTotal']")
            #     )
            # ).text

            prod_code = re.search(r'\/prod\/(\w*-\w*)', url).group(1)
            pchome_api = f'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/{prod_code}-000&fields=Id,Name,Price&_callback=jsonp_prod'
            response = requests.get(pchome_api, self.headers).text
            if response:
                prod_info = re.search(r'\{\"Id.*[\"\d]\}\}', response).group(0)
                prod_info = json.loads(prod_info)
                new_prod_price = prod_info['Price']['P']

        elif 'momoshop' in url:
            try:
                response = requests.get(self.url, headers=self.headers)

            except Exception:
                return new_prod_price

            soup = BeautifulSoup(response.text, features='html.parser')
            try:
                new_prod_price = soup.select('td.priceTxtArea b')[0].text

            except Exception:
                new_prod_price = soup.select('td.priceArea b')[0].text
            new_prod_price = int(new_prod_price.replace(',', ''))

            # try:
            #     self.driver.get(url)
            #     new_prod_price = self.WebWait.until(
            #         EC.visibility_of_element_located(
            #             (By.XPATH, "//li[@class='special']//span")
            #         )
            #     ).text
            #     new_prod_price = new_prod_price.replace(',', '')
            #     new_prod_price = int(new_prod_price)
            #
            # except Exception:
            #     logger.warning(f'{str(self.chat_id)} {url} not found')

        return new_prod_price

    def write_back(self):

        # self.redis_conc.set(self.chat_id, str(self.prods))

        path = './user_info/' + str(self.chat_id) + '.json'
        with open(path, 'w') as json_file:
            json.dump(self.user_data, json_file)
