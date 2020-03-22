from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

chat_bot = ChatBot(name='No Name Bot', read_only=True,
                   logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                   'chatterbot.logic.BestMatch'])

intro = ['I\'d like to do something',
         'Would you like to do somthing alone?']

hello = ['Hi',
         'Hi, how can I help you?']

something_to_do_negative_1 = ['Would you like to do somthing alone?',
                              'no',
                              'Are you starving?',
                              'yes, i am hungry',
                              'Would you like to go to an elegant restaurant?',
                              'not my type',
                              'I know the perfect place.... PARKING PIZZA',
                              'What\'s the schedule?',
                              'Let me check it... It will open at 8pm and will close at 12pm. What do you think?',
                              'it closes too early',
                              'Are you sure that you want to go out?... Why don\'t just stay at home and watch some Netflix?',
                              'I am going to do that',
                              'Do you need anything else?']

something_to_do_negative_2 = ['Would you like to do somthing alone?',
                              'no',
                              'Are you hungry?',
                              'i am not hungry',
                              'What about playing videogames with your friends?',
                              'not in the mood',
                              'I\'ve no more ideas :(']

something_to_do_positive_1 = ['Would you like to do somthing alone?',
                              'yes',
                              'What about a walk?',
                              'great, i love walking',
                              'I have the best idea: Park Guell, go and have some fun ;)']

thank_you = ['thank you',
             'NICE! Glad to help you']

thank_you_2 = ['thanks',
               'NICE! Glad to help you']

default = ['',
           'I can\'t help you with that']

list_trainer = ListTrainer(chat_bot)
for item in (
        hello, intro, something_to_do_negative_1, something_to_do_positive_1, something_to_do_negative_2, thank_you,
        thank_you_2, default):
    list_trainer.train(item)

user_input = ''

while str(chat_bot.get_response(user_input)) != 'NICE! Glad to help you':
    user_input = input('You: ')
    response = str(chat_bot.get_response(user_input))
    print(response)
