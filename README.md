# CheckInRecord


## 背景说明

公司福利报销的方式有两种

- 餐补补助，每天下班打卡时间超过20:00
- 交通补助，每天下班打卡时间超过21:00

提交报销单时需要填写日期，目前使用的打卡工具钉钉/飞书，并未给职工接口权限，因此只能手动查询符合报销条件的日期

填写过程比较繁琐，浪费太多时间，因此开发此小工具，直接打印符合报销条件的日期，简化报销单的填写流程



## 实现方法

1. 利用IOS系统的快捷指令，在每天20点,21点定时执行任务，根据地理位置判断是否在公司
2. 根据判断结果，请求url，将报销状态入库
3. 一键统计符合报销条件的日期

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

访问量很低，因此使用Flask自带的开发服务器进行使用，





