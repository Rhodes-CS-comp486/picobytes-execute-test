import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
# Set the target URL (your service's URL)

TOTAL_REQUESTS = 300  # Total number of requests to send
CONCURRENT_REQUESTS = 50  # Number of concurrent threads to simulate

# Counters to track requests and responses
requests_sent = 0
requests_received = 0
successful_requests = 0
failed_requests = 0

filepath1 = "./testcode1.json"
try:
    with open(filepath1, "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise RuntimeError(f"Error reading test file: {e}")
json_payload = {"code": data.get("code", ""), "tests": data.get("tests"), "timeout": data.get("timeout"), "perTestTimeout": data.get("perTestTimeout")}

# Function to send a request
def send_request():
    global requests_sent, requests_received, successful_requests, failed_requests
    requests_sent += 1

    try:
        response = requests.post("http://localhost:5000/submit", json=json_payload)
        requests_received += 1

        # Log the response code and time
        if response.status_code == 200:
            successful_requests += 1
        else:
            failed_requests += 1

        print(f"Response Code: {response.status_code}, Time Taken: {response.elapsed.total_seconds()}s,Response: {response.json()}")
    except Exception as e:
        failed_requests += 1
        print(f"Request failed: {e}")


# Function to perform the stress test
def stress_test():
    start_time = time.time()
    DELAY = 0.01
    # Create a thread pool to simulate concurrent requests
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = []
        for _ in range(TOTAL_REQUESTS):
            futures.append(executor.submit(send_request))
            time.sleep(DELAY)

        # Wait for all requests to complete
        for future in as_completed(futures):
            future.result()  # We don't need to do anything with the result
    end_time = time.time()
    total_time = end_time - start_time

    # Print the results after the test
    print("\nStress Test Completed")
    print(f"Total Requests Sent: {requests_sent}")
    print(f"Total Requests Received: {requests_received}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Failed Requests: {failed_requests}")
    print(f"Test Duration: {total_time:.2f} seconds")
    print(f"Requests per Second: {requests_sent / total_time:.2f}")


if __name__ == "__main__":
    stress_test()