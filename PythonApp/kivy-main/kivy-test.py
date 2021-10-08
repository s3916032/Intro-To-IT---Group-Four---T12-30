# Simon Bird (s3916032) - Introduction to Information Technology COSC1078
# This program is a DRAFT and should be treated as such
# It also implements Kivy 2.0.0 for the creation and rendering of applications and widgets

# The following people are credited:
#   Arjun Kumar - mobile porting
#   Liam Folie - interface design

# TODO:
#   Implement pages from guizero:
#       Splash (drafted)
#       Login (drafted)
#       Register
#       Main page

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, TransitionBase
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget

kivy.require("2.0.0")  # developer requires kivy 2.0.0


class SplashScreen(Screen):
    """
    Creates the splash screen and schedules the window to change
    """

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.switch_screen, 5)  # switch to login screen after some seconds

    def switch_screen(self, *args):
        # switches the screen manager's current window to login
        self.parent.current = 'login'


class LoginScreen(Screen):
    """
    Creates the login screen - rest is done in kv file
    """
    pass


class WindowManager(ScreenManager):
    """
    Manager for the application screens (windows)
    """

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

    # get widget ids from kv file
    splash_screen = ObjectProperty(None)
    login_screen = ObjectProperty(None)

# application class - subclass of an app - allows building apps as objects
class TestApp(App):
    """
    Creates a new kivy App with inherited widgets and such
    """

    def build(self):
        return WindowManager()


if __name__ == "__main__":
    TestApp().run()  # build and then run the test app
