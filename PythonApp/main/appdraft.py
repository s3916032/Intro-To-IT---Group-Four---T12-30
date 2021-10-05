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
#   PIL implementation (image resizing addon)
#   Opening page
#   Account pages: Register and Login
#   PIN pages: Create and request
#   Main page

from guizero import *
from time import sleep

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
        new.show()  # show the new window
        return new


def splash(window, display=False):
    """
    Sets up a window as a splash window

    :param Window window: Window to alter
    :param bool display: Should the window display once the function is complete?
    """

    logo = Picture(window, "test-logo.PNG", align="top", width=window.width, height=window.height)
    if display:
        window.show()
    else:
        window.hide()


def build_app():
    """
    Creates an app and some windows for splash, account, pin and main pages
    """

    splash_time = 3  # time to wait after splash window

    app_main = App("Safe Box", 500, 800, bg=COLORS['bg'], visible=False)  # main app container
    window_splash = Window(app_main, title="Splash", bg=COLORS['bg'], visible=False)  # splash screen
    window_login = Window(app_main, title="Login", bg=COLORS['bg'], visible=False)  # login screen
    window_register = Window(app_main, title="Register", bg=COLORS['bg'], visible=False)  # register screen

    current_window = window_splash  # current window of the app
    splash(window_splash, True)

    sleep(splash_time)  # show the splash for a little while


build_app()
