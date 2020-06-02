from handler.command_handler import Commands
from db.dump_database_file import DumpDatabaseFile
from singleton_bot import Bot
from handler.message_handler import UserLikes

user_likes = UserLikes.get_instance()
Commands()
bot = Bot.get_instance().bot
dump = DumpDatabaseFile()
# dump.dump_database_menu()
bot.polling()
