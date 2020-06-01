import time
from difflib import SequenceMatcher

from telebot import types

from category.category import Categories
from neo4jDB.Controllers.PlacesController import PlacesController
from neo4jDB.Controllers.UserController import UserController
from singletonBot import Bot

CATEGORY = 6
NEXT_DECISION = 4
LAST_RECOMMENDATION = 8
START = 0

class Category_Decision:
    __instance = None

    @staticmethod
    def getInstance():
        if Category_Decision.__instance is None:
            Category_Decision()
        return Category_Decision.__instance

    def __init__(self):  # Declare the constructor with or without parameters
        Category_Decision.__instance = self
        activities = Categories.getInstance().get_activities().copy()
        self.activity = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.option = []

        while len(activities) > 0:
            a1 = activities.pop(0)
            if len(activities) == 0:
                self.activity.add(a1.name + " " + a1.emoji)
                break
            a2 = activities.pop(0)
            self.activity.add(a1.name + " " + a1.emoji, a2.name + " " + a2.emoji)

    def set_option(self, option):
        self.option = option
        pass

    def get_option(self):
        return self.option


bot = Bot.getInstance().bot
category_decision = Category_Decision.getInstance()
users = UserController.getInstance()


@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == CATEGORY,
                     content_types=['text'])
def evaluate_category(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    correct = False

    for category in Categories.getInstance().get_activities():
        if check_similarity_percentage(m.text, category.name):
            user_id.node = category.node
            correct = True
            users.storeStep(user_id, NEXT_DECISION)
            #show_last_recommendations(category.name, m)
            bot.send_message(cid, users.get_node(cid).question, reply_markup=category_decision.get_option()[category.node])
            break

    if correct is False:
        bot.send_message(m.chat.id, "Escoje entre las categorías que te ofrezco",
                         reply_markup=category_decision.activity)


def choose_category(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)

    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    bot.send_message(m.chat.id, "¿Cuál de estas categorias te atrae más?", reply_markup=category_decision.activity)
    users.storeStep(user_id, CATEGORY)


def check_similarity_percentage(text, option):
    if text is None:
        return False

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False


def show_last_recommendations(category, m):

    category_name = Categories.getInstance().get_name_category(category)
    if category_name is None:
        return

    recommendation_array = PlacesController.getInstance().recomendation(category_name, m.chat.id)

    if len(recommendation_array) <= 0:
        return 0

    bot.send_message(m.chat.id, "Las últimas veces fuiste a los siguientes sitios:", parse_mode="Markdown")

    options = ['Ninguno']

    for recommendation in recommendation_array:
        pass
        #bot.send_message(m.chat.id, recommendation[0].placeName + "que está en la dirección:\n _" + address + "_", parse_mode="Markdown")
        options.append(recommendation[0].placeName)
        #last_recommendations.append(Recommendation(name, ))

    #name, latitude, longitude, address, category, cat, user_id

    category_decision.recommendation.add(options)

    bot.send_message(m.chat.id, "¿Te gusta volver a alguno de estos sitios? 👍 😉",
                     reply_markup=category_decision.recommendation, parse_mode="Markdown")
    #user_id.set_step(LAST_RECOMMENDATION)


