import sqlite3 as sq

db = sq.connect('database/bot.db')
cur = db.cursor()


async def db_start():
    cur.execute('CREATE TABLE IF NOT EXISTS accounts('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'tg_id INTEGER,'
                'card_id INTEGER,'
                'active BOOLEAN DEFAULT(TRUE))')
    cur.execute('CREATE TABLE IF NOT EXISTS items('
                'ite_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'category TEXT,'
                'name TEXT,'
                'desc TEXT,'
                'price TEXT,'
                'photo TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS categories('
                'cat_id INTEGER PRIMARY KEY,'
                'name TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS cart('
                'card_id INTEGER PRIMARY KEY,'
                'tg_id INTEGER,'
                'item_id INTEGER)')
    db.commit()


async def add_user(user_id):
    user = cur.execute('SELECT * FROM accounts WHERE tg_id == {key}'.format(key=user_id)).fetchone()
    if not user:
        cur.execute('INSERT INTO accounts (tg_id) VALUES ({key})'.format(key=user_id))
        db.commit()


async def add_item(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (category, name, desc, price, photo) VALUES (?, ?, ?, ?, ?)",
                    (data['category'], data['name'], data['desc'], data['price'], data['photo']))
        db.commit()


async def get_item(item_id):
    item = cur.execute("SELECT * FROM items WHERE ite_id=?", (item_id,)).fetchone()
    return item


async def delete_item(item_id):
    cur.execute("DELETE FROM items WHERE ite_id=?", (item_id,))
    db.commit()


async def set_active(tg_id, active):
    cur.execute("UPDATE accounts set active=? WHERE tg_id=?", (active, tg_id,))
    db.commit()


async def get_user():
    users = cur.execute("SELECT tg_id, active FROM accounts").fetchall()
    return users


async def get_items_by_category(category):
    items = cur.execute("SELECT * FROM items WHERE category=?", (category,)).fetchall()
    return items


async def add_category(name):
    cur.execute('INSERT INTO categories (name) VALUES (?)', (name,))
    db.commit()


async def delete_categories(cat_id):
    cur.execute('DELETE FROM categories WHERE cat_id=?', (cat_id,))
    db.commit()


async def get_all_categories():
    categories = cur.execute('SELECT * FROM categories').fetchall()
    return categories


async def add_to_cart(tg_id, item_id):
    cur.execute('INSERT INTO cart (tg_id, item_id) VALUES (?, ?)', (tg_id, item_id))
    db.commit()


async def show_item_in_cart(tg_id):
    cur.execute('SELECT * FROM cart WHERE tg_id=?'), (tg_id,)


async def get_items_in_cart(tg_id):
    items = cur.execute("SELECT item_id FROM cart WHERE tg_id=?", (tg_id,)).fetchall()
    return [item[0] for item in items]


async def delete_items_from_cart(tg_id):
    cur.execute('DELETE FROM cart WHERE tg_id=?', (tg_id,)).fetchall()
    db.commit()


async def delete_item_from_cart(tg_id, item_id):
    cur.execute('DELETE FROM cart WHERE tg_id=? AND item_id=?', (tg_id, item_id))
    db.commit()

