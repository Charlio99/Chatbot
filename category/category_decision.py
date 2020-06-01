import time
from difflib import SequenceMatcher

from telebot import types

from category.category import Categories
from singletonBot import Bot

CATEGORY = 6
NEXT_DECISION = 4


class Category_Decision:
    __instance = None

    @staticmethod
    def getInstance():
        if Category_Decision.__instance is None:
            Category_Decision()
        return Category_Decision.__instance

    def __init__(self):  # Declare the constructor with or without parameters

        Category_Decision.__instance = self

        self.activity = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        index = 0
        self.option = []

        for activity in Categories.getInstance().get_activities():
            self.activity.add(activity.name + " " + activity.emoji)
            index += 1

    def set_option(self, option):
        self.option = option
        pass

    def get_option(self):
        return self.option


bot = Bot.getInstance().bot
category_decision = Category_Decision.getInstance()


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == CATEGORY,
                     content_types=['text'])
def evaluate_category(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    correct = False

    for category in Categories.getInstance().get_activities():
        if check_similarity_percentage(m.text, category.name):
            user_id.set_node(category.node)
            correct = True
            user_id.set_step(NEXT_DECISION)
            bot.send_message(cid, user_id.get_node().question, reply_markup=category_decision.get_option()[category.node])
            break

    if correct is False:
        bot.send_message(m.chat.id, "Escoje entre las categorías que te ofrezco",
                         reply_markup=category_decision.activity)


def choose_category(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)

    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)

    bot.send_message(m.chat.id, "¿Cuál de estas categorias te atrae más?", reply_markup=category_decision.activity)
    user_id.set_step(CATEGORY)


def check_similarity_percentage(text, option):
    if text is None:
        return False

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False
