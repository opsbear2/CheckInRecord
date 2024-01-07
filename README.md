# CheckInRecord


## 背景说明

公司福利报销的方式有两种

- 餐补补助，每天下班打卡时间超过20:00
- 交通补助，每天下班打卡时间超过21:00

提交报销单时需要填写日期，目前使用的打卡工具钉钉/飞书，并未给职工接口权限，因此只能手动查询符合报销条件的日期

填写过程比较繁琐，浪费太多时间，因此开发此小工具，直接打印符合报销条件的日期，简化报销单的填写流程



## 实现方法

1. 创建定时任务快捷指令： 利用iOS快捷指令，在每天20点和21点触发，获取当前地理位置。

2. 判断是否在公司： 使用条件判断当前位置是否在公司，若是则继续，否则结束。

3. 更新报销状态： 根据位置判断的结果，发起HTTP请求将报销状态更新到数据库中。

4. 一键统计报销日期: 脚本查询数据库，用于一键统计符合报销条件的日期。


## 快速开始

### 部署环境

- 硬件环境：iPhone（iOS 12及以上版本）、云主机
- 软件环境：Docker、Python、Mysql、Shortcuts

### 部署mysql

用于记录每天的20:00、21:00是否满足报销条件，docker容器部署mysql服务

**拉取mysql镜像**

```shell
docker pull mysql:latest
```

**运行mysql容器**

```shell
docker run -d --name mysql_checkin -e MYSQL_ROOT_PASSWORD='MYSQL_ROOT_PASSWORD' mysql:latest
```

**创建库表**

```mysql
# 建库
CREATE DATABASE checkin;

# 建表
CREATE TABLE offline_work_record (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    date DATE,
    type VARCHAR(255),
    status BOOLEAN
);
```



### 部署falsk应用

由于访问量很低，不考虑稳定和高效性，因此选择最简单的部署方式，直接使用 Flask 内置的开发服务器运行，并注册成service

**创建service文件**

新建文件 `/etc/systemd/system/checkin.service`

```shell
[Unit]
Description=checkin
After=network.target

[Service]
User=root
WorkingDirectory=/data1/checkin
ExecStart=/root/.pyenv/versions/env368/bin/python3 checkin.py

[Install]
WantedBy=multi-user.target
```

**启动服务**

```shell
# 启动服务
systemctl start  checkin

# 设置开机启动
systemctl enable checkin
```


**请求测试**

请求url格式 `http://your_ip:your_port/checkin_record?username=<用户名>&type=<签到类型>&status=<签到状态>`

```shell
<用户名>: 用户的唯一标识符
<签到类型>: 签到的类型，可选值为 "meal" 或 "transport"
<签到状态>: 签到的状态，可选值为 "true" 或 "false"
```

请求url示例

```
http://your_ip:your_port/checkin_record?username=bear2&type=meal&status=True
```

测试数据插入

```mysql
mysql> select * from offline_work_record;
+----+------------+------------+-----------+--------+
| id | username   | date       | type      | status |
+----+------------+------------+-----------+--------+
| 60 | bear2      | 2024-01-05 | meal      |      1 |
| 62 | bear2      | 2024-01-05 | transport |      0 |
| 64 | bear2      | 2024-01-06 | meal      |      0 |
| 65 | bear2      | 2024-01-06 | transport |      0 |
| 66 | bear2      | 2024-01-07 | transport |      0 |
| 67 | bear2      | 2024-01-07 | transport |      0 |
| 68 | test       | 2024-01-07 | meal      |      1 |
+----+------------+------------+-----------+--------+
8 rows in set (0.00 sec)
```



### 配置定时任务

使用IOS系统自带的`快捷指令`和`自动化`功能，在每天20:00、21:00定时执行任务=

根据地理位置判断结果，请求不同的url，例如，在20:00判断是否在公司

- 如果在，请求 `http://your_ip:your_port/checkin_record?username=bear2&type=meal&status=True`
- 如果不在，请求`http://your_ip:your_port/checkin_record?username=bear2&type=meal&status=Flase`



**访问链接，一键安装IOS的快捷指令**


判断20点是否在公司：https://www.icloud.com/shortcuts/edd7ddda849f41a4b1e182688b22b3af

判断21点是否在公司：https://www.icloud.com/shortcuts/1c8b0e5297f2438881fd64709269556b



安装之后根据实际情况调整`位置列表`和`url`

![image-20240107162540634](C:\Users\Admin\AppData\Roaming\Typora\typora-user-images\image-20240107162540634.png)



添加完成快捷指令后配置自动化，选择`立即运行`，去掉运行时通知，选择时间和对应的快捷指令

![image-20240107161409316](C:\Users\Admin\AppData\Roaming\Typora\typora-user-images\image-20240107161409316.png)


### 查询报销记录

```shell
# 使用方法
# python3 get_reimbursement_date.py 
Usage: get_reimbursement_date.py [username] [year] [month] [type]
Arguments:
  username   The username for the query
  year       The year for the query
  month      The month for the query
  type       The type for the query (meal or transport)
  
# 查询bear在2024年1月满足餐补报销的日期
# python3 get_reimbursement_date.py bear2 2024 1 meal
[bear2 2024-1 meal reimbursement]
2024-01-03
2024-01-04
2024-01-05
```

