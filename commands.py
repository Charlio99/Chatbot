from singletonBot import Bot
from user import User


class Commands:
    commands = {  # command description used in the "help" command
        'start': 'Inicia el bot y ajusta tu información',
        'ayuda': 'Informacion sobre los comandos disponibles'
    }

    def __init__(self):
        pass


commandClass = Commands()
bot = Bot.getInstance().bot


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    if user is None:  # if user hasn't used the "/start" command yet:
        Bot.getInstance().users[cid] = User(cid)
        bot.send_message(cid, "¡Hola! Soy Pilus, un bot recomendador de planes")
        command_help(m)
        bot.send_message(cid, "Antes de nada, vamos a configurar tu perfil para perfeccionar mis recomendaciones")
        from userLikes import command_settings
        command_settings(m)
    else:
        bot.send_message(cid, "Ya has iniciado el bot previamente, si necesitas ver los comandos, puedes usar /ayuda")


# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    user = Bot.getInstance().users.get(cid)
    help_text = "Los comandos disponibles son los siguientes: \n"
    for key in commandClass.commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commandClass.commands[key] + "\n"
    help_text += "Si quieres que te recomiende algo simplemente di: _recomiendame algo_"
    bot.send_message(cid, help_text, parse_mode="Markdown")  # send the generated help page
