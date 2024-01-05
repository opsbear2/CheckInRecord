#!/bin/bash

# 用于打印每天下班打卡超过20点,21点的记录,返回日期yyyy-mm-dd

# 帮助信息
print_help() {
    echo "Usage: $0 [username] [year] [month] [type]"
    echo "Arguments:"
    echo "  username   The username for the query"
    echo "  year       The year for the query"
    echo "  month      The month for the query"
    echo "  type       The type for the query (meal or transport)"
    echo ""
    echo "Example: $0 zhangyonggang 2024 1 meal"
}

# 如果没有传递足够的参数，打印帮助信息
if [ "$#" -ne 4 ]; then
    print_help
    exit 1
fi

# 定义数据库连接信息
DB_USER="DB_USER"
DB_PASSWORD="DB_PASSWORD"
DB_NAME="checkin"

# 获取命令行参数
username="$1"
year="$2"
month="$3"
type="$4"


echo -e "\e[32m[$username $year-$month $type reimbursement]\e[0m"

docker exec -it mysql_checkin mysql -u $DB_USER --password=$DB_PASSWORD $DB_NAME -B -N -e "SELECT date FROM offline_work_record WHERE username = '$username' AND YEAR(date) = $year AND MONTH(date) = $month AND type = '$type' AND status = 1;" |grep -v 'Warning' | sort | uniq


