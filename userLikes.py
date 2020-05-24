import time

from telebot import types

from Graph.readGraph import Decision
from singletonBot import Bot

import re

START = 0
POSTAL_CODE = 1
NEW_POSTAL_CODE = 2
ALONE_FRIENDS = 3
NEXT_DECISION = 4


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.option = []

        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        for aux in list(Decision.getInstance().graph.nodes):
            self.option.insert(aux, types.ReplyKeyboardMarkup(one_time_keyboard=True))

        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):

        self.yes_no_select.add('Si', 'No')
        for node_graph in list(Decision.getInstance().graph.nodes):
            node = Decision.getInstance().graph.nodes[node_graph]['node']
            self.option[node_graph].add(node.get_left_name(), node.get_right_name())


userLikes = UserLikes()
bot = Bot.getInstance().bot


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    if user_id.get_postal_code() is None:
        # ForceReply: forces a user to reply to a message
        # Takes an optional selective argument (True/False, default False)
        bot.send_message(cid, "¿Cuál es tu código postal?", reply_markup=markup)
        user_id.set_step(POSTAL_CODE)
    else:
        bot.send_message(cid, "Tu código postal actual es: " + user_id.get_postal_code() + "\n¿Quieres cambiarlo?",
                         reply_markup=userLikes.yes_no_select)
        user_id.set_step(NEW_POSTAL_CODE)
    print("")


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEXT_DECISION)
def cp_reply(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)

    if text == user_id.get_node().get_left_name() or user_id.get_node().get_left_key().lower() in text.lower():

        showDecision(m, user_id.get_node().left, user_id)

    elif text == user_id.get_node().get_right_name() or user_id.get_node().get_right_key().lower() in text.lower():

        showDecision(m, user_id.get_node().right, user_id)

    else:
        bot.send_message(cid, 'Por favor, pulsa solo \"' + user_id.get_node().get_left_name() + '\" o \"' +
                         user_id.get_node().get_right_name() + '\"')


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == POSTAL_CODE)
def cp_reply(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if re.match("^08\d{3}$", text, flags=0):
        user_id.set_postal_code(text)
        bot.send_message(cid, "Código postal guardado con éxito!")
        user_id.set_step(START)
        what_now(m)
    else:
        if re.match("^\d{5}$", text, flags=0):
            bot.send_message(cid,
                             "¡Todavía no operamos fuera de Barcelona, pero en breves operaremos en toda España "
                             "también!")
            user_id.set_step(START)
        else:
            markup = types.ForceReply(selective=False)
            bot.send_message(cid, "Código postal no válido, por favor, intentelo de nuevo", reply_markup=markup)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEW_POSTAL_CODE)
def new_cp_reply(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Si':
        bot.send_message(cid, "¿Cuál es tu nuevo código postal?", reply_markup=markup)
        user_id.set_step(POSTAL_CODE)
    elif text == 'No':
        user_id.set_step(NEXT_DECISION)
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "recomiendame algo")
def command_text_recommend(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    if user_id.get_postal_code() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar")
    else:
        bot.send_message(cid, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])
        user_id.set_step(NEXT_DECISION)


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te ayude /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "hola")
def command_text_hi(m):
    bot.send_message(m.chat.id, "¡Hola! Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "ayuda")
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")


def showDecision(m, decision, user_id):
    if decision.end == 1:
        bot.send_message(m.chat.id, "Me alegra haberte ayudado", parse_mode="Markdown")
        user_id.set_step(START)

    elif decision.end == -1:
        bot.send_message(m.chat.id, "Lo siento, no se me ocurre mas planes, yo de ti me iría a dormir",
                         parse_mode="Markdown")
        bot.send_message(m.chat.id, "🥺", parse_mode="Markdown")
        user_id.set_step(START)

    else:
        user_id.set_node(decision.next_step)

        bot.send_message(m.chat.id, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])

        if decision.photo is not None:
            bot.send_photo(m.chat.id, decision.photo, reply_markup=Bot.getInstance().hideBoard)
