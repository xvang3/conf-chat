# conf-chat
A P2P Chat System (Abstract System on single system)

Overview

This project is a theoretical abstract of a peer-to-peer (P2P) chat application that allows users to do the following on a single system:

- Register, log in, and manage friends
- Start live chat sessions with their peers
- Check their friends' online/offline status
- Send and receive messages in real time

This application is designed with P2P functionality in mind, using Python's ZeroMQ for message parsing and Flask for managing server-based operations. This README will provide some general instructions, and details about the applications's features.

Dependencies and Requirements

System Requirements
- Operating Systems: Linux (created with Linux), macOS, or Windows
- Python Version: 3.10 or higher

Python Libraries
- flask
- requests
- zmq
- json

Setup Instructions

Clone Repository
- git clone https://github.com/xvang3/conf-chat.git
- cd conf-chat

Set up a Virtual Environment
- python3 -m venv venv # On Windows: python -m venv venv
- source venv/bin/activate # On Windows: venv/Scripts/activate

Install Dependencies
- pip install -r requirements.txt

Run Server
- python3 server.py

Start P2P application:
- python3 main.py

Application Features
1. Registration and login
    - users can register with username and password
        - note: no security features/input validation were created
    - on login, users will be marked online and can interact with peers

2. Friends Management
    - can add or remove friends by name
    - check friends to see their status (online/offline)
    
3. Live Chat
    - start real time chat session with another online user

4. Online/Offline Status
    - view friends status in real time
    - automatically updates online/offline during login/logout
    
5. P2P Architecture
    - Designed for decentralized communication without reliance on central server
    - Peers connect using ZeroMQ
    
Usage Guide
1. Starting Application
    - To start, first start the server "python3 server.py"
    - Then, run "python3 main.py"
    - Application is simple providing numbers with options, having user provide number input for their action
        - Can register, login, or exit
        - After login, will see longer menu for other options like adding/removing friends, intiating live chat, checking friends' status, commands in live chat

2. Initiating Live Chat
    - Select start chat
    - enter a message
    - then enter recipient's address; must be in the format of "tcp://localhost:<port>
    - to go back, just enter "exit"; sometimes has a bug in print statement, haven't figured out how to solve yet

3. Checking Friend's status
    - Should show all friends and their statuses online/offline
    
Troubleshooting
Common Issues

Unable to Start Server:
    - Ensure the server_data directory exists and is writable.
    - Check for port conflicts when running the server.

Cannot Connect to Peer:
    - Verify that both peers are running the application and listening on the specified ports.
    - Ensure firewall settings allow communication on the chosen ports.
    - Friend Status Not Updating:
    - Ensure both peers have logged in and synchronized their data.
    

Methodology:

The P2P Architecture does not necessarily work as I had intended, but here was my original idea for the system. A server exists to hold data, just in case there are no online nodes and a new node joins. It and gather data and sync it with this server, but it does not need the server to exist. If new nodes join and there are existing nodes, it will sync its data from them instead (at first anyways). When a new user is registered, they will have their own directory in the local system, this is to simulate that if they were actually their own endpoint system, they would store some data of the network in themselves. When performing functions, these nodes will sync with each other and/or the server as a way to stay up to date. When users run main.py it is as if they are connecting to the network, but in this simulation, they are connecting to a port. 


