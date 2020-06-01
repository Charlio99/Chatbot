import time
from itertools import count

from api import nearby_places
from difflib import SequenceMatcher

from telebot import types

from Graph.node import Response
from Graph.readGraph import Decision
from category_decision import Category_Decision, check_similarity_percentage
from singletonBot import Bot

START = 0
LOCATION = 1
NEW_LOCATION = 2
ALONE_FRIENDS = 3
NEXT_DECISION = 4
RECOMMENDATIONS = 5
cat = ''
counter = 0


class UserLikes:

    __instance = None

    @staticmethod
    def getInstance():
        if UserLikes.__instance is None:
            UserLikes()
        return UserLikes.__instance

    def __init__(self):  # Declare the constructor with or without parameters

        UserLikes.__instance = self

        self.option = []

        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.recommendation_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)

        for aux in list(Decision.getInstance().graph.nodes):
            self.option.insert(aux, types.ReplyKeyboardMarkup(one_time_keyboard=True))

        self.category_decision = Category_Decision()
        self.location = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()
        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):

        self.yes_no_select.add('Si', 'No')
        self.recommendation_select.add('Me gusta', 'Prueba con otro', 'Cancelar')
        for node_graph in list(Decision.getInstance().graph.nodes):
            node = Decision.getInstance().graph.nodes[node_graph]['node']
            self.option[node_graph].add(node.get_left_name(), node.get_right_name())
        self.location.row(types.KeyboardButton(text='Enviar mi ubicación', request_location=True))


userLikes = UserLikes.getInstance()
bot = Bot.getInstance().bot


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if user_id.get_latitude() is None or user_id.get_longitude() is None:
        bot.send_message(cid, "Para poder ofrecerte resultados el bot necesita saber tu ubicación.\n"
                              "A continuación te aparecerá un botón para enviarla", reply_markup=userLikes.location)
        user_id.set_step(LOCATION)
    else:
        bot.send_message(cid, "Tu ubicación actual es: ")
        bot.send_location(cid, user_id.get_latitude(), user_id.get_longitude(),
                          reply_markup=Bot.getInstance().hideBoard)
        bot.send_message(cid, "\n¿Quieres cambiarla?", reply_markup=userLikes.yes_no_select)
        user_id.set_step(NEW_LOCATION)


# filter on a specific message
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(
    message.chat.id).get_step() == START and check_similarity_percentage(message.text, "hola"), content_types=['text'])
def command_text_hi(m):
    time.sleep(2)
    bot.send_message(m.chat.id, "¡Hola!")
    bot.send_animation(m.chat.id, 'https://i.pinimg.com/originals/2d/a5/cc/2da5cccdaa10e142846390f3851feb46.gif',
                       duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None,
                       disable_notification=None, timeout=None)
    bot.send_message(m.chat.id, "Si necesitas ayuda puedes usar /ayuda para ver la página de ayuda")


# filter on a specific message
@bot.message_handler(
    func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == START and 0.8 <= SequenceMatcher(
        None, message.text.lower(), "ayuda").ratio(),
    content_types=['text'])
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == START and
                                          (check_similarity_percentage(message.text, "adiós") or
                                           check_similarity_percentage(message.text, "cancelar")),
                     content_types=['text'])
def command_text_bye(m):
    time.sleep(2)
    bot.send_message(m.chat.id, "Adiós, nos vemos pronto")
    bot.send_animation(m.chat.id, 'https://reygif.com/media/pocahontas-saludo-83409.gif', duration=None, caption=None,
                       reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
                       timeout=None)

    user_id = Bot.getInstance().users.get(m.chat.id)
    user_id.set_step(START)
    user_id.set_node(START)


# filter on a specific message
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(
    message.chat.id).get_step() == START and check_similarity_percentage(message.text, "recomiendame algo"),
                     content_types=['text'])
def command_text_recommend(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if user_id.get_longitude is None or user_id.get_latitude is None:
        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar")
    else:
        bot.send_message(cid, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])
        user_id.set_step(NEXT_DECISION)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEXT_DECISION,
                     content_types=['text'])
def this_or_that(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)

    if chosen_option(text, user_id.get_node().get_left_name(), user_id.get_node().get_left_key()):
        show_decision(m, user_id.get_node().left, user_id)

    elif chosen_option(text, user_id.get_node().get_right_name(), user_id.get_node().get_right_key()):
        show_decision(m, user_id.get_node().right, user_id)
    else:
        bot.send_message(cid, 'Por favor, pulsa solo \"' + user_id.get_node().get_left_name() + '\" o \"' +
                         user_id.get_node().get_right_name() + '\"')


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == LOCATION,
                     content_types=['location'])
def configure_location(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    time.sleep(1.5)
    user.set_latitude(m.location.latitude)
    user.set_longitude(m.location.longitude)
    bot.send_message(cid, "Ubicación guardada con éxito.")
    user.set_step(0)
    what_now(m)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == LOCATION,
                     content_types=['text'])
def configure_location_text(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    markup = types.ForceReply(selective=False)
    bot.send_message(cid, "Ubicación no válida, intentalo de nuevo.", reply_markup=markup)


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == NEW_LOCATION,
                     content_types=['text'])
def configure_new_location(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)
    if text == 'Si':
        bot.send_message(cid, "A continuación te aparecerá un botón para enviar la ubicación",
                         reply_markup=userLikes.location)
        user_id.set_step(LOCATION)
    elif text == 'No':
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
        user_id.set_step(NEXT_DECISION)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == RECOMMENDATIONS,
                     content_types=['text'])
def recommendations_yes_or_no(m):
    cid = m.chat.id
    user_id = Bot.getInstance().users.get(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(1.5)

    if text == 'Me gusta':
        end_message(m, user_id)
    elif text == 'Prueba con otro':
        bot.send_message(cid, "Vamos a ver...", reply_markup=Bot.getInstance().hideBoard)
        bot.send_chat_action(cid, 'typing')
        time.sleep(1)
        next_recommendation(m, user_id)
        user_id.set_step(RECOMMENDATIONS)
    elif text == 'Cancelar':
        command_text_bye(m)
    else:
        bot.send_message(cid, "Por favor, utiliza solo los botones")


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


def show_decision(m, decision, user_id):
    if decision.end == 1:
        category = decision.category
        if category is not None:
            if category == 'chefbot':
                bot.send_message(m.chat.id, "@NoteolvidesBot 👨‍🍳", parse_mode="Markdown",
                                 reply_markup=Bot.getInstance().hideBoard)
                time.sleep(1)
                end_message(m, user_id)
            elif category == 'netflix':
                bot.send_message(m.chat.id, "Aquí puedes ver los últimos lanzamientos de Netflix:\n"
                                            "_https://www.netflix.com/browse/new-releases_", parse_mode="Markdown",
                                 reply_markup=Bot.getInstance().hideBoard)
                end_message(m, user_id)
            else:
                global cat
                cat = category
                next_recommendation(m, user_id)

    elif decision.end == -1:
        bot.send_message(m.chat.id, "Lo siento, no se me ocurren más planes")
        bot.send_message(m.chat.id, "😧", parse_mode="Markdown", reply_markup=Bot.getInstance().hideBoard)
        user_id.set_step(START)

    else:
        user_id.set_node(decision.next_step)

        if user_id.get_node().photo is not None:
            bot.send_photo(m.chat.id, user_id.get_node().photo, reply_markup=userLikes.option[user_id.get_node().num])

        if user_id.get_node().gif is not None:
            bot.send_animation(m.chat.id, user_id.get_node().gif, duration=None, caption=None, reply_to_message_id=None,
                               reply_markup=None, parse_mode=None, disable_notification=None, timeout=None)

        bot.send_message(m.chat.id, user_id.get_node().question, reply_markup=userLikes.option[user_id.get_node().num])


def next_recommendation(m, user_id):
    global cat, counter
    result = nearby_places(user_id.get_latitude(), user_id.get_longitude(), cat)
    loc = result[counter].get('geometry').get('location')
    name = result[counter].get('name')
    address = result[counter].get('vicinity')
    bot.send_location(m.chat.id, loc.get('lat'), loc.get('lng'))
    bot.send_message(m.chat.id, "He encontrado este restaurante cerca de ti, ¿Qué te parece?\n"
                                "*" + name + "*\nDirección: _" + address + "_",
                     reply_markup=userLikes.recommendation_select, parse_mode="Markdown")
    counter += 1
    user_id.set_step(RECOMMENDATIONS)


def end_message(m, user_id):
    global cat, counter
    bot.send_message(m.chat.id, "Espero haberte ayudado")
    bot.send_message(m.chat.id, "🥰", parse_mode="Markdown", reply_markup=Bot.getInstance().hideBoard)
    cat = ''
    counter = 0
    user_id.set_step(START)
