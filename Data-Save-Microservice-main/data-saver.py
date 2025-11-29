# data_saver_service.py
import zmq
import json
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

DATA_FILE = "data.json"

# Load data 
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = f.read().strip()
                if data == "":
                    return []  # empty file
                return json.loads(data)
        except json.JSONDecodeError:
            return []  # corrupted file
    return []

# Save data
def save_to_file(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Persistent Data Storage
saved_data = load_data()

print("Data Save Running")

while True:
    message = socket.recv().decode("utf-8")
    request = json.loads(message)
    action = request.get("action")

    if action == "save":
        saved_data.append(request.get("data"))
        save_to_file(saved_data)
        socket.send_string("Data saved")

    elif action == "get_all":
        socket.send(json.dumps(saved_data).encode("utf-8"))

    elif action == "delete":
        index = request.get("index")
        if index < 0 or index >= len(saved_data):
            socket.send_string("Error: Invalid index")
        else:
            deleted_item = saved_data.pop(index)
            save_to_file(saved_data)
            socket.send_string(f"Deleted: {deleted_item}")

    else:
        socket.send_string("Error: Unknown action")
