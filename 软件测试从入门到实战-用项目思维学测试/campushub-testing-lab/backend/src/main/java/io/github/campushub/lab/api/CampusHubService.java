package io.github.campushub.lab.api;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

@Service
public class CampusHubService {

    private static final int MAX_ACTIVE_BORROWS = 3;
    private static final int BORROW_DAYS = 30;
    private static final int RENEW_DAYS = 14;

    private final JdbcClient jdbcClient;

    public CampusHubService(JdbcClient jdbcClient) {
        this.jdbcClient = jdbcClient;
    }
    public Map<String, String> health() {
        return Map.of("status", "UP", "project", "campushub-testing-lab");
    }
    public OverviewResponse overview() {
        List<ModuleSummary> modules = List.of(
            new ModuleSummary("账号中心", "登录、角色、连续失败锁定", "等价类、权限矩阵、自动化前置条件"),
            new ModuleSummary("活动中心", "活动浏览、报名、取消报名", "场景法、判定表、性能测试"),
            new ModuleSummary("场地预约", "场地查询、预约申请、审核流转", "边界值、时间冲突、状态流转"),
            new ModuleSummary("设备借用", "设备库存、借用申请、通知提醒", "库存边界、审批链路、消息一致性"),
            new ModuleSummary("BookNest", "图书检索、借阅、续借、归还", "边界值、状态流转、数据一致性"),
            new ModuleSummary("后台审核", "审核任务、操作日志", "权限测试、审计字段完整性")
        );

        Map<String, Integer> statistics = Map.of(
            "users", count("campus_user"),
            "activities", count("activity"),
            "books", count("book"),
            "rooms", count("room"),
            "devices", count("device")
        );

        return new OverviewResponse("CampusHub Testing Lab", "0.2.0-SNAPSHOT", modules, statistics);
    }
    public LoginResponse login( LoginRequest request) {
        UserItem user = findUserByUsername(request.username());
        if (!"ACTIVE".equals(user.status())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "账号已锁定或不可用");
        }
        if (!user.passwordHint().equals(request.password())) {
            jdbcClient.sql("update campus_user set failed_login_count = failed_login_count + 1 where id = :id")
                .param("id", user.id())
                .update();
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "用户名或密码错误");
        }
        jdbcClient.sql("update campus_user set failed_login_count = 0 where id = :id")
            .param("id", user.id())
            .update();
        writeAudit(user.username(), "LOGIN", "User", user.id());
        return new LoginResponse("demo-token-" + user.username(), user, permissionsFor(user.roleCode()));
    }
    public List<ActivityItem> activities( String username) {
        return jdbcClient.sql("""
                select a.id, a.title, a.organizer, a.location, a.capacity, a.registered_count, a.status,
                       case when exists (
                           select 1 from activity_registration ar
                           join campus_user cu on cu.id = ar.user_id
                           where ar.activity_id = a.id
                             and ar.status = 'CONFIRMED'
                             and cu.username = :username
                       ) then true else false end as registered
                from activity a
                order by a.id
                """)
            .param("username", username)
            .query((rs, rowNum) -> new ActivityItem(
                rs.getLong("id"),
                rs.getString("title"),
                rs.getString("organizer"),
                rs.getString("location"),
                rs.getInt("capacity"),
                rs.getInt("registered_count"),
                rs.getString("status"),
                rs.getBoolean("registered")
            ))
            .list();
    }
    public ActionResponse registerActivity(
         Long activityId,
         UserActionRequest request
    ) {
        UserItem user = requireActiveUser(request.username());
        ActivityState activity = findActivity(activityId);
        if (!"OPEN".equals(activity.status())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "活动当前不可报名");
        }
        if (activity.registeredCount() >= activity.capacity()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "活动名额已满");
        }
        int existing = jdbcClient.sql("""
                select count(*) from activity_registration
                where activity_id = :activityId and user_id = :userId and status = 'CONFIRMED'
                """)
            .param("activityId", activityId)
            .param("userId", user.id())
            .query(Integer.class)
            .single();
        if (existing > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "不能重复报名同一个活动");
        }

        jdbcClient.sql("""
                insert into activity_registration (activity_id, user_id, status, created_at)
                values (:activityId, :userId, 'CONFIRMED', :createdAt)
                """)
            .param("activityId", activityId)
            .param("userId", user.id())
            .param("createdAt", LocalDateTime.now())
            .update();
        jdbcClient.sql("""
                update activity
                set registered_count = registered_count + 1,
                    status = case when registered_count + 1 >= capacity then 'FULL' else status end
                where id = :activityId
                """)
            .param("activityId", activityId)
            .update();
        createNotification(user.id(), activity.title() + "报名成功");
        writeAudit(user.username(), "REGISTER_ACTIVITY", "Activity", activityId);
        return new ActionResponse("ACTIVITY_REGISTERED", "活动报名成功");
    }
    public ActionResponse cancelActivity( Long activityId,  String username) {
        UserItem user = requireActiveUser(username);
        int changed = jdbcClient.sql("""
                update activity_registration
                set status = 'CANCELLED'
                where activity_id = :activityId and user_id = :userId and status = 'CONFIRMED'
                """)
            .param("activityId", activityId)
            .param("userId", user.id())
            .update();
        if (changed == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "没有可取消的报名记录");
        }
        jdbcClient.sql("""
                update activity
                set registered_count = case when registered_count > 0 then registered_count - 1 else 0 end,
                    status = case when status = 'FULL' then 'OPEN' else status end
                where id = :activityId
                """)
            .param("activityId", activityId)
            .update();
        writeAudit(user.username(), "CANCEL_ACTIVITY", "Activity", activityId);
        return new ActionResponse("ACTIVITY_CANCELLED", "活动报名已取消");
    }
    public List<BookItem> books( String keyword) {
        String likeKeyword = "%" + keyword.trim().toLowerCase() + "%";
        return jdbcClient.sql("""
                select id, isbn, title, author, category, total_copies, available_copies
                from book
                where lower(title) like :keyword
                   or lower(author) like :keyword
                   or lower(category) like :keyword
                   or lower(isbn) like :keyword
                order by id
                """)
            .param("keyword", likeKeyword)
            .query((rs, rowNum) -> new BookItem(
                rs.getLong("id"),
                rs.getString("isbn"),
                rs.getString("title"),
                rs.getString("author"),
                rs.getString("category"),
                rs.getInt("total_copies"),
                rs.getInt("available_copies")
            ))
            .list();
    }
    public List<BookBorrowItem> bookBorrows( String username) {
        UserItem user = requireActiveUser(username);
        return jdbcClient.sql("""
                select bb.id, b.title, bb.status, bb.borrowed_at, bb.due_at, bb.renew_count
                from book_borrow bb
                join book b on b.id = bb.book_id
                where bb.user_id = :userId
                order by bb.id desc
                """)
            .param("userId", user.id())
            .query((rs, rowNum) -> new BookBorrowItem(
                rs.getLong("id"),
                rs.getString("title"),
                rs.getString("status"),
                rs.getDate("borrowed_at").toLocalDate(),
                rs.getDate("due_at").toLocalDate(),
                rs.getInt("renew_count")
            ))
            .list();
    }
    public ActionResponse borrowBook( Long bookId,  UserActionRequest request) {
        UserItem user = requireActiveUser(request.username());
        BookState book = findBook(bookId);
        if (book.availableCopies() <= 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "图书当前无可借库存");
        }
        int activeBorrows = jdbcClient.sql("""
                select count(*) from book_borrow
                where user_id = :userId and status in ('BORROWED', 'OVERDUE')
                """)
            .param("userId", user.id())
            .query(Integer.class)
            .single();
        if (activeBorrows >= MAX_ACTIVE_BORROWS) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "已达到最大借阅数量");
        }
        LocalDate borrowedAt = LocalDate.now();
        jdbcClient.sql("""
                insert into book_borrow (book_id, user_id, status, borrowed_at, due_at, renew_count)
                values (:bookId, :userId, 'BORROWED', :borrowedAt, :dueAt, 0)
                """)
            .param("bookId", bookId)
            .param("userId", user.id())
            .param("borrowedAt", borrowedAt)
            .param("dueAt", borrowedAt.plusDays(BORROW_DAYS))
            .update();
        jdbcClient.sql("update book set available_copies = available_copies - 1 where id = :bookId")
            .param("bookId", bookId)
            .update();
        createNotification(user.id(), book.title() + "借阅成功");
        writeAudit(user.username(), "BORROW_BOOK", "Book", bookId);
        return new ActionResponse("BOOK_BORROWED", "图书借阅成功");
    }
    public ActionResponse renewBook( Long borrowId,  UserActionRequest request) {
        UserItem user = requireActiveUser(request.username());
        BorrowState borrow = findBorrow(borrowId, user.id());
        if (!"BORROWED".equals(borrow.status())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "只有借阅中图书可以续借");
        }
        if (borrow.renewCount() >= 1) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "该图书已达到续借次数上限");
        }
        if (borrow.dueAt().isBefore(LocalDate.now())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "逾期图书不能续借");
        }
        jdbcClient.sql("""
                update book_borrow
                set renew_count = renew_count + 1, due_at = :dueAt
                where id = :borrowId
                """)
            .param("borrowId", borrowId)
            .param("dueAt", borrow.dueAt().plusDays(RENEW_DAYS))
            .update();
        writeAudit(user.username(), "RENEW_BOOK", "BookBorrow", borrowId);
        return new ActionResponse("BOOK_RENEWED", "图书续借成功");
    }
    public ActionResponse returnBook( Long borrowId,  UserActionRequest request) {
        UserItem user = requireActiveUser(request.username());
        BorrowState borrow = findBorrow(borrowId, user.id());
        if (!List.of("BORROWED", "OVERDUE").contains(borrow.status())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "当前借阅记录不能归还");
        }
        jdbcClient.sql("update book_borrow set status = 'RETURNED' where id = :borrowId")
            .param("borrowId", borrowId)
            .update();
        jdbcClient.sql("update book set available_copies = available_copies + 1 where id = :bookId")
            .param("bookId", borrow.bookId())
            .update();
        writeAudit(user.username(), "RETURN_BOOK", "BookBorrow", borrowId);
        return new ActionResponse("BOOK_RETURNED", "图书归还成功");
    }
    public List<RoomItem> rooms() {
        return jdbcClient.sql("""
                select r.id, r.name, r.building, r.capacity, r.status,
                       (select count(*) from room_reservation rr
                        where rr.room_id = r.id and rr.status in ('PENDING', 'APPROVED')) as active_reservations
                from room r
                order by r.id
                """)
            .query((rs, rowNum) -> new RoomItem(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getString("building"),
                rs.getInt("capacity"),
                rs.getString("status"),
                rs.getInt("active_reservations")
            ))
            .list();
    }

    public List<RoomReservationItem> roomReservations(String username) {
        UserItem user = requireActiveUser(username);
        return jdbcClient.sql("""
                select rr.id, r.name, rr.reservation_date, rr.start_hour, rr.end_hour, rr.status
                from room_reservation rr
                join room r on r.id = rr.room_id
                where rr.user_id = :userId
                order by rr.reservation_date desc, rr.start_hour
                """)
            .param("userId", user.id())
            .query((rs, rowNum) -> new RoomReservationItem(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getDate("reservation_date").toLocalDate(),
                rs.getInt("start_hour"),
                rs.getInt("end_hour"),
                rs.getString("status")
            ))
            .list();
    }

    public ActionResponse reserveRoom(Long roomId, RoomReservationRequest request) {
        UserItem user = requireActiveUser(request.username());
        RoomState room = findRoom(roomId);
        if (!"AVAILABLE".equals(room.status())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "场地当前不可预约");
        }
        if (request.reservationDate() == null || request.reservationDate().isBefore(LocalDate.now())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "只能预约今天或未来日期");
        }
        if (request.startHour() < 8 || request.endHour() > 22 || request.startHour() >= request.endHour()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "预约时间必须在 8:00-22:00 且开始时间早于结束时间");
        }
        if (request.endHour() - request.startHour() > 3) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "单次预约不能超过 3 小时");
        }
        int conflicts = jdbcClient.sql("""
                select count(*) from room_reservation
                where room_id = :roomId
                  and reservation_date = :reservationDate
                  and status in ('PENDING', 'APPROVED')
                  and start_hour < :endHour
                  and end_hour > :startHour
                """)
            .param("roomId", roomId)
            .param("reservationDate", request.reservationDate())
            .param("startHour", request.startHour())
            .param("endHour", request.endHour())
            .query(Integer.class)
            .single();
        if (conflicts > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "该时段已有预约或待审核申请");
        }
        jdbcClient.sql("""
                insert into room_reservation (room_id, user_id, reservation_date, start_hour, end_hour, status, created_at)
                values (:roomId, :userId, :reservationDate, :startHour, :endHour, 'PENDING', :createdAt)
                """)
            .param("roomId", roomId)
            .param("userId", user.id())
            .param("reservationDate", request.reservationDate())
            .param("startHour", request.startHour())
            .param("endHour", request.endHour())
            .param("createdAt", LocalDateTime.now())
            .update();
        jdbcClient.sql("""
                insert into review_task (task_type, title, applicant, status, reviewer, comment, created_at, reviewed_at)
                values ('ROOM_RESERVATION', :title, :applicant, 'PENDING', null, null, :createdAt, null)
                """)
            .param("title", room.name() + "预约申请")
            .param("applicant", user.username())
            .param("createdAt", LocalDateTime.now())
            .update();
        createNotification(user.id(), room.name() + "预约申请已提交");
        writeAudit(user.username(), "RESERVE_ROOM", "Room", roomId);
        return new ActionResponse("ROOM_RESERVATION_SUBMITTED", "场地预约申请已提交");
    }

    public List<DeviceItem> devices() {
        return jdbcClient.sql("""
                select id, name, category, total_quantity, available_quantity, status
                from device
                order by id
                """)
            .query((rs, rowNum) -> new DeviceItem(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getString("category"),
                rs.getInt("total_quantity"),
                rs.getInt("available_quantity"),
                rs.getString("status")
            ))
            .list();
    }

    public List<DeviceBorrowItem> deviceBorrows(String username) {
        UserItem user = requireActiveUser(username);
        return jdbcClient.sql("""
                select db.id, d.name, db.quantity, db.status, db.borrowed_at, db.due_at
                from device_borrow db
                join device d on d.id = db.device_id
                where db.user_id = :userId
                order by db.id desc
                """)
            .param("userId", user.id())
            .query((rs, rowNum) -> new DeviceBorrowItem(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getInt("quantity"),
                rs.getString("status"),
                rs.getDate("borrowed_at").toLocalDate(),
                rs.getDate("due_at").toLocalDate()
            ))
            .list();
    }

    public ActionResponse borrowDevice(Long deviceId, DeviceBorrowRequest request) {
        UserItem user = requireActiveUser(request.username());
        DeviceState device = findDevice(deviceId);
        if (!"AVAILABLE".equals(device.status())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "设备当前不可借用");
        }
        if (request.quantity() == null || request.quantity() <= 0) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "借用数量必须大于 0");
        }
        if (request.quantity() > device.availableQuantity()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "设备可借数量不足");
        }
        if (request.borrowedAt() == null || request.dueAt() == null || request.borrowedAt().isAfter(request.dueAt())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "借用日期和归还日期不合法");
        }
        int existing = jdbcClient.sql("""
                select count(*) from device_borrow
                where device_id = :deviceId
                  and user_id = :userId
                  and status in ('PENDING', 'BORROWED')
                """)
            .param("deviceId", deviceId)
            .param("userId", user.id())
            .query(Integer.class)
            .single();
        if (existing > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "同一设备已有待处理或借用中记录");
        }
        jdbcClient.sql("""
                insert into device_borrow (device_id, user_id, quantity, status, borrowed_at, due_at, created_at)
                values (:deviceId, :userId, :quantity, 'PENDING', :borrowedAt, :dueAt, :createdAt)
                """)
            .param("deviceId", deviceId)
            .param("userId", user.id())
            .param("quantity", request.quantity())
            .param("borrowedAt", request.borrowedAt())
            .param("dueAt", request.dueAt())
            .param("createdAt", LocalDateTime.now())
            .update();
        jdbcClient.sql("""
                insert into review_task (task_type, title, applicant, status, reviewer, comment, created_at, reviewed_at)
                values ('DEVICE_BORROW', :title, :applicant, 'PENDING', null, null, :createdAt, null)
                """)
            .param("title", device.name() + "借用申请")
            .param("applicant", user.username())
            .param("createdAt", LocalDateTime.now())
            .update();
        createNotification(user.id(), device.name() + "借用申请已提交");
        writeAudit(user.username(), "BORROW_DEVICE", "Device", deviceId);
        return new ActionResponse("DEVICE_BORROW_SUBMITTED", "设备借用申请已提交");
    }

    public List<NotificationItem> notifications(String username) {
        UserItem user = requireActiveUser(username);
        return jdbcClient.sql("""
                select id, title, read_flag
                from notification
                where user_id = :userId
                order by id desc
                """)
            .param("userId", user.id())
            .query((rs, rowNum) -> new NotificationItem(
                rs.getLong("id"),
                rs.getString("title"),
                rs.getBoolean("read_flag")
            ))
            .list();
    }

    public ActionResponse markNotificationRead(Long notificationId, UserActionRequest request) {
        UserItem user = requireActiveUser(request.username());
        int changed = jdbcClient.sql("""
                update notification
                set read_flag = true
                where id = :notificationId and user_id = :userId
                """)
            .param("notificationId", notificationId)
            .param("userId", user.id())
            .update();
        if (changed == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "通知不存在或不属于当前用户");
        }
        writeAudit(user.username(), "READ_NOTIFICATION", "Notification", notificationId);
        return new ActionResponse("NOTIFICATION_READ", "通知已标记为已读");
    }

    public List<ReviewTaskItem> reviewTasks() {
        return jdbcClient.sql("""
                select id, task_type, title, applicant, status, reviewer, comment, created_at, reviewed_at
                from review_task
                order by case when status = 'PENDING' then 0 else 1 end, id
                """)
            .query((rs, rowNum) -> new ReviewTaskItem(
                rs.getLong("id"),
                rs.getString("task_type"),
                rs.getString("title"),
                rs.getString("applicant"),
                rs.getString("status"),
                rs.getString("reviewer"),
                rs.getString("comment"),
                rs.getTimestamp("created_at").toLocalDateTime(),
                rs.getTimestamp("reviewed_at") == null ? null : rs.getTimestamp("reviewed_at").toLocalDateTime()
            ))
            .list();
    }
    public ActionResponse decideReviewTask(
         Long taskId,
         ReviewDecisionRequest request
    ) {
        UserItem reviewer = requireActiveUser(request.reviewer());
        if (!List.of("SYSTEM_ADMIN", "LIBRARIAN", "LOGISTICS_ADMIN").contains(reviewer.roleCode())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "当前角色无审核权限");
        }
        String decision = request.decision().toUpperCase();
        if (!List.of("APPROVED", "REJECTED").contains(decision)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "审核结果只能是 APPROVED 或 REJECTED");
        }
        int changed = jdbcClient.sql("""
                update review_task
                set status = :decision, reviewer = :reviewer, comment = :comment, reviewed_at = :reviewedAt
                where id = :taskId and status = 'PENDING'
                """)
            .param("decision", decision)
            .param("reviewer", reviewer.username())
            .param("comment", request.comment() == null ? "" : request.comment())
            .param("reviewedAt", LocalDateTime.now())
            .param("taskId", taskId)
            .update();
        if (changed == 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "审核任务不存在或已处理");
        }
        writeAudit(reviewer.username(), "DECIDE_REVIEW_TASK", "ReviewTask", taskId);
        return new ActionResponse("REVIEW_TASK_" + decision, "审核任务已处理");
    }

    private int count(String tableName) {
        return jdbcClient.sql("select count(*) from " + tableName).query(Integer.class).single();
    }

    private UserItem findUserByUsername(String username) {
        return jdbcClient.sql("""
                select id, username, display_name, role_code, password_hint, status, failed_login_count
                from campus_user
                where username = :username
                """)
            .param("username", username)
            .query((rs, rowNum) -> new UserItem(
                rs.getLong("id"),
                rs.getString("username"),
                rs.getString("display_name"),
                rs.getString("role_code"),
                rs.getString("password_hint"),
                rs.getString("status"),
                rs.getInt("failed_login_count")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED, "用户名或密码错误"));
    }

    private UserItem requireActiveUser(String username) {
        UserItem user = findUserByUsername(username);
        if (!"ACTIVE".equals(user.status())) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "账号已锁定或不可用");
        }
        return user;
    }

    private ActivityState findActivity(Long activityId) {
        return jdbcClient.sql("select id, title, capacity, registered_count, status from activity where id = :id")
            .param("id", activityId)
            .query((rs, rowNum) -> new ActivityState(
                rs.getLong("id"),
                rs.getString("title"),
                rs.getInt("capacity"),
                rs.getInt("registered_count"),
                rs.getString("status")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "活动不存在"));
    }

    private RoomState findRoom(Long roomId) {
        return jdbcClient.sql("select id, name, status from room where id = :id")
            .param("id", roomId)
            .query((rs, rowNum) -> new RoomState(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getString("status")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "场地不存在"));
    }

    private DeviceState findDevice(Long deviceId) {
        return jdbcClient.sql("select id, name, available_quantity, status from device where id = :id")
            .param("id", deviceId)
            .query((rs, rowNum) -> new DeviceState(
                rs.getLong("id"),
                rs.getString("name"),
                rs.getInt("available_quantity"),
                rs.getString("status")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "设备不存在"));
    }

    private BookState findBook(Long bookId) {
        return jdbcClient.sql("select id, title, available_copies from book where id = :id")
            .param("id", bookId)
            .query((rs, rowNum) -> new BookState(
                rs.getLong("id"),
                rs.getString("title"),
                rs.getInt("available_copies")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "图书不存在"));
    }

    private BorrowState findBorrow(Long borrowId, Long userId) {
        return jdbcClient.sql("""
                select id, book_id, status, due_at, renew_count
                from book_borrow
                where id = :borrowId and user_id = :userId
                """)
            .param("borrowId", borrowId)
            .param("userId", userId)
            .query((rs, rowNum) -> new BorrowState(
                rs.getLong("id"),
                rs.getLong("book_id"),
                rs.getString("status"),
                rs.getDate("due_at").toLocalDate(),
                rs.getInt("renew_count")
            ))
            .optional()
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "借阅记录不存在"));
    }

    private List<String> permissionsFor(String roleCode) {
        return switch (roleCode) {
            case "SYSTEM_ADMIN" -> List.of("ACTIVITY_READ", "BOOK_READ", "REVIEW_TASK_DECIDE", "AUDIT_READ");
            case "LIBRARIAN" -> List.of("BOOK_READ", "BOOK_MANAGE", "REVIEW_TASK_DECIDE");
            case "LOGISTICS_ADMIN" -> List.of("ROOM_READ", "DEVICE_READ", "REVIEW_TASK_DECIDE");
            case "CLUB_OWNER" -> List.of("ACTIVITY_READ", "ACTIVITY_MANAGE");
            default -> List.of("ACTIVITY_READ", "ACTIVITY_REGISTER", "BOOK_READ", "BOOK_BORROW");
        };
    }

    private void createNotification(Long userId, String title) {
        jdbcClient.sql("insert into notification (user_id, title, read_flag) values (:userId, :title, false)")
            .param("userId", userId)
            .param("title", title)
            .update();
    }

    private void writeAudit(String actor, String action, String targetType, Long targetId) {
        jdbcClient.sql("""
                insert into audit_log (actor, action, target_type, target_id, created_at)
                values (:actor, :action, :targetType, :targetId, :createdAt)
                """)
            .param("actor", actor)
            .param("action", action)
            .param("targetType", targetType)
            .param("targetId", targetId)
            .param("createdAt", LocalDateTime.now())
            .update();
    }

    public record OverviewResponse(
        String project,
        String version,
        List<ModuleSummary> modules,
        Map<String, Integer> statistics
    ) {
    }

    public record ModuleSummary(String name, String scope, String testingValue) {
    }

    public record LoginRequest(String username, String password) {
    }

    public record LoginResponse(String token, UserItem user, List<String> permissions) {
    }

    public record UserActionRequest(String username) {
    }

    public record ReviewDecisionRequest(String reviewer, String decision, String comment) {
    }

    public record ActionResponse(String code, String message) {
    }

    public record UserItem(
        Long id,
        String username,
        String displayName,
        String roleCode,
        String passwordHint,
        String status,
        Integer failedLoginCount
    ) {
    }

    public record ActivityItem(
        Long id,
        String title,
        String organizer,
        String location,
        Integer capacity,
        Integer registeredCount,
        String status,
        Boolean registered
    ) {
    }

    public record BookItem(
        Long id,
        String isbn,
        String title,
        String author,
        String category,
        Integer totalCopies,
        Integer availableCopies
    ) {
    }

    public record BookBorrowItem(
        Long id,
        String title,
        String status,
        LocalDate borrowedAt,
        LocalDate dueAt,
        Integer renewCount
    ) {
    }

    public record RoomItem(
        Long id,
        String name,
        String building,
        Integer capacity,
        String status,
        Integer activeReservations
    ) {
    }

    public record RoomReservationRequest(String username, LocalDate reservationDate, Integer startHour, Integer endHour) {
    }

    public record RoomReservationItem(
        Long id,
        String roomName,
        LocalDate reservationDate,
        Integer startHour,
        Integer endHour,
        String status
    ) {
    }

    public record DeviceItem(
        Long id,
        String name,
        String category,
        Integer totalQuantity,
        Integer availableQuantity,
        String status
    ) {
    }

    public record DeviceBorrowRequest(String username, Integer quantity, LocalDate borrowedAt, LocalDate dueAt) {
    }

    public record DeviceBorrowItem(
        Long id,
        String deviceName,
        Integer quantity,
        String status,
        LocalDate borrowedAt,
        LocalDate dueAt
    ) {
    }

    public record NotificationItem(Long id, String title, Boolean readFlag) {
    }

    public record ReviewTaskItem(
        Long id,
        String taskType,
        String title,
        String applicant,
        String status,
        String reviewer,
        String comment,
        LocalDateTime createdAt,
        LocalDateTime reviewedAt
    ) {
    }

    private record ActivityState(Long id, String title, Integer capacity, Integer registeredCount, String status) {
    }

    private record RoomState(Long id, String name, String status) {
    }

    private record DeviceState(Long id, String name, Integer availableQuantity, String status) {
    }

    private record BookState(Long id, String title, Integer availableCopies) {
    }

    private record BorrowState(Long id, Long bookId, String status, LocalDate dueAt, Integer renewCount) {
    }
}


