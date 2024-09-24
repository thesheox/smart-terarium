import socket
import threading
import json
from enum import Enum
from typing import Dict, Union


class DeviceType(Enum):
    MOTOR = "motor"
    SENSOR = "sensor"
    RELAY = "relay"


class DeviceAction(Enum):
    CHANGE_SPEED = "change_speed"
    CHANGE_PATH = "change_path"
    GET_VALUE = "get_value"
    ON = "on"
    OFF = "off"


class Server:
    """Server class to handle client connections and process requests."""

    def __init__(self, host: str, port: int) -> None:
        """
        Initialize the Server with host and port.

        Args:
            host (str): The server hostname or IP address.
            port (int): The server port number.
        """
        self.__server_host = host
        self.__server_port = port
        self.__device_map: Dict[int, DeviceType] = {}  # A dictionary to keep track of devices
        self.setup_server()
        self.get_connection()

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

    @property
    def server_socket(self) -> socket.socket:
        """Return the server my_socket."""
        return self.__server_socket

    @server_socket.setter
    def server_socket(self, my_socket: socket.socket) -> None:
        """Set the server my_socket."""
        self.__server_socket = my_socket

    @property
    def device_map(self) -> Dict[int, DeviceType]:
        """Return the device map."""
        return self.__device_map

    @device_map.setter
    def device_map(self, data: Dict[int, DeviceType]) -> None:
        """Set the device map."""
        self.__device_map = data

    def setup_server(self) -> None:
        """Set up the server to listen for incoming connections."""
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__server_host, self.__server_port))
        self.__server_socket.listen(5)
        print(f"Server started on {self.__server_host}:{self.__server_port}")

    def get_connection(self) -> None:
        """Accept and handle incoming connections."""
        while True:
            client_socket, address = self.__server_socket.accept()
            print(f"Connection from {address}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def send_data(self, client_socket: socket.socket, data: Dict[str, Union[int, str]]) -> None:
        """Send data to the client."""
        client_socket.sendall(json.dumps(data).encode('utf-8'))

    def receive_data(self, client_socket: socket.socket) -> str:
        """Receive data from the client."""
        return client_socket.recv(1024).decode('utf-8')

    def close_connection(self, client_socket: socket.socket) -> None:
        """Close the client connection."""
        client_socket.close()

    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handle communication with a connected client.

        Args:
            client_socket (socket.socket): The my_socket object for client communication.
        """
        try:
            while True:
                data = self.receive_data(client_socket)
                if not data:
                    break
                message = json.loads(data)
                response = self.process_message(message)
                self.send_data(client_socket, response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.close_connection(client_socket)

    def process_message(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
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
                return self.create_device(message)

            elif request_type == 2:  # Control device
                return self.control_device(message)

            elif request_type == 3:  # Get device state
                return self.get_device_state(message)

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

    def create_device(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle device creation requests.

        Args:
            message (Dict[str, Union[int, str]]): The message containing device creation details.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            device_id_str = message.get("device_id")
            if not device_id_str.isdigit():
                raise ValueError("Device ID must be an integer greater than zero.")
            device_id = int(device_id_str)
            if device_id <= 0:
                raise ValueError("Device ID must be greater than zero.")

            if device_id in self.__device_map:
                raise ValueError("Device ID already exists.")

            device_type_str = message.get("device_type").upper()
            try:
                device_type = DeviceType[device_type_str]
            except KeyError:
                raise ValueError("Device type must be one of: MOTOR, SENSOR, RELAY.")

            self.__device_map[device_id] = device_type
            print(f"Device with ID {device_id} and type {device_type.value} created on the server.")
            return {
                "result_code": 0,
                "error_message": "",
                "data": {"device_id": device_id, "device_type": device_type.value}
            }
        except ValueError as ve:
            return {
                "result_code": 1,
                "error_message": str(ve),
                "data": {}
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def control_device(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle device control requests.

        Args:
            message (Dict[str, Union[int, str]]): The message containing device control details.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            device_id_str = message.get("device_id")
            if not device_id_str.isdigit():
                raise ValueError("Device ID must be an integer greater than zero.")
            device_id = int(device_id_str)
            if device_id <= 0:
                raise ValueError("Device ID must be greater than zero.")

            device_action_str = message.get("device_action").upper()
            try:
                device_action = DeviceAction[device_action_str]
            except KeyError:
                raise ValueError("Device action must be one of: CHANGE_SPEED, CHANGE_PATH, GET_VALUE, ON, OFF.")

            device_type = self.__device_map.get(device_id)
            if not device_type:
                raise ValueError("Invalid device ID.")

            if device_action in [DeviceAction.ON, DeviceAction.OFF]:
                state_str = "ON" if device_action == DeviceAction.ON else "OFF"
                result_message = {"device_id": device_id, "device_state": state_str}

            elif device_action == DeviceAction.CHANGE_SPEED:
                if device_type != DeviceType.MOTOR:
                    raise ValueError("CHANGE_SPEED action is only valid for MOTOR devices.")
                speed_str = message.get("value")
                if not speed_str.isdigit():
                    raise ValueError("Speed must be an integer.")
                speed = int(speed_str)
                if not (0 <= speed <= 100):
                    raise ValueError("Speed must be between 0 and 100.")
                result_message = {"device_id": device_id, "device_action": device_action.value, "speed": speed}

            elif device_action == DeviceAction.CHANGE_PATH:
                if device_type != DeviceType.RELAY:
                    raise ValueError("CHANGE_PATH action is only valid for RELAY devices.")
                path_str = message.get("value")
                if not path_str.isdigit():
                    raise ValueError("Path must be an integer.")
                path = int(path_str)
                if not (0 <= path <= 3):
                    raise ValueError("Path must be between 0 and 3.")
                result_message = {"device_id": device_id, "device_action": device_action.value, "path": path}

            elif device_action == DeviceAction.GET_VALUE:
                if device_type != DeviceType.SENSOR:
                    raise ValueError("GET_VALUE action is only valid for SENSOR devices.")
                result_message = {"device_id": device_id, "device_action": device_action.value, "value": "unknown"}

            else:
                raise ValueError("Invalid device action.")

            print(f"Device controlled with details: {result_message}")
            return {
                "result_code": 0,
                "error_message": "",
                "data": result_message
            }
        except ValueError as ve:
            return {
                "result_code": 1,
                "error_message": str(ve),
                "data": {}
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }

    def get_device_state(self, message: Dict[str, Union[int, str]]) -> Dict[str, Union[int, str]]:
        """
        Handle device state retrieval requests.

        Args:
            message (Dict[str, Union[int, str]]): The message containing device state retrieval details.

        Returns:
            Dict[str, Union[int, str]]: The response message.
        """
        try:
            device_id_str = message.get("device_id")
            if not device_id_str.isdigit():
                raise ValueError("Device ID must be an integer greater than zero.")
            device_id = int(device_id_str)
            if device_id <= 0:
                raise ValueError("Device ID must be greater than zero.")

            device_type = self.__device_map.get(device_id)
            if not device_type:
                raise ValueError("Invalid device ID.")

            result_message = {
                "device_id": device_id,
                "device_type": device_type.value,
                "state": "ON"  # Placeholder, would be determined dynamically
            }
            print(f"Device state retrieved: {result_message}")
            return {
                "result_code": 0,
                "error_message": "",
                "data": result_message
            }
        except ValueError as ve:
            return {
                "result_code": 1,
                "error_message": str(ve),
                "data": {}
            }
        except Exception as e:
            return {
                "result_code": 1,
                "error_message": str(e),
                "data": {}
            }


if __name__ == "__main__":
    server = Server("127.0.0.1", 8080)
