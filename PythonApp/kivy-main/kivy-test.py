# Simon Bird (s3916032) - Introduction to Information Technology COSC1078
# It also implements Kivy 2.0.0 for the creation and rendering of applications and widgets

# The following people are credited:
#   Arjun Kumar - mobile porting
#   Liam Folie - interface design

# ----------------------------------------------------------------------------------------------------------
# NOTE:
#   Do NOT input sensitive information (such as an actual password) into the user_info.txt file or fields!
#   The stored information is not secured at all and is written in plain text.
#   If you are testing the register/login, random common names and simple-worded passwords are ideal
#
#   Furthermore, the app can only store one user on file for security purposes - I definitely do not want
#   a lot of files containing potentially personal information!
# ----------------------------------------------------------------------------------------------------------

# TODO:
#   Implement pages:
#       Login - layout, button to switch to register, switch to pin if logged in
#       Register - layout, button to switch to login
#       PIN - layout, error label
#       Main page

# Possible additions:
#   Account page (log out, change PIN, change account)
#   Email address (not very necessary for a basic prototype)
#   Store multiple accounts

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
ILLEGAL_CHARS = "/\\][}{)(`~ "


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
        self.current_user = {'name': '', 'pass': ''}  # temporarily stores the current user
        self.button_text = 'Login'  # label to print on the button

    def check_information(self):
        # check user's information in a file and then clears the variable (it's still insecure!)
        self.current_user['name'] = self.ids.username_field.text
        self.current_user['pass'] = self.ids.password_field.text

        # check if the user info file exists
        if os.path.isfile(self.file):
            print(str(self.file) + " exists. Checking for information...")
            file = open(self.file, "r")  # open the file in read mode

            # if the user's current login info matches the current file line, validate and go to PIN
            count = 0
            for line in file.readlines():
                count += 1
                # if the user is in the line...
                if str(self.current_user) in line:
                    print("User validated. Name: " + self.current_user['name'] + " Pass: " + self.current_user['pass'])
                    self.current_user['name'] = ''  # clear the username...
                    self.current_user['pass'] = ''  # ...and the password
                    self.switch_pin()
                else:
                    # otherwise, invalidate and display an error
                    print("User does not exist.")
                    self.ids.login_error.size_hint_y = 1

            # if there is no line in the file, register a user
            print("Read " + str(count) + " lines.")
            if count <= 0:
                print("No user exists in " + str(self.file))
                self.switch_register()

    def switch_register(self):
        # switches the screen manager's current window to Register
        self.parent.current = 'register'

    def switch_pin(self):
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
        self.button_text = 'Register'  # button to display on the page

    def check_information(self):
        # overwrites the user info file with the register information
        self.current_user['name'] = self.ids.username_field.text
        self.current_user['pass'] = self.ids.password_field.text

        # if the length of the name/pass is nothing or contains illegal characters, do nothing
        for char in self.current_user['name']:
            if char in ILLEGAL_CHARS:
                self.ids.login_error.text = "The following characters are not allowed '" + ILLEGAL_CHARS + "'"
        if self.current_user['name'].replace(" ", "") <= '' or self.current_user['pass'].replace(" ", "") <= '':
            print("Invalid credentials!")
            self.ids.login_error.size_hint_y = 1
        else:
            # otherwise, truncate the user info file
            print(str(self.file) + " is being truncated... PIN reset")
            file = open(self.file, "w")  # open and truncate the file...
            file.writelines(str(self.current_user))  # ... then write the user to the file
            file.close()  # close the file
            print("Done! Switching screens to login...")
            self.current_user['name'] = ''  # reset name...
            self.current_user['pass'] = ''  # ...and password
            self.switch_login()  # switch the current screen to register

    def switch_login(self, *args):
        # switches the screen manager's current window to login
        self.parent.current = 'login'


class PinScreen(Screen):
    """
    Creates the PIN Screen and checks the user PIN in the user_info file.\n
    If a PIN exists, request the PIN. If it doesn't, request a PIN to enter.\n
    If the user logs in or registers, the PIN should need to be set again.
    """

    def __init__(self, **kwargs):
        super(PinScreen, self).__init__(**kwargs)
        self.current_pin = {'pin': ''}  # user's entered pin as a dict
        self.pin_exists = False  # does a PIN exist in the user info file?
        self.label_text = 'Enter PIN'
        self.check_pin_exists()  # check if the PIN does indeed exist

    def check_pin_exists(self):
        # checks if a pin exists and then returns True or False

        file = open("user_info.txt", "r")  # open the user info file
        count = 0
        self.pin_exists = False
        for line in file.readlines():
            # if the user info file does not contain a pin, set it
            count += 1
            if count == 2 and 'pin' in line:
                print("PIN found. Does not need to be set.")
                self.pin_exists = True

        if not self.pin_exists:
            print("PIN not found. Needs to be set.")
            self.label_text = 'Set PIN'

        file.close()

    def on_pin_entered(self):
        # the 'enter pin' button should call this method so the pin screen can choose to check or set

        if self.pin_exists:
            print("Running PIN check method")
            self.check_pin()
        else:
            print("Running PIN set method")
            self.set_pin()

    def check_pin(self):
        # checks the pin against the one in the user file and then goes to main screen
        # this function is not very well optimised - it should be ok for a prototype, but tread carefully

        self.current_pin['pin'] = self.ids.pin_field.text  # get the PIN from the input field
        # if the pin is not a length of 4, it contains spaces, or it contains non-digit characters, it's invalid
        if len(self.current_pin['pin']) != 4 or not self.current_pin['pin'].isdigit():
            print("Invalid PIN!")
        else:
            # otherwise, check the PIN in the file
            file = open("user_info.txt", "r")

            # check the second line of the file
            count = 0
            for line in file.readlines():
                # if the PIN is in the file, validate and go to main screen
                print("Checking line " + str(count) + "...")
                count += 1
                if count == 2:
                    print("PIN found in user_info.txt at line " + str(count))
                    # check if the PIN is valid
                    if str(self.current_pin) == line:
                        count = 0
                        file.close()  # close the file
                        print("PIN correct. Switching to main...")
                        self.switch_main()  # go to the main screen
                        self.current_pin['pin'] = ''  # reset the entered pin
                        break  # break the loop prematurely
                    else:
                        print("PIN incorrect.")
            file.close()

    def set_pin(self):
        # sets the current pin of the user and adds it to the user_info file

        self.current_pin['pin'] = self.ids.pin_field.text  # get the PIN from the input field
        if len(self.current_pin['pin']) != 4 or not self.current_pin['pin'].isdigit():
            print("Invalid PIN!")
        else:
            # reads a file and appends text to it
            self.current_pin['pin'] = self.ids.pin_field.text  # get the PIN from the input field
            file = open("user_info.txt", "a")  # open the file in append mode
            file.writelines("\n" + str(self.current_pin))  # append the line to the end
            print("PIN Set to " + self.current_pin['pin'])
            file.close()
            self.current_pin['pin'] = ''  # reset current pin
            # check if the pin now exists
            self.check_pin_exists()
            if self.pin_exists:
                self.on_pin_entered()  # finally, run the check or set method again
            else:
                print("An error has occurred. The application will now exit.")
                test_app.stop()  # exit the application

    def switch_main(self, *args):
        # switches the screen manager's current window to main
        self.parent.current = 'main'


class MainScreen(Screen):
    """
    Creates the main screen
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
    Creates a new kivy App with the ScreenManager as the root widget
    """

    def build(self):
        Window.size = (250, 500)  # set window size to 250 x 500
        check_integrity()
        return WindowManager()


def check_integrity():
    # check if the user info file exists and create it if it doesn't
    if os.path.isfile("user_info.txt"):
        print("User info file exists.")
    else:
        print("Creating user info file...")
        file = open("user_info.txt", "x")
        file.close()


if __name__ == "__main__":
    test_app = TestApp()  # build and then run the test app
    test_app.run()
