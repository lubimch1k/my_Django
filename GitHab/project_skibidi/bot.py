# Основная логика бота
import telebot
import buttons
import database


# Создаем объект бота
bot = telebot.TeleBot('7782541505:AAFodYSmv2GasUXW2clxK47UW6kfAV-Ozdo') #https://t.me/siki_bi_di_bot
# Временные данные
users = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if database.check_user(user_id):
        pr = database.get_pr_buttons()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=buttons.main_menu(pr))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Введите свое имя', reply_markup=telebot.types.ReplyKeyboardRemove())
        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)


# Этап получения имени
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text

    bot.send_message(user_id, 'Отлично! Теперь отправьте свой номер телефона!',
                     reply_markup=buttons.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_num, user_name)


# Этап получения номера
def get_num(message, user_name):
    user_id = message.from_user.id

    # Проверка, если пользователь отправил номер по кнопке
    if message.contact:
        user_num = message.contact.phone_number
        database.register(user_id, user_name, user_num)

        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер телефона по кнопке!')
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_num, user_name)


@bot.callback_query_handler(lambda call: call.data in ['cart', 'clear', 'order'])
def cart_handle(call):
    user_id = call.message.chat.id
    text = 'Ваша корзина:\n\n'

    if call.data == 'cart':
        user_cart = database.show_cart(user_id)
        total = 0.0

        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n\n')
            total += database.get_exact_price(i[1])[0] * i[2]
        text += f'Итого: ${round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, text, reply_markup=buttons.cart_buttons())

    elif call.data == 'clear':
        database.clear_cart(user_id)
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Ваша корзина очищена!',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))

    elif call.data == 'order':
        text = text.replace('Ваша корзина:', f'Новый заказ!\nКлиент @{call.message.chat.username}\n\n')
        user_cart = database.show_cart(user_id)
        total = 0.0

        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n\n')
            total += database.get_exact_price(i[1])[0] * i[2]
        text += f'Итого: ${round(total, 2)}'
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(user_id, 'Для оформления заказа, отправьте локацию!', reply_markup=buttons.loc_buttons())
        # Переход на этап получения локации
        bot.register_next_step_handler(call.message, get_loc, text)


# Этап получения локации
def get_loc(message, text):
    user_id = message.from_user.id
    if message.location:
        bot.send_message(1482646413, text)
        bot.send_location(1482646413, longitude=message.location.longitude, latitude=message.location.latitude)
        database.make_order(user_id)
        bot.send_message(user_id, 'Ваш заказ оформлен! Скоро с вами свяжутся!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=buttons.main_menu(database.get_pr_buttons()))
    else:
        bot.send_message(user_id, 'Отправьте локацию по кнопке!')
        # Возвращение на этап получения локации
        bot.register_next_step_handler(message, get_loc, text)


@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'] or int(call.data) in [i[0] for i in database.get_all_pr()])
def choose_product(call):
    user_id = call.message.chat.id
    if call.data.isdigit():
        pr_info = database.get_exact_pr(int(call.data))
        bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        bot.send_photo(user_id, photo=pr_info[-1], caption=f'{pr_info[1]}\n\n'
                                                           f'Описание: {pr_info[2]}\n'
                                                           f'Количество: {pr_info[3]}\n'
                                                           f'Цена: ${pr_info[4]}',
                       reply_markup=buttons.choose_pr_count(pr_info[3]))
        users[user_id] = {'pr_name': pr_info[0], 'pr_count': 1}
    else:
        if call.data == 'increment':
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=buttons.choose_pr_count(
                                              database.get_exact_pr(users[user_id]['pr_name'])[3],
                                              'increment', users[user_id]['pr_count']))
            users[user_id]['pr_count'] += 1
        elif call.data == 'decrement':
            bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id,
                                          reply_markup=buttons.choose_pr_count(
                                              database.get_exact_pr(users[user_id]['pr_name'])[3],
                                              'decrement', users[user_id]['pr_count']))
            users[user_id]['pr_count'] -= 1
        elif call.data == 'back':
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            bot.send_message(user_id, 'Выберите пункт меню:',
                             reply_markup=buttons.main_menu(database.get_pr_buttons()))
        elif call.data == 'to_cart':
            pr_name = database.get_exact_pr(users[user_id]['pr_name'])[1]
            database.add_to_cart(user_id, pr_name, users[user_id]['pr_count'])
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
            bot.send_message(user_id, 'Товар помещен в корзину! Желаете что-то еще?',
                             reply_markup=buttons.main_menu(database.get_pr_buttons()))


# Админ-панель
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == 1482646413 :
        bot.send_message(message.from_user.id,
                         'Введите информацию о продукте в следующем порядке:\n\n'
                         '<b>Название, описание, количество, цена, фото</b>\n\n'
                         'Фотографию загружать на <a href="https://postimages.org/">сайте</a> '
                         'и отправлять прямую ссылку!', parse_mode='HTML')
        bot.register_next_step_handler(message, get_product)


def get_product(message):
    data = message.text.split(', ')

    if len(data) == 5:
        database.add_product(data[0].strip(), data[1].strip(),
                             data[2].strip(), data[3].strip(), data[4].strip())
        bot.send_message(message.from_user.id, 'Успешно!')
    else:
        bot.send_message(message.from_user.id, 'Ошибка в данных!')




bot.polling(non_stop=True)
