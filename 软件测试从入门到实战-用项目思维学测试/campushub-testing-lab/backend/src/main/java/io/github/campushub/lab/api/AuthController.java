package io.github.campushub.lab.api;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(originPatterns = {"http://localhost:*", "http://127.0.0.1:*"})
public class AuthController {

    private final CampusHubService campusHubService;

    public AuthController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @PostMapping("/login")
    public CampusHubService.LoginResponse login(@RequestBody CampusHubService.LoginRequest request) {
        return campusHubService.login(request);
    }
}
