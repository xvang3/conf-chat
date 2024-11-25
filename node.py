import os
import json
import zmq

# Reuse functions for node bootstrapping and listening
from main import start_node, bootstrap_to_network

if __name__ == "__main__":
    # Start the node and bind to a port
    node_socket, node_port = start_node()
    
    # Bootstrap to the network
    bootstrap_to_network(node_port)

    print(f"Node is running on {node_port}. Listening for messages...")

    # Keep the node alive for peer-to-peer interactions
    while True:
        try:
            message = node_socket.recv_json()
            print(f"Received message: {message}")
            node_socket.send_json({"status": "received", "message": "Acknowledged"})
        except zmq.ZMQError as e:
            print(f"Error in node: {e}")
            break
