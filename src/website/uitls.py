from lib2to3.pgen2 import token
import string
import random
from random import shuffle

class TokenGenerator():
    
    def __init__(self):
        print('00')

    def generateToken(self):
        token = ''
        letters = string.ascii_lowercase

        token += ''.join(random.choice(letters) for i in range(7))

        letters = string.ascii_uppercase

        token += ''.join(random.choice(letters) for i in range(7))

        letters = string.digits

        token += ''.join(random.choice(letters) for i in range(7))
        
        token = list(token)
        shuffle(token)
        token = ''.join(token)
        return token







