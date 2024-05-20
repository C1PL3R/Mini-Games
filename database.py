import sqlite3

with sqlite3.connect("mini_game.db") as conn:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS game 
                   (id INTEGER,
                   name TEXT,
                   link TEXT,
                   score INTEGER DEFAULT 0 CHECK(typeof(score) = 'integer'),
                   skin TEXT DEFAULT standart,
                   
                   group_id INTEGER,
                   group_name TEXT,
                   group_link TEXT,
                   answer INTEGER DEFAULT 0,
                   x2_score INTEGER DEFAULT 1,
                   lang TEXT DEFAULT en,

                   premium_stars INEGER DEFAULT 0,
                   premium INTEGER DEFAULT 0)""")
                   
    cursor.execute("""CREATE TABLE IF NOT EXISTS skins
                   (id INTEGER,
                   basketball_ball_skin INTEGER DEFAULT 0,
                   soccer_ball_skin INTEGER DEFAULT 0,
                   volleyball_ball_skin INTEGER DEFAULT 0,
                   football_ball_skin INTEGER DEFAULT 0,
                   fire_skin INTEGER DEFAULT 0,
                   note_skin INTEGER DEFAULT 0,
                   snow_skin INTEGER DEFAULT 0,
                   sword_skin INTEGER DEFAULT 0,
                   fire_heart_skin INTEGER DEFAULT 0,
                   purple_heart_skin INTEGER DEFAULT 0,
                   table_tennis_skin INTEGER DEFAULT 0,
                   trophy_skin INTEGER DEFAULT 0,
                   poo_skin INTEGER DEFAULT 0,
                   star_skin INTEGER DEFAULT 0,
                   premium_star_skin INTEGER DEFAULT 0)""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS online
                   (id INTEGER,
                   name TEXT,
                   online INTEGER DEFAULT 0,
                   opponent_id INTEGER DEFAULT 0,
                   my_id INTEGER DEFAULT 0)""")
