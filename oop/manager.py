from typing import Optional, Union

from oop.device import Device
from oop.device_status import DeviceStatus
from oop.enums import SensorType
from oop.device import Motor
from oop.device import Relay
from oop.device import Sensor
from server import DeviceType, DeviceAction


class Manager:
    """Manager class to handle the creation, control, and status retrieval of devices."""

    def __init__(self) -> None:
        """Initialize the Manager with an empty devices list."""
        self.__devices = []

    def create_device(
            self,
            device_type: DeviceType,
            id: int,
            speed: int = 0,
            sensor_type: Optional[SensorType] = None,
            path: Optional[str] = None
    ) -> str:
        """
        Create a new device and add it to the devices list.

        Args:
            device_type (DeviceType): The type of device to create.
            id (int): The ID of the device.
            speed (int): Speed of the motor, if applicable.
            sensor_type (Optional[SensorType]): Type of the sensor, if applicable.
            path (Optional[str]): Path of the relay, if applicable.

        Returns:
            str: Confirmation message of device creation.
        """
        device = Device.create(device_type, id, speed, sensor_type, path)
        self.__devices.append(device)
        return f"A {device_type.value} created with id {id}"

    def control_device(
            self,
            id: int,
            action: DeviceAction,
            value: Optional[Union[int, str]] = None
    ) -> str:
        """
        Control a device by performing the specified action.

        Args:
            id (int): The ID of the device.
            action (DeviceAction): The action to perform on the device.
            value (Optional[Union[int, str]]): The value for the action, if applicable.

        Returns:
            str: Result of the action performed.

        Raises:
            ValueError: If the action is unknown or inappropriate for the device type.
        """
        device = next((d for d in self.__devices if d.id == id), None)

        if device:
            if action == DeviceAction.ON:
                return device.on()
            elif action == DeviceAction.OFF:
                return device.off()
            elif action == DeviceAction.CHANGE_SPEED and isinstance(device, Motor):
                return device.perform_action(value)
            elif action == DeviceAction.CHANGE_PATH and isinstance(device, Relay):
                return device.perform_action(value)
            elif action == DeviceAction.GET_VALUE and isinstance(device, Sensor):
                value = device.perform_action()
                return f"Value of sensor {device.id}: {value}"
            else:
                raise ValueError(f"Unknown action or inappropriate device type for action: {action}")
        else:
            raise ValueError(f"Device with ID {id} does not exist.")

    def get_state(self, id: int) -> DeviceStatus:
        """
        Retrieve the status of a device by its ID.

        Args:
            id (int): The ID of the device.

        Returns:
            DeviceStatus: The status of the device.

        Raises:
            ValueError: If the device with the given ID does not exist.
        """
        device = next((d for d in self.__devices if d.id == id), None)

        if device:
            return device.device_status()
        else:
            raise ValueError(f"Device with ID {id} does not exist.")
