import time

from telebot import types

from singletonBot import Bot


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.outside_inside = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.house_relax = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.sure_inside = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()

    def replay_all_keyboard_makeup(self):
        self.yes_no_select.add('Si', 'No')
        self.amigos_solo.add('Con amigos', 'Solo')
        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')
        self.outside_inside.add('Salir de casa', 'Estoy vago, mejor en casa')
        self.house_relax.add('Me apetece relajarme', 'Si me relajo me duermo')
        self.sure_inside.add('Que si pesado', 'Bueno... ¿Qué me propones hacer?')


bot = Bot.getInstance().bot
""""

@bot.message_handler(func=lambda message: Bot.getInstance().users.get(message.chat.id).get_step() == 3)
def with_or_without_friends(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    text = m.text

    markup = types.ForceReply(selective=False)
    bot.send_chat_action(cid, 'typing')
    time.sleep(2)
    if text == 'Con amigos':
        bot.send_location(cid, 41.41021, 2.137828, reply_markup= Bot.getInstance().hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece este restaurante nuevo de comida Japonesa?\n"
                              "https://goo.gl/maps/NiNRxBpZTB66c9Lt6", reply_markup= Bot.getInstance().userLikes.genial_otro)
        user.set_step(4)
    elif text == 'Solo':
        photo = open('./tmp/el_hoyo.jpg', 'rb')
        bot.send_photo(cid, photo, reply_markup= Bot.getInstance().hideBoard)
        bot.send_message(cid, "¡Genial! ¿Que te parece esta pelicula de Netflix?\n"
                              "https://www.netflix.com/title/81128579",
                         reply_markup= Bot.getInstance().userLikes.genial_otro)

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
        bot.send_message(cid, "¡Encantado de ayudarte! " + m.from_user.first_name, reply_markup=Bot.getInstance().hideBoard)
    elif text == 'Mejor otra cosa':
        user.set_step(0)
        bot.send_message(cid, "Lo siento " + m.from_user.first_name + ",se me han acabado las recomendaciones, "
                                                                      "pero sigo mejorando para tener más opciones",
                         reply_markup=Bot.getInstance().hideBoard)
    else:
        bot.send_message(cid, "Por favor, pulsa solo \"¡Genial!\" o \"Mejor otra cosa\"")




@bot.message_handler(func=lambda message: users.get(message.chat.id).get_step() == OUTSIDE_INSIDE)
def inside_outside_decision(m):
    cid = m.chat.id
    user = users.get(cid)
    text = m.text

    bot.send_chat_action(cid, 'typing')
    time.sleep(2)

    if text == 'Salir de casa':
        bot.send_message(cid, "¡Genial! ¿Que te parece este restaurante nuevo de comida Japonesa?\n"
                              "https://goo.gl/maps/NiNRxBpZTB66c9Lt6", reply_markup=userLikes.genial_otro)
        user.set_step(4)
    elif text == 'Estoy vago, mejor en casa':
        bot.send_message(cid, "Eres un vago de mierda chaval\n", reply_markup=userLikes.genial_otro)

"""""