from barcode import Code128
from barcode.writer import ImageWriter
import os
import win32com.client as win32
import csv


class Barcode:
    def __init__(self, studentID):
        self.studentID = studentID

    def barcode_number(self):
        number = self.studentID
        return number

   
def send_email(barcode):
    olApp = win32.Dispatch('Outlook.Application')
    olNS = olApp.GetNameSpace('MAPI')

    mailItem = olApp.CreateItem(0)
    mailItem.Subject = 'StudentID Barcode'
    mailItem.body = 'This is your student ID barcode, you can save it on your phone and use it like your student ID card.'
    mailItem.to = 'lwilmoth@eriesd.org'
 

    mailItem.Save()
    mailItem.Send()
'''
with open('example.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        barcode = Barcode(row['id'])

        number = barcode.barcode_number()

        my_code = Code128(number, writer=ImageWriter())

        my_code.save(f"new_code{number}")
        send_email(barcode)
        '''
send_email("hi")