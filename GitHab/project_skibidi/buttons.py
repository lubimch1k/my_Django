# Работа с кнопками
from telebot import types


# Кнопка отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    num = types.KeyboardButton('Отправить номер📞', request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(num)

    return kb


# Кнопка главного меню
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем кнопки
    cart = types.InlineKeyboardButton(text='Корзина🛒', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=i[1], callback_data=i[0])
                    for i in products]
    # Добавляем кнопки в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb


def choose_pr_count(pr_amount, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    count = types.InlineKeyboardButton(text=str(amount), callback_data='ignore')
    to_cart = types.InlineKeyboardButton(text='Добавить в корзину🛒', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')

    # Алгоритм изменения количества
    if plus_or_minus == 'increment':
        if amount <= pr_amount:
            count = types.InlineKeyboardButton(text=str(amount + 1), callback_data='ignore')
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount - 1), callback_data='ignore')

    # Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(back, to_cart)

    return kb


# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ🛒', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину🗑️', callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад🔙', callback_data='back')
    # Добавляем кнопки в пространство
    kb.add(order, clear)
    kb.row(back)

    return kb



# Кнопка локации
def loc_buttons():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить локацию📍', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)

    return kb
