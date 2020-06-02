import time

from api import nearby_places
from difflib import SequenceMatcher

from telebot import types

from graphh.node import Response
from graphh.read_graph import Decision
from db.controllerss.places_controller import PlacesController
from db.controllerss.user_controller import UserController
from category.category_decision import Category_Decision, check_similarity_percentage, choose_category
from places import Places
from singleton_bot import Bot

START = 0
LOCATION = 1
NEW_LOCATION = 2
ALONE_FRIENDS = 3
NEXT_DECISION = 4
RECOMMENDATIONS = 5
CATEGORY = 6

# Stickers
PEPE_CLAP = 'CAACAgQAAxkBAAIBYl7U8kAqKtLeONW1sOIXsGq6vDMyAAJMAQACqCEhBmMqtFaxxhbIGQQ'
PEPE_CRY = 'CAACAgIAAxkBAAIDkV7VWkNQWAGHRyUWeR38JVRuYanQAAJYAQACierlB4x5Q0a9uaZGGQQ'
CHEF = 'CAACAgIAAxkBAAIBvV7U9YzwilBbM6k3LNfTmQxwcJKaAALfAAMw1J0REW2Q6CUm530ZBA'

cat = ''
counter = 0
name = ''
address = ''
latitude = ''
longitude = ''


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
        Decision.getInstance().read_json()

        for aux in list(Decision.getInstance().graph.nodes):
            self.option.insert(aux, types.ReplyKeyboardMarkup(one_time_keyboard=True))

        self.location = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()

        Category_Decision.getInstance().set_option(self.option)

        Bot.getInstance().setHideBoard(types)

    def replay_all_keyboard_makeup(self):

        self.yes_no_select.add('Si', 'No')
        self.recommendation_select.add('Me gusta 😍')
        self.recommendation_select.add('Prueba con otro 🔄')
        self.recommendation_select.add('Cancelar ❌')
        for node_graph in list(Decision.getInstance().graph.nodes):
            node = Decision.getInstance().graph.nodes[node_graph]['node']
            self.option[node_graph].add(node.get_left_name())
            self.option[node_graph].add(node.get_right_name())
        self.location.row(types.KeyboardButton(text='Enviar mi ubicación', request_location=True))


userLikes = UserLikes.getInstance()
bot = Bot.getInstance().bot
users = UserController.getInstance()


@bot.message_handler(
    func=lambda message: True, content_types=['sticker'])
def get_sticker_id(m):
    cid = m.chat.id
    print(m.sticker.file_id)


def settings(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    loc = users.getUserLocationByUserID(cid)

    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)

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
    time.sleep(0.5)
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
    time.sleep(0.5)
    bot.send_message(m.chat.id, "Adiós, nos vemos pronto")
    bot.send_animation(m.chat.id, 'https://reygif.com/media/pocahontas-saludo-83409.gif', duration=None, caption=None,
                       reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
                       timeout=None)

    user_id = users.getUserById(m.chat.id)
    users.storeStep(user_id, START)
    users.save_node(user_id, START)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == NEXT_DECISION,
                     content_types=['text'])
def this_or_that(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)

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

    time.sleep(0.5)
    bot.send_message(cid, "Ubicación guardada con éxito.")
    what_now(m)
    users.storeStep(user_id, START)


# if the user has issued the "/configure" command, process the answer
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == LOCATION,
                     content_types=['text'])
def configure_location_text(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)
    markup = types.ForceReply(selective=False)
    bot.send_message(cid, "Ubicación no válida, intentalo de nuevo.", reply_markup=markup)


@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == NEW_LOCATION,
                     content_types=['text'])
def configure_new_location(m):
    cid = m.chat.id
    user_id = users.getUserById(cid)
    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)
    if text == 'Si':
        bot.send_message(cid, "A continuación te aparecerá un botón para enviar la ubicación",
                         reply_markup=userLikes.location)
        users.storeStep(user_id, LOCATION)
    elif text == 'No':
        bot.send_message(cid, "¡De acuerdo!", reply_markup=Bot.getInstance().hideBoard)
        users.storeStep(user_id, START)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"Si\" o \"No\"")


@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == RECOMMENDATIONS,
                     content_types=['text'])
def recommendations_yes_or_no(m):
    global cat, name, address, latitude, longitude
    cid = m.chat.id
    user_id = users.getUserById(cid)

    text = m.text
    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)

    if text == 'Me gusta 😍':
        end_message(m, user_id)

        categories = Places.getInstance().get_category(cat)

        for category in categories:
            PlacesController.get_instance().create_place(name, latitude, longitude, address, category, cat, user_id)

    elif text == 'Prueba con otro 🔄':
        bot.send_message(cid, "Vamos a ver...", reply_markup=Bot.getInstance().hideBoard)
        bot.send_chat_action(cid, 'typing')
        time.sleep(0.5)
        next_recommendation(m, user_id)
        users.storeStep(user_id, RECOMMENDATIONS)
    elif text == 'Cancelar ❌':
        command_text_bye(m)
    else:
        bot.send_message(cid, "Por favor, utiliza solo los botones")


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == START and 0.8 <= SequenceMatcher(
        None, message.text, "ayuda").ratio(),
    content_types=['text'])
def command_text_help(m):
    bot.send_message(m.chat.id, "Para ver la página de ayuda puedes usar /ayuda")


# filter on a specific message
@bot.message_handler(func=lambda message: users.getUserById(message.chat.id).step == START and
                                          (check_similarity_percentage(message.text, "adiós") or
                                           check_similarity_percentage(message.text, "cancelar")),
                     content_types=['text'])
def command_text_bye(m):
    time.sleep(0.5)
    bot.send_message(m.chat.id, "Adiós, nos vemos pronto", reply_markup=Bot.getInstance().hideBoard)
    bot.send_animation(m.chat.id, 'https://reygif.com/media/pocahontas-saludo-83409.gif', duration=None, caption=None,
                       reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None,
                       timeout=None)

    user_id = users.getUserById(m.chat.id)
    users.storeStep(user_id, START)
    users.storeStep(user_id, START)


def what_now(m):
    bot.send_message(m.chat.id, "¿Que quieres hacer ahora?\n(Prueba con: _recomiéndame algo_)", parse_mode="Markdown")


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
    cid = m.chat.id
    if decision.end == 1:
        category = decision.category
        if category is not None:
            if category == 'chefbot':
                bot.send_message(m.chat.id, "@NoteolvidesBot 👨‍🍳", parse_mode="Markdown")
                bot.send_sticker(m.chat.id, CHEF, reply_markup=Bot.getInstance().hideBoard)
                time.sleep(0.5)
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
        users.storeStep(user_id, START)

    else:
        users.save_node(user_id, decision.next_step)

        bot.send_message(cid, users.get_node(cid).question, reply_markup=userLikes.option[users.get_node(cid).num])

        if users.get_node(cid).photo is not None:
            bot.send_photo(cid, users.get_node(cid).photo, reply_markup=userLikes.option[users.get_node(cid).num])

        if users.get_node(cid).gif is not None:
            bot.send_animation(cid, users.get_node(cid).gif, duration=None, caption=None, reply_to_message_id=None,
                               reply_markup=None, parse_mode=None, disable_notification=None, timeout=None)


def next_recommendation(m, user_id):
    global cat, counter, name, address, latitude, longitude
    loc = users.getUserLocationByUserID(m.chat.id)
    result = nearby_places(loc.latitude, loc.longitude, cat)

    if result is None:
        bot.send_message(m.chat.id, "Lo siento, cerca de tu localización no encuentro ningún/ninguna "
                         + Places.getInstance().get_place_name(cat))
        bot.send_sticker(m.chat.id, PEPE_CRY, reply_markup=Bot.getInstance().hideBoard)
        users.storeStep(user_id, START)

    else:
        if counter >= len(result):
            bot.send_message(m.chat.id, "Lo siento, no encuentro más resultados en tu zona")
            bot.send_sticker(m.chat.id, PEPE_CRY, reply_markup=Bot.getInstance().hideBoard)
            users.storeStep(user_id, START)
            counter = 0
            return
        loc = result[counter].get('geometry').get('location')
        name = result[counter].get('name')
        address = result[counter].get('vicinity')
        latitude = loc.get('lat')
        longitude = loc.get('lng')
        bot.send_location(m.chat.id, latitude, longitude)
        bot.send_message(m.chat.id, "He encontrado este " + Places.getInstance().get_place_name(cat) + " cerca de ti, "
                                                                                                       "¿Qué te parece?\n*" + name + "*\nDirección: _" + address + "_",
                         reply_markup=userLikes.recommendation_select, parse_mode="Markdown")
        counter += 1
        users.storeStep(user_id, RECOMMENDATIONS)


def end_message(m, user_id):
    global cat, counter
    bot.send_message(m.chat.id, "Espero haberte ayudado")
    bot.send_sticker(m.chat.id, PEPE_CLAP, reply_markup=Bot.getInstance().hideBoard)
    counter = 0
    users.storeStep(user_id, START)


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo \"" + m.text + "\"\nPuede que la página de ayuda te sirva /ayuda")


def cancel_action(m):
    users.storeStep(users.getUserById(m.chat.id), START)
