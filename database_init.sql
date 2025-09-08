-- 图书馆座位预约系统数据库初始化脚本
-- Database initialization script for Library Reservation System

-- 创建数据库
CREATE DATABASE IF NOT EXISTS library_reveration_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library_reveration_system;

-- 创建学生账号表
CREATE TABLE IF NOT EXISTS 学生账号 (
    学号 VARCHAR(20) PRIMARY KEY,
    密码 VARCHAR(255) NOT NULL,
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建教师账号表
CREATE TABLE IF NOT EXISTS 教师账号 (
    职工号 VARCHAR(20) PRIMARY KEY,
    密码 VARCHAR(255) NOT NULL,
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建座位表
CREATE TABLE IF NOT EXISTS 座位 (
    座位id INT PRIMARY KEY AUTO_INCREMENT,
    区域 VARCHAR(10) NOT NULL,
    座位号 VARCHAR(20) NOT NULL,
    状态 TINYINT DEFAULT 0 COMMENT '0:可用, 1:已预约',
    楼层 INT NOT NULL COMMENT '楼层号',
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_seat (区域, 座位号)
);

-- 创建学生座位预约表
CREATE TABLE IF NOT EXISTS 学生座位预约 (
    预约id INT PRIMARY KEY AUTO_INCREMENT,
    座位id INT NOT NULL,
    学号 VARCHAR(20) NOT NULL,
    起始时间 DATETIME NOT NULL,
    结束时间 DATETIME NOT NULL,
    状态 VARCHAR(20) DEFAULT '未开始',
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (座位id) REFERENCES 座位(座位id) ON DELETE CASCADE,
    FOREIGN KEY (学号) REFERENCES 学生账号(学号) ON DELETE CASCADE,
    INDEX idx_student_time (学号, 起始时间, 结束时间),
    INDEX idx_seat_time (座位id, 起始时间, 结束时间)
);

-- 创建教师座位预约表
CREATE TABLE IF NOT EXISTS 教师座位预约 (
    预约id INT PRIMARY KEY AUTO_INCREMENT,
    座位id INT NOT NULL,
    职工号 VARCHAR(20) NOT NULL,
    起始时间 DATETIME NOT NULL,
    结束时间 DATETIME NOT NULL,
    状态 VARCHAR(20) DEFAULT '未开始',
    创建时间 TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (座位id) REFERENCES 座位(座位id) ON DELETE CASCADE,
    FOREIGN KEY (职工号) REFERENCES 教师账号(职工号) ON DELETE CASCADE,
    INDEX idx_teacher_time (职工号, 起始时间, 结束时间),
    INDEX idx_seat_time (座位id, 起始时间, 结束时间)
);

-- 插入座位数据
-- 一楼：A区、B区
INSERT IGNORE INTO 座位 (区域, 座位号, 楼层) VALUES 
('A', 'A001', 1), ('A', 'A002', 1), ('A', 'A003', 1), ('A', 'A004', 1), ('A', 'A005', 1),
('A', 'A006', 1), ('A', 'A007', 1), ('A', 'A008', 1), ('A', 'A009', 1), ('A', 'A010', 1),
('B', 'B001', 1), ('B', 'B002', 1), ('B', 'B003', 1), ('B', 'B004', 1), ('B', 'B005', 1),
('B', 'B006', 1), ('B', 'B007', 1), ('B', 'B008', 1), ('B', 'B009', 1), ('B', 'B010', 1);

-- 二楼：C区
INSERT IGNORE INTO 座位 (区域, 座位号, 楼层) VALUES 
('C', 'C001', 2), ('C', 'C002', 2), ('C', 'C003', 2), ('C', 'C004', 2), ('C', 'C005', 2),
('C', 'C006', 2), ('C', 'C007', 2), ('C', 'C008', 2), ('C', 'C009', 2), ('C', 'C010', 2),
('C', 'C011', 2), ('C', 'C012', 2), ('C', 'C013', 2), ('C', 'C014', 2), ('C', 'C015', 2);

-- 三楼：D区、E区
INSERT IGNORE INTO 座位 (区域, 座位号, 楼层) VALUES 
('D', 'D001', 3), ('D', 'D002', 3), ('D', 'D003', 3), ('D', 'D004', 3), ('D', 'D005', 3),
('D', 'D006', 3), ('D', 'D007', 3), ('D', 'D008', 3), ('D', 'D009', 3), ('D', 'D010', 3),
('E', 'E001', 3), ('E', 'E002', 3), ('E', 'E003', 3), ('E', 'E004', 3), ('E', 'E005', 3),
('E', 'E006', 3), ('E', 'E007', 3), ('E', 'E008', 3), ('E', 'E009', 3), ('E', 'E010', 3);

-- 四楼：F区
INSERT IGNORE INTO 座位 (区域, 座位号, 楼层) VALUES 
('F', 'F001', 4), ('F', 'F002', 4), ('F', 'F003', 4), ('F', 'F004', 4), ('F', 'F005', 4),
('F', 'F006', 4), ('F', 'F007', 4), ('F', 'F008', 4), ('F', 'F009', 4), ('F', 'F010', 4),
('F', 'F011', 4), ('F', 'F012', 4), ('F', 'F013', 4), ('F', 'F014', 4), ('F', 'F015', 4);

-- 插入测试用户数据
INSERT IGNORE INTO 学生账号 (学号, 密码) VALUES 
('2021001', 'password123'),
('2021002', 'password123'),
('2021003', 'password123'),
('2022001', 'password123'),
('2022002', 'password123');

INSERT IGNORE INTO 教师账号 (职工号, 密码) VALUES 
('T001', 'password123'),
('T002', 'password123'),
('T003', 'password123');

-- 创建存储过程用于更新用户密码
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS update_account(
    IN p_user_id VARCHAR(20),
    IN p_user_type VARCHAR(10),
    IN p_password VARCHAR(255)
)
BEGIN
    IF p_user_type = '学生' THEN
        UPDATE 学生账号 SET 密码 = p_password WHERE 学号 = p_user_id;
    ELSEIF p_user_type = '教师' THEN
        UPDATE 教师账号 SET 密码 = p_password WHERE 职工号 = p_user_id;
    END IF;
END//
DELIMITER ;

-- 创建视图用于查看预约统计
CREATE OR REPLACE VIEW 预约统计 AS
SELECT 
    '学生' as 用户类型,
    COUNT(*) as 预约总数,
    COUNT(CASE WHEN 状态 = '未开始' THEN 1 END) as 未开始,
    COUNT(CASE WHEN 状态 = '进行中' THEN 1 END) as 进行中,
    COUNT(CASE WHEN 状态 = '已结束' THEN 1 END) as 已结束
FROM 学生座位预约
UNION ALL
SELECT 
    '教师' as 用户类型,
    COUNT(*) as 预约总数,
    COUNT(CASE WHEN 状态 = '未开始' THEN 1 END) as 未开始,
    COUNT(CASE WHEN 状态 = '进行中' THEN 1 END) as 进行中,
    COUNT(CASE WHEN 状态 = '已结束' THEN 1 END) as 已结束
FROM 教师座位预约;

COMMIT;

-- 显示初始化完成信息
SELECT '数据库初始化完成！' AS Message;
SELECT COUNT(*) AS 座位总数 FROM 座位;
SELECT COUNT(*) AS 学生账号数 FROM 学生账号;
SELECT COUNT(*) AS 教师账号数 FROM 教师账号;