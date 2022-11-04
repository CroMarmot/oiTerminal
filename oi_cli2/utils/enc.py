from hashlib import md5
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:

  def __init__(self, key: str):
    self.key = md5(key.encode('utf8')).digest()

  def encrypt(self, data: str) -> str:
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(self.key, AES.MODE_CBC, iv)
    return b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))).decode('utf-8')

  def decrypt(self, data: str) -> str:
    raw = b64decode(data)
    cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
    return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode('utf-8')
