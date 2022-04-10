# Sessions文件夹
## 目录结构
里面用于存储每一个session的信息
```
sessions
|----........session1.json
|----........session2.json
|----........session3.json
|----.....
```

## {session}.json
```json
{
    "session_name":"session的名称",
    "session_id":"session id",
    "session_command":"执行的命令",
    "stdout_log":"输出的文件",
    "stderr_log":"错误的文件"
}
```