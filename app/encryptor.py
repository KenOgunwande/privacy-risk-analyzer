import base64
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_key():
    key = AESGCM.generate_key(bit_length=128)
    return base64.b64encode(key).decode()

def encrypt_text(text, b64_key):
    key = base64.b64decode(b64_key)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, text.encode(), None)
    return base64.b64encode(nonce).decode(), base64.b64encode(ciphertext).decode()

def decrypt_text(nonce_b64, ciphertext_b64, b64_key):
    key = base64.b64decode(b64_key)
    nonce = base64.b64decode(nonce_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode()
