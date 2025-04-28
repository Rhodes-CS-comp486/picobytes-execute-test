import threading
import time
import json
import requests

NUM_THREADS = 10
NUM_REQUESTS = None  # Set to an integer to limit total requests

# Event to signal threads to stop
stop_event = threading.Event()

def send_test_request():
    filepath1 = "./testcode1.json"

    try:
        with open(filepath1, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Error reading test file: {e}")

    json_payload = {"code": data.get("code", ""), "tests": data.get("tests"), "timeout": data.get("timeout"), "perTestTimeout": data.get("perTestTimeout")}

    response = requests.post("http://localhost:5000/submit", json=json_payload)
    return response

def send_request():
    count = 0
    while not stop_event.is_set() and (NUM_REQUESTS is None or count < NUM_REQUESTS):
        try:
            response = send_test_request()
            print(f"[{threading.current_thread().name}] Status: {response.status_code}, Response: {response.json()}")
        except Exception as e:
            print(f"[{threading.current_thread().name}] Request failed: {e}")
        count += 1
        time.sleep(0.01)  # Small delay to simulate real traffic

# Start multiple threads to simulate load
threads = []
for i in range(NUM_THREADS):
    thread = threading.Thread(target=send_request, name=f"Thread-{i}")
    thread.start()
    threads.append(thread)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping stress test...")
    stop_event.set()  # Signal threads to stop
    for thread in threads:
        thread.join()  # Wait for all threads to exit
    print("All threads stopped.")
