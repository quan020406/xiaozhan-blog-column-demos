package io.github.campushub.lab.api;

import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/activities")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class ActivityController {

    private final CampusHubService campusHubService;

    public ActivityController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping
    public List<CampusHubService.ActivityItem> activities(@RequestParam(defaultValue = "") String username) {
        return campusHubService.activities(username);
    }

    @PostMapping("/{activityId}/registrations")
    public CampusHubService.ActionResponse registerActivity(
        @PathVariable Long activityId,
        @RequestBody CampusHubService.UserActionRequest request
    ) {
        return campusHubService.registerActivity(activityId, request);
    }

    @DeleteMapping("/{activityId}/registrations/{username}")
    public CampusHubService.ActionResponse cancelActivity(
        @PathVariable Long activityId,
        @PathVariable String username
    ) {
        return campusHubService.cancelActivity(activityId, username);
    }
}
