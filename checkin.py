from flask import Flask, request, jsonify
from datetime import datetime
import pymysql

app = Flask(__name__)

# MySQL数据库连接配置
db_config = {
    'host': 'host',
    'user': 'user',
    'password': 'password',
    'db': 'checkin',
    'charset': 'utf8mb4',
}

# 处理GET请求
@app.route('/checkin_record', methods=['GET'])
def process_request():
    # 获取请求参数
    username = request.args.get('username')
    type = request.args.get('type')
    # 将字符串 'True' 转换为布尔值
    status_str = request.args.get('status')
    status = status_str.lower() == 'true' if status_str else None
    current_datetime = datetime.now()
    date = current_datetime.strftime('%Y-%m-%d')

    # 初始化连接变量
    connection = None

    # 执行数据库插入操作
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql = "INSERT INTO offline_work_record (username, date, type, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (username, date, type, status))
        connection.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 关闭连接前检查是否存在
        if connection:
            connection.close()

    return jsonify({'success': True})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=11002, debug=True)
