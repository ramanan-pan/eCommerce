from datetime import datetime
from pickle import NONE
import yagmail

class EmailBot:
    def __init__(self):
        self.yag = yagmail.SMTP(user="bkstr3@gmail.com", password="NewNebula62")
        self.subject = NONE
        self.message = NONE

    def confirmAccount(self,  fname:str, lname:str, email:str ):
        self.subject = 'Book Store Confirmation'
        self.message = [
        'Hi, ' + fname + " " + lname ,

        'Welcome to Book Store!',

        'Happy Shopping!',

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]

        self.yag.send(to=email, subject=self.subject, contents=self.message)


    def orderConfirmation(self, email:str, text:list):
        self.subject = 'Order Confirmation'
        self.message = text
        self.message.append('DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED')
        self.yag.send(to=email, subject=self.subject, contents=self.message)

    def recoveryKey(self, email:str, link:str, rkey:str, fname:str, lname:str):
        self.subject = 'Book Store Password Recovery Key'
        self.message = [
        'Hi, ' + fname + " " + lname ,

        'Here is your key: '  + rkey,

        'Follow this link to reset your password:',

        link,

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]

        self.yag.send(to=email, subject=self.subject, contents=self.message)

    def reserveConfirmation(self, email:str, text:list):
        self.subject = 'Reservation Confirmation'
        self.message = text
        self.message.append('DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED')
        self.yag.send(to=email, subject=self.subject, contents=self.message)

    def newsletter(self, emaillist:list, content:str, title:str):
        self.subject = 'Book Store Newsletter: ' + title
        self.message = [content,

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]
        self.yag.send(to = emaillist, subject=self.subject, contents=self.message)

    def promotion(self, emaillist:list, start:datetime, end:datetime, code:str, name:str, desc:str):
        self.subject = 'Book Store Promotion: ' + name
        startdate = start.strftime('%B %d, %Y')
        enddate = end.strftime('%B %d, %Y')
        self.message = [
            'Hello! Book Store is rolling out a new promotion that starts on '+ startdate +  ' and ends on ' + enddate + '.',

            'This promotion can be applied site-wide when purchasing books online or when creating a reservation for in-store pickup.',

            'Promo Code: ' + code,

            desc,

            "Be sure to use this promotion before it's over!",

            'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' 
        ]
        self.yag.send(to = emaillist, subject=self.subject, contents=self.message)