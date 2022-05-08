from CryptoCore import cryptoCore
from TaskStack import *

public_key = '''-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAMYDmoov9/tesKXOjQSr+no7Vq0sguxEnArR+dkjrO3NXbqH3hrxGwly
FnxshkuG+UcTviVHjOfNkppdDLKLviXzxOWyfvUx2JdBI3N6oWLfIg8CRSGVyzYa
dTXM3apdikCWVyVMKkw2iFI0O5lueMsBxhB1irg08FvtfvzDV8Z9AgMBAAE=
-----END RSA PUBLIC KEY-----
'''
# url, sess = applySession('test', 'python -c "print(1+2+3)"')
# print(url)
# runSession(sess)
configServer(public_key)
url, session = applySession('test', 'tree')
print(url)
