import telebot
from telebot import types


class Bot:
    __instance = None
    TOKEN = '1187131516:AAFM9NyvopcDLFOEbvDW73K7thN3r7jph3M'

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Bot.__instance is None:
            Bot()
        return Bot.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Bot.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Bot.__instance = self
            self.bot = telebot.TeleBot(Bot.TOKEN)
            self.bot.set_update_listener(listener)
            self.users = {}  # register listener
            self.hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
