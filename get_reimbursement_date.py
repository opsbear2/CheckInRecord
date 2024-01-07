#!/usr/bin/env python3
import subprocess
import sys

def print_help():
    print("Usage: {} [username] [year] [month] [type]".format(sys.argv[0]))
    print("Arguments:")
    print("  username   The username for the query")
    print("  year       The year for the query")
    print("  month      The month for the query")
    print("  type       The type for the query (meal or transport)")
    print("")
    print("Example: {} zhangyonggang 2024 1 meal".format(sys.argv[0]))

def query_records(username, year, month, type_val):
    # 定义数据库连接信息
    DB_USER = "DB_USER"
    DB_PASSWORD = "DB_PASSWORD"
    DB_NAME = "checkin"

    # 构建数据库查询命令
    query_command = "SELECT date FROM offline_work_record WHERE username = '{}' AND YEAR(date) = {} AND MONTH(date) = {} AND type = '{}' AND status = 1;".format(username, year, month, type_val)

    # 执行命令并返回结果
    try:
        process = subprocess.Popen(["docker", "exec", "-i", "mysql_checkin", "mysql", "-u", DB_USER, "--password=" + DB_PASSWORD, DB_NAME, "-B", "-N", "-e", query_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result_bytes, error_bytes = process.communicate()
        result_str = result_bytes.decode("utf-8").strip()
        error_str = error_bytes.decode("utf-8").strip()

        if "Using a password on the command line interface" in error_str:
            print("Warning: Using a password on the command line interface can be insecure.")

        return result_str

    except subprocess.CalledProcessError as e:
        return "Error executing command: {}".format(e)

def main():
    # 如果没有传递足够的参数，打印帮助信息
    if len(sys.argv) != 5:
        print_help()
        sys.exit(1)

    # 获取命令行参数
    username = sys.argv[1]
    year = sys.argv[2]
    month = sys.argv[3]
    type_val = sys.argv[4]

    print("\033[32m[{} {}-{} {} reimbursement]\033[0m".format(username, year, month, type_val))

    # 执行查询并打印结果
    result = query_records(username, year, month, type_val)
    print(result)

if __name__ == "__main__":
    main()

