import os
import telegram
import pandas as pd
from telegram import KeyboardButton, ReplyKeyboardMarkup

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
df = pd.read_csv("FoodDatabase.csv")


def hello_world(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        msg_text = update.message.text

        if msg_text.startswith('/'):
            if msg_text == '/start':
                options = []
                options.append(KeyboardButton(text='Canteen', callback_data='Canteen'))
                options.append(KeyboardButton(text='BPP', callback_data='BPP'))
                options.append(KeyboardButton(text='Hillion', callback_data='Hillion'))
                reply_markup = ReplyKeyboardMarkup([options])

                bot.sendMessage(chat_id=chat_id, text='''
Hello! If you are from Gombak and are thinking of where to eat for lunch, this bot is designed to help you decide!

Select a place to eat from one of the three buttons below!''', reply_markup=reply_markup)
            
        if msg_text in ['BPP', 'Hillion', 'Canteen']:
            selected = df[df.Location == msg_text].sample()
            if msg_text == 'Canteen':
                text = f'May I suggest you eat at \n\n{selected.Store.item()}'
                bot.sendMessage(chat_id=chat_id, text=text)
            else:
                text = f'''May I suggest you eat at

{selected.Store.item()}
Cuisine: {selected.Cuisine.item()}
Unit No: {selected.UnitNo.item()}'''

                if selected.Seating.item() == 'No':
                    text2 = f'There are no seats at {selected.Store.item()}, so arrange for takeaway.'
                elif selected.Seating.item() == 'Limited':
                    text2 = f'There are limited seats at {selected.Store.item()}, so be prepared to takeaway if necessary.'
                else:
                    text2 = f'There are seats at {selected.Store.item()}, hope it will not be too full!'

                bot.sendMessage(chat_id=chat_id, text=text)
                bot.sendMessage(chat_id=chat_id, text=text2)
        else:
            if msg_text != '/start':
                bot.sendMessage(chat_id=chat_id, text="Did not recognise your input. If you would like to bring up the buttons again, simply send '/start' to me! ")

    return "ok"