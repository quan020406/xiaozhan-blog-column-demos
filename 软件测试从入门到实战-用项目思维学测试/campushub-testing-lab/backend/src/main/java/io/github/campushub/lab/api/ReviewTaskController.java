package io.github.campushub.lab.api;

import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/admin/review-tasks")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class ReviewTaskController {

    private final CampusHubService campusHubService;

    public ReviewTaskController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping
    public List<CampusHubService.ReviewTaskItem> reviewTasks() {
        return campusHubService.reviewTasks();
    }

    @PostMapping("/{taskId}/decision")
    public CampusHubService.ActionResponse decideReviewTask(
        @PathVariable Long taskId,
        @RequestBody CampusHubService.ReviewDecisionRequest request
    ) {
        return campusHubService.decideReviewTask(taskId, request);
    }
}
