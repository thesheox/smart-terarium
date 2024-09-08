from typing import Optional, Union
class DeviceStatus:
    """Class to encapsulate the status of a device."""

    def __init__(
            self,
            id: int,
            status: str,
            speed: Optional[int] = None,
            path: Optional[str] = None,
            sensor_type: Optional[str] = None,
            value: Optional[Union[int, float]] = None
    ) -> None:
        """
        Initialize a DeviceStatus instance.

        Args:
            id (int): ID of the device.
            status (str): Current status of the device (e.g., "on" or "off").
            speed (Optional[int]): Speed of the motor (optional).
            path (Optional[str]): Path of the relay (optional).
            sensor_type (Optional[str]): Type of the sensor (optional).
            value (Optional[Union[int, float]]): Value of the sensor (optional).
        """
        self.__id = id
        self.__status = status
        self.__speed = speed
        self.__path = path
        self.__sensor_type = sensor_type
        self.__value = value

    @property
    def id(self) -> int:
        """Return the ID of the device."""
        return self.__id

    @property
    def status(self) -> str:
        """Return the status of the device."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the status of the device.

        Args:
            value (str): The status to set (must be "on" or "off").

        Raises:
            ValueError: If the status is not "on" or "off".
        """
        if value in ["on", "off"]:
            self.__status = value
        else:
            raise ValueError("Status must be 'on' or 'off'")

    @property
    def speed(self) -> Optional[int]:
        """Return the speed of the motor, if applicable."""
        return self.__speed

    @property
    def path(self) -> Optional[str]:
        """Return the path of the relay, if applicable."""
        return self.__path

    @property
    def sensor_type(self) -> Optional[str]:
        """Return the type of the sensor, if applicable."""
        return self.__sensor_type

    @property
    def value(self) -> Optional[Union[int, float]]:
        """Return the value of the sensor, if applicable."""
        return self.__value

