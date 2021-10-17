# Simon Bird (s3916032) - Introduction to Information Technology COSC1078
# It also implements Kivy 2.0.0 for the creation and rendering of applications and widgets

# The following people are credited:
#   Arjun Kumar - mobile porting
#   Liam Folie - interface design

# ----------------------------------------------------------------------------------------------------------
#   [NOTE]:
#
#   Do NOT input sensitive information (such as an actual password) into the user_info.txt file or fields!
#
#   The stored information is not secured at all and is written in plain text. Ideally, if we were to
#   implement an online database for the users, there would not be a storage file at all.
#
#   If you are testing the register/login, random common names and simple-worded passwords are ideal.
#
#   Furthermore, the app can only store one user on file for security purposes - I definitely do not want
#   a lot of files containing potentially personal information!
# ----------------------------------------------------------------------------------------------------------

# TODO:
#   Implement pages:
#       Login - layout, button to switch to register, switch to pin if logged in
#       Register - layout, button to switch to login
#       PIN - layout, error label
#       Main page - layout, generate token, open/lock lockers (locker is_hired, is_locked)

# Possible additions:
#   Account page (log out, change PIN, change username/password)
#   Email address (not very necessary for a basic prototype)
#   Store multiple accounts (would need to change file read to read pin at top line, all users below)
#   Timeout tokens after around 1 hour


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
from random import random

kivy.require("2.0.0")  # developer requires kivy 2.0.0
ILLEGAL_CHARS = "/\\][}{)(`~ "

__version__ = "0.1"

def generate_token():
    # generates a random four-digit string and returns it
    token = "{:04d}".format(int(random() * 10000))  # format to four digits
    return token  # call setter


def token_is_equal(value_one, value_two):
    # checks if a token is equal to another token
    if value_one == value_two:
        return True
    else:
        return False


class User:
    """
    A user holds a username, password, and one hired locker and its token.

    Otherwise, a user does not boast any special qualities
    """

    def __init__(self, username, password):
        """
        :param str username:
            (required) User's username
        :param str password:
            (required) User's password
        """
        self.username = username
        self.password = password
        self.current_locker = None  # locker the user is currently hiring
        self.current_token = None  # user's token - it should match the locker they are currently hiring
        self.is_hiring = False  # is the user currently hiring a locker?

    def __repr__(self):
        # represent overload
        represent = 'User ' + self.username + ' is hiring ' + ('no locker.' if self.is_hiring is False else
                                                               'Locker ' + self.current_locker.name)

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if 3 < len(value) <= 20:
            self.__username = value
        else:
            print("ERROR: USERNAME INCORRECT LENGTH.\nUsername must be between 4 and 20 characters.")

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if 3 < len(value) <= 20:
            self.__password = value
        else:
            print("ERROR: PASSWORD INCORRECT LENGTH.\nPassword must be between 4 and 20 characters.")

    @property
    def current_locker(self):
        return self.__current_locker

    @current_locker.setter
    def current_locker(self, value):
        self.__current_locker = value

    @property
    def current_token(self):
        return self.__current_token

    @current_token.setter
    def current_token(self, value):
        self.__current_token = value

    @property
    def is_hiring(self):
        return self.__is_hiring

    @is_hiring.setter
    def is_hiring(self, value):
        self.__is_hiring = value


class Locker:
    """
    A locker holds a locked/unlocked state and can only be opened using a generated token.

    Token generation is rudimentary and insecure. It is merely a random four-digit string and a single letter
    to signify the owning locker.

    When a user hires a locker, the token is generated until they unlock the locker again.

    The token is not stored on file - that would be too unsafe!
    """

    def __init__(self, name, is_locked=True):
        """
        :param bool is_locked:
            (default True) Is the locker currently locked?
        :param str name:
            (required) Locker's name representation - case sensitive
        """
        self.is_locked = is_locked
        self.is_hired = False  # is the locker currently hired?
        self.name = name  # the name representation of the locker (e.g A) - this is case sensitive
        self.current_token = 'NONE'  # current token of the locker - defaults to 0000

    def __repr__(self):
        # represent overload
        represent = ('Locker ' + self.name + ' is ' + ('locked. ' if self.is_locked else ' unlocked. ') +
                     'Its current token is ' + self.current_token)
        return represent

    @property
    def current_token(self):
        return self.__current_token

    @current_token.setter
    def current_token(self, value):
        # tries to set the token of the locker if it is valid (correct type, length and value)
        try:
            self.__current_token = str(value + self.name)
        except ValueError:
            print("Incorrect token value!")
        except TypeError:
            print("Incorrect token type! Token is String.")
        else:
            if len(self.current_token) != 5:
                print("Token is invalid. Token length is: " + str(len(self.current_token)))
                self.__current_token = 'NONE' + self.name
        finally:
            print("Token generated by Locker " + self.name + ": " + self.current_token)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def is_locked(self):
        return self.__is_locked

    @is_locked.setter
    def is_locked(self, value):
        self.__is_locked = value

    @property
    def is_hired(self):
        return self.__is_hired

    @is_hired.setter
    def is_hired(self, value):
        self.__is_hired = value

    def unlock(self, user=None):
        # unlocks the locker after checking if the user's token is valid
        if user is None:
            user = test_app.user
        if token_is_equal(self.current_token, user.current_token):
            self.is_locked = False
            print(user.username + " unlocked Locker " + self.name)
        else:
            print("Token is invalid!")

    def lock(self, user=None):
        # locks the locker after checking if the user's token is valid
        if user is None:
            user = test_app.user
        if token_is_equal(self.current_token, user.current_token):
            self.is_locked = True
            print(user.username + " unlocked Locker " + self.name)
        else:
            print("Token is invalid!")

    def hire(self, user=None):
        # sets this locker and user to hired/hiring and generates a token for the user and locker
        # this method should be called by the attached button
        # by default, user is the application user
        if user is None:
            user = test_app.user  # if no user is passed, set it to the app user

        if not user.is_hiring:
            self.is_hired = True  # set the locker to hired
            user.is_hiring = True
            token = generate_token()  # generate the new token
            self.current_token = token  # set the locker's token to the new token
            user.current_locker = self  # set the user's current locker to this locker
            user.current_token = self.current_token  # finally, set the user's token to the new token
            print(user.username + " is hiring " + self.name)
        else:
            print("Locker " + user.current_locker.name + " is already hired by " + user.username)

    def cancel_hire(self, user=None):
        # sets this locker and user to not hired/hiring and generates a token for the user and locker
        # this method should be called by the attached button
        # by default, user is the application user
        if user is None:
            user = test_app.user  # if no user is passed, set it to the app user

        if user.is_hiring:
            self.is_hired = False  # set the locker to not hired
            user.is_hiring = False
            self.current_token = None  # reset the token
            user.current_locker = None  # set the user's current locker to none
            user.current_token = None  # finally, set the user's token to none
            print("Locker " + self.name + " is no longer hired by " + user.username)
        else:
            print(user.username + " is not hiring a locker.")


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
                    test_app.user = User(self.current_user['name'], self.current_user['pass'])  # set app user
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
        for char in self.current_user['name'] + self.current_user['pass']:
            if char in ILLEGAL_CHARS:
                self.ids.login_error.text = "The following characters are not allowed '" + ILLEGAL_CHARS + "'"
        if len(self.current_user['name']) < 4 or len(self.current_user['pass']) < 4:
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

    def switch_login(self):
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
        # checks if a pin exists and then sets the pin_exists value

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
                        count = 0  # reset the count
                        file.close()  # close the file
                        print("PIN correct. Switching to main...")
                        self.switch_main()  # go to the main screen
                        self.current_pin['pin'] = ''  # reset the entered pin
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

    def switch_main(self):
        # switches the screen manager's current window to main
        self.parent.current = 'main'


class MainScreen(Screen):
    """
    Creates the main screen with three hireable lockers.

    On this screen, there are three buttons representing the lockers and one button to lock/unlock.
    """

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.lockers = [Locker('A'), Locker('B'), Locker('C')]  # list of virtual lockers on this screen
        print("Lockers created:")
        for locker in self.lockers:
            print(repr(locker))

    def hire_locker(self, button):
        # calls a locker's hire or cancel_hire method, passing the app user as the user
        if button == self.ids.button_hire_a:
            if test_app.user.current_locker is None:
                self.lockers[0].hire(test_app.user)
                self.ids.locker_label.text = 'Locker ' + self.lockers[0].name + ' hired.'
                self.ids.button_hire_a.text = 'Cancel Locker A'
            else:
                self.lockers[0].cancel_hire(test_app.user)
                self.ids.locker_label.text = ''
                self.ids.button_hire_a.text = 'Hire Locker A'
        elif button == self.ids.button_hire_b:
            if test_app.user.current_locker is None:
                self.lockers[1].hire(test_app.user)
                self.ids.locker_label.text = 'Locker ' + self.lockers[1].name + ' hired.'
                self.ids.button_hire_b.text = 'Cancel Locker B'
            else:
                self.lockers[1].cancel_hire(test_app.user)
                self.ids.locker_label.text = ''
                self.ids.button_hire_b.text = 'Hire Locker B'
        elif button == self.ids.button_hire_c:
            if test_app.user.current_locker is None:
                self.lockers[2].hire(test_app.user)
                self.ids.locker_label.text = 'Locker ' + self.lockers[2].name + ' hired.'
                self.ids.button_hire_c.text = 'Cancel Locker C'
            else:
                self.lockers[2].cancel_hire(test_app.user)
                self.ids.locker_label.text = ''
                self.ids.button_hire_c.text = 'Hire Locker C'

    def activate_locker(self):
        # calls the currently hired locker's unlock or lock button
        locker = test_app.user.current_locker  # cache the current locker
        if locker is not None:
            if locker.is_locked:
                locker.unlock(test_app.user)
                self.ids.lock_button.text = 'Unlock'
            else:
                locker.lock(test_app.user)
                self.ids.lock_button.text = 'Lock'
        else:
            print("Locker is not being hired.")


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

    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.user = None  # the current user of the app

    @property
    def user(self):
        return self.__current_user

    @user.setter
    def user(self, value):
        self.__current_user = value

    def build(self):
        Window.size = (250, 500)  # set window size to 250 x 500
        check_integrity()  # check the user file
        return WindowManager()


def check_integrity():
    # check if the user info file exists and create it if it doesn't
    if os.path.isfile("user_info.txt"):
        print("User info file exists.")
        file = open("user_info.txt", "r")
        # check the number of lines in the user_info file and if it's more than 2, reset the file
        count = 0
        for _ in file.readlines():
            count += 1
        if count >= 3:
            file = open("user_info.txt", "w")  # truncate the file
            print("File cleared due to incorrect line amount.")
        file.close()
    else:
        print("Creating user info file...")
        file = open("user_info.txt", "x")
        file.close()


if __name__ == "__main__":
    test_app = TestApp()  # build and then run the test app
    test_app().run()
