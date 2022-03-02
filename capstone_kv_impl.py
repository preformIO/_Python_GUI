from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


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


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()