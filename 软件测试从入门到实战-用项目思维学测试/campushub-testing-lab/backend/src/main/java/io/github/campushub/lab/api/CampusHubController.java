package io.github.campushub.lab.api;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class CampusHubController {

    private static final int MAX_ACTIVE_BORROWS = 3;
    private static final int BORROW_DAYS = 30;
    private static final int RENEW_DAYS = 14;

    private final JdbcClient jdbcClient;

    public CampusHubController(JdbcClient jdbcClient) {
        this.jdbcClient = jdbcClient;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of("status", "UP", "project", "campushub-testing-lab");
    }

    @GetMapping("/overview")
    public OverviewResponse overview() {
        List<ModuleSummary> modules = List.of(
            new ModuleSummary("账号中心", "登录、角色、连续失败锁定", "等价类、权限矩阵、自动化前置条件"),
            new ModuleSummary("活动中心", "活动浏览、报名、取消报名", "场景法、判定表、性能测试"),
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

    @PostMapping("/auth/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
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

    @GetMapping("/activities")
    public List<ActivityItem> activities(@RequestParam(defaultValue = "") String username) {
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

    @PostMapping("/activities/{activityId}/registrations")
    public ActionResponse registerActivity(
        @PathVariable Long activityId,
        @RequestBody UserActionRequest request
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

    @DeleteMapping("/activities/{activityId}/registrations/{username}")
    public ActionResponse cancelActivity(@PathVariable Long activityId, @PathVariable String username) {
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

    @GetMapping("/books")
    public List<BookItem> books(@RequestParam(defaultValue = "") String keyword) {
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

    @GetMapping("/book-borrows")
    public List<BookBorrowItem> bookBorrows(@RequestParam String username) {
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

    @PostMapping("/books/{bookId}/borrow")
    public ActionResponse borrowBook(@PathVariable Long bookId, @RequestBody UserActionRequest request) {
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

    @PostMapping("/book-borrows/{borrowId}/renew")
    public ActionResponse renewBook(@PathVariable Long borrowId, @RequestBody UserActionRequest request) {
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

    @PostMapping("/book-borrows/{borrowId}/return")
    public ActionResponse returnBook(@PathVariable Long borrowId, @RequestBody UserActionRequest request) {
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

    @GetMapping("/admin/review-tasks")
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

    @PostMapping("/admin/review-tasks/{taskId}/decision")
    public ActionResponse decideReviewTask(
        @PathVariable Long taskId,
        @RequestBody ReviewDecisionRequest request
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

    private record BookState(Long id, String title, Integer availableCopies) {
    }

    private record BorrowState(Long id, Long bookId, String status, LocalDate dueAt, Integer renewCount) {
    }
}
