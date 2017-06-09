
import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)


class MessageCounter(telepot.helper.UserHandler):

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0
        self.currentCategory = 0
        self.votes = []

        self.candidates = [
            ['Dani Bolaasdos', 'Saez'],
            ['limao', 'asdsad', 'asdasddada']
        ]
        self.categories = ['Categoria 1', 'Categoria 2']

        

    def on_chat_message(self, msg):
     content_type, chat_type, chat_id = telepot.glance(msg)

     if self.currentCategory == len(self.categories):
        return 
     lista = zip(self.candidates[self.currentCategory], [i for i in range(1,len(self.candidates[self.currentCategory])+1)])
     keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text=x, callback_data=str(n)) for x,n in lista],
               ])
     bot.sendMessage(chat_id, 'Categoria: ' + self.categories[self.currentCategory], reply_markup=keyboard)
     self.currentCategory += 1


    def on_callback_query(self, msg):
     query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
     print('Callback Query:', query_id, from_id, query_data)
     if self.currentCategory != len(self.categories):
        bot.sendMessage(from_id, 'Dale a  /siguiente')
     bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(),create_open, MessageCounter, timeout=10),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
