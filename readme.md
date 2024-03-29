# Python 本地任务分发中心服务

## 此项目已经重构，新项目[地址](https://github.com/N0I0C0K/TaskStack)

> PyTaskStack

## 目前进度

- 后端

**PyTaskStack**

全面 Python Task Stack ⇒ 任务栈.

---

# 功能

- 共给本地部分
  - 申请任务
  - 返回外链供给远程访问执行
- 供给外部部分
  - 外链访问
  - 界面

# 模块详细

## Auth

认证模块包含了

- 登录, 每次登录都会经过安全处理
- 注册, 用户密码经过了加盐处理
- 鉴权

## Task

任务模块, 负责

- 任务的创建,删除,更改
- 任务的调度

## Session

每次任务的执行都会生成一个 Session 对象, 储存了

- 对应的 taskid
- 开始的时间
- 结束的时间
- 输出
- 错误输出

该模块负责

- Session 的查询

## Data

基于 sqlite 储存数据, 负责

- 数据的操作
- 数据的查询
