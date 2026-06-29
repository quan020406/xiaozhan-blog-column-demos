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
public class RoomController {

    private final CampusHubService campusHubService;

    public RoomController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping("/rooms")
    public List<CampusHubService.RoomItem> rooms() {
        return campusHubService.rooms();
    }

    @GetMapping("/room-reservations")
    public List<CampusHubService.RoomReservationItem> roomReservations(@RequestParam String username) {
        return campusHubService.roomReservations(username);
    }

    @PostMapping("/rooms/{roomId}/reservations")
    public CampusHubService.ActionResponse reserveRoom(
        @PathVariable Long roomId,
        @RequestBody CampusHubService.RoomReservationRequest request
    ) {
        return campusHubService.reserveRoom(roomId, request);
    }
}
