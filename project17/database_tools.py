import sqlite3
import datetime


def get_categories():
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    result = cur.execute("""SELECT name FROM categories""").fetchall()
    con.close()
    catlis = tuple([i[0] for i in result])
    return catlis


def add_category(name0, icon0):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    cur.execute("""INSERT INTO categories(name,icon) VALUES(?,?)""", (name0, icon0))
    con.commit()
    con.close()


def new_note(note, amount, category):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    date_time = int(datetime.datetime.now().timestamp())
    if type(category) is int:
        category_id = category
    else:
        category_id = (cur.execute("""SELECT id FROM categories
                WHERE name = ?""", (category,)).fetchone())[0]
    cur.execute("""INSERT INTO transactions(action_title,money_amount,date_time,category_id) VALUES(?,?,?,?)""",
                (note, amount, date_time, category_id))
    con.commit()
    con.close()


def history(n):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    notes = cur.execute("""SELECT
        categories.icon,
        transactions.action_title,
        transactions.money_amount,
        transactions.date_time,
        categories.name
    FROM
        transactions
    INNER JOIN categories
        ON transactions.category_id = categories.id""").fetchmany(n)
    con.close()
    return notes


def get_alerts(title="", description=""):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    alert_list = cur.execute("""SELECT title, description FROM alerts""").fetchall()
    if title != "":
        cur.execute("""INSERT INTO alerts(title,description) VALUES(?,?)""", (title, description))
        con.commit()
    con.close()
    return alert_list


def update_config(binds0=None, notifications0=None, important0=None, money0=None, minmoney0=None):
    f = (open("config.txt"))
    binds, notifications, important, money, minmoney = f.read().split()
    f.close()
    if binds0 is not None:
        binds = binds0
    if notifications0 is not None:
        notifications = notifications0
    if important0 is not None:
        important = important0
    if money0 is not None:
        money = money0
    if minmoney0 is not None:
        minmoney = minmoney0
    f = open("config.txt", "w")
    f.write(" ".join(map(str, [binds, notifications, important, money, minmoney])))
    f.close()
    return int(binds), int(notifications), important, int(money), int(minmoney)


def edit_automation(a_id, caption, money, cooldown, repeat, category_name):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    cur.execute("""UPDATE automatic
            SET caption = ?
            WHERE id = ?""", (caption, a_id))
    cur.execute("""UPDATE automatic
            SET money = ?
            WHERE id = ?""", (money, a_id))
    cur.execute("""UPDATE automatic
            SET cooldown = ?
            WHERE id = ?""", (cooldown, a_id))
    cur.execute("""UPDATE automatic
            SET repeat = ?
            WHERE id = ?""", (repeat, a_id))
    cur.execute("""UPDATE automatic
            SET category_id =(
            SELECT id FROM categories
            WHERE name = ?)
            WHERE id = ?""", (category_name, a_id))
    con.commit()
    con.close()


def del_plan(a_id):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    cur.execute("""DELETE from automatic
                                        WHERE id = ?""", (a_id,))
    con.commit()
    con.close()


def script_cards(is_repeat=True):
    con = sqlite3.connect("finance.sqlite3")
    cur = con.cursor()
    res = cur.execute("""SELECT caption, money, cooldown, id, category_id
                FROM automatic
                WHERE repeat = ?""", (int(is_repeat),)).fetchall()
    con.close()
    return res

