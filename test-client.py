import zmq

def main():
    """Connect to Playlist Microservice and send sample category requests."""

    # set up zmq context and request socket, connect to Playlist Microservice endpoint
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")

    # Test 1: send "classical" request, print response
    print("Calling Playlist Microservice with 'classical' request...")
    socket.send_string("classical")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 2: send "upbeat" request, print response
    print("Calling Playlist Microservice with 'upbeat' request...")
    socket.send_string("upbeat")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 3: send "lofi" request, print response
    print("Calling Playlist Microservice with 'lofi' request...")
    socket.send_string("lofi")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 4: send "focus" request, print response
    print("Calling Playlist Microservice with 'focus' request...")
    socket.send_string("focus")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 5: add "focus" URL, print response
    print("Calling Playlist Microservice with 'add' request...")
    socket.send_string("add focus https://www.youtube.com/watch?v=oPVte6aMprI&list=RDoPVte6aMprI&start_radio=1")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # Test 6: fail add URL
    print("Calling Playlist Microservice with 'add' request...")
    socket.send_string("add focus https://www.youtube.com/watch?v=nMfPqeZjc2c")
    response = socket.recv_string()
    print(f"Response: {response}\n")

    # make a clean exit
    socket.close()
    context.term()

if __name__ == "__main__":
    main()