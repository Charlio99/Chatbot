from commands import Commands
from neo4jDB.DumpDatabaseFile import DumpDatabaseFile
from singletonBot import Bot
from userLikes import UserLikes

userLikes = UserLikes.getInstance()
Commands()
bot = Bot.getInstance().bot
dump = DumpDatabaseFile()
# dump.dumpDatabaseMenu()
bot.polling()
