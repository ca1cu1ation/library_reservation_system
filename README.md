# 图书馆座位预约系统

一个基于Web的图书馆座位预约管理系统，支持学生和教师用户登录、座位预约、预约管理等功能。

## 📋 项目概述

本系统是一个完整的图书馆座位预约解决方案，提供了用户友好的界面和强大的后端管理功能。系统支持多楼层多区域的座位布局，实现了时间冲突检测、用户身份验证等核心功能。

## ✨ 主要功能

### 用户功能
- **用户登录**: 支持学生和教师两种用户类型登录
- **座位预约**: 选择时间段和座位进行预约
- **预约管理**: 查看和取消个人预约记录
- **用户信息管理**: 修改个人密码等信息

### 系统功能
- **多楼层布局**: 支持四个楼层的座位管理
  - 一楼：A区、B区
  - 二楼：C区
  - 三楼：D区、E区
  - 四楼：F区
- **时间冲突检测**: 自动检测预约时间冲突
- **实时座位状态**: 动态显示座位可用状态
- **用户权限管理**: 区分学生和教师用户类型

## 🛠 技术栈

### 前端技术
- **HTML5**: 页面结构
- **CSS3**: 样式设计，响应式布局
- **JavaScript (ES6+)**: 交互逻辑和API调用
- **Fetch API**: 异步数据请求

### 后端技术
- **Python 3.x**: 后端开发语言
- **Flask**: Web框架
- **Flask-CORS**: 跨域资源共享
- **MySQL**: 关系型数据库
- **mysql-connector-python**: MySQL数据库连接

### 数据库
- **MySQL**: 主数据库
- **连接池**: 优化数据库连接性能

## 📁 项目结构

```
library_reservation_system/
├── html/                   # 前端页面
│   ├── index.html         # 登录页面
│   └── home.html          # 主页面(座位预约)
├── css/                   # 样式文件
│   ├── index.css          # 登录页样式
│   └── home.css           # 主页样式
├── js/                    # JavaScript文件
│   ├── index.js           # 登录页逻辑
│   └── home.js            # 主页逻辑
├── server/                # 后端服务
│   └── app.py             # Flask应用主文件
├── database_init.sql      # 数据库初始化脚本
├── config.example.py      # 配置文件示例
├── requirements.txt       # Python依赖包列表
├── .gitignore            # Git忽略文件配置
└── README.md              # 项目说明文档
```

## 🚀 安装和部署

### 环境要求
- Python 3.7+
- MySQL 5.7+
- 现代Web浏览器

### 1. 克隆项目
```bash
git clone https://github.com/ca1cu1ation/library_reservation_system.git
cd library_reservation_system
```

### 2. 安装Python依赖
```bash
pip install -r requirements.txt
```
或者手动安装：
```bash
pip install flask flask-cors mysql-connector-python
```

### 3. 数据库配置

#### 3.1 快速初始化（推荐）
使用提供的初始化脚本：
```bash
mysql -u root -p < database_init.sql
```

#### 3.2 手动创建数据库
如果需要手动创建，请按以下步骤操作：

##### 创建数据库
```sql
CREATE DATABASE library_reveration_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library_reveration_system;
```

#### 3.2 创建数据表

**用户账号表**
```sql
-- 学生账号表
CREATE TABLE 学生账号 (
    学号 VARCHAR(20) PRIMARY KEY,
    密码 VARCHAR(255) NOT NULL
);

-- 教师账号表
CREATE TABLE 教师账号 (
    职工号 VARCHAR(20) PRIMARY KEY,
    密码 VARCHAR(255) NOT NULL
);
```

**座位管理表**
```sql
-- 座位表
CREATE TABLE 座位 (
    座位id INT PRIMARY KEY AUTO_INCREMENT,
    区域 VARCHAR(10) NOT NULL,
    座位号 VARCHAR(20) NOT NULL,
    状态 TINYINT DEFAULT 0 COMMENT '0:可用, 1:已预约'
);
```

**预约记录表**
```sql
-- 学生座位预约表
CREATE TABLE 学生座位预约 (
    预约id INT PRIMARY KEY AUTO_INCREMENT,
    座位id INT NOT NULL,
    学号 VARCHAR(20) NOT NULL,
    起始时间 DATETIME NOT NULL,
    结束时间 DATETIME NOT NULL,
    状态 VARCHAR(20) DEFAULT '未开始',
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (座位id) REFERENCES 座位(座位id),
    FOREIGN KEY (学号) REFERENCES 学生账号(学号)
);

-- 教师座位预约表
CREATE TABLE 教师座位预约 (
    预约id INT PRIMARY KEY AUTO_INCREMENT,
    座位id INT NOT NULL,
    职工号 VARCHAR(20) NOT NULL,
    起始时间 DATETIME NOT NULL,
    结束时间 DATETIME NOT NULL,
    状态 VARCHAR(20) DEFAULT '未开始',
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (座位id) REFERENCES 座位(座位id),
    FOREIGN KEY (职工号) REFERENCES 教师账号(职工号)
);
```

#### 3.3 插入示例数据
```sql
-- 插入座位数据 (示例)
INSERT INTO 座位 (区域, 座位号) VALUES 
('A', 'A001'), ('A', 'A002'), ('A', 'A003'),
('B', 'B001'), ('B', 'B002'), ('B', 'B003'),
('C', 'C001'), ('C', 'C002'), ('C', 'C003'),
('D', 'D001'), ('D', 'D002'), ('D', 'D003'),
('E', 'E001'), ('E', 'E002'), ('E', 'E003'),
('F', 'F001'), ('F', 'F002'), ('F', 'F003');

-- 插入测试用户数据
INSERT INTO 学生账号 (学号, 密码) VALUES 
('2021001', 'password123'),
('2021002', 'password123');

INSERT INTO 教师账号 (职工号, 密码) VALUES 
('T001', 'password123'),
('T002', 'password123');
```

### 4. 修改数据库配置

#### 方法1：使用配置文件（推荐）
```bash
# 复制配置文件模板
cp config.example.py config.py
# 编辑配置文件，修改数据库连接信息
nano config.py  # 或使用其他编辑器
```

#### 方法2：直接修改代码
编辑 `server/app.py` 文件中的数据库配置：
```python
db_config = {
    'host': 'localhost',        # 数据库主机
    'user': 'your_username',    # 数据库用户名
    'password': 'your_password', # 数据库密码
    'port': 3306,
    'database': 'library_reveration_system',
    "pool_name": "mypool",
    "pool_size": 5
}
```

### 5. 启动应用

#### 5.1 启动后端服务
```bash
cd server
python app.py
```
服务将在 http://localhost:3000 启动

#### 5.2 访问前端
使用浏览器打开 `html/index.html` 文件，或通过Web服务器访问。

## 📖 使用说明

### 用户登录
1. 打开登录页面 (`html/index.html`)
2. 输入用户ID和密码
3. 选择用户类型（学生/教师）
4. 点击登录按钮

### 座位预约
1. 登录成功后进入主页面
2. 选择开始时间和结束时间
3. 浏览各楼层和区域的座位
4. 点击可用座位进行预约
5. 确认预约信息

### 预约管理
1. 在主页面查看"我的预约记录"
2. 可以取消未开始的预约
3. 查看预约状态和时间

### 用户信息管理
1. 点击页面右上角用户头像
2. 选择"修改信息"
3. 更新个人密码

## 🔌 API接口文档

### 用户认证
- **POST** `/login` - 用户登录
  ```json
  // 请求
  {
    "username": "用户ID",
    "password": "密码",
    "usertype": "student|teacher"
  }
  // 响应
  {
    "success": true,
    "user": {
      "username": "用户ID",
      "usertype": "用户类型"
    }
  }
  ```

### 用户管理
- **GET** `/api/user/<user_type>&<user_id>` - 获取用户信息
- **PUT** `/api/user/<user_type>&<user_id>` - 更新用户信息

### 座位管理
- **GET** `/api/seats` - 获取所有座位信息
- **POST** `/api/reserve` - 创建座位预约
  ```json
  // 请求
  {
    "seat_id": "座位ID",
    "user_id": "用户ID",
    "user_type": "用户类型",
    "start_time": "开始时间",
    "end_time": "结束时间"
  }
  ```

### 预约管理
- **GET** `/api/reservations/<user_id>&<user_type>` - 获取用户预约列表
- **DELETE** `/api/cancel_reservations/<usertype>&<reservation_id>` - 取消预约

## 🔧 开发和维护

### 开发环境设置
1. 安装开发依赖
2. 配置代码编辑器
3. 设置调试环境

### 代码规范
- Python: 遵循PEP 8规范
- JavaScript: 使用ES6+语法
- HTML/CSS: 保持语义化和响应式设计

### 测试
- 单元测试：测试API接口功能
- 集成测试：测试前后端交互
- 用户测试：验证用户体验

## 📝 注意事项

1. **安全性**: 
   - 数据库密码请勿提交到版本控制
   - 建议使用环境变量管理敏感配置
   - 生产环境应使用HTTPS

2. **性能优化**:
   - 数据库查询优化
   - 前端资源压缩
   - 缓存策略实施

3. **备份与恢复**:
   - 定期备份数据库
   - 制定灾难恢复计划

## 🐛 常见问题

### 数据库连接失败
- 检查数据库服务是否启动
- 验证连接配置信息
- 确认网络连接正常

### 座位预约冲突
- 系统会自动检测时间冲突
- 选择其他时间段或座位

### 页面显示异常
- 检查浏览器兼容性
- 清除浏览器缓存
- 确认静态资源加载正常

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 👥 作者

- [ca1cu1ation](https://github.com/ca1cu1ation)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！