from pickle import NONE
import yagmail

class EmailBot:
    def __init__(self):
        self.yag = yagmail.SMTP(user="bkstr3@gmail.com", password="NewNebula62")
        self.subject = NONE
        self.message = NONE

    def confirmAccount(self, email:str ):
        self.subject = 'Book Store Confirmation'
        self.message = [
        'Hi, Name' ,

        'Welcome to Book Store!',

        'Happy Shopping!',

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]

        self.yag.send(to=email, subject=self.subject, contents=self.message)


    def recoveryPass(self, email:str, password:str):
        self.subject = 'Book Store Recovery Password'
        self.message = [
        'Hi, Name' ,

        'Here is your password: ',

        'DO NOT RESPOND TO THIS EMAIL, ANY EMAILS SENT REGARDING THIS WILL BE IGNORED' ]

        self.yag.send(to=email, subject=self.subject, contents=self.message)

