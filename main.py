from Graph.readGraph import Decision
from commands import Commands
from singletonBot import Bot

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

graph = Decision()
graph.read_json()

Commands()
bot = Bot.getInstance().bot
bot.polling()
