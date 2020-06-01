from difflib import SequenceMatcher

from telebot import types

from category import Categories
from singletonBot import Bot

CATEGORY = 5


class Category_Decision:

    def __init__(self):  # Declare the constructor with or without parameters

        self.activity = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        options = []
        index = 0
        for activity in Categories.getInstance().get_activities():
            options.append(activity.name + " " + activity.emoji)
            self.activity.add(options[index])
            index += 1


bot = Bot.getInstance().bot


# filter on a specific message
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(
    message.chat.id).get_step() == CATEGORY and check_similarity_percentage(message.text, "recomiendame algo"),
                     content_types=['text'])
def choose_category(m):
    pass


def check_similarity_percentage(text, option):
    if text is None:
        return False

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False
