import time
from api import nearby_places
from difflib import SequenceMatcher

from telebot import types

from Graph.node import Response
from Graph.readGraph import Decision
from neo4jDB.Controllers.UserController import UserController
from singletonBot import Bot

START = 0
LOCATION = 1
NEW_LOCATION = 2
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
users = UserController.getInstance()


def settings(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    loc = users.getUserLocationByUserID(cid)

    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    if loc.latitude is None or loc.longitude is None:
        bot.send_message(cid, "Para poder ofrecerte resultados el bot necesita saber tu ubicación.\n"
                              "A continuación te aparecerá un botón para enviarla", reply_markup=userLikes.location)
        users.storeStep(user_id, LOCATION)
    else:
        bot.send_message(cid, "Tu ubicación actual es: ")
        bot.send_location(cid, loc.latitude, loc.longitude,
                          reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "\n¿Quieres cambiarla?", reply_markup=userLikes.yes_no_select)
        users.storeStep(user_id, NEW_LOCATION)


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == START and
                         check_similarity_percentage(message.text, "hola"), content_types=['text'])
def command_text_hi(m):
    time.sleep(1)
    bot.send_message(m.chat.id, "¡Hola!")
    bot.send_animation(m.chat.id, 'https://i.pinimg.com/originals/2d/a5/cc/2da5cccdaa10e142846390f3851feb46.gif',
                       duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None,
                       disable_notification=None, timeout=None)
    bot.send_message(m.chat.id, "Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == START and 0.8 <= SequenceMatcher(
        None, message.text.lower(), "ayuda").ratio(),
    content_types=['text'])
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == START and check_similarity_percentage(message.text,
                                                                                                          "adiós"),
    content_types=['text'])
def command_text_hi(m):
    time.sleep(1)
    bot.send_message(m.chat.id, "Adiós, nos vemos pronto")
    bot.send_animation(m.chat.id, 'https://reygif.com/media/pocahontas-saludo-83409.gif', duration=None, caption=None,
                       reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
                       timeout=None)

    user_id = users.getUserById(m.chat.id)
    users.storeStep(user_id, START)
    users.save_node(user_id, START)


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == START and check_similarity_percentage(message.text,
                                                                                                          "recomiendame algo"),
    content_types=['text'])
def command_text_recommend(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    loc = users.getUserLocationByUserID(cid)

    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    if loc.latitude is None or loc.longitude is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu localización.\n"
                              "Para hacerlo usa el comando /configurar")
    else:
        bot.send_message(cid, users.get_node(cid).question, reply_markup=userLikes.option[users.get_node(cid).num])
        users.storeStep(user_id, NEXT_DECISION)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == NEXT_DECISION,
                     content_types=['text'])
def this_or_that(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(1)

    if chosen_option(text, users.get_node(cid).get_left_name(), users.get_node(cid).get_left_key()):
        show_decision(m, users.get_node(cid).left, user_id)

    elif chosen_option(text, users.get_node(cid).get_right_name(), users.get_node(cid).get_right_key()):
        show_decision(m, users.get_node(cid).right, user_id)
    else:
        bot.send_message(cid, 'Por favor, pulsa solo \"' + users.get_node(cid).get_left_name() + '\" o \"' +
                         users.get_node(cid).get_right_name() + '\"')


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == LOCATION,
                     content_types=['location'])
def configure_location(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    users.save_location(user_id, m.location.latitude, m.location.longitude)

    time.sleep(1)
    bot.send_message(cid, "Ubicación guardada con éxito.")
    what_now(m)
    users.storeStep(user_id, START)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == LOCATION,
                     content_types=['text'])
def configure_location_text(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    markup = types.ForceReply(selective=False)
    bot.send_message(cid, "Ubicación no válida, intentalo de nuevo.", reply_markup=markup)


@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == NEW_LOCATION,
                     content_types=['text'])
def configure_new_location(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1)
    if text == 'Si':
        bot.send_message(cid, "A continuación te aparecerá un botón para enviar la ubicación",
                         reply_markup=userLikes.location)
        users.storeStep(user_id, LOCATION)
    elif text == 'No':
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
        users.storeStep(user_id, NEXT_DECISION)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te sirva /ayuda")


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiendame algo_)", parse_mode="Markdown")


def chosen_option(text, option, key):
    if check_similarity_percentage(text, option):
        return True

    if check_similarity_percentage(text, key):
        return True

    if key == 'si':
        for response in Response.get_instance().get_affirmative():
            if check_similarity_percentage(text, response):
                return True

    elif key == 'no':
        for response in Response.get_instance().get_negative():
            if check_similarity_percentage(text, response):
                return True

    return False


def check_similarity_percentage(text, option):
    if text is None:
        return False

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False


def show_decision(m, decision, user_id):
    cid = m.chat.id
    if decision.end == 1:
        category = decision.category
        if category is not None:
            if category != 'chefbot':
                loc = users.getUserLocationByUserID(cid)
                (lat, lon) = nearby_places(loc.latitude, loc.longitude, category)
                bot.send_location(cid, lat, lon)
            elif category == 'chefbot':
                bot.send_message(cid, "@NoteolvidesBot 👨‍🍳", parse_mode="Markdown")

        bot.send_message(cid, "Me alegra haberte ayudado")
        bot.send_message(cid, "🥰", parse_mode="Markdown")
        users.storeStep(user_id, START)

    elif decision.end == -1:
        bot.send_message(cid, "Lo siento, no se me ocurren más planes")
        bot.send_message(cid, "😧", parse_mode="Markdown")
        users.storeStep(user_id, START)

    else:
        users.save_node(user_id, decision.next_step)

        bot.send_message(cid, users.get_node(cid).question, reply_markup=userLikes.option[users.get_node(cid).num])

        if users.get_node(cid).photo is not None:
            bot.send_photo(cid, users.get_node(cid).photo, reply_markup=userLikes.option[users.get_node(cid).num])

        if users.get_node(cid).gif is not None:
            bot.send_animation(cid, users.get_node(cid).gif, duration=None, caption=None, reply_to_message_id=None,
                               reply_markup=None, parse_mode=None, disable_notification=None, timeout=None)
