from typing import *


class SessionInfo:
    token: str = None
    key: str = None
    stdout_log: str = None
    stderr_log: str = None
    session_id: str = None
    session_name: str = None
    session_command: str = None
    session_task = None

    def __init__(self) -> None:
        '''
        Session info的一个单元
        '''
        pass
