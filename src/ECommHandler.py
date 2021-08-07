import json
import re
import logging
import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class ECommHandler:
    
    def __init__(self, url, prod_code=None, store=None):

        # run local
        # if store == 'momoshop':
        #     opts = Options()
        #     opts.headless = True
        #     self.driver = webdriver.Firefox(firefox_options=opts)
        #     self.WebWait = WebDriverWait(self.driver, 20)

        self.url = url
        self.prod_code = prod_code
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

    def pchome(self):

        prod_name = None
        prod_price = -1

        pchome_api = f'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/{self.prod_code}-000&fields=Id,Name,Price&_callback=jsonp_prod'
        response = requests.get(pchome_api, self.headers).text
        if response:
            prod_info = re.search(r'\{\"Id.*[\"\d]\}\}', response).group(0)
            prod_info = json.loads(prod_info)
            prod_name = prod_info['Name']
            prod_price = prod_info['Price']['P']

        # try:
        #     self.driver.get(self.url)
        #
        # except InvalidArgumentException:
        #     return None, None
        #
        # try:
        #     prod_name = self.WebWait.until(
        #         EC.visibility_of_element_located(
        #             (By.XPATH, "//h3[@class='prod_name']/span[@itemprop='name']")
        #             )
        #         ).text
        #
        #     prod_price = self.WebWait.until(
        #         EC.visibility_of_element_located(
        #             (By.XPATH, "//span[@class='price']/span[@id='PriceTotal']")
        #             )
        #         ).text
        #
        # except Exception as e:
        #     e = str(e)
        #     print(self.driver.page_source)
        #     logger.warning(e + ', ' + self.url + ', not found')
        #     return prod_name, prod_price
        #

        return prod_name, int(prod_price)

    def momoshop(self):

        prod_name = None
        prod_price = -1

        try:
            response = requests.get(self.url, headers=self.headers)

        except Exception:
            return prod_name, prod_price

        soup = BeautifulSoup(response.text, features='html.parser')
        prod_name = soup.select('p.fprdTitle')[0].text
        prod_price = soup.select('td.priceTxtArea b')[0].text
        prod_price = prod_price.replace(',', '')

        # try:
        #     self.driver.get(self.url)
        #
        # except InvalidArgumentException:
        #     return None, None
        #
        # try:
        #     prod_name = self.WebWait.until(
        #         EC.visibility_of_element_located(
        #             (By.XPATH, "//div[@class='prdnoteArea jsCartFloat']//h3")
        #             )
        #         ).text
        #
        #     prod_price = self.WebWait.until(
        #         EC.visibility_of_element_located(
        #             (By.XPATH, "//li[@class='special']//span")
        #             )
        #         ).text
        #     prod_price = prod_price.replace(',', '')
        #
        # except:
        #     logger.warning(self.url + ' not found')
        #     self.driver.quit()
        #     return prod_name, prod_price
        #
        # self.driver.quit()

        return prod_name, int(prod_price)
