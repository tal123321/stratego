from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import rsa


class Player:
    def __init__(self, name):
        self._name = name
        self._symmetricKey = generate_symmetric_key()

    def name(self):
        return self._name

    def name(self, value):
        self._name = value

    def symmetricKey(self):
        return self._symmetricKey

    def symmetricKey(self, value):
        self._symmetricKey = value

    def decrypt_data(enc_data, key_SYMETRIC):
        enc_iv = b64decode(enc_data[:24])
        enc_msg = b64decode(enc_data[24:])

        cipher = AES.new(key_SYMETRIC, AES.MODE_CBC, enc_iv)
        dec = cipher.decrypt(enc_msg)
        dec_unpad = unpad(dec)
        plain_txt = dec_unpad.decode('utf-8')
        return plain_txt

    def encrypt_data(new_data, key_SYMETRIC):
        raw = pad(new_data)
        cipher = AES.new(key_SYMETRIC, AES.MODE_CBC)
        cipher_bytes = cipher.encrypt(raw)
        iv = b64encode(cipher.iv).decode('utf-8')
        ct = b64encode(cipher_bytes).decode('utf-8')
        print(len(iv))
        print((len(ct)))
        iv_ct = iv + ct
        return iv_ct

    def generate_symmetric_key():
        """"generate 16 byte key, randomly each time this function call"""
        key_sem = get_random_bytes(16)
        return key_sem

publicKey, privateKey = rsa.newkeys(512)
print(publicKey.save_pkcs1().decode('utf-8'))