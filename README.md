# TCP Chatroom

## Overview
This project is a simple TCP chatroom application that allows multiple clients to connect to a server and communicate with each other in real-time. The application consists of a client-side implementation and a server-side implementation.

## Files
- **client/client.py**: Contains the client-side implementation of the TCP chatroom. It handles connecting to the server, sending and receiving messages, and managing user input and display.
- **server/server.py**: Contains the server-side implementation of the TCP chatroom. It manages client connections, broadcasts messages to connected clients, and handles client disconnections.
- **requirements.txt**: Lists the Python dependencies required for the project. Use this file to install the necessary packages using pip.
- **.gitignore**: Specifies files and directories that should be ignored by Git, including temporary files, compiled files, and environment files.

## Setup Instructions
1. Clone the repository to your local machine:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd tcp-chatroom
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the server:
   ```
   python server/server.py
   ```
2. Start the client:
   ```
   python client/client.py
   ```
3. Follow the prompts to enter your nickname and start chatting.

## Contributing
Feel free to submit issues or pull requests if you would like to contribute to this project.

## License
This project is open-source and available under the MIT License.