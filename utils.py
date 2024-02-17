# validate string function that checks if a string is null or not, may take any amount of inputs

def validate_string(*args):
    for arg in args:
        if arg is None or arg == '':
            return False
    return True


def messagebox(title, message):
    from tkinter import messagebox
    messagebox.showinfo(title, message)
