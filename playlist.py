import zmq
import random
import json

# collection of moods (classical, upbeat, lofi, focus) and corresponding YouTube playlists
playlist_dictionary = {
    "classical": [
        "https://www.youtube.com/watch?v=n74kKqwWViU&list=RDQMMEp4Sg6L1VI&start_radio=1",
        "https://www.youtube.com/watch?v=_ioc6sdgugo&list=PL_qM1lclHDwXIxlaa1jDtslnFCEN846rm",
        "https://www.youtube.com/watch?v=VRYRgA8Zbuo&list=RDVRYRgA8Zbuo&start_radio=1",
        "https://www.youtube.com/watch?v=rvigx5N-wu4&list=RDrvigx5N-wu4&start_radio=1",
        "https://www.youtube.com/watch?v=895pPv4l_9Q&list=RD895pPv4l_9Q&start_radio=1"
    ],
    "upbeat": [
        "https://www.youtube.com/watch?v=OPf0YbXqDm0&list=RDQMXWO_c5BE-zc&start_radio=1",
        "https://www.youtube.com/watch?v=ljnGl5nvUJY&list=RDljnGl5nvUJY&start_radio=1",
        "https://www.youtube.com/watch?v=pIgZ7gMze7A&list=PLJNlve0_Ebae2aPbjfolLT-6LvZkP8UZA"
    ],
    "lofi": [
        "https://www.youtube.com/watch?v=XDpoBc8t6gE&list=RDQMwbpzXXO29_k&start_radio=1",
        "https://www.youtube.com/watch?v=sF80I-TQiW0",
        "https://www.youtube.com/watch?v=q0ff3e-A7DY"
    ],
    "ambient": [
        "https://www.youtube.com/watch?v=mPZkdNFkNps",
        "https://www.youtube.com/watch?v=8myYyMg1fFE",
        "https://www.youtube.com/watch?v=nMfPqeZjc2c"
    ]
}

def load_playlists():
    """If playlists.json exists, load playlists. Otherwise, default to playlist_dictionary."""
    global playlist_dictionary

    try:
        with open("playlists.json", "r") as infile:
            json_data = json.load(infile)

        if isinstance(json_data, dict):
            playlist_dictionary = json_data
        else:
            print("Error: playlists.json has invalid format. Using default playlists.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error: Could not read playlists.json. Using default playlists.")
        print(f"Details: {e}")

def save_playlists():
    """Save all playlists to playlists.json."""
    with open("playlists.json", "w") as outfile:
        json.dump(playlist_dictionary, outfile, indent=2)

def get_playlist(mood):
    """Given a mood, returns a pseudorandom playlist."""
    if mood not in playlist_dictionary:
        return "Invalid mood. Try: classical, upbeat, lofi, or ambient."
    return random.choice(playlist_dictionary[mood])

def add_playlist(mood, url):
    """Adds Youtube URL to playlist_dictionary for given mood."""
    if mood not in playlist_dictionary:
        return "Invalid mood. Try: classical, upbeat, lofi, or ambient."
    if not isinstance(url, str) or not url.startswith("https://www.youtube.com"):
        return "Invalid URL. Must begin with https://www.youtube.com"
    if url in playlist_dictionary[mood]:
        return "URL already exists in playlist collection."

    playlist_dictionary[mood].append(url)
    save_playlists()
    return f"Playlist added to {mood}."

def main():
    """Sets up and runs Playlist Service."""

    # load existing playlists
    load_playlists()

    # set up zmq context and reply socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # set 1s receive-timeout to periodically check for shutdown
    socket.setsockopt(zmq.RCVTIMEO, 1000)

    # bind socket to port
    address = "tcp://*:5556"
    socket.bind(address)
    print(f"Playlist Microservice listening on {address}\n")

    try:
        # infinite loop to receive messages from client
        while True:
            try:
                message = socket.recv_string()
            except zmq.Again:
                continue

            print(f"Received request from a client: {message}")

            # parse input
            parts = message.strip().split(maxsplit=2)

            # handle get request
            if len(parts) == 1:
                mood = parts[0].lower()
                response = get_playlist(mood)

            # handle add request
            elif len(parts) == 3 and parts[0].lower() == "add":
                mood = parts[1].lower()
                url = parts[2]
                response = add_playlist(mood, url)

            else:
                response = ("Invalid request. Try one of:\n"
                            "    classical\n"
                            "    upbeat\n"
                            "    lofi\n"
                            "    ambient\n"
                            "    add <mood> <https://www.youtube.com/...>")

            socket.send_string(response)
            print(f"Sent message to client: {response}\n")

    # allow microservice to shut down via keyboard interrupt
    except KeyboardInterrupt:
        print("Playlist Microservice shutting down...")

    # make a clean exit
    finally:
        socket.close()
        context.term()
        print("Playlist Microservice stopped.\n")

if __name__ == "__main__":
    main()