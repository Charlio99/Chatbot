from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chat_bot = ChatBot(name='Jarvis', read_only=True,
                   logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                   'chatterbot.logic.BestMatch'])

small_talk = ['hi there!',
              'hi!',
              'how do you do?',
              'how are you?',
              'i\'m cool.',
              'fine, you?',
              'always cool.',
              'i\'m ok',
              'glad to hear that.',
              'i\'m fine',
              'glad to hear that.',
              'i feel awesome',
              'excellent, glad to hear that.',
              'not so good',
              'sorry to hear that.',
              'what\'s your name?',
              'i\'m pybot. ask me a math question, please.']

list_trainer = ListTrainer(chat_bot)
for item in small_talk:
    list_trainer.train(item)

while 1:
    nb = input('You: ')
    print("Bot: " + chat_bot.get_response(nb))


