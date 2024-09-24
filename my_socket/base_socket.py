import socket
import json
from typing import Optional, Dict, Union


class BaseSocket:
    """Base class for socket communication."""

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = None

    def establish_connection(self) -> None:
        """Establish a connection to the server or bind the server socket."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message: Dict[str, Union[int, str]]) -> None:
        """Send a JSON message to the server."""
        try:
            self.socket.sendall(json.dumps(message).encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message: {e}")

    def receive_data(self) -> Optional[Dict[str, Union[int, str]]]:
        """Receive and decode a JSON response from the server."""
        try:
            response = self.socket.recv(1024).decode('utf-8')
            return json.loads(response)
        except socket.error as e:
            print(f"Error receiving data: {e}")
            return None

    def close_connection(self) -> None:
        """Close the connection to the server."""
        if self.socket:
            try:
                self.socket.close()
            except socket.error as e:
                print(f"Error closing connection: {e}")
