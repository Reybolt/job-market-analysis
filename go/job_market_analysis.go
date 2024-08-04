package main

import "fmt"

type IndeedPayload struct {
	City     string `json:"city"`
	Province string `json:"province"`
}

func getJobBreakdown(requestPayload []IndeedPayload) {
	fmt.Println(requestPayload)
}

func main() {
	var requestPayload []IndeedPayload
	// TODO: Need to look at alternatives instead of append per record.
	requestPayload = append(requestPayload, IndeedPayload{City: "Vancouver", Province: "BC"})
	requestPayload = append(requestPayload, IndeedPayload{City: "Ottawa", Province: "ON"})
	getJobBreakdown(requestPayload)
}
