import datetime

from custom import *


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


def message_box(title, message):
    from tkinter import messagebox
    messagebox.showinfo(title, message)


def confirm_box(title, message):
    from tkinter import messagebox
    return messagebox.askquestion(title, message)


def convert_date(date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%B %d')

# Reversion of above function
def reverse_date(date):
    return datetime.datetime.strptime(date, '%B %d').strftime('%Y-%m-%d')


# Convert Currency, take a float and return a string, Rs. at front and 2 decimal places with commas
def convert_currency(amount):
    return 'Rs. {:,.2f}'.format(float(amount))

# A function to reverse above function, take the string and return the float, etc Rs. 10,000.00 to 10000.00
def currencyStringToFloat(amount):
    return float(amount.replace('Rs. ', '').replace(',', ''))


# validate currency, may be an int as well
def validate_currency(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False
