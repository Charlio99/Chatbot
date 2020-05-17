import time

from telebot import types

from singletonBot import Bot

import re

START = 0
POSTAL_CODE = 1
NEW_POSTAL_CODE = 2
ALONE_FRIENDS = 3
END = 4
OUTSIDE_HOME = 5
RELAX = 6
READ = 7


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.outside_inside = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.house_relax = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.sure_inside = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.read = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):
        self.yes_no_select.add('Si', 'No')
        self.amigos_solo.add('Con amigos', 'Solo')
        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')
        self.outside_inside.add('Salir de casa', 'Estoy vago, mejor en casa')
        self.house_relax.add('Me apetece relajarme', 'Si me relajo me duermo')
        self.sure_inside.add('Que si pesado', 'Bueno... ¿Qué me propones hacer?')
        self.read.add('Buena idea, me voy a leer', 'No es lo que más me apetece')


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
        user_id.set_step(ALONE_FRIENDS)
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == ALONE_FRIENDS)
def with_or_without_friends(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Con amigos':
        bot.send_location(cid, 41.41021, 2.137828, reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece este restaurante nuevo de comida Japonesa?\n"
                              "https://goo.gl/maps/NiNRxBpZTB66c9Lt6", reply_markup=userLikes.genial_otro)
        user_id.set_step(END)
    elif text == 'Solo':

        bot.send_message(cid, "¿Te apetece salir de casa?\n", reply_markup=userLikes.outside_inside)
        user_id.set_step(OUTSIDE_HOME)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Con amigos\" o \"Solo\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == END)
def this_or_that(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == '¡Genial!':
        user_id.set_step(START)
        bot.send_message(cid, "¡Encantado de ayudarte! " + m.from_user.first_name,
                         reply_markup=Bot.getInstance().hideBoard)
    elif text == 'Mejor otra cosa':
        if user_id.lastStep == RELAX:
            user_id.set_step(READ)
            bot.send_message(cid, "Mucha gente encuentra la lectura relajante",
                             reply_markup=userLikes.read)
        else:
            user_id.set_step(START)
            bot.send_message(cid, "Lo siento " + m.from_user.first_name + ",se me han acabado las recomendaciones, "
                                                                          "pero sigo mejorando para tener más opciones",
                             reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"¡Genial!\" o \"Mejor otra cosa\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == OUTSIDE_HOME)
def inside_outside(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Estoy vago, mejor en casa':
        bot.send_message(cid, "Así que en casa eee..... ¿Te apetece relajarte?\n", reply_markup=userLikes.house_relax)
        user_id.set_step(RELAX)

    elif text == 'Salir de casa ':
        bot.send_message(cid, "¿Te apetece salir de casa?\n", reply_markup=userLikes.outside_inside)
        user_id.set_step(END)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Salir de casa\" o \"Estoy vago, mejor en casa\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == RELAX)
def inside_outside(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Me apetece relajarme':
        bot.send_message(cid, "¿Quieres que busque alguna película?\n", reply_markup=userLikes.genial_otro)
        user_id.set_step(END)
    elif text == 'Si me relajo me duermo':

        bot.send_message(cid, "Hay muchas actividades divertidas para hacer en casa... ¿Has probado de cocinar?\n",
                         reply_markup=userLikes.genial_otro)
        user_id.set_step(END)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Me apetece relajarme\" o \"Si me relajo me duermo\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == READ)
def inside_outside(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Buena idea, me voy a leer':
        bot.send_message(cid, "Me alegra haberte ayudado" + m.from_user.first_name + "\n",
                         reply_markup=userLikes.genial_otro)
        user_id.set_step(START)
    elif text == 'No es lo que más me apetece':
        bot.send_message(cid, "Siempre puedes cocinar\n", reply_markup=userLikes.genial_otro)
        user_id.set_step(START)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Buena idea, me voy a leer\" o \"No es lo que más me apetece\"")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "recomiendame algo")
def command_text_recommend(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    if user_id.get_postal_code() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar", reply_markup=userLikes.amigos_solo)
    else:
        bot.send_message(cid, "Quieres un plan con más gente o solo?", reply_markup=userLikes.amigos_solo)
    user_id.set_step(ALONE_FRIENDS)


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
