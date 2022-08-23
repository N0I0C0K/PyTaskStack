import os
import rsa
import json
from typing import *
from .utils import *

import PacketCrypto.PacketCrypto as packetCrypto


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
        packetCrypto.setPrivateKey(private_key)

    def DecodeFormRaw(self, form: FormRaw) -> SessionForm:
        '''
        解码`FormRaw` -> `SessionForm`
        :return :`SessionForm`
        '''
        res, key = packetCrypto.decryptPacket(form.dict())
        data = json.loads(res)
        sess = SessionForm.parse_obj(data)
        return sess


def generateRsa():
    print('[*] start generate private/public key')
    pub, pri = rsa.newkeys(1024)
    path = os.path.dirname(__file__)
    with open(path+'\\private_key', 'wb') as file:
        print(f'[*] private key => {file.name}')
        file.write(pri.save_pkcs1())
    with open(path+'\\public_key', 'wb') as file:
        print(f'[*] public key => {file.name}')
        file.write(pub.save_pkcs1())


cryptoCore = CryptoCore()
'''
信息的加密解密
'''
