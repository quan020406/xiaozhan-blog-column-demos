package io.github.campushub.lab.api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.LocalDate;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class CampusHubControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void studentAndAdminCoreFlowsWork() throws Exception {
        String futureReservationDate = LocalDate.now().plusDays(1).toString();
        String deviceBorrowDate = LocalDate.now().toString();
        String deviceDueDate = LocalDate.now().plusDays(7).toString();

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"password\":\"campus123\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.user.username", is("student02")));

        mockMvc.perform(post("/api/activities/7/registrations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("ACTIVITY_REGISTERED")));

        mockMvc.perform(post("/api/books/5/borrow")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("BOOK_BORROWED")));
        mockMvc.perform(post("/api/rooms/2/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"reservationDate\":\"" + futureReservationDate + "\",\"startHour\":10,\"endHour\":12}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("ROOM_RESERVATION_SUBMITTED")));

        mockMvc.perform(post("/api/devices/8/borrow")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"quantity\":1,\"borrowedAt\":\"" + deviceBorrowDate + "\",\"dueAt\":\"" + deviceDueDate + "\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("DEVICE_BORROW_SUBMITTED")));

        mockMvc.perform(post("/api/book-borrows/5/renew")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("BOOK_RENEWED")));

        mockMvc.perform(post("/api/book-borrows/5/return")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("BOOK_RETURNED")));

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"admin01\",\"password\":\"campus123\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.user.roleCode", is("SYSTEM_ADMIN")));

        mockMvc.perform(post("/api/admin/review-tasks/1/decision")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"reviewer\":\"admin01\",\"decision\":\"APPROVED\",\"comment\":\"unit test\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("REVIEW_TASK_APPROVED")));

        mockMvc.perform(get("/api/overview"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.statistics.books", is(20)));
    }

    @Test
    void loginRejectsWrongPasswordAndLockedUser() throws Exception {
        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\",\"password\":\"wrong-password\"}"))
            .andExpect(status().isUnauthorized());

        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student_locked\",\"password\":\"campus123\"}"))
            .andExpect(status().isForbidden());
    }

    @Test
    void activityRegistrationRejectsDuplicateAndFullActivity() throws Exception {
        mockMvc.perform(post("/api/activities/1/registrations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\"}"))
            .andExpect(status().isConflict());

        mockMvc.perform(post("/api/activities/2/registrations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isConflict());
    }

    @Test
    void bookBorrowRejectsOutOfStockAndSecondRenewal() throws Exception {
        mockMvc.perform(post("/api/books/18/borrow")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\"}"))
            .andExpect(status().isConflict());

        mockMvc.perform(post("/api/book-borrows/1/renew")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("BOOK_RENEWED")));

        mockMvc.perform(post("/api/book-borrows/1/renew")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\"}"))
            .andExpect(status().isConflict());
    }


    @Test
    void roomReservationRejectsMaintenanceAndConflictingSlot() throws Exception {
        String futureReservationDate = LocalDate.now().plusDays(1).toString();

        mockMvc.perform(get("/api/rooms"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].name", is("A101 自习室")));

        mockMvc.perform(post("/api/rooms/5/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"reservationDate\":\"" + futureReservationDate + "\",\"startHour\":9,\"endHour\":11}"))
            .andExpect(status().isConflict());

        mockMvc.perform(post("/api/rooms/1/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\",\"reservationDate\":\"" + futureReservationDate + "\",\"startHour\":15,\"endHour\":17}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("ROOM_RESERVATION_SUBMITTED")));

        mockMvc.perform(post("/api/rooms/1/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"reservationDate\":\"" + futureReservationDate + "\",\"startHour\":16,\"endHour\":18}"))
            .andExpect(status().isConflict());
    }

    @Test
    void deviceBorrowRejectsOutOfStockAndDuplicateBorrow() throws Exception {
        String deviceBorrowDate = LocalDate.now().toString();
        String deviceDueDate = LocalDate.now().plusDays(7).toString();

        mockMvc.perform(get("/api/devices"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].name", is("投影仪")));

        mockMvc.perform(post("/api/devices/7/borrow")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student02\",\"quantity\":1,\"borrowedAt\":\"" + deviceBorrowDate + "\",\"dueAt\":\"" + deviceDueDate + "\"}"))
            .andExpect(status().isConflict());

        mockMvc.perform(post("/api/devices/4/borrow")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\",\"quantity\":1,\"borrowedAt\":\"" + deviceBorrowDate + "\",\"dueAt\":\"" + deviceDueDate + "\"}"))
            .andExpect(status().isConflict());
    }

    @Test
    void notificationsCanBeListedAndMarkedRead() throws Exception {
        mockMvc.perform(get("/api/notifications?username=student01"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$[0].title", is("新生编程训练营报名成功")))
            .andExpect(jsonPath("$[0].readFlag", is(false)));

        mockMvc.perform(post("/api/notifications/1/read")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.code", is("NOTIFICATION_READ")));

        mockMvc.perform(post("/api/notifications/2/read")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"student01\"}"))
            .andExpect(status().isNotFound());
    }

    @Test
    void studentCannotDecideReviewTask() throws Exception {
        mockMvc.perform(post("/api/admin/review-tasks/1/decision")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"reviewer\":\"student01\",\"decision\":\"APPROVED\",\"comment\":\"should fail\"}"))
            .andExpect(status().isForbidden());
    }

    @Test
    void openApiDocumentIsAvailable() throws Exception {
        mockMvc.perform(get("/v3/api-docs"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.openapi").exists())
            .andExpect(jsonPath("$.info.title", is("CampusHub Testing Lab API")))
            .andExpect(jsonPath("$.paths['/api/auth/login']").exists())
            .andExpect(jsonPath("$.paths['/api/rooms']").exists())
            .andExpect(jsonPath("$.paths['/api/devices']").exists())
            .andExpect(jsonPath("$.paths['/api/notifications']").exists());
    }
}

