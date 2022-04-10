# Python本地任务分发中心服务

> PyTaskStack
> 

**PyTaskStack**

全面Python Task Stack ⇒ 任务栈.

---

- **情景再现**
    
    当服务器定时任务失败, 需要重新执行任务, 我们需要一个中间件来分发任务来远程执行任务.
    
- 预想的功能
    - 打卡失败
        
        ```python
        Nick, cheer打卡失败.
        访问 http://192.168.0.1/session/sahdisad21bnjh1761vjv17t  重新任务
        # 其中链接部分是申请的外链
        ```
        

# 功能

- 共给本地部分
    - 申请任务
    - 返回外链供给远程访问执行
- 供给外部部分
    - 外链访问
    - 界面