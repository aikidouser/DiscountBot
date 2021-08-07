import os
import time
import logging
import json
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from MsgReplyer import start_cmd, help_cmd, add_cmd, del_cmd, list_cmd, notf_cmd, exp_msg, error_callback


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.WARNING,
                    filename='bot_main.log')
logger = logging.getLogger(__name__)


if __name__ == '__main__':
    
    with open('configure.json', 'r') as json_file:
        configure = json.load(json_file)
    TOKEN = configure['token']
    # PORT = int(os.environ.get('PORT', '5000'))
    
    updater = Updater(TOKEN, workers=100)
    dispatcher = updater.dispatcher
    
    # ignore edit
    dispatcher.add_handler(MessageHandler(Filters.update.edited_message, exp_msg))
    
    # Command
    dispatcher.add_handler(CommandHandler('start', start_cmd))
    dispatcher.add_handler(CommandHandler('help', help_cmd))
    # dispatcher.add_handler(CommandHandler('add', add_cmd))
    dispatcher.add_handler(CommandHandler('del', del_cmd))
    dispatcher.add_handler(CommandHandler('list', list_cmd))
    dispatcher.add_handler(CommandHandler('notf', notf_cmd))

    dispatcher.add_handler(MessageHandler(Filters.text
                                          & (Filters.entity('url'))
                                          & ~Filters.command, add_cmd))

    dispatcher.add_handler(MessageHandler(~Filters.command & ~Filters.text, exp_msg))
    dispatcher.add_handler(MessageHandler(Filters.text, exp_msg))
    dispatcher.add_error_handler(error_callback)

    # local
    updater.start_polling()

    # heroku
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=PORT,
    #                       url_path=TOKEN,
    #                       webhook_url="https://dc-notf-bot.herokuapp.com/" + TOKEN)

    logger.info('Listening')

    updater.idle()
