import telebot
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Product,Users

from models import *
TOKEN = '6466895331:AAE99D5h-v6yOIw_tit2LnTJP6gA1xArGAQ'
bot = telebot.TeleBot(TOKEN)

# Подключение и создание базы данных с помощью SQLAlchemy
engine = create_engine('sqlite:///store.db')
Session = sessionmaker(bind=engine)
session = Session()


'''
#Тест веь-приложения раскоментить чтоб заработало
@bot.message_handler(commands=['start'])
def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo("https://telegram.mihailgok.ru") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Тестовая страница", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру
    return keyboard #возвращаем клавиатуру
'''

# Обработчик команды /start
#Проверка на админа

class AdminChecker:
    is_admin = False
                   
adminka = AdminChecker()    


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.reply_to(message, 'Добро пожаловать в наш магазин')
    users = []
    for user in users:
        if user.tg_id == message.from_user.id:
            bot.send_message(chat_id,'Вы сотрудник компании')
            if user.role == 'admin':
                adminka.is_admin = True
                bot.send_message(chat_id,'Вы админ, можете удалять добавлять и т.д товары')

    
# Обработчик команды /add
@bot.message_handler(commands=['add'])
def add_product(message):
    chat_id = message.chat.id
    if adminka.is_admin == True:
        
        msg = bot.send_message(chat_id, 'Введите название продукта:')
        bot.register_next_step_handler(msg, process_name_step)
    else:
        bot.send_message(chat_id, 'Вы не админ')    

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    msg = bot.send_message(chat_id, 'Введите цену продукта:')
    bot.register_next_step_handler(msg, process_price_step, name)
    bot.send_message(chat_id, 'Вы не админ')


def process_price_step(message, name):
    chat_id = message.chat.id
    price = float(message.text)

    # Добавляем продукт в базу данных
    product = Product(name=name, price=price)
    session.add(product)
    session.commit()

    bot.send_message(chat_id, 'Продукт успешно добавлен!')
    

# Обработчик команды /list
@bot.message_handler(commands=['list'])

def get_product_list(message):
    chat_id = message.chat.id
    if adminka.is_admin == True:
        

    # Получение списка всех продуктов из базы данных
        products = session.query(Product).all()

        response = 'Список продуктов:\n'
        for product in products:
            response += f"{product.name} - {product.price} coin.\n"

        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, 'Вы не админ')

# Запуск бота
bot.polling()