# Simon Bird (s3916032) - Introduction to Information Technology COSC1078
# This program is a DRAFT and should be treated as such
# It also implements Kivy 2.0.0 for the creation and rendering of applications and widgets

# The following people are credited:
#   Arjun Kumar - mobile porting
#   Liam Folie - interface design

# TODO:
#   Implement pages from guizero:
#       Login (drafted)
#       Register
#       Main page

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import *
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
import os

kivy.require("2.0.0")  # developer requires kivy 2.0.0


class SplashScreen(Screen):
    """
    Creates the splash screen and schedules the window to change
    """

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.switch_login, 3)  # switch to login screen after some seconds

    def switch_login(self, *args):
        # switches the screen manager's current window to login
        self.parent.current = 'login'


class LoginScreen(Screen):
    """
    Creates the login screen and checks the user's info.\n
    If the info exists in file, skip to PIN. Otherwise, alert the user.
    """

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.file = "user_info.txt"  # file to check
        self.current_user = {'name': '', 'pass': ''}  # stores the current user, after each check it gets erased
        self.button_text = 'Login'  # label to print on the button

    def check_information(self):
        # check user's information in a file and then clears the variable (it's still insecure!)
        self.current_user['name'] = self.ids.username_field.text
        self.current_user['pass'] = self.ids.password_field.text

        # check if the user info file exists
        if os.path.isfile(self.file):
            print("user_info.txt exists. Checking for information...")
            file = open(self.file, "r")  # open the file in read mode

            # if the user's current login info matches the file, validate and go to PIN
            if str(self.current_user) in file:
                print("User validated. Name: " + self.current_user['name'] + " Password: " + self.current_user['pass'])
                self.current_user['name'] = ''  # delete the username entry
                self.current_user['pass'] = ''  # delete the password, too
                trigger = Clock.create_trigger(self.switch_pin)  # create a trigger (call once) to switch to PIN screen
                trigger()  # call the trigger
            else:
                # otherwise, invalidate and display an error
                print("User does not exist.")
                self.ids.login_error.text_size = (12, 12)
        else:
            # if the user info file does not exist, create it
            print(str(self.file) + " does not exist. Writing file...")
            file = open(self.file, "x")  # create and open the file...
            file.close()  # ...then close the file
            print("Done!\nFile exists: " + str(os.path.isfile(self.file)))
            print("Switching screens to register...")
            self.switch_register()  # switch the current screen to register

    def switch_register(self, *args):
        # switches the screen manager's current window to Register
        self.parent.current = 'register'

    def switch_pin(self, *args):
        # switches the screen manager's current window to PIN
        self.parent.current = 'pin'


class RegisterScreen(Screen):
    """
    Creates the register screen and requests user information to store.\n
    Does not actually register anywhere other than a single file with a single line.\n
    This file is overwritten whenever the user re-registers.
    """
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.file = "user_info.txt"  # file to check
        self.current_user = {'name': '', 'pass': ''}  # stores the current user to add to the file
        self.validated = False  # is the user info correct?
        self.button_text = 'Register'

    def check_information(self):
        # overwrites the user info file with the register information
        self.current_user['name'] = self.ids.username_field.text
        self.current_user['pass'] = self.ids.password_field.text

        # if the length of the name/pass is nothing, do nothing
        if self.current_user['name'].replace(" ", "") <= '' or self.current_user['pass'].replace(" ", "") <= '':
            print("Invalid credentials!")
        else:
            # otherwise, truncate the user info file
            print(str(self.file) + " is being truncated...")
            file = open(self.file, "w")  # open and truncate the file...
            file.write(str(self.current_user))  # write the user to the file
            file.close()
            print("Done!\nFile exists: " + str(os.path.isfile(self.file)))
            print("Switching screens to login...")
            self.switch_login()  # switch the current screen to register

    def switch_login(self, *args):
        # switches the screen manager's current window to login
        self.parent.current = 'login'


class PinScreen(Screen):
    """
    Creates the PIN Screen and checks the user PIN.\n
    If a PIN exists, request the PIN. If it doesn't, request a PIN to enter.
    """
    pass


class WindowManager(ScreenManager):
    """
    Manager for the application screens ('windows').
    """

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        self.transition = FadeTransition()

    # get widget ids from kv file
    splash_screen = ObjectProperty(None)
    login_screen = ObjectProperty(None)
    register_screen = ObjectProperty(None)
    pin_screen = ObjectProperty(None)


# application class - subclass of an app - allows building apps as objects
class TestApp(App):
    """
    Creates a new kivy App with inherited widgets and such
    """

    def build(self):
        Window.size = (250, 500)  # set window size to 250 x 500
        return WindowManager()


if __name__ == "__main__":
    TestApp().run()  # build and then run the test app
