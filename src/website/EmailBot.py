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


    def recoveryPass(self, email:str, fname:str, lname:str, password:str, link:str):
        self.subject = 'Book Store Recovery Password'
        self.message = [
        'Hi, ' + fname + " " + lname ,

        'Here is your password: '  + password,

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]

        self.yag.send(to=email, subject=self.subject, contents=self.message)



    def orderConfirmation(self, email:str, text:list):
        self.subject = 'Order Confirmation'
        self.message = text
        self.message.append('DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED')
        self.yag.send(to=email, subject=self.subject, contents=self.message)

