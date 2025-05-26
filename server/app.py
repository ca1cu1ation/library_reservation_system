import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from mysql.connector import pooling

app = Flask(__name__)
CORS(app)
# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Qwe248931',
    'port': 3306,
    'database': 'library_reveration_system',
    "pool_name": "mypool",
    "pool_size": 5
}

# 创建连接池
try:
    connection_pool = pooling.MySQLConnectionPool(**db_config)
    print("成功创建数据库连接池")
except mysql.connector.Error as err:
    print(f"数据库连接错误: {err}")


def get_db_connection():
    return connection_pool.get_connection()


# 密码验证函数
def verify_password(plain_password, hashed_password):
    return plain_password.encode('utf-8') == hashed_password.encode('utf-8')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    usertype = data.get('usertype')

    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        if usertype == "student":
            cursor.execute(
                "SELECT 学号, 密码 FROM 学生账号 WHERE 学号 = %s",
                (username,)
            )
        else:
            cursor.execute(
                "SELECT 职工号, 密码 FROM 教师账号 WHERE 职工号 = %s",
                (username,)
            )
        user = cursor.fetchone()

        if not user:
            return jsonify({"success": False, "message": "用户不存在"}), 401

        if not verify_password(password, user['密码']):
            return jsonify({"success": False, "message": "密码错误"}), 401

        # 登录成功，返回用户信息（实际应该返回token）
        if usertype == "student":
            return jsonify({
                "success": True,
                "user": {
                    "username": user['学号'],
                    "usertype": "学生"
                }
            })
        else:
            return jsonify({
                "success": True,
                "user": {
                    "username": user['职工号'],
                    "usertype": "教师"
                }
            })

    except Exception as e:
        print(f"数据库错误: {e}")
        return jsonify({"success": False, "message": "服务器错误"}), 500

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/user/<user_type>&<user_id>', methods=['GET', 'PUT'])
def user_profile(user_type,user_id):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'GET':
            if user_type=="学生":
                cursor.execute("SELECT * FROM 学生账号 WHERE 学号 = %s", (user_id,))
            else:
                cursor.execute("SELECT * FROM 教师账号 WHERE 职工号 = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "用户不存在"}), 404
            return jsonify(user)

        elif request.method == 'PUT':
            data = request.get_json()
            user_password=data['password']
            query = """CALL update_account(%s,%s,%s)"""
            cursor.execute(query, (user_id,user_type,user_password))
            conn.commit()
            return jsonify({"success": True})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/seats', methods=['GET'])
def get_seats():
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT s.*,l.楼层,l.区域
            FROM 座位 s 
            JOIN 具体位置 l ON s.位置id =l.位置id
        """
        cursor.execute(query)
        seats = cursor.fetchall()

        # 将布尔值转换为Python原生布尔类型
        for seat in seats:
            seat['has_power'] = bool(seat['插座'])
            seat['near_window'] = bool(seat['靠窗'])

        return jsonify(seats)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/reserve', methods=['POST'])
def reserve_seat():
    data = request.get_json()
    seat_id = data.get('seatId')
    user_id = data.get('userId')
    user_type = data.get('usertype')
    start_time = data.get('startTime')
    end_time = data.get('endTime')

    if not all([seat_id, user_id, start_time, end_time]):
        return jsonify({"error": "缺少必要参数"}), 400

    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)

        # 检查时间冲突
        if user_type == "学生":
            conflict_query = """
                SELECT 座位id FROM 学生座位预约 
                WHERE 座位id = %s                
                AND ((起始时间 BETWEEN %s AND %s) 
                    OR (结束时间 BETWEEN %s AND %s))                
            """
        else:
            conflict_query = """
                SELECT 座位id FROM 教师座位预约 
                WHERE 座位id = %s                
                AND ((起始时间 BETWEEN %s AND %s) 
                    OR (结束时间 BETWEEN %s AND %s))
            """
        cursor.execute(conflict_query, (seat_id, start_time, end_time, start_time, end_time))
        conflicts = cursor.fetchall()

        if conflicts:
            return jsonify({"error": "时间冲突，请选择其他时间段"}), 400

        # 创建预约
        if user_type=="学生":
            insert_query = """
                INSERT INTO 学生座位预约 
                (座位id, 学号, 起始时间, 结束时间,状态)
                VALUES (%s, %s, %s, %s,"未开始")
            """
        else:
            insert_query = """
                INSERT INTO 教师座位预约 
                (座位id, 职工号, 起始时间, 结束时间,状态)
                VALUES (%s, %s, %s, %s,"未开始")
            """

        cursor.execute(insert_query, (seat_id, user_id, start_time, end_time))
        conn.commit()

        return jsonify({"success": True})

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


@app.route('/api/reservations/<user_id>&<user_type>', methods=['GET'])
def get_reservations(user_id, user_type):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        if user_type == "学生":
            query = """
                SELECT * 
                FROM 学生座位预约视图
                WHERE 学号 = %s
                ORDER BY 起始时间 DESC;
            """
        else:
            query = """
                SELECT * 
                FROM 教师座位预约视图
                WHERE 职工号 = %s
                ORDER BY 起始时间 DESC;
            """
        cursor.execute(query, (user_id,))
        reservations = cursor.fetchall()

        # 格式化时间
        for res in reservations:
            res['起始时间'] = res['起始时间'].strftime('%Y-%m-%d %H:%M:%S')
            res['结束时间'] = res['结束时间'].strftime('%Y-%m-%d %H:%M:%S')

        return jsonify(reservations)

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# 取消预约
@app.route('/api/cancel_reservations/<usertype>&<reservation_id>', methods=['DELETE'])
def cancel_reservation(usertype,reservation_id):
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        # 开始事务,关闭自动提交
        conn.autocommit = False
        # 查找并删除预约记录
        if usertype=="学生":
            delete_query = """
                DELETE FROM 学生座位预约                
                WHERE 预约id = %s                 
            """
            update_query = """
               UPDATE 座位
               SET 状态=0
               WHERE 状态=1 
               AND 座位id=(SELECT 座位id FROM 学生座位预约 WHERE 预约id=%s)
            """
        else:
            delete_query = """
                DELETE FROM 教师座位预约                
                WHERE 预约id = %s
            """
            update_query = """
               UPDATE 座位
               SET 状态=0
               WHERE 状态=1 
               AND 座位id=(SELECT 座位id FROM 学生座位预约 WHERE 预约id=%s)
            """
        cursor.execute(delete_query, (reservation_id,))
        cursor.execute(update_query,(reservation_id,))
        conn.commit()
        return jsonify({"success": True})

    except mysql.connector.Error as err:
        # 发生错误时回滚
        conn.rollback()
        return jsonify({"error": str(err)}), 500

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
