import zmq
import random

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("RNG Service Listening on Port 5555")

    while True:
        # wait for request from client
        message = socket.recv_string()
        print(f"[RNG] Received request: {message}")

        if message == "generate":
            rand_num = rng_begin()
            socket.send_string(str(rand_num))
        else:
            socket.send_string("Error: Unknown command...")


def rng_begin():
    x = random.randint(1, 100000)
    print(f"[RNG] Generated: {x}")
    return x

if __name__ == "__main__":
    main()


