import time
from difflib import SequenceMatcher

from telebot import types

from Graph.node import Response
from Graph.readGraph import Decision
from singletonBot import Bot


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

        self.location = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):

        self.yes_no_select.add('Si', 'No')
        for node_graph in list(Decision.getInstance().graph.nodes):
            node = Decision.getInstance().graph.nodes[node_graph]['node']
            self.option[node_graph].add(node.get_left_name(), node.get_right_name())
        self.location.row(types.KeyboardButton(text='Enviar mi ubicación', request_location=True))


userLikes = UserLikes()
bot = Bot.getInstance().bot


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if user.get_latitude() is None or user.get_longitude() is None:
        bot.send_message(cid, "Para poder ofrecerte resultados el bot necesita saber tu ubicación.\n"
                              "A continuación te aparecerá un botón para enviarla", reply_markup=userLikes.location)
        user_id.set_step(POSTAL_CODE)
    else:
        bot.send_message(cid, "Tu ubicación actual es: ")
        bot.send_location(cid, user.get_latitude(), user.get_longitude(), reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "\n¿Quieres cambiarla?", reply_markup=userLikes.yes_no_select)
        user_id.set_step(NEW_POSTAL_CODE)


<<<<<<<
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
=======
# filter on a specific message
@bot.message_handler(func=lambda message: check_similarity_percentage(message.text, "hola"))
def command_text_hi(m):
    time.sleep(2)
    bot.send_message(m.chat.id, "¡Hola!")
    bot.send_animation(m.chat.id, 'https://i.pinimg.com/originals/2d/a5/cc/2da5cccdaa10e142846390f3851feb46.gif',
                       duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None,
                       disable_notification=None, timeout=None)
    bot.send_message(m.chat.id, "Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: 0.8 <= SequenceMatcher(None, message.text.lower(), "ayuda").ratio())
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: check_similarity_percentage(message.text, "adiós"))
def command_text_hi(m):
    time.sleep(2)
    bot.send_message(m.chat.id, "Adiós, nos vemos pronto")
>>>>>>>

<<<<<<<
        user.set_step(4)
=======
    bot.send_animation(m.chat.id, 'https://reygif.com/media/pocahontas-saludo-83409.gif',duration=None, caption=None,
                       reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
                       timeout=None)

    user_id = Bot.getInstance().users.get(m.chat.id)
    user_id.set_step(START)
    user_id.set_node(START)


# filter on a specific message
@bot.message_handler(
    func=lambda message: check_similarity_percentage(message.text, "recomiendame algo"))
def command_text_recommend(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    if user_id.get_postal_code() is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar")
    else:
        bot.send_message(cid, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])
        user_id.set_step(NEXT_DECISION)
>>>>>>>


<<<<<<<
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 4,
                     content_types=['text'])
def this_or_that(m):
=======
# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEXT_DECISION)
def cp_reply(m):
>>>>>>>
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text
<<<<<<<
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
=======

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
>>>>>>>

<<<<<<<
    time.sleep(2)
=======
    if chosenOption(text, user_id.get_node().get_left_name(), user_id.get_node().get_left_key()):
>>>>>>>

<<<<<<<

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
=======
        showDecision(m, user_id.get_node().left, user_id)

    elif chosenOption(text, user_id.get_node().get_right_name(), user_id.get_node().get_right_key()):

        showDecision(m, user_id.get_node().right, user_id)

>>>>>>>
    else:
<<<<<<<
        bot.send_message(cid, "Quieres un plan con más gente o solo?", reply_markup=userLikes.amigos_solo)
        user.set_step(3)
=======
        bot.send_message(cid, 'Por favor, pulsa solo \"' + user_id.get_node().get_left_name() + '\" o \"' +
                         user_id.get_node().get_right_name() + '\"')
>>>>>>>


# if the user has issued the "/configure" command, process the answer
<<<<<<<
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 1,
                     content_types=['location'])
def configure_location(m):
=======
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == POSTAL_CODE)
def cp_reply(m):
>>>>>>>
    cid = m.chat.id
<<<<<<<
    user = Bot.getInstance().users.get(cid)
    time.sleep(1.5)
    user.set_latitude(m.location.latitude)
    user.set_longitude(m.location.longitude)
    bot.send_message(cid, "Ubicación guardada con éxito.")
    user.set_step(0)
=======
    user_id = Bot.getInstance().users.get(cid)
    text = m.text
>>>>>>>


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 1,
                     content_types=['text'])
def configure_location_text(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
<<<<<<<
    time.sleep(1.5)
    markup = types.ForceReply(selective=False)
    bot.send_message(cid, "Ubicación no válida, intentalo de nuevo.", reply_markup=markup)
=======
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
>>>>>>>


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEW_POSTAL_CODE)
def new_cp_reply(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if text == 'Si':
<<<<<<<
        bot.send_message(cid, "A continuación te aparecerá un botón para enviar la ubicación",
                         reply_markup=userLikes.location)
        user.set_step(1)
=======
        bot.send_message(cid, "¿Cuál es tu nuevo código postal?", reply_markup=markup)
        user_id.set_step(POSTAL_CODE)
>>>>>>>
    elif text == 'No':
<<<<<<<
        user.set_step(0)
=======
        user_id.set_step(NEXT_DECISION)
>>>>>>>
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te ayude /ayuda")


<<<<<<<
def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")
=======
def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")


def chosenOption(text, option, key):

    if check_similarity_percentage(text, option):
        return True

    if check_similarity_percentage(text, key):
        return True
>>>>>>>

    if key == 'si':

        for response in Response.getInstance().get_affirmative():
            if check_similarity_percentage(text, response):
                return True

    elif key == 'no':

        for response in Response.getInstance().get_negative():
            if check_similarity_percentage(text, response):
                return True

    return False


def check_similarity_percentage(text, option):

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False


def showDecision(m, decision, user_id):
    if decision.end == 1:
        bot.send_message(m.chat.id, "Me alegra haberte ayudado", parse_mode="Markdown")
        bot.send_message(m.chat.id, "🥰", parse_mode="Markdown")
        user_id.set_step(START)

    elif decision.end == -1:
        bot.send_message(m.chat.id, "Lo siento, no se me ocurre mas planes, yo de ti me iría a dormir",
                         parse_mode="Markdown")
        bot.send_message(m.chat.id, "😧", parse_mode="Markdown")
        user_id.set_step(START)

    else:
        user_id.set_node(decision.next_step)

        bot.send_message(m.chat.id, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])

        if user_id.get_node().photo is not None:
            bot.send_photo(m.chat.id, user_id.get_node().photo, reply_markup=userLikes.option[user_id.get_node().num])

        if user_id.get_node().gif is not None:
            bot.send_animation(m.chat.id, user_id.get_node().gif, duration=None, caption=None, reply_to_message_id=None,
                               reply_markup=None, parse_mode=None, disable_notification=None, timeout=None)
