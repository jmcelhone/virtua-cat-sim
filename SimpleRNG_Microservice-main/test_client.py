import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send_string("generate")
random_number = socket.recv_string()

print(f"Received RNG number: {random_number}")