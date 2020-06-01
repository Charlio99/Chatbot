from Graph.readGraph import Decision
from commands import Commands
from neo4jDB.DumpDatabaseFile import DumpDatabaseFile
from singletonBot import Bot

graph = Decision.getInstance()
graph.read_json()

Commands()
bot = Bot.getInstance().bot
dump = DumpDatabaseFile()
dump.dumpDatabaseMenu()
bot.polling()
