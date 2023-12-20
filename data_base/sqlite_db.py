import sqlite3 as sq
from keylinks import *
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect(db_name)
    cur = base.cursor()
    if base:
        print(connected)
        base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT)')
        base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM menu ORDER BY RANDOM() LIMIT 1').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]} {ret[2]}')


async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall()


async def sql_delete_command(data):
    cur.execute('''DELETE FROM menu WHERE name = ?;''', (data,))
    base.commit()
    print(deleted)
