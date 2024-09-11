from abc import ABC, abstractmethod
from typing import Optional, Union
from oop.device_status import DeviceStatus
from oop.enums import SensorType

from server import DeviceType


class Device(ABC):
    """Abstract base class for all devices."""

    @abstractmethod
    def device_status(self) -> DeviceStatus:
        """
        Return the status of the device.

        Returns:
            DeviceStatus: The current status of the device.
        """
        pass

    @abstractmethod
    def on(self) -> None:
        """Turn the device on."""
        pass

    @abstractmethod
    def off(self) -> None:
        """Turn the device off."""
        pass

    @abstractmethod
    def perform_action(self, value: Optional[Union[int, str]] = None) -> Union[None, float]:
        """
        Perform a specific action on the device.

        Args:
            value (Optional[Union[int, str]]): The value for the action, if applicable.

        Returns:
            Union[None, float]: The result of the action, if applicable.
        """
        pass

    @staticmethod
    def create(
            device_type: DeviceType,
            id: int,
            sensor_type: Optional[SensorType] = None,
    ) -> Union['Motor', 'Sensor', 'Relay']:
        """
        Factory method to create an instance of a specific device type.

        Args:
            device_type (DeviceType): The type of device to create.
            id (int): The ID of the device.
            sensor_type (Optional[SensorType]): Type of the sensor, if applicable.
        Returns:
            Union['Motor', 'Sensor', 'Relay']: An instance of the specified device type.

        Raises:
            ValueError: If the device type is unknown.
        """
        if device_type == DeviceType.MOTOR:
            from oop.motor import Motor
            return Motor(id)
        elif device_type == DeviceType.SENSOR:
            from oop.sensor import Sensor
            return Sensor(id,sensor_type)
        elif device_type == DeviceType.RELAY:
            from oop.relay import Relay
            return Relay(id)
        else:
            raise ValueError(f"Unknown device type: {device_type}")





