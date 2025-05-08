# Работа с базой данных
import sqlite3


# Подключение к БД
connection = sqlite3.connect('delivery.db', check_same_thread=False)
# Python + SQL
sql = connection.cursor()


# Создание таблиц
sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(user_id INTEGER, user_name TEXT, user_num TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS products '
            '(pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, '
            'pr_price REAL, pr_photo TEXT);')
sql.execute('CREATE TABLE IF NOT EXISTS cart '
            '(user_id INTEGER, user_pr TEXT, user_pr_count INTEGER);')



## Методы пользователя ##
# Регистрация
def register(user_id, user_name, user_num):
    sql.execute('INSERT INTO users VALUES (?, ?, ?);',
                (user_id, user_name, user_num))
    # Фиксируем изменения
    connection.commit()


# Проверка на наличие пользователя в БД
def check_user(user_id):
    if sql.execute('SELECT * FROM users WHERE user_id=?;', (user_id,)).fetchone():
        return True
    else:
        return False


## Методы продуктов ##
# Вывод всех продуктов
def get_all_pr():
    return sql.execute('SELECT * FROM products;').fetchall()


# Получение товаров для кнопок
def get_pr_buttons():
    all_products = get_all_pr()
    in_stock = [p[:2] for p in all_products if p[3] > 0]

    return in_stock


# Вывод определенного товара
def get_exact_pr(pr_id):
    return sql.execute('SELECT * FROM products WHERE pr_id=?;', (pr_id,)).fetchone()


# Вывод цены товара по имени
def get_exact_price(pr_name):
    return sql.execute('SELECT pr_price FROM products WHERE pr_name=?;', (pr_name,)).fetchone()


## Методы корзины ##
# Добавление товара в корзину
def add_to_cart(user_id, user_product, user_pr_count):
    sql.execute('INSERT INTO cart VALUES (?, ?, ?);', (user_id, user_product, user_pr_count))
    # Фиксируем изменения
    connection.commit()


# Очистка корзины
def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    # Фиксируем изменения
    connection.commit()


# Отображение корзины
def show_cart(user_id):
    return sql.execute('SELECT * FROM cart WHERE user_id=?;', (user_id,)).fetchall()



# Оформление
def make_order(user_id):
    user_products = sql.execute('SELECT user_pr FROM cart WHERE user_id=?;', (user_id,)).fetchall()
    user_pr_counts = sql.execute('SELECT user_pr_count FROM cart WHERE user_id=?;', (user_id,)).fetchall()

    stock_quantity = [sql.execute('SELECT pr_count FROM products WHERE pr_name=?;', (p[0],)).fetchone()[0]
                      for p in user_products]

    totals = []

    for i in range(len(stock_quantity)):
        totals.append(stock_quantity[i] - user_pr_counts[i][0])

    for t in range(len(user_products)):
        sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;', (totals[t], user_products[t][0]))

    # Фиксируем изменения
    connection.commit()
    return totals, stock_quantity


## Админ-панель ##
# Добавление продукта в БД
def add_product(pr_name, pr_des, pr_count, pr_price, pr_photo):
    sql.execute('INSERT INTO products (pr_name, pr_des, pr_count, pr_price, pr_photo) '
                'VALUES (?, ?, ?, ?, ?);', (pr_name, pr_des, pr_count, pr_price, pr_photo))
    # Фиксируем изменения
    connection.commit()
