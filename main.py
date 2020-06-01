from Graph.readGraph import Decision
from commands import Commands
from neo4jDB.DumpDatabaseFile import DumpDatabaseFile
from singletonBot import Bot

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

graph = Decision()
graph.readJson()

Commands()
bot = Bot.getInstance().bot
dump = DumpDatabaseFile()
dump.dumpDatabaseMenu()
bot.polling()
