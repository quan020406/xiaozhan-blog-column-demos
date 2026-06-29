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
public class DeviceController {

    private final CampusHubService campusHubService;

    public DeviceController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping("/devices")
    public List<CampusHubService.DeviceItem> devices() {
        return campusHubService.devices();
    }

    @GetMapping("/device-borrows")
    public List<CampusHubService.DeviceBorrowItem> deviceBorrows(@RequestParam String username) {
        return campusHubService.deviceBorrows(username);
    }

    @PostMapping("/devices/{deviceId}/borrow")
    public CampusHubService.ActionResponse borrowDevice(
        @PathVariable Long deviceId,
        @RequestBody CampusHubService.DeviceBorrowRequest request
    ) {
        return campusHubService.borrowDevice(deviceId, request);
    }
}
