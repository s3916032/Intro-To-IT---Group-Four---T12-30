# Python App Project Draft
#
# This draft is NOT a final version of the application and should NOT be treated as such
# It is intended to prototype the application's base functionality so it can be ported to other devices
# The draft also implements the guizero Python package by Laura Sach (2016)
#
# Started by Simon Bird (s3916032) and probably not finished by Simon Bird (s3916032)
# The following program is not endorsed by Simon Bird (s3916032)
#
# TODO:
#   Account pages: Register and Login
#       Store user data with register; Only login when matched
#       Automatically login until 30 days or manually logged out
#   PIN pages: Create and request
#       Store pin with user data; Reset after 30 days or when logging in
#   Main page: Token creation and unlock
#       Create a token that deletes itself after about 10 minutes or if locker is unlocked
#       Use token to unlock 3 virtual lockers
#       Lockers automatically lock after about 5 minutes

from guizero import *
import PIL

# Opening page
# Requirements:
#   Splash logo
#   Login
#   If user does not exist, request login information or register

# - constants - #
COLORS = {'bg': 'white', 'text': 'black', 'accent': 'red'}  # application colours dictionary constant


def switch_window(current, new):
    """
    Switches the active window of the application by closing a window and opening another\n
    Returns the new window

    :param Window current: Current window to close
    :param Window new: Window to change to
    """

    if new is None or current is None:
        raise TypeError("Invalid Window.")  # raise a TypeError if a parameter Window is None
    else:
        current.hide()  # hide the current window,
        new.show(wait=True)  # show the new window and set it to the main window
        return new


def set_splash_window(window, display=False):
    """
    Sets up a window as a splash window

    :param Window window: Window to alter
    :param bool display: Should the window display once the function is complete?
    """

    # display the splash image the size of the window
    logo = Picture(window, "test-logo.PNG", width=window.width, height=window.height)
    if display:
        window.show()
    else:
        window.hide()


def set_login_window(window, display=False):
    """
    Sets up a window as a login window

    :param Window window: Window to alter
    :param bool display: Should the window display once the function is complete?
    """

    # two fields - username and password - each commanded as login
    # two texts - username and password (beside fields)
    # two buttons - login (after fields) and register
    # commands:
    #   login - once pressed, check credentials (can be instant for now) and switch screen to PIN
    #   register - once pressed, save credentials (does not need to be secure for now as it's a draft)

    text_size = 10  # size to display field texts
    margin = 100  # size of border margins

    # set up margins
    top_margin = Box(window, width=window.width, height=margin, align="top")

    # set up fields
    outer_box = Box(window, layout="grid", width=window.width-margin*2, height=window.height-margin*2,
                    border=True)
    Text(outer_box, "Username:", grid=[0, 1], size=text_size)  # login text
    Text(outer_box, "Password:", grid=[0, 2], size=text_size)  # password text
    login_field = TextBox(outer_box, "", "fill", grid=[1, 1])
    password_field = TextBox(outer_box, "", "fill", grid=[1, 2], hide_text=True)

    if display:
        window.show()
    else:
        window.hide()


def build_app():
    """
    Creates an app and some windows for splash, account, pin and main pages
    """

    splash_time = 1000  # time to wait after splash window appears (ms)

    app_main = App("Safe Box", 500, 800, layout="grid", bg=COLORS['bg'], visible=False)  # main app container
    window_splash = Window(app_main, title="Splash", bg=COLORS['bg'], width=app_main.width, height=app_main.height,
                           visible=True)  # splash screen
    window_login = Window(app_main, title="Login", bg=COLORS['bg'], width=app_main.width, height=app_main.height,
                          visible=False)  # login screen
    window_register = Window(app_main, title="Register", bg=COLORS['bg'], width=app_main.width, height=app_main.height,
                             visible=False)  # register screen

    # setup the windows
    set_splash_window(window_splash, True)
    set_login_window(window_login)

    app_main.after(splash_time, switch_window, (window_splash, window_login))  # show the splash for some time
    app_main.display()  # finally, display the app


build_app()
