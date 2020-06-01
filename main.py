from Graph.readGraph import Decision
from commands import Commands
from neo4jDB.DumpDatabaseFile import DumpDatabaseFile
from singletonBot import Bot

graph = Decision()
graph.read_json()

Commands()
bot = Bot.getInstance().bot
bot.polling()
dump = DumpDatabaseFile()
dump.dumpDatabaseMenu()
