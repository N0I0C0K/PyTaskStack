import rsa
import base64
import requests
import json
from typing import *

__all__ = ['server_port', 'server_host',
           'public_key', 'checkServer', 'applySession', 'runSession']

server_port = 5555
'''
服务的端口
'''
server_host = '127.0.0.1'
'''
服务的主机
'''
public_key = '''-----BEGIN RSA PUBLIC KEY-----
MIGJAoGBAIRNNXAVS3b84Cn3SbTpcUCTri6QMukknwzA1PVheAC6ax2cVz2SM/wP
v0Od6a33U6JQzfzN6+k5ts5YmV+UW6jJJehFLKLZAfJd+O28m0ZdJrm/dBR/8zyH
Prc8gi5NhmTXBq90fD5LyazlSg8lfJtxYt/35drYd/7r4TfBasSrAgMBAAE=
-----END RSA PUBLIC KEY-----
'''
'''
公钥, 需要手动更改
'''


class Session:
    token: str = None
    stdout_log: str = None
    stderr_log: str = None
    session_id: str = None
    session_name: str = None
    session_command: str = None


def configServer(pub_key: str, host: str = '127.0.0.1', port: int = 5555):
    '''
    初始化设置
    :param host: 服务提供的主机
    :param port: 主机的端口
    :public_key: 公钥
    '''
    global server_host, server_port, public_key
    server_host, server_port, public_key = host, port, pub_key


def formUrl(s: str = '') -> str:
    '''
    获得转换后的url, 比如`s = /test`就会返回`http://host:port/test`
    :param s: 拼接的部分
    '''
    return f'http://{server_host}:{server_port}{s}'


def checkServer() -> bool:
    '''
    检测服务是否启动
    '''
    try:
        res = requests.get(formUrl('/')).json()
    except TimeoutError:
        return False
    except:
        return False
    else:
        return res['code'] == 200


def applySession(session_name: str, session_command: str) -> Tuple[str, Session]:
    '''
    申请一个`Session`
    :param session_name: 名称
    :param session_command: 需要执行的命令
    :return: Tuple[url, Session] 
    '''
    if not checkServer():
        return None
    session = requests.get(formUrl('/getsession')).json()
    if session['code'] != 200:
        return None
    pub = rsa.PublicKey.load_pkcs1(public_key.encode())
    token = base64.b64encode(rsa.encrypt(
        session['key'].encode(), pub)).decode()
    form = {
        'token': token,
        'session_id': session['session_id'],
        'session_name': session_name,
        'session_command': session_command
    }
    res = requests.post(formUrl('/pushsession'), json=form).json()
    sess = Session()
    sess.__dict__.update(form)
    return (res['url'], sess)


def runSession(session: Session) -> bool:
    if not checkServer():
        return None
    res = requests.get(formUrl(f'/run/{session.session_id}')).json()
    return res['code'] == 200