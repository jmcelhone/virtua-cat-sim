import zmq
import time
context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def get_noun(quantity, category = "random"):
    time.sleep(1)
    socket.send_string(f"{quantity} {category}")
    noun_array = socket.recv()
    return noun_array

while True:
    q = input("choose quantity of nouns: ")
    c = input("choose category of nouns(or random): ")
    noun = get_noun(q, c)
    print(noun)