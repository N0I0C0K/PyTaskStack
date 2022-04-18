import os
import rsa
import base64
import json
from typing import *
from utils import *
import Crypto.Cipher.AES as CryCes


class CryptoCore:

    def __init__(self, private_key: str = None) -> None:
        if private_key is None:
            key_path = os.path.dirname(__file__)+'\\private_key'
            if not os.path.exists(key_path):
                raise ValueError(f'{key_path} 不存在, 未能初始化验证组件')
            with open(key_path, 'r', encoding='utf-8') as file:
                private_key = file.read()
        self.__privateKey = rsa.PrivateKey.load_pkcs1(
            private_key.encode('utf-8'))
        pass
    
    def FormRawToSessionForm(self, form:FormRaw)->SessionForm:
        aes_key = rsa.decrypt(base64.b64decode(form.key),
                              self.__privateKey)
        aes = CryCes.new(aes_key, CryCes.MODE_EAX)
        plaintext = aes.decrypt(base64.b64decode(form.data)).decode()
        data = json.loads(plaintext)
        sess = SessionForm.parse_obj(data)
        return sess

cryptoCore = CryptoCore()
        