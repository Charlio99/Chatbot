import time

from telebot import types
from singletonBot import Bot
from user import User

import re


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters

        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):
        self.yes_no_select.add('Si', 'No')
        self.amigos_solo.add('Con amigos', 'Solo')
        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')


userLikes = UserLikes()
bot = Bot.getInstance().bot


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    if user.get_postal_code() is None:
        # ForceReply: forces a user to reply to a message
        # Takes an optional selective argument (True/False, default False)
        bot.send_message(cid, "¿Cuál es tu código postal?", reply_markup=markup)
        user.set_step(1)
    else:
        bot.send_message(cid, "Tu código postal actual es: " + user.get_postal_code() + "\n¿Quieres cambiarlo?",
                         reply_markup=userLikes.yes_no_select)
        user.set_step(2)
    print("")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 3)
def with_or_without_friends(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Con amigos':
        bot.send_location(cid, 41.41021, 2.137828, reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece este restaurante nuevo de comida Japonesa?\n"
                              "https://goo.gl/maps/NiNRxBpZTB66c9Lt6", reply_markup=userLikes.genial_otro)
        user.set_step(4)
    elif text == 'Solo':
        photo = open('./tmp/el_hoyo.jpg', 'rb')
        bot.send_photo(cid, photo, reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece esta pelicula de Netflix?\n"
                              "https://www.netflix.com/title/81128579",
                         reply_markup=userLikes.genial_otro)

        user.set_step(4)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Con amigos\" o \"Solo\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 4)
def this_or_that(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == '¡Genial!':
        user.set_step(0)
        bot.send_message(cid, "¡Encantado de ayudarte! " + m.from_user.first_name,
                         reply_markup=Bot.getInstance().hideBoard)
    elif text == 'Mejor otra cosa':
        user.set_step(0)
        bot.send_message(cid, "Lo siento " + m.from_user.first_name + ",se me han acabado las recomendaciones, "
                                                                      "pero sigo mejorando para tener más opciones",
                         reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"¡Genial!\" o \"Mejor otra cosa\"")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("recomiendame algo"))
def command_text_recommend(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    if user.get_postal_code() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar", reply_markup=userLikes.amigos_solo)
    else:
        bot.send_message(cid, "Quieres un plan con más gente o solo?", reply_markup=userLikes.amigos_solo)
    user.set_step(3)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 1)
def cp_reply(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if re.match("^08\d{3}$", text, flags=0):
        user.set_postal_code(text)
        bot.send_message(cid, "Código postal guardado con éxito!")
        user.set_step(0)
        what_now(m)
    else:
        if re.match("^\d{5}$", text, flags=0):
            bot.send_message(cid,
                             "¡Todavía no operamos fuera de Barcelona, pero en breves operaremos en toda España "
                             "también!")
            user.set_step(0)
        else:
            markup = types.ForceReply(selective=False)
            bot.send_message(cid, "Código postal no válido, por favor, intentelo de nuevo", reply_markup=markup)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 2)
def new_cp_reply(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Si':
        bot.send_message(cid, "¿Cuál es tu nuevo código postal?", reply_markup=markup)
        user.set_step(1)
    elif text == 'No':
        user.set_step(3)
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te ayude /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("hola"))
def command_text_hi(m):
    bot.send_message(m.chat.id, "¡Hola! Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("ayuda"))
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")
