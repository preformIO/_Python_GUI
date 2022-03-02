from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# ---------------------
# database handling
# ---------------------
import sqlite3
# source tutorial: https://www.youtube.com/watch?v=byHcYRpMgI4
def db_init(db_name = 'profile.db', table_name = "users"):
    # connect to database
    # database file is created if it doesn't exist
    conn = sqlite3.connect(db_name)
    # use line below instead if you'd like to use a sqlite database in temporary memory only
    # conn = sqlite3.connect(':memory:')
    #
    # create a cursor
    c = conn.cursor()
    # create a table | DATYPES: null, integer, real, text, blob
    c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            un text,
            pw text,
            first_name text,
            last_name text,
            email text,
            interests text
        )
    """)
    # commit our command
    conn.commit()
    # close connection (good practice)
    conn.close()

    print(f'Initialized database "{db_name}" and table "{table_name}".')

    return

def db_newprofile(
    un, 
    pw, 
    fn, 
    ln, 
    em, 
    int,
    db_name = 'profile.db'
):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    if not db_un_exists(un):
        c.execute(f"""INSERT INTO users VALUES (
                '{un}', 
                '{pw}', 
                '{fn}', 
                '{ln}', 
                '{em}', 
                '{int}'
            )
        """)
        conn.commit()
        print(f'Created new profile for "{un}".')
        pass
    else:
        print(f'CANNOT create new profile. Profile for "{un}" already exists.')
        pass

    conn.close()


    return

def db_login(un, pw, db_name = 'profile.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"""SELECT rowid, first_name 
        FROM users 
        WHERE un = '{un}' 
        AND pw = '{pw}'
    """)
    # first_name = c.fetchone()
    # first_name = c.fetchmany(3)
    first_name = c.fetchall()

    result = True if len(first_name) else False

    print(f'db_login("{un}", "{pw}") result = "{result}"')

    conn.close()

    return result

def db_update_profile(un, **kwargs):
    # handle default kwargs
    if "db_name" not in kwargs.keys():
        db_name = 'profile.db'

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for key in kwargs.keys():
        c.execute(f"""UPDATE users 
            SET '{key}' = '{kwargs[key]}'
            WHERE un = '{un}'
        """)

    print(f'db_update_profile({un}, {kwargs}) executed.')

    conn.commit()
    conn.close()

    return

def db_un_exists(un, db_name = 'profile.db'):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(f"""SELECT un 
        FROM users 
        WHERE un = '{un}'
    """)
    un_result = c.fetchall()

    result = True if len(un_result) else False

    print(f'db_un_exists("{un}") result = "{result}"')

    conn.close()

    return result

# ----------------------
# Kivy Window management
# ----------------------
class SplashWindow(Screen):
    pass

class LoginWindow(Screen):

    def login_released(self, usnm_input, passw_input):
        usnm_input.text = ""
        passw_input.text = ""

        return

    pass

class ProfileWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

# ----------------------
# Main Kivy app
# ----------------------
class MyMainApp(App):
    def build(self):
        return kv
    pass


# ----------------------
# Main application function
# ----------------------
if __name__ == "__main__":
    # Database initialization and tests
    db_init()
    db_newprofile(
        'davidDelSol',
        'encrypted?',
        'david',
        'aloka',
        'test@preform.io',
        'salsa,extended intelligence,marathon running in a full suit'
    )
    db_newprofile(
        'Python733t',
        'encrypted?',
        'Doroteo ',
        'Bonilla',
        'doabonilla@yahoo.com',
        'work,school,sleep,repeat'
    )
    db_login('davidDelSol', 'encrypted?')
    db_update_profile('davidDelSol', pw = 'definitelyNotEncripted!')
    db_login('davidDelSol', 'definitelyNotEncripted!')
    db_un_exists('davidDelSol')

    # Run Kivy app
    MyMainApp().run()