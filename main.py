from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chat_bot = ChatBot(name='Carvis', read_only=True,
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
              'ok boomer.',
              'what\'s your name?',
              'i\'m Carvis. Boomer']
math_talk_1 = ['pythagorean theorem',
               'a squared plus b squared equals c squared.']
math_talk_2 = ['law of cosines',
               'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)']

list_trainer = ListTrainer(chat_bot)
for item in (small_talk, math_talk_1, math_talk_2):
    list_trainer.train(item)

while 1:
    nb = input('You: ')
    print(chat_bot.get_response(nb))
