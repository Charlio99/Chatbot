import time

from telebot import types
from singletonBot import Bot


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.option = []

        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.location = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):
        self.yes_no_select.add('Si', 'No')
        self.amigos_solo.add('Con amigos', 'Solo')
        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')
        self.location.row(types.KeyboardButton(text='Enviar mi ubicación', request_location=True))


userLikes = UserLikes()
bot = Bot.getInstance().bot


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if user.get_latitude() is None or user.get_longitude() is None:
        bot.send_message(cid, "Para poder ofrecerte resultados el bot necesita saber tu ubicación.\n"
                              "A continuación te aparecerá un botón para enviarla", reply_markup=userLikes.location)
        user.set_step(1)
    else:
        bot.send_message(cid, "Tu ubicación actual es: ")
        bot.send_location(cid, user.get_latitude(), user.get_longitude(), reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "\n¿Quieres cambiarla?", reply_markup=userLikes.yes_no_select)
        user.set_step(2)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 3,
                     content_types=['text'])
def with_or_without_friends(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
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


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 4,
                     content_types=['text'])
def this_or_that(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text
    time.sleep(1.5)
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

    time.sleep(2)


# filter on a specific message
@bot.message_handler(
    func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 0 and message.text.lower() == (
            "recomiendame algo"), content_types=['text'])
def command_text_recommend(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    if user.get_latitude() is None or user.get_longitude() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu ubicación.\n"
                              "Para hacerlo usa el comando /configurar", reply_markup=userLikes.amigos_solo)
    else:
        bot.send_message(cid, "Quieres un plan con más gente o solo?", reply_markup=userLikes.amigos_solo)
        user.set_step(3)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 1,
                     content_types=['location'])
def configure_location(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    time.sleep(1.5)
    user.set_latitude(m.location.latitude)
    user.set_longitude(m.location.longitude)
    bot.send_message(cid, "Ubicación guardada con éxito.")
    user.set_step(0)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 1,
                     content_types=['text'])
def configure_location_text(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    markup = types.ForceReply(selective=False)
    bot.send_message(cid, "Ubicación no válida, intentalo de nuevo.", reply_markup=markup)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEW_POSTAL_CODE)
def new_cp_reply(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if text == 'Si':
        bot.send_message(cid, "A continuación te aparecerá un botón para enviar la ubicación",
                         reply_markup=userLikes.location)
        user.set_step(1)
    elif text == 'No':
        user.set_step(0)
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te ayude /ayuda")


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")
