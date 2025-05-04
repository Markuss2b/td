import sqlite3

def get_all_profiles():
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Profile")
        result = cursor.fetchall()
        cursor.close()
    return result

def get_profile_with_id(id):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM Profile WHERE id = {id}')
        result = cursor.fetchone()
        cursor.close()
    return result

def get_profile_with_name(name):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Profile WHERE name = '{name}'")
        result = cursor.fetchone()
        cursor.close()
    return result

def create_profile(name):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO Profile (name, wins, losses) VALUES('{name}', 0, 0)")
        conn.commit()
        cursor.close()

def delete_profile_with_id(id):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM Profile WHERE id = {id}')
        conn.commit()
        cursor.close()


def get_all_towers():
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Tower")
        result = cursor.fetchall()
        cursor.close()
    return result

def get_tower_with_name(name):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Tower WHERE name = '{name}'")
        result = cursor.fetchone()
        cursor.close()
    return result