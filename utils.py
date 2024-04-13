import datetime
import re
from calendar import calendar

from custom import *


# Check for Null Inputs
def validate_string(*args):
    for arg in args:
        if arg is None or arg == '':
            return False
    return True


# To check mobile number
def validate_mobileNo(mobileNo):
    if re.fullmatch(r'^0[0-9]{9}$', mobileNo):
        return True
    else:
        return False


def validate_email(email):
    if re.fullmatch(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return True
    else:
        return False


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

# Input (January-December), Output (1-12)
def convert_monthToNumber(month):
    if month == 'January':
        return '01'
    elif month == 'February':
        return '02'
    elif month == 'March':
        return '03'
    elif month == 'April':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June':
        return '06'
    elif month == 'July':
        return '07'
    elif month == 'August':
        return '08'
    elif month == 'September':
        return '09'
    elif month == 'October':
        return '10'
    elif month == 'November':
        return '11'
    elif month == 'December':
        return '12'

# Get month as number and return corresponding string word like January
def convert_numberToMonth(month):
    str(month)
    if month == '01' or month == '1':
        return 'January'
    elif month == '02' or month == '2':
        return 'February'
    elif month == '03' or month == '3':
        return 'March'
    elif month == '04' or month == '4':
        return 'April'
    elif month == '05' or month == '5':
        return 'May'
    elif month == '06' or month == '6':
        return 'June'
    elif month == '07' or month == '7':
        return 'July'
    elif month == '08' or month == '8':
        return 'August'
    elif month == '09' or month == '9':
        return 'September'
    elif month == '10':
        return 'October'
    elif month == '11':
        return 'November'
    elif month == '12':
        return 'December'


# validate currency, may be an int as well
def validate_currency(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False


def cutEmail(email):
    if '@' not in email:
        return email
    else:
        return email.split('@')[0]
