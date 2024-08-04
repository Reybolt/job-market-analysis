package main

import (
	"bufio"
	"fmt"
	"net/http"
)

type IndeedPayload struct {
	City     string `json:"city"`
	Province string `json:"province"`
}

func getJobBreakdown(requestPayload []IndeedPayload) {

	for i := 0; i < len(requestPayload); i++ {
		fmt.Println(requestPayload[i])
		// TODO: Make these calls concurrent.
		indeedRequest(requestPayload[i])
	}

}

func indeedRequest(IndeedPayload) {
	// Copied from https://gobyexample.com/http-client
	resp, err := http.Get("https://ca.indeed.com/jobs?q=software+developer&l=Ottawa%2C+ON")
	// resp, err := http.Get("https://gobyexample.com")
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("Response status:", resp.Status)

	scanner := bufio.NewScanner(resp.Body)
	for i := 0; scanner.Scan() && i < 5; i++ {
		fmt.Println(scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		panic(err)
	}
}

func main() {
	var requestPayload []IndeedPayload
	// TODO: Need to look at alternatives instead of append per record.
	requestPayload = append(requestPayload, IndeedPayload{City: "Vancouver", Province: "BC"})
	requestPayload = append(requestPayload, IndeedPayload{City: "Ottawa", Province: "ON"})
	getJobBreakdown(requestPayload)
}
