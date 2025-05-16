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

def add_profile_win_by_name(name):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Profile SET wins = wins + 1 WHERE name = '{name}'")
        conn.commit()
        cursor.close()

def add_profile_loss_by_name(name):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Profile SET losses = losses + 1 WHERE name = '{name}'")
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

def get_enemy_with_title(title):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM Enemy WHERE title = '{title}'")
        result = cursor.fetchone()
        cursor.close()
    return result

def get_all_enemies():
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Enemy")
        result = cursor.fetchall()
        cursor.close()
    return result

def update_enemy(enemy_title, health, speed, attack):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"UPDATE Enemy SET health = {health}, speed = {speed}, attack = {attack} WHERE title = '{enemy_title}'")
        conn.commit()
        cursor.close()

def add_game_in_history(player_id, map_name, game_result, wave, towers_placed, seconds):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO game_history (player_id, map_name, result, wave, towers_placed, seconds) VALUES({player_id}, '{map_name}', '{game_result}', {wave}, {towers_placed}, {seconds})")
        result = cursor.fetchone()
        cursor.close()
    return result

def get_history_with_id(player_id):
    with sqlite3.connect('towerdefense.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM game_history WHERE player_id = '{player_id}'")
        result = cursor.fetchall()
        cursor.close()
    return result