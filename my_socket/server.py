from typing import Dict, Union

from base_socket import BaseSocket
import socket
import json


class Server(BaseSocket):
    """Server class to handle incoming client connections."""

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)


    def handle_client(self, client_socket: socket.socket) -> None:
        """Handle incoming client requests."""

        self.socket = client_socket  # Use the client socket for communication
        while True:
            try:
                request = self.receive_data()  # Use receive_data from BaseSocket
                if not request:
                    break

                response = self.process_request(request)
                self.send_message(response)  # Use send_message from BaseSocket

            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()

    def process_request(self, request: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str, Dict]]:
        """Process the received request and generate a response."""
        if request["request_type"] == 1:
            device_id = request["device_id"]
            device_type = request["device_type"]
            return {'result_code': 0, 'error_message': '', 'data': {'message': f'Device of type {device_type} created'}}

        elif request["request_type"] == 2:
            device_id = request["device_id"]
            device_action = request["device_action"]
            value = request.get("value")
            return {'result_code': 0, 'error_message': '',
                    'data': {'message': f'Device {device_id} turned {device_action.lower()}'}}

        elif request["request_type"] == 3:
            device_id = request["device_id"]
            return {'result_code': 0, 'error_message': '', 'data': {'device_id': device_id, 'state': 'ON'}}

        else:
            return {'result_code': 1, 'error_message': 'Invalid request type', 'data': {}}

    def start(self) -> None:
        """Start the server to accept clients."""
        self.establish_connection()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print("Server started. Waiting for clients...")

        client_socket, addr = self.socket.accept()
        print(f"Connection established with {addr}")
        self.handle_client(client_socket)


if __name__ == "__main__":
    server = Server('127.0.0.1', 65432)
    server.start()
