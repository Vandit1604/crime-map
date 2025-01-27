import requests
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Configuration
url = "http://127.0.0.1:5000/analyze"  # Replace with the target endpoint
payload = {"text": "Analyze crime trends in Chennai"}
headers = {"Content-Type": "application/json"}
num_requests = 100  # Total number of requests
concurrent_users = [1, 5, 10, 20, 50]  # Different levels of concurrency
latency_data = {}

# Function to send a POST request and measure latency
def measure_latency():
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Ensure the response is successful
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    end_time = time.time()
    return end_time - start_time

# Measure latency for different levels of concurrency
for users in concurrent_users:
    latencies = []
    with ThreadPoolExecutor(max_workers=users) as executor:
        # Send requests concurrently and collect latencies
        results = list(executor.map(lambda _: measure_latency(), range(num_requests)))
        latencies = [lat for lat in results if lat is not None]  # Filter successful requests
    latency_data[users] = latencies

# Generate and plot the graph
plt.figure(figsize=(10, 6))

for users, latencies in latency_data.items():
    plt.plot(range(len(latencies)), latencies, label=f"{users} concurrent users")

plt.title("Latency of API Calls")
plt.xlabel("Request Number")
plt.ylabel("Latency (seconds)")
plt.legend()
plt.grid(True)
plt.savefig('latency_plot.png')
