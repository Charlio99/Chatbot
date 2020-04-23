import time

import telebot
from telebot import types
import re
from user import User

TOKEN = '1187131516:AAFM9NyvopcDLFOEbvDW73K7thN3r7jph3M'

users = {}
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start': 'Inicia el bot y ajusta tu información',
    'ayuda': 'Información sobre los comandos disponibles'
}

yesNoSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)
yesNoSelect.add('Si', 'No')

amigosSolo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
amigosSolo.add('Con amigos', 'Solo')

genialOtro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
genialOtro.add('¡Genial!', 'Mejor otra cosa')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    user = users.get(cid)
    if user is None:  # if user hasn't used the "/start" command yet:
        users[cid] = User(cid)
        bot.send_message(cid, "¡Hola! Soy Pilus, un bot recomendador de planes")
        command_help(m)
        bot.send_message(cid, "Antes de nada, vamos a configurar tu perfil para perfeccionar mis recomendaciones")
        command_settings(m)
    else:
        bot.send_message(cid, "Ya has iniciado el bot previamente, si necesitas ver los comandos, puedes usar /ayuda")


# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    user = users.get(cid)
    help_text = "Los comandos disponibles son los siguientes: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    help_text += "Si quieres que te recomiende algo simplemente di: _recomiendame algo_"
    bot.send_message(cid, help_text, parse_mode="Markdown")  # send the generated help page


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user = users.get(cid)
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
                         reply_markup=yesNoSelect)
        user.set_step(2)
    print("")


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.get(message.chat.id).get_step() == 1)
def cp_reply(m):
    cid = m.chat.id
    user = users.get(cid)
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
                             "¡Todavía no operamos fuera de Barcelona, pero en breves operaremos en toda España también!")
            user.set_step(0)
        else:
            markup = types.ForceReply(selective=False)
            bot.send_message(cid, "Código postal no válido, por favor, intentelo de nuevo", reply_markup=markup)


@bot.message_handler(func=lambda message: users.get(message.chat.id).get_step() == 2)
def new_cp_reply(m):
    cid = m.chat.id
    user = users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Si':
        bot.send_message(cid, "¿Cuál es tu nuevo código postal?", reply_markup=markup)
        user.set_step(1)
    elif text == 'No':
        user.set_step(3)
        bot.send_message(cid, "¡De acuerdo!", reply_markup=hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


@bot.message_handler(func=lambda message: users.get(message.chat.id).get_step() == 3)
def with_or_without_friends(m):
    cid = m.chat.id
    user = users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Con amigos':
        bot.send_location(cid, 41.41021, 2.137828, reply_markup=hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece este restaurante nuevo de comida Japonesa?\n"
                              "https://goo.gl/maps/NiNRxBpZTB66c9Lt6", reply_markup=genialOtro)
        user.set_step(4)
    elif text == 'Solo':
        photo = open('./tmp/el_hoyo.jpg', 'rb')
        bot.send_photo(cid, photo, reply_markup=hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece esta pelicula de Netflix?\n"
                              "https://www.netflix.com/title/81128579",
                         reply_markup=genialOtro)

        user.set_step(4)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Con amigos\" o \"Solo\"")


@bot.message_handler(func=lambda message: users.get(message.chat.id).get_step() == 4)
def this_or_that(m):
    cid = m.chat.id
    user = users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == '¡Genial!':
        user.set_step(0)
        bot.send_message(cid, "¡Encantado de ayudarte! " + m.from_user.first_name, reply_markup=hideBoard)
    elif text == 'Mejor otra cosa':
        user.set_step(0)
        bot.send_message(cid, "Lo siento " + m.from_user.first_name + ",se me han acabado las recomendaciones, "
                              "pero sigo mejorando para tener más opciones", reply_markup=hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"¡Genial!\" o \"Mejor otra cosa\"")


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("hola"))
def command_text_hi(m):
    bot.send_message(m.chat.id, "¡Hola! Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("ayuda"))
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == ("recomiendame algo"))
def command_text_recommend(m):
    cid = m.chat.id
    user = users.get(cid)
    if user.get_postal_code() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar", reply_markup=amigosSolo)
    else:
        bot.send_message(cid, "Quieres un plan con más gente o solo?", reply_markup=amigosSolo)
    user.set_step(3)


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te ayude /ayuda")


bot.polling()
