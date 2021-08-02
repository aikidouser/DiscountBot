import json
import re
import logging
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException


logger = logging.getLogger(__name__)


class ECommHandler:
    
    def __init__(self, url, prod_code, store=None):

        # run local
        if store == 'momoshop':
            opts = Options()
            opts.headless = True
            self.driver = webdriver.Firefox(firefox_options=opts)
            self.WebWait = WebDriverWait(self.driver, 20)

        # heroku
        # if store == 'momoshop':
        #     chrome_options = webdriver.ChromeOptions()
        #     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #     chrome_options.add_argument("--headless")  # 無頭模式
        #     chrome_options.add_argument("--disable-dev-sh-usage")
        #     chrome_options.add_argument("--no-sandbox")
        #     self.driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        #                                    chrome_options=chrome_options)
        #     self.WebWait = WebDriverWait(self.driver, 20)

        self.url = url
        self.prod_code = prod_code
        self.headers = {'cookie': 'ECC=IHATEIT',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

    def pchome(self):

        prod_name = 'Fail'
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

        logger.info('pchome selenium success')
        return prod_name, int(prod_price)

    def momoshop(self):

        prod_name = 'Fail'
        prod_price = -1

        try:
            self.driver.get(self.url)

        except InvalidArgumentException:
            return None, None

        try:
            prod_name = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='prdnoteArea']/h3")
                    )
                ).text

            prod_price = self.WebWait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//li[@class='special']/span")
                    )
                ).text
            prod_price = prod_price.replace(',', '')
            
        except:
            logger.warning(self.url + ' not found')
            return prod_name, prod_price
        
        self.driver.quit()
        logger.info('momo selenium success')
        return prod_name, int(prod_price)

