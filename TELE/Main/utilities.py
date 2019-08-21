from hashlib import pbkdf2_hmac
from binascii import hexlify
from hmac import compare_digest

class Token():
    @staticmethod
    def generate(password, salt):
        AUTH_SIZE = 16
        byte_password = bytes(str(password),'utf-8')
        byte_salt = bytes(str(salt),'utf-8')
        dk = pbkdf2_hmac('sha256',byte_password, byte_salt, 100000, AUTH_SIZE)
        return hexlify(dk).decode('utf-8')