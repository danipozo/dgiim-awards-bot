
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
import json


class MessageCounter(telepot.helper.UserHandler):

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0
        self.currentCategory = 0
        self.votes = []
        self.voter = ""

        self.candidates = [
            ['Test1', 'Test2'],
            ['Test1', 'Test2', 'Test3'],
            ['Test 1', 'Test 2'],
            ['Test 1', 'Test 2', 'Test 3', 'Test 4'],
            ['Test1', 'Test2', 'Test3'],
            ['Test 1', 'Test 2', 'Test 3', 'Test 4']
        ]
        self.categories = ['Categoría 1', 'Categoría 2',
                           'Categoría 3', 'Categoría 4',
                           'Categoría 5', 'Categoría 6']

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.voter = chat_id

        if self.currentCategory == len(self.categories):
            bot.sendMessage(chat_id, 'Gracias por tu participación')
            return

        numberedCands = zip(self.candidates[self.currentCategory], [
            i for i in range(1, len(self.candidates[self.currentCategory]) + 1)])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=
            [[InlineKeyboardButton(text=x, callback_data=str(n))]
             for x, n in numberedCands],
        )

        bot.sendMessage(chat_id,
                        'Categoría: ' + self.categories[self.currentCategory],
                        reply_markup=keyboard)
        

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(
            msg, flavor='callback_query')

       
        
        if self.currentCategory != len(self.categories):
            self.votes.append({ str(self.categories[self.currentCategory]) : self.candidates[self.currentCategory][int(query_data)-1] })

            if self.currentCategory != len(self.categories)-1:
                bot.sendMessage(from_id, 'Dale a  /siguiente')

        if self.currentCategory == len(self.categories)-1:

            bot.sendMessage(from_id, 'Gracias por tu participación')
            with open(str(self.voter), 'w') as f:
                json.dump(self.votes, f)

        self.currentCategory += 1
        bot.answerCallbackQuery(query_id, text='Respuesta registrada')


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(), create_open, MessageCounter, timeout=1000),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while True:
    time.sleep(10)
