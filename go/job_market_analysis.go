package main

import "fmt"

func getJobBreakdown(requestPayload []map[string]interface{}) {
	fmt.Println(requestPayload)
}

func main() {
	requestPayload := []map[string]interface{}{
		{
			"city":     "Ottawa",
			"province": "ON",
		},
		{
			"city":     "Vancouver",
			"province": "BC",
		},
	}
	getJobBreakdown(requestPayload)
}

