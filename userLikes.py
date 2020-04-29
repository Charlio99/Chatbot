from telebot import types


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replayAllKeyboardMakeup()

    def replayAllKeyboardMakeup(self):
        self.yes_no_select.add('Si', 'No')

        self.amigos_solo.add('Con amigos', 'Solo')

        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')
