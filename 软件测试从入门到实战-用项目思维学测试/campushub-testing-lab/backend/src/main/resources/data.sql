insert into campus_user (username, display_name, role_code, password_hint, status, failed_login_count) values
('student01', '测试学生一号', 'STUDENT', 'campus123', 'ACTIVE', 0),
('student02', '测试学生二号', 'STUDENT', 'campus123', 'ACTIVE', 0),
('club01', '社团负责人一号', 'CLUB_OWNER', 'campus123', 'ACTIVE', 0),
('library01', '图书管理员一号', 'LIBRARIAN', 'campus123', 'ACTIVE', 0),
('logistics01', '后勤管理员一号', 'LOGISTICS_ADMIN', 'campus123', 'ACTIVE', 0),
('admin01', '系统管理员一号', 'SYSTEM_ADMIN', 'campus123', 'ACTIVE', 0),
('student_locked', '锁定样例学生', 'STUDENT', 'campus123', 'LOCKED', 5),
('student_overdue', '逾期样例学生', 'STUDENT', 'campus123', 'ACTIVE', 0);

insert into activity (title, organizer, location, capacity, registered_count, status) values
('新生编程训练营', '软件协会', '创新楼 301', 60, 42, 'OPEN'),
('校园摄影工作坊', '摄影社', '艺术楼 205', 30, 30, 'FULL'),
('毕业设计答辩观摩', '教务中心', '图书馆报告厅', 120, 87, 'OPEN'),
('社团招新宣讲会', '学生社团联合会', '大学生活动中心', 200, 156, 'OPEN'),
('数据分析入门分享', '数据科学社', '教学楼 B203', 50, 18, 'OPEN'),
('志愿服务说明会', '青年志愿者协会', '教学楼 A101', 80, 80, 'FULL'),
('英语角交流活动', '外语协会', '图书馆二楼', 40, 12, 'OPEN'),
('校园跑步打卡挑战', '体育社', '东操场', 100, 64, 'OPEN'),
('心理健康公开课', '心理中心', '行政楼报告厅', 90, 45, 'OPEN'),
('创新创业路演', '创业协会', '创新楼路演厅', 70, 69, 'OPEN');

insert into room (name, building, capacity, status) values
('A101 自习室', '教学楼 A', 48, 'AVAILABLE'),
('B203 会议室', '教学楼 B', 24, 'AVAILABLE'),
('创新楼路演厅', '创新楼', 80, 'AVAILABLE'),
('图书馆研讨间 1', '图书馆', 12, 'AVAILABLE'),
('图书馆研讨间 2', '图书馆', 12, 'MAINTENANCE'),
('大学生活动中心排练室', '活动中心', 30, 'AVAILABLE');

insert into device (name, category, total_quantity, available_quantity, status) values
('投影仪', '展示设备', 8, 5, 'AVAILABLE'),
('无线麦克风', '音频设备', 12, 7, 'AVAILABLE'),
('移动白板', '教学设备', 6, 3, 'AVAILABLE'),
('录音笔', '采集设备', 10, 6, 'AVAILABLE'),
('活动帐篷', '活动物资', 15, 2, 'AVAILABLE'),
('折叠桌', '活动物资', 30, 18, 'AVAILABLE'),
('便携音箱', '音频设备', 5, 0, 'OUT_OF_STOCK'),
('手持云台', '拍摄设备', 4, 1, 'AVAILABLE');

insert into device_borrow (device_id, user_id, quantity, status, borrowed_at, due_at, created_at) values
(1, 3, 1, 'BORROWED', date '2026-06-16', date '2026-06-30', timestamp '2026-06-15 10:00:00'),
(4, 1, 1, 'PENDING', date '2026-06-28', date '2026-07-05', timestamp '2026-06-21 09:30:00');

insert into book (isbn, title, author, category, total_copies, available_copies) values
('978-7-001-00001-1', '软件测试入门实践', 'CampusHub 教研组', '软件测试', 5, 3),
('978-7-001-00002-8', 'Web 自动化测试基础', 'CampusHub 教研组', '自动化测试', 4, 2),
('978-7-001-00003-5', '接口测试任务手册', 'CampusHub 教研组', '接口测试', 6, 6),
('978-7-001-00004-2', '性能测试指标导读', 'CampusHub 教研组', '性能测试', 3, 1),
('978-7-001-00005-9', '数据库基础与数据校验', 'CampusHub 教研组', '数据库', 5, 5),
('978-7-001-00006-6', '需求分析与评审', 'CampusHub 教研组', '需求分析', 4, 4),
('978-7-001-00007-3', '缺陷报告写作训练', 'CampusHub 教研组', '缺陷管理', 6, 2),
('978-7-001-00008-0', '测试用例设计方法', 'CampusHub 教研组', '用例设计', 8, 7),
('978-7-001-00009-7', 'Java Web 项目导读', 'CampusHub 教研组', '开发基础', 5, 3),
('978-7-001-00010-3', '前端页面测试要点', 'CampusHub 教研组', '前端测试', 4, 1),
('978-7-001-00011-0', '校园服务系统案例集', 'CampusHub 教研组', '案例实践', 7, 6),
('978-7-001-00012-7', '测试新人面试准备', 'CampusHub 教研组', '职业发展', 5, 5),
('978-7-001-00013-4', '代码阅读与灰盒测试', 'CampusHub 教研组', '灰盒测试', 3, 2),
('978-7-001-00014-1', 'JMeter 练习册', 'CampusHub 教研组', '性能测试', 6, 4),
('978-7-001-00015-8', 'Selenium 练习册', 'CampusHub 教研组', '自动化测试', 6, 5),
('978-7-001-00016-5', '测试计划与发布检查', 'CampusHub 教研组', '测试管理', 4, 4),
('978-7-001-00017-2', '状态流转测试案例', 'CampusHub 教研组', '用例设计', 5, 2),
('978-7-001-00018-9', '边界值分析案例', 'CampusHub 教研组', '用例设计', 5, 0),
('978-7-001-00019-6', '判定表设计案例', 'CampusHub 教研组', '用例设计', 5, 3),
('978-7-001-00020-2', '回归测试策略入门', 'CampusHub 教研组', '测试策略', 5, 5);

insert into activity_registration (activity_id, user_id, status, created_at) values
(1, 1, 'CONFIRMED', timestamp '2026-06-01 09:00:00'),
(1, 2, 'CONFIRMED', timestamp '2026-06-01 09:05:00'),
(3, 1, 'CONFIRMED', timestamp '2026-06-02 10:00:00'),
(5, 2, 'CANCELLED', timestamp '2026-06-03 11:00:00'),
(8, 1, 'CONFIRMED', timestamp '2026-06-04 12:00:00');

insert into book_borrow (book_id, user_id, status, borrowed_at, due_at, renew_count) values
(1, 1, 'BORROWED', date '2026-06-10', date '2026-07-10', 0),
(4, 8, 'OVERDUE', date '2026-05-01', date '2026-06-01', 1),
(7, 2, 'BORROWED', date '2026-06-15', date '2026-07-15', 0),
(18, 1, 'RESERVED', date '2026-06-20', date '2026-07-20', 0);

insert into room_reservation (room_id, user_id, reservation_date, start_hour, end_hour, status, created_at) values
(4, 2, date '2026-06-28', 9, 11, 'APPROVED', timestamp '2026-06-18 15:00:00'),
(1, 1, date '2026-06-29', 14, 16, 'PENDING', timestamp '2026-06-20 09:00:00');

insert into notification (user_id, title, read_flag) values
(1, '新生编程训练营报名成功', false),
(2, '校园摄影工作坊名额已满', true),
(8, '图书即将逾期提醒', false);

insert into review_task (task_type, title, applicant, status, reviewer, comment, created_at, reviewed_at) values
('ROOM_RESERVATION', 'A101 自习室预约申请', 'student01', 'PENDING', null, null, timestamp '2026-06-20 09:00:00', null),
('DEVICE_BORROW', '投影仪借用申请', 'club01', 'PENDING', null, null, timestamp '2026-06-21 10:30:00', null),
('BOOK_EXCEPTION', '逾期图书人工处理', 'student_overdue', 'PENDING', null, null, timestamp '2026-06-22 14:20:00', null),
('ROOM_RESERVATION', '图书馆研讨间 1 预约申请', 'student02', 'APPROVED', 'admin01', '用途明确，准予预约', timestamp '2026-06-18 15:00:00', timestamp '2026-06-18 16:00:00');

insert into audit_log (actor, action, target_type, target_id, created_at) values
('admin01', 'CREATE_ACTIVITY', 'Activity', 1, timestamp '2026-05-25 10:00:00'),
('library01', 'MARK_BOOK_OVERDUE', 'BookBorrow', 2, timestamp '2026-06-02 09:30:00'),
('logistics01', 'UPDATE_DEVICE_STOCK', 'Device', 7, timestamp '2026-06-05 15:20:00');

