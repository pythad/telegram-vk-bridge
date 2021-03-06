import logging
import re

from requests.exceptions import HTTPError

import vk_api

from telegram.ext import CommandHandler
from telegram.ext import Updater

from utils import get_func_name
from utils import get_env_variable
from utils import COMMAND_PATTERN

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()


class TelegramVkBot:

    def __init__(self, TELEGRAM_TOKEN, VK_USERNAME, VK_PASSWORD, VK_RECIPIENT):
        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        self.VK_USERNAME = VK_USERNAME
        self.VK_PASSWORD = VK_PASSWORD
        self.VK_RECIPIENT = VK_RECIPIENT
        self._set_telegran_api()
        self._set_telegram_handlers()

    def _set_telegran_api(self):
        self.updater = Updater(token=self.TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

    def _get_vk_api(self):
        try:
            vk_session = vk_api.VkApi(self.VK_USERNAME, self.VK_PASSWORD)
            vk_session.auth()
            vk = vk_session.get_api()
            return vk
        except (vk_api.exceptions.VkApiError, HTTPError):
            logger.exception('Exception while handling _get_vk_api')

    def alarm_vk(self, bot, update):
        '''
        Alarms VK chat to visit Telegram in order to see something important
        '''
        func_name = get_func_name()
        username = self._get_update_trigger(bot, update)[2]
        user_str = self._repr_update_trigger(bot, update)
        if username:
            telegram_reply_user_str = '@{}'.format(username)
        else:
            telegram_reply_user_str = user_str
        pattern = re.compile(COMMAND_PATTERN)
        match = pattern.fullmatch(update.message.text)
        # Check if user hasn't passed any args
        args = match.group('args')
        if args:
            telegram_reply = telegram_reply_user_str + \
                ', \'{}\' doesn\'t take any args. Please, use \'send_to_vk\' if you want to send a custom message'.format(func_name)
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)
            return
        message = user_str + \
            ' wants VK PI community to visit Telegram in order to see something important'
        try:
            self._forward_to_vk(message)
        except Exception:  # log it
            logger.exception('Exception while forwarding message to vk')
            telegram_reply = telegram_reply_user_str + \
                ', sorry, something went wrong while sending message to VK'
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)
        else:
            telegram_reply = telegram_reply_user_str + \
                ', message to VK has been successfully sent'
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)

    def send_to_vk(self, bot, update):
        '''
        Forwards a custom message to VK chat
        '''
        username = self._get_update_trigger(bot, update)[2]
        user_str = self._repr_update_trigger(bot, update)
        if username:
            telegram_reply_user_str = '@{}'.format(username)
        else:
            telegram_reply_user_str = user_str
        pattern = re.compile(COMMAND_PATTERN)
        match = pattern.fullmatch(update.message.text)
        message_to_send = match.group('args')
        if not message_to_send:
            telegram_reply = telegram_reply_user_str + \
                ', please, provide a message to forward'
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)
            return
        message = user_str + ' says "{}"'.format(
            message_to_send
        )
        try:
            self._forward_to_vk(message)
        except Exception:
            logger.exception('Exception while forwarding message to vk')
            telegram_reply = telegram_reply_user_str + \
                ', sorry, something went wrong while forwarding your message'
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)
        else:
            telegram_reply = telegram_reply_user_str + \
                ', your message has been forwarded to VK'
            bot.send_message(chat_id=update.message.chat_id,
                             text=telegram_reply)

    def _forward_to_vk(self, message):
        vk = self._get_vk_api()
        recipient = self.VK_RECIPIENT
        vk.messages.send(peer_id=recipient, message=message)

    def _set_telegram_handlers(self):
        alarm_vk_handler = CommandHandler('alarm_vk', self.alarm_vk)
        send_to_vk_handler = CommandHandler(
            'send_to_vk', self.send_to_vk)

        self.dispatcher.add_handler(alarm_vk_handler)
        self.dispatcher.add_handler(send_to_vk_handler)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    def _get_update_trigger(self, bot, update):
        trigger_user = update.message.from_user
        return (trigger_user.first_name,
                trigger_user.last_name,
                trigger_user.username)

    def _repr_update_trigger(self, bot, update):
        first_name, last_name, username = self._get_update_trigger(bot, update)
        message_li = []
        if first_name:
            message_li.append(first_name)
        if last_name:
            message_li.append(last_name)
        message = ' '.join(message_li)
        if username:
            if message:
                message += '(@{})'.format(username)
            else:
                message = '@{}'.format(username)
        return message


if __name__ == '__main__':
    TELEGRAM_TOKEN = get_env_variable('TELEGRAM_TOKEN')
    VK_USERNAME = get_env_variable('VK_USERNAME')
    VK_PASSWORD = get_env_variable('VK_PASSWORD')
    VK_RECIPIENT = get_env_variable('VK_RECIPIENT')
    bot = TelegramVkBot(TELEGRAM_TOKEN, VK_USERNAME, VK_PASSWORD, VK_RECIPIENT)
    bot.run()
