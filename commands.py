import time
from difflib import SequenceMatcher

from db.controllerss.user_controller import UserController
from singleton_bot import Bot


class Commands:
    commands = {  # command description used in the "help" command
        'start': 'Inicia el bot y ajusta tu información',
        'ayuda': 'Informacion sobre los comandos disponibles',
        'cancelar': 'Volver al inicio de las preguntas'
    }

    def __init__(self):
        pass


commandClass = Commands()
bot = Bot.getInstance().bot
users = UserController.getInstance()


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if UserController.getInstance().checkUserByIdIfExists(cid):  # if user hasn't used the "/start" command yet:
        UserController.getInstance().storeUser(cid, m.chat.first_name, 0)
        bot.send_message(cid, "¡Hola! Soy Pilus, un bot recomendador de planes")
        bot.send_message(cid, "Antes de nada, vamos a configurar tu perfil para perfeccionar mis recomendaciones")
        command_settings(m)
    else:
        bot.send_message(cid, "Ya has iniciado el bot previamente, si necesitas ver los comandos, puedes usar /ayuda")


# config page
@bot.message_handler(commands=['configurar'])
def command_settings(m):
    from user_likes import settings
    settings(m)

# config page
@bot.message_handler(commands=['cancelar'])
def command_settings_cancelation(m):
    from user_likes import cancel_action
    cancel_action(m)
    bot.send_message(m.chat.id, 'Cancelación exitosa.\n'
                                'Si quieres que te recomiende algo simplemente di: recomiéndame algo')


# filter on a specific message
@bot.message_handler(
    func=lambda message: users.getUserById(message.chat.id).step == 0 and check_similarity_percentage(message.text, "recomiendame algo"),
    content_types=['text'])
def command_text_recommend(m):
    cid = m.chat.id

    bot.send_chat_action(cid, 'typing')
    time.sleep(0.5)

    loc = users.getUserLocationByUserID(cid)

    if loc.latitude is None or loc.longitude is None:

        bot.send_message(cid, "Para poder usar las recomendaciones primero tienes que configurar tu código postal.\n"
                              "Para hacerlo usa el comando /configurar")
    else:
        from category.category_decision import choose_category
        choose_category(m)


# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Los comandos disponibles son los siguientes: \n"
    for key in commandClass.commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commandClass.commands[key] + "\n"
    help_text += "Si quieres que te recomiende algo simplemente di: _recomiéndame algo_"
    bot.send_message(cid, help_text, parse_mode="Markdown")  # send the generated help page


def check_similarity_percentage(text, option):
    if text is None:
        return False

    if SequenceMatcher(None, text.lower(), option.lower()).ratio() >= 0.8:
        return True

    if option.lower() in text.lower():
        return True

    return False


