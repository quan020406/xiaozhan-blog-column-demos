package io.github.campushub.lab.api;

import static org.hamcrest.Matchers.is;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class CampusHubControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void studentAndAdminCoreFlowsWork() throws Exception {
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
}
