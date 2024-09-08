import socket
import json
from typing import Optional, Dict, Union
from server import DeviceType, DeviceAction  # Ensure to adjust the import path as needed

class Client:
    """Client class to communicate with the server via socket."""

    def __init__(self, host: str , port: int ) -> None:
        """
        Initialize the Client with server host and port.

        Args:
            host (str): The server hostname or IP address.
            port (int): The server port number.
        """
        self.__server_host = host
        self.__server_port = port
        self.__client_socket = None
        self.__connect()
        self.__show_menu()

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

    def __connect(self) -> None:
        """Establish connection to the server."""
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.server_host, self.server_port))

    def __send_message(self, message: Dict[str, Union[int, str]]) -> None:
        """
        Send a JSON message to the server.

        Args:
            message (Dict[str, Union[int, str]]): The message to send.
        """
        self.__client_socket.sendall(json.dumps(message).encode('utf-8'))

    def __receive_data(self) -> Dict[str, Union[int, str]]:
        """
        Receive and decode a JSON response from the server.

        Returns:
            Dict[str, Union[int, str]]: The decoded JSON response.
        """
        response = self.__client_socket.recv(1024).decode('utf-8')
        return json.loads(response)

    def __close_connection(self) -> None:
        """Close the connection to the server."""
        self.__client_socket.close()

    def __show_menu(self) -> None:
        """Display the menu and handle user choices."""
        while True:
            print("\nMenu:")
            print("1. Create Device")
            print("2. Control Device")
            print("3. Get Device State")
            print("4. Exit")
            choice = input("Enter choice: ")

            if choice == '1':
                self.__create_device()
            elif choice == '2':
                self.__control_device()
            elif choice == '3':
                self.__get_device_state()
            elif choice == '4':
                self.__close_connection()
                break
            else:
                print("Invalid choice, try again.")



    def __create_device(self) -> None:
        """Handle device creation."""
        print("Device Types:")
        print("1. MOTOR")
        print("2. SENSOR")
        print("3. RELAY")
        choice = input("Enter choice (1-3): ")

        try:
            device_type = {
                '1': DeviceType.MOTOR,
                '2': DeviceType.SENSOR,
                '3': DeviceType.RELAY
            }[choice]
        except KeyError:
            print("Invalid choice.")
            return

        device_id = input("Enter device ID: ")
        message = {
            "request_type": 1,
            "device_id": device_id,
            "device_type": device_type.name  # Use the name of the enum
        }
        self.__send_message(message)
        response = self.__receive_data()
        print(response)

    def __control_device(self) -> None:
        """Handle controlling a device."""
        device_id = input("Enter device ID: ")

        # Send request to get device type and display appropriate options
        get_device_type_message = {
            "request_type": 3,
            "device_id": device_id
        }
        self.__send_message(get_device_type_message)
        response = self.__receive_data()

        if response['result_code'] == 0:
            device_type_str = response['data'].get('device_type').upper()

            try:
                device_type = DeviceType[device_type_str]
            except KeyError:
                print("Unknown device type.")
                return

            print(f"Device Type: {device_type.name}")

            if device_type == DeviceType.MOTOR:
                print("You can:")
                print("1. Change Speed")
                print("2. Turn On")
                print("3. Turn Off")
                choice = input("Enter choice (1-3): ")
                try:
                    action = {
                        '1': DeviceAction.CHANGE_SPEED,
                        '2': DeviceAction.ON,
                        '3': DeviceAction.OFF
                    }[choice]
                except KeyError:
                    print("Invalid choice.")
                    return

                if action == DeviceAction.CHANGE_SPEED:
                    value = input("Enter speed (0-100): ")
                else:
                    value = None

            elif device_type == DeviceType.RELAY:
                print("You can:")
                print("1. Change Path")
                print("2. Turn On")
                print("3. Turn Off")
                choice = input("Enter choice (1-3): ")
                try:
                    action = {
                        '1': DeviceAction.CHANGE_PATH,
                        '2': DeviceAction.ON,
                        '3': DeviceAction.OFF
                    }[choice]
                except KeyError:
                    print("Invalid choice.")
                    return

                if action == DeviceAction.CHANGE_PATH:
                    value = input("Enter path (0-3): ")
                else:
                    value = None

            elif device_type == DeviceType.SENSOR:
                print("You can:")
                print("1. Get Value")
                print("2. Turn On")
                print("3. Turn Off")
                choice = input("Enter choice (1-3): ")
                try:
                    action = {
                        '1': DeviceAction.GET_VALUE,
                        '2': DeviceAction.ON,
                        '3': DeviceAction.OFF
                    }[choice]
                except KeyError:
                    print("Invalid choice.")
                    return

                value = None

            else:
                print("Unknown device type.")
                return

            message = {
                "request_type": 2,
                "device_id": device_id,
                "device_action": action.value,  # Use the value of the enum
                "value": value
            }
            self.__send_message(message)
            response = self.__receive_data()
            print(response)

        else:
            print("Invalid device ID.")

    def __get_device_state(self) -> None:
        """Retrieve the state of a device."""
        device_id = input("Enter device ID: ")
        message = {
            "request_type": 3,
            "device_id": device_id
        }
        self.__send_message(message)
        response = self.__receive_data()
        print(response)


if __name__ == "__main__":
    client = Client()
