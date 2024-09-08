import socket
import threading
import json
from enum import Enum
from typing import Dict, Union
from main import Manager, DeviceType, DeviceAction  # Import the Manager class

class Server:
    """Server class to handle client connections and process requests."""

    def __init__(self, host: str = '127.0.0.1', port: int = 8080) -> None:
        """
        Initialize the Server with host and port.

        Args:
            host (str): The server hostname or IP address.
            port (int): The server port number.
        """
        self.server_host = host
        self.server_port = port
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.manager = Manager()  # Instance of the Manager class
        self.__setup_server()
        self.__collect_connection()

    @property
    def server_host(self) -> str:
        """Return the server host."""
        return self.__server_host

    @server_host.setter
    def server_host(self, value: str) -> None:
        """Set the server host."""
        self.__server_host = value

    @property
    def server_port(self) -> int:
        """Return the server port."""
        return self.__server_port

    @server_port.setter
    def server_port(self, value: int) -> None:
        """Set the server port."""
        self.__server_port = value

    def __setup_server(self) -> None:
        """Setup the server to listen for incoming connections."""
        self.__server_socket.bind((self.server_host, self.server_port))
        self.__server_socket.listen(5)
        print(f"Server started on {self.server_host}:{self.server_port}")

    def __collect_connection(self) -> None:
        """Accept and handle incoming connections."""
        while True:
            client_socket, address = self.__server_socket.accept()
            print(f"Connection from {address}")
            threading.Thread(target=self.__handle_client, args=(client_socket,)).start()

    def __handle_client(self, client_socket: socket.socket) -> None:
        """
        Handle communication with a connected client.

        Args:
            client_socket (socket.socket): The socket object for client communication.
        """
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                message = json.loads(data)
                response = self.__process_message(message)
                client_socket.sendall(json.dumps(response).encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def __process_message(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Process incoming messages based on request type.

        Args:
            message (Dict[str, Union[int, str]]): The incoming message.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            request_type = message.get("request_type")

            if request_type == 1:  # Create device
                return self.__create_device(message)

            elif request_type == 2:  # Control device
                return self.__control_device(message)

            elif request_type == 3:  # Get device state
                return self.__get_device_state(message)

            else:
                return {
                    "result_code": 1,
                    "error_message": "Invalid request type.",
                    "data": {}
                }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def __create_device(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle device creation requests.

        Args:
            message (Dict[str, Union[int, str]]): The message containing device creation details.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            device_type = DeviceType[message.get("device_type").upper()]
            device_id = message.get("device_id")
            result_message = self.manager.create_device(device_type, device_id)
            print(result_message)
            return {
                "result_code": 0,
                "error_message": "",
                "data": {"device_id": device_id, "details": result_message}
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def __control_device(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle device control requests.

        Args:
            message (Dict[str, Union[int, str]]): The message containing device control details.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            device_id = message.get("device_id")
            device_action = DeviceAction[message.get("device_action").upper()]
            value = message.get("value")
            result_message = self.manager.control_device(device_id, device_action, value)
            print(f"Device controlled with details: {result_message}")
            return {
                "result_code": 0,
                "error_message": "",
                "data": result_message
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def __get_device_state(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle requests to get device state.

        Args:
            message (Dict[str, Union[int, str]]): The message requesting the device state.

        Returns:
            Dict[str, Union[int, str]]: The response message with device state.
        """
        try:
            device_id = message.get("device_id")
            device_state = self.manager.get_state(device_id)
            print(f"Device state retrieved: {device_state}")
            return {
                "result_code": 0,
                "error_message": "",
                "data": device_state
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def close_connection(self) -> None:
        """Close the server socket."""
        self.__server_socket.close()

if __name__ == "__main__":
    server = Server()
