# 配置文件示例 (config.example.py)
# 复制此文件为 config.py 并修改相应的配置

# 数据库配置
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',      # 修改为你的数据库用户名
    'password': 'your_password',  # 修改为你的数据库密码
    'port': 3306,
    'database': 'library_reveration_system',
    'pool_name': 'mypool',
    'pool_size': 5
}

# Flask应用配置
FLASK_CONFIG = {
    'host': '0.0.0.0',
    'port': 3000,
    'debug': True  # 生产环境应设置为 False
}

# 安全配置
SECRET_KEY = 'your-secret-key-here'  # 生产环境请使用复杂的随机字符串

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'file': 'app.log'
}