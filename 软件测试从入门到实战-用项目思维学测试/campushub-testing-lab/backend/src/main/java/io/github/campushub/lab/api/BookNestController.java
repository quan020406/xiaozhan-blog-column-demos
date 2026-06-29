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
public class BookNestController {

    private final CampusHubService campusHubService;

    public BookNestController(CampusHubService campusHubService) {
        this.campusHubService = campusHubService;
    }

    @GetMapping("/books")
    public List<CampusHubService.BookItem> books(@RequestParam(defaultValue = "") String keyword) {
        return campusHubService.books(keyword);
    }

    @GetMapping("/book-borrows")
    public List<CampusHubService.BookBorrowItem> bookBorrows(@RequestParam String username) {
        return campusHubService.bookBorrows(username);
    }

    @PostMapping("/books/{bookId}/borrow")
    public CampusHubService.ActionResponse borrowBook(
        @PathVariable Long bookId,
        @RequestBody CampusHubService.UserActionRequest request
    ) {
        return campusHubService.borrowBook(bookId, request);
    }

    @PostMapping("/book-borrows/{borrowId}/renew")
    public CampusHubService.ActionResponse renewBook(
        @PathVariable Long borrowId,
        @RequestBody CampusHubService.UserActionRequest request
    ) {
        return campusHubService.renewBook(borrowId, request);
    }

    @PostMapping("/book-borrows/{borrowId}/return")
    public CampusHubService.ActionResponse returnBook(
        @PathVariable Long borrowId,
        @RequestBody CampusHubService.UserActionRequest request
    ) {
        return campusHubService.returnBook(borrowId, request);
    }
}
