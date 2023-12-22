import os
import subprocess
import json
import datetime

def check_status(service_name):
    result = subprocess.run(["systemctl", "is-active", service_name], capture_output=True, text=True)
    return result.stdout.strip() == "active"

def json_payload(service_name, service_status, host_name, timestamp):
    filename = f"{service_name}-status-{timestamp}.json"
    data = {
        "service_name": service_name,
        "service_status": service_status,
        "host_name": host_name
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def final_status(service_statuses):
    return "UP" if all(status == "active" for status in service_statuses) else "DOWN"

def monitor_and_create(service_names, host_name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    service_statuses = []
    for service_name in service_names:
        service_status = "UP" if check_status(service_name) else "DOWN"
        service_statuses.append(service_status)
        json_payload(service_name, service_status, host_name, timestamp)
    overall_status = final_status(service_statuses)
    print(f"rbcapp1 state: {overall_status}")

if __name__ == "__main__":
    services_to_monitor = ["apache2", "rabbitmq-server", "postgresql"] #Ubuntu Supports apache2 instead of httpd
    host_name = os.uname()[1]
    monitor_and_create(services_to_monitor, host_name)