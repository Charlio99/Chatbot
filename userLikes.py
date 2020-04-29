from telebot import types


class UserLikes:

    def __init__(self):  # Declare the constructor with or without parameters
        self.yes_no_select = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.amigos_solo = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.genial_otro = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.exterior_interior = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.house_relax = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.sure_inside = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.replay_all_keyboard_makeup()

    def replay_all_keyboard_makeup(self):
        self.yes_no_select.add('Si', 'No')
        self.amigos_solo.add('Con amigos', 'Solo')
        self.genial_otro.add('¡Genial!', 'Mejor otra cosa')
        self.exterior_interior.add('Salir de casa', 'Estoy vago, mejor en casa')
        self.house_relax.add('Me apetece relajarme', 'Si me relajo me duermo')
        self.sure_inside.add('Que si pesado', 'Bueno... ¿Qué me propones hacer?')

