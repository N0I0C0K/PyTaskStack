import random
from TaskStack import *

public_key = '''-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAIRNNXAVS3b84Cn3SbTpcUCTri6QMukknwzA1PVheAC6ax2cVz2SM/wP
v0Od6a33U6JQzfzN6+k5ts5YmV+UW6jJJehFLKLZAfJd+O28m0ZdJrm/dBR/8zyH
Prc8gi5NhmTXBq90fD5LyazlSg8lfJtxYt/35drYd/7r4TfBasSrAgMBAAE=
-----END RSA PUBLIC KEY-----
'''
# url, sess = applySession('test', 'python -c "print(1+2+3)"')
# print(url)
# runSession(sess)
configServer(public_key)
print(getEncodedData('123', '123', 'ssssss'))
