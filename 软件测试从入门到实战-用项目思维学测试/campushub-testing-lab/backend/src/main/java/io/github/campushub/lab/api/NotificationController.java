package io.github.campushub.lab.api;

import java.util.List;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class NotificationController {

    private final CampusHubService campusHubService;

    public NotificationController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping("/notifications")
    public List<CampusHubService.NotificationItem> notifications(@RequestParam String username) {
        return campusHubService.notifications(username);
    }

    @PostMapping("/notifications/{notificationId}/read")
    public CampusHubService.ActionResponse markNotificationRead(
        @PathVariable Long notificationId,
        @RequestBody CampusHubService.UserActionRequest request
    ) {
        return campusHubService.markNotificationRead(notificationId, request);
    }
}
