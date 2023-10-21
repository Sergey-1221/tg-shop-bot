import telebot
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TOKEN = '6466895331:AAE99D5h-v6yOIw_tit2LnTJP6gA1xArGAQ'
bot = telebot.TeleBot(TOKEN)

# Подключение и создание базы данных с помощью SQLAlchemy
engine = create_engine('sqlite:///store.db')
Session = sessionmaker(bind=engine)
session = Session()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Добро пожаловать в наш магазин!')

# Обработчик команды /add
@bot.message_handler(commands=['add'])
def add_product(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Введите название продукта:')
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    msg = bot.send_message(chat_id, 'Введите цену продукта:')
    bot.register_next_step_handler(msg, process_price_step, name)

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

    # Получение списка всех продуктов из базы данных
    products = session.query(Product).all()

    response = 'Список продуктов:\n'
    for product in products:
        response += f"{product.name} - {product.price} руб.\n"

    bot.send_message(chat_id, response)

# Запуск бота
bot.polling()