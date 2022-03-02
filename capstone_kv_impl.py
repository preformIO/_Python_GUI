import string
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

def db_profile_new(
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

def db_profile_print(*args, **kwargs):
    uns = []
    print_all = False
    profiles = []
    if len(args):
        for arg in args:
            if type(arg) == str:
                uns.append(arg)
            if type(arg) == list and len(arg) and type(arg[0]) == str:
                for un in arg:
                    uns.append(un)
    
    # print(f'uns = {uns}')

    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = 'profile.db'
        pass
    else:
        db_name = kwargs['db_name']
        pass
    if 'all' in kwargs.keys():
        # print all profiles
        print_all = kwargs['all']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if print_all:
        c.execute(f"""SELECT rowid, * 
            FROM users
            ORDER BY un
        """)
        profiles = c.fetchall()
        pass
    else:
        for un in uns:
            print(f'un = {un}')
            c.execute(f"""SELECT rowid, *
                FROM users 
                WHERE un = '{un}'
            """)
            profiles.append(c.fetchone())


    result = True if len(profiles) else False

    print(f'db_profile_print("*{args}, **{kwargs}") profiles =')
    for profile in profiles:
        print(profile)

    conn.close()

    return result

def db_un_login(un, pw, db_name = 'profile.db'):
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

    print(f'db_un_login("{un}", "{pw}") result = "{result}"')

    conn.close()

    return result

def db_profile_update(un, **kwargs):
    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = 'profile.db'
        pass
    else:
        db_name = kwargs['db_name']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    for key in kwargs.keys():
        c.execute(f"""UPDATE users 
            SET '{key}' = '{kwargs[key]}'
            WHERE un = '{un}'
        """)

    print(f'db_profile_update({un}, {kwargs}) executed.')

    conn.commit()
    conn.close()

    return

def db_profile_delete(un, **kwargs):
    # handle default kwargs
    if 'db_name' not in kwargs.keys():
        db_name = 'profile.db'
        pass
    else:
        db_name = kwargs['db_name']
        pass

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(f"""DELETE from users 
        WHERE un = '{un}'
    """)

    print(f'db_profile_delete({un}) profile deleted, if it existed in the first place.')

    conn.commit()
    conn.close()

    return

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
    db_un_exists('userNameThatDoesNotExist')
    db_profile_delete('userNameThatDoesNotExist')
    db_profile_delete('davidDelSol')
    db_profile_new(
        'davidDelSol',
        'encrypted?',
        'david',
        'aloka',
        'test@preform.io',
        'salsa,extended intelligence,marathon running in a full suit'
    )
    db_profile_new(
        'Python733t',
        'encrypted?',
        'Doroteo ',
        'Bonilla',
        'doabonilla@yahoo.com',
        'work,school,sleep,repeat'
    )
    db_un_login('davidDelSol', 'encrypted?')
    db_profile_update('davidDelSol', pw = 'definitelyNotEncripted!')
    db_un_login('davidDelSol', 'definitelyNotEncripted!')
    db_un_exists('davidDelSol')
    db_profile_print(all = True)
    db_profile_print(['Python733t'])
    db_profile_print('Python733t')

    # Run Kivy app
    MyMainApp().run()