# Python App Project Draft
#
# This draft is not a final version of the application and should not be treated as such
# It is intended to prototype the application's base functionality so it can be ported to other devices
# The draft also implements the guizero Python package by Laura Sach (2016)
#
# Started by Simon Bird (s3916032) and probably not finished by Simon Bird (s3916032)
#
# TODO: Opening page
#       Account pages: Register and Login
#       Pin pages: Create and request
#       Main page

from guizero import App, Text

starter_app = App()
starter_text = Text(starter_app, "Woah, Nelly!")
starter_app.display()
