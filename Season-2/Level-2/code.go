package main

import (
	"encoding/json"
	"log"
	"net/http"
	"regexp"

	"golang.org/x/crypto/bcrypt"
	"golang.org/x/time/rate"
)

var reqBody struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

// Password hashes for test users (bcrypt hashed)
var testFakeMockUsers = map[string]string{
	"user1@example.com": "$2a$10$N9qo8uLOickgx2ZMRZo5i.U3t6eTWo2xZG.OsbcQbs0h80xjo4zqW", // password12345
	"user2@example.com": "$2a$10$7bZhTG/jzg5.X5gzpVbEqOiOhT5f44PTslqFTV1ZbSl3Cx1LfbYx6", // B7rx9OkWVdx13$QF6Imq
	"user3@example.com": "$2a$10$C9peHPcXPhEo5F32bcTyeuUtwqoz/5JhGmO0IUwUB3QF3jCTzGB2m", // hoxnNT4g&ER0&9Nz0pLO
	"user4@example.com": "$2a$10$56OJJ2D8uOYaz1tM5D2PuOLR/1/kZK.O4zKgaLUp5nSCwRLVgfG36", // Log4Fun
}

var limiter = rate.NewLimiter(1, 3) // 1 request per second with a burst size of 3

func isValidEmail(email string) bool {
	// The provided regular expression pattern for email validation by OWASP
	// https://owasp.org/www-community/OWASP_Validation_Regex_Repository
	emailPattern := `^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$`
	match, err := regexp.MatchString(emailPattern, email)
	if err != nil {
		return false
	}
	return match
}

func loginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		if !limiter.Allow() {
			http.Error(w, "Too many requests", http.StatusTooManyRequests)
			return
		}

		decode := json.NewDecoder(r.Body)
		decode.DisallowUnknownFields()

		err := decode.Decode(&reqBody)
		if err != nil {
			http.Error(w, "Cannot decode body", http.StatusBadRequest)
			return
		}
		email := reqBody.Email
		password := reqBody.Password

		if !isValidEmail(email) {
			log.Printf("Invalid email format: %q", email)
			http.Error(w, "Invalid email or password", http.StatusUnauthorized)
			return
		}

		hashedPassword, ok := testFakeMockUsers[email]
		if !ok {
			http.Error(w, "Invalid email or password", http.StatusUnauthorized)
			return
		}

		err = bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
		if err != nil {
			http.Error(w, "Invalid email or password", http.StatusUnauthorized)
			return
		}

		log.Printf("User %q logged in successfully", email)
		w.WriteHeader(http.StatusOK)
	} else {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
	}
}

func main() {
	http.HandleFunc("/login", loginHandler)
	log.Print("Server started. Listening on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatalf("HTTP server ListenAndServe: %q", err)
	}
}
