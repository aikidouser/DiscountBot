import re
import os
import logging
import json
from ECommHandler import ECommHandler


logger = logging.getLogger(__name__)

# url = urlparse(os.environ.get("REDIS_URL"))
# conc_pool = redis.ConnectionPool(
#     host=url.hostname,
#     port=url.port,
#     username=url.username,
#     password=url.password,
#     decode_responses=True
# )


class CmdHandler:

    def __init__(self, chat_id, keyword=None, url=None):
        
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.url = url
        self.prods = list()
        self.prod_code = str()
        
        # Check if the json/ exists
        try:
            os.mkdir('./user_info')

        except FileExistsError:
            pass

        # dill with url
        if self.url:
            self.url_check = self.get_fixed_type_url()

        # self.redis_conc = redis.Redis(connection_pool=conc_pool)
        # if self.redis_conc.exists(self.chat_id):
        #     prods_list_str = self.redis_conc.get(self.chat_id)
        #     prods_list_str = prods_list_str.replace('\'', '\"')
        #     self.prods = json.loads(prods_list_str)

        # Check if the user file exists
        path = './user_info/' + str(self.chat_id) + '.json'
        try:
            with open(path, 'r') as json_file:
                self.user_data = json.load(json_file)
                self.prods = self.user_data['prods']

        except Exception:
            self.user_data = dict()
            self.user_data['chat_id'] = self.chat_id
            self.user_data['prods'] = list()
            with open(path, 'w') as json_file:
                json.dump(self.user_data, json_file)

    def get_fixed_type_url(self):

        if 'pchome' in self.url and 'prod' in self.url:
            pchome_basic_url = 'https://24h.pchome.com.tw/prod/'
            self.prod_code = re.search(r'\/prod\/(\w*-\w*)', self.url).group(1)
            self.url = pchome_basic_url + self.prod_code

        elif 'momoshop' in self.url and 'goods' in self.url:
            momo_basic_url = 'https://www.momoshop.com.tw/goods/GoodsDetail.jsp?'
            self.prod_code = re.search(r'i_code=\d+', self.url).group(0)
            self.url = momo_basic_url + self.prod_code

        else:
            return False

        return True

    def add_url(self):

        if len(self.prods) >= 10:
            re_msg = '你已加入十個商品囉'
            return re_msg

        for prod in self.prods:
            if self.url == prod["url"]:
                re_msg = '這個網址已經在追蹤列表裡囉'
                return re_msg

        if self.url_check:
            if '24h.pchome' in self.url:
                prod_name, prod_price = ECommHandler(self.url, self.prod_code, 'pchome').pchome()
                ecomm_store = '24hpchome'

            elif 'momoshop' in self.url:
                prod_name, prod_price = ECommHandler(self.url, self.prod_code, 'momoshop').momoshop()
                ecomm_store = 'momoshop'

        else:
            re_msg = '請貼 24pchome 或是 momo 的 商品頁面 喔'
            return re_msg

        if prod_name and prod_price:
            replace_list = ['-', '(', ')', '[', ']', '+', '.', '|', '_', '`', '*']
            for c in replace_list:
                if c in prod_name:
                    prod_name = prod_name.replace(c, '\\' + c)

            self.prods.append({'name': prod_name,
                               'store': ecomm_store,
                               'price': prod_price,
                               'url': self.url})
            self.write_back()
        
            re_msg = f'{prod_name} {prod_price}元 已成功加入囉'
            return re_msg

        elif not prod_name:
            re_msg = '不小心出了一點意外，請稍後再試一次喔'
            return re_msg

        else:
            re_msg = '請貼網址喔'
            return re_msg

    def prods_list(self):
        
        pchome_list = list()
        momoshop_list = list()
        # pchome_msg = ''
        # momoshop_msg = ''

        for prod in self.prods:
            if prod['store'] == '24hpchome':
                pchome_list.append(f'[{prod["name"]}]({prod["url"]})')
            
            elif prod['store'] == 'momoshop':
                momoshop_list.append(f'[{prod["name"]}]({prod["url"]})')

        separator = '\n'
        pchome_msg = separator.join(pchome_list)
        momoshop_msg = separator.join(momoshop_list)

        # for i, link_text in enumerate(pchome_list):
        #     pchome_msg += link_text
        #
        #     if i != len(pchome_list)-1:
        #         pchome_msg += '\n'
        #
        # for i, link_text in enumerate(momoshop_list):
        #     momoshop_msg += link_text
        #
        #     if i != len(momoshop_list)-1:
        #         momoshop_msg += '\n'

        return pchome_msg, momoshop_msg

    def del_by_keyword(self):

        num_del_sum = 0
        self.keyword = self.keyword.lower()
        while True:
            num_del = 0
            for prod in self.prods:
                if self.keyword in prod['name'].lower():
                    self.prods.remove(prod)
                    num_del += 1

            num_del_sum += num_del

            if not num_del:
                break

        if num_del_sum:
            self.write_back()
            re_msg = f'已刪除 {num_del_sum} 項追蹤商品'
        else:
            re_msg = f'追蹤商品中並沒有包含 {self.keyword} 的商品喔'
        return re_msg

    def write_back(self):

        # self.redis_conc.set(self.chat_id, str(self.prods))

        self.user_data['prods'] = self.prods

        path = './user_info/' + str(self.chat_id) + '.json'
        with open(path, 'w') as json_file:
            json.dump(self.user_data, json_file)
