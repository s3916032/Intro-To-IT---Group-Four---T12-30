# DRAFT - DO NOT SHOWCASE

import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
kivy.require("2.0.0")  # user requires kivy 2.0.0


# gridlayout is a window which stores widgets in a grid layout
class LoginScreen(GridLayout):
    """
    Creates the login screen with necessary widgets
    """
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='Username'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


# application class - subclass of an app - allows building apps as objects
class TestApp(App):
    """
    Creates a new kivy App with inherited widgets and such
    """
    def build(self):
        return LoginScreen()


if __name__ == "__main__":
    TestApp().run()
