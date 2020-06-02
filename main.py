from commands import Commands
from db.dump_database_file import DumpDatabaseFile
from singleton_bot import Bot
from user_likes import UserLikes

userLikes = UserLikes.getInstance()
Commands()
bot = Bot.getInstance().bot
dump = DumpDatabaseFile()
# dump.dumpDatabaseMenu()
bot.polling()
