import rsa
import base64
key = '''-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAIRNNXAVS3b84Cn3SbTpcUCTri6QMukknwzA1PVheAC6ax2cVz2SM/wP
v0Od6a33U6JQzfzN6+k5ts5YmV+UW6jJJehFLKLZAfJd+O28m0ZdJrm/dBR/8zyH
Prc8gi5NhmTXBq90fD5LyazlSg8lfJtxYt/35drYd/7r4TfBasSrAgMBAAE=
-----END RSA PUBLIC KEY-----
'''
pubkey = rsa.PublicKey.load_pkcs1(key.encode('utf8'))
res = rsa.encrypt(
    'e66844caa3ac3b54aa6080e3914109fc'.encode(), pubkey)
print(base64.b64encode(res).decode())
