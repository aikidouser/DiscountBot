import os
import json
import logging
import datetime
from Notification import NotifyThread
from telegram.ext import Updater


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING,
                    filename='notf_main.log')
logger = logging.getLogger(__name__)

# url = urlparse(os.environ.get("REDIS_URL"))
# conc_pool = redis.ConnectionPool(
#     host=url.hostname,
#     port=url.port,
#     username=url.username,
#     password=url.password,
#     decode_responses=True
# )


if __name__ == "__main__":

    with open('configure.json', 'r') as json_file:
        data = json.load(json_file)
    TOKEN = data['token']

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # redis_conc = redis.Redis(connection_pool=conc_pool)
    # # print(redis_conc.keys())
    # for chat_id in redis_conc.keys():
    #     NotifyThread(dispatcher, conc_pool, chat_id).start()

    path = './user_info'
    json_files = os.listdir(path)
    for file in json_files:
        user_data_path = os.path.join(path, file)
        NotifyThread(dispatcher, user_data_path).start()
