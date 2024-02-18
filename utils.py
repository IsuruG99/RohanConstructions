import datetime


# Check for Null Inputs
def validate_string(*args):
    for arg in args:
        if arg is None or arg == '':
            return False
    return True


# Validate Date Strings
def validate_date(*args):
    for arg in args:
        if arg is None or arg == '':
            return False
        try:
            datetime.datetime.strptime(arg, '%Y-%m-%d')
        except ValueError:
            return False
    return True


def messagebox(title, message):
    from tkinter import messagebox
    messagebox.showinfo(title, message)
