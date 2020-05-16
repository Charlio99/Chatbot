# from commands import Commands
from commands import Commands
from singletonBot import Bot
from userLikes import UserLikes

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

Commands()
UserLikes()
bot = Bot.getInstance().bot
bot.polling()
