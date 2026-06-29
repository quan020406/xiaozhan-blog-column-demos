package io.github.campushub.lab.api;

import java.util.Map;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class SystemController {

    private final CampusHubService campusHubService;

    public SystemController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return campusHubService.health();
    }

    @GetMapping("/overview")
    public CampusHubService.OverviewResponse overview() {
        return campusHubService.overview();
    }
}
