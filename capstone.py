# from adodbapi.examples.db_print import db
import adodbapi.ado_consts as adc

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from app import sm, invalidForm
from database import DataBase

class CreateAccountWindow(Screen): #create an account window.
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.name.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.name.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen): # create login window
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBotton(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBotton(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class KivyApp(App):
    def build(self):
        self.title = "Login Screen"
        Window.size = (400, 200)
        layout = GridLayout(cols=2, rows=2, padding=10, spacing=10, row_default_height=30)
        usernameinput = TextInput()
        print(usernameinput.text)
        passwordinput = TextInput(password=True)
        usernamelbl = Label(text="Username", size_hint_x=None, width=100)
        passwordlbl = Label(text="Password", size_hint_x=None, width=100)

        layout.add_widget(usernamelbl)
        layout.add_widget(usernameinput)
        layout.add_widget(passwordlbl)
        layout.add_widget(passwordinput)

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        main_layout.add_widget(layout)

        loginbutton = Button(text="Login")

        main_layout.add_widget(loginbutton)

        return main_layout


if __name__ == '__main__':
  print("Hello world!")
  print(f"adc = {adc}")
  # print(f"db = {db}")

  app = KivyApp()
  app.run()