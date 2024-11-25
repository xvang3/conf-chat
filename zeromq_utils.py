import zmq

class ZeroMQUtils:
    def __init__(self):
        self.context = zmq.Context()

    def start_server(self, port):
        """Starts a ZeroMQ server."""
        socket = self.context.socket(zmq.REP)  # Reply socket for requests
        socket.bind(f"tcp://*:{port}")
        return socket

    def start_client(self, address, port):
        """Starts a ZeroMQ client."""
        socket = self.context.socket(zmq.REQ)  # Request socket for sending messages
        socket.connect(f"tcp://{address}:{port}")
        return socket

    def send_message(self, socket, message):
        """Send a message and wait for a reply."""
        socket.send_json(message)
        reply = socket.recv_json()
        return reply

    def receive_message(self, socket):
        """Receive a message and send a reply."""
        message = socket.recv_json()
        return message
