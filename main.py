from commands import Commands
from db.dump_database_file import DumpDatabaseFile
from singleton_bot import Bot
from user_likes import UserLikes

userLikes = UserLikes.getInstance()
Commands()
bot = Bot.get_instance().bot
dump = DumpDatabaseFile()
# dump.dump_database_menu()
bot.polling()
