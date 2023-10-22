import telebot
from telebot import types
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from models import Product,Users

from models import *
TOKEN = '6844494900:AAFTOmNtMuCMxppLk0IuwihdA_DZrM8u9FU'
bot = telebot.TeleBot(TOKEN)

# Подключение и создание базы данных с помощью SQLAlchemy
engine = create_engine('sqlite:///store.db')
Session = sessionmaker(bind=engine)
session = Session()





# Обработчик команды /start

def check_user(user_id):
    user = session.get(Users, user_id)
    if user == None:
        user = Users(tg_id=user_id)
        session.add(user)
        session.commit()
    is_admin = (user.role == "admin")

    return {
        "object": user,
        "admin": is_admin
        }


def webAppKeyboard(): #создание клавиатуры с webapp кнопкой
   keyboard = types.ReplyKeyboardMarkup(row_width=1) #создаем клавиатуру
   webAppTest = types.WebAppInfo("https://127.0.0.1:50100") #создаем webappinfo - формат хранения url
   one_butt = types.KeyboardButton(text="Товары", web_app=webAppTest) #создаем кнопку типа webapp
   keyboard.add(one_butt) #добавляем кнопки в клавиатуру

   return keyboard #возвращаем клавиатуру


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user = check_user(message.from_user.id)
    bot.reply_to(message, 'Добро пожаловать в наш магазин')
    bot.send_message(chat_id, 'Добро пожаловать в наш магазин', reply_markup=webAppKeyboard())
    #bot.send_message(chat_id,'/me Информация обо мне \n/help список всех команд')
            

@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    user = check_user(message.from_user.id)

    if user["admin"]:
        bot.send_message(chat_id, 'Команды администратора:\n /add Добавить товар')

    
# Обработчик команды /add
@bot.message_handler(commands=['add'])
def add_product(message):
    chat_id = message.chat.id
    user = check_user(message.from_user.id)
    if user["admin"]:
        msg = bot.send_message(chat_id, 'Введите название продукта:')
        bot.register_next_step_handler(msg, process_name_step) 
        
        

def process_name_step(message):
    chat_id = message.chat.id
    name = message.text
    msg = bot.send_message(chat_id, 'Введите цену продукта:')
    bot.register_next_step_handler(msg, process_price_step, name)


def process_price_step(message, name):
    chat_id = message.chat.id
    try:
        price = float(message.text)
        msg = bot.send_message(chat_id, 'Загрузите изображение:')
        bot.register_next_step_handler(msg, process_image_step, name, price) 

    except ValueError:
        msg = bot.send_message(chat_id, 'Введите коректоне число (Например 3.14):')
        bot.register_next_step_handler(msg, process_price_step, name)

def process_image_step(message, name, price):   
    chat_id = message.chat.id
    if message.photo != None:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        name_image = message.photo[1].file_id+".jpg"
        src = 'static/image/' + message.photo[1].file_id+".jpg"
        
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
        product = Product(name=name, price=price, image=name_image)
        session.add(product)
        session.commit()
        bot.send_message(chat_id, 'Продукт успешно добавлен!')
    else:
        msg = bot.send_message(chat_id, 'Фото не найдено.')
        bot.register_next_step_handler(msg, process_image_step, name, price) 
 


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