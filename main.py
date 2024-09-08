from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Union


class DeviceType(Enum):
    """Enum representing different types of devices."""
    MOTOR = "Motor"
    SENSOR = "Sensor"
    RELAY = "Relay"


class DeviceAction(Enum):
    """Enum representing possible actions that a device can perform."""
    ON = "on"
    OFF = "off"
    CHANGE_SPEED = "change_speed"
    CHANGE_PATH = "change_path"
    GET_VALUE = "get_value"


class SensorType(Enum):
    """Enum representing the types of sensors available."""
    LIGHT_SENSOR = "Light Sensor"
    CO2_SENSOR = "CO2 Sensor"
    SOIL_HUMIDITY_SENSOR = "Soil Humidity Sensor"
    AIR_HUMIDITY_AND_TEMPERATURE_SENSOR = "Air Temperature and Humidity Sensor"


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
            speed: Optional[int] = 0,
            sensor_type: Optional[SensorType] = None,
            path: Optional[str] = None
    ) -> Union['Motor', 'Sensor', 'Relay']:
        """
        Factory method to create an instance of a specific device type.

        Args:
            device_type (DeviceType): The type of device to create.
            id (int): The ID of the device.
            speed (Optional[int]): Speed of the motor, if applicable.
            sensor_type (Optional[SensorType]): Type of the sensor, if applicable.
            path (Optional[str]): Path of the relay, if applicable.

        Returns:
            Union['Motor', 'Sensor', 'Relay']: An instance of the specified device type.

        Raises:
            ValueError: If the device type is unknown.
        """
        if device_type == DeviceType.MOTOR:
            return Motor(id, speed)
        elif device_type == DeviceType.SENSOR:
            return Sensor(id, sensor_type)
        elif device_type == DeviceType.RELAY:
            return Relay(id, path)
        else:
            raise ValueError(f"Unknown device type: {device_type}")


class Motor(Device):
    """Concrete class representing a Motor device."""

    def __init__(self, id: int, speed: int) -> None:
        """
        Initialize a Motor instance.

        Args:
            id (int): The ID of the motor.
            speed (int): The initial speed of the motor.
        """
        self.__id = id
        self.__status = "off"
        self.__speed = speed

    @property
    def id(self) -> int:
        """Return the ID of the motor."""
        return self.__id

    @property
    def status(self) -> str:
        """Return the status of the motor."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the status of the motor.

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
    def speed(self) -> int:
        """Return the speed of the motor."""
        return self.__speed

    @speed.setter
    def speed(self, value: int) -> None:
        """
        Set the speed of the motor.

        Args:
            value (int): The speed to set (must be non-negative).

        Raises:
            ValueError: If the speed is negative.
        """
        if value >= 0:
            self.__speed = value
        else:
            raise ValueError("Speed must be a non-negative value")

    def on(self) -> None:
        """Turn the motor on and update its status."""
        self.__status = "on"
        return f"Motor {self.__id} is now ON."

    def off(self) -> None:
        """Turn the motor off and update its status."""
        self.__status = "off"
        return f"Motor {self.__id} is now OFF."

    def perform_action(self, speed: int) -> None:
        """
        Set the motor speed and return the change.

        Args:
            speed (int): The speed to set.
        """
        self.__speed = speed
        return f"Speed of motor {self.__id} changed to {self.__speed}"

    def device_status(self) -> DeviceStatus:
        """
        Return the current status of the motor, including its speed.

        Returns:
            DeviceStatus: The status of the motor.
        """
        return DeviceStatus(
            id=self.__id,
            status=self.__status,
            speed=self.__speed
        )


class Sensor(Device):
    """Concrete class representing a Sensor device."""

    def __init__(self, id: int, sensor_type: SensorType) -> None:
        """
        Initialize a Sensor instance.

        Args:
            id (int): The ID of the sensor.
            sensor_type (SensorType): The type of the sensor.
        """
        self.__id = id
        self.__status = "off"
        self.__sensor_type = sensor_type
        self.__value = 0

    @property
    def id(self) -> int:
        """Return the ID of the sensor."""
        return self.__id

    @property
    def status(self) -> str:
        """Return the status of the sensor."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the status of the sensor.

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
    def sensor_type(self) -> SensorType:
        """Return the type of the sensor."""
        return self.__sensor_type

    @property
    def value(self) -> float:
        """Return the value of the sensor."""
        return self.__value

    def on(self) -> None:
        """Turn the sensor on and update its status."""
        self.__status = "on"
        return f"Sensor {self.__id} is now ON."

    def off(self) -> None:
        """Turn the sensor off and update its status."""
        self.__status = "off"
        return f"Sensor {self.__id} is now OFF."

    def perform_action(self) -> float:
        """
        Return the current value of the sensor.

        Returns:
            float: The value of the sensor.
        """
        return self.__value

    def device_status(self) -> DeviceStatus:
        """
        Return the current status of the sensor, including its type and value.

        Returns:
            DeviceStatus: The status of the sensor.
        """
        return DeviceStatus(
            id=self.__id,
            status=self.__status,
            sensor_type=self.__sensor_type.value,
            value=self.perform_action()
        )


class Relay(Device):
    """Concrete class representing a Relay device."""

    def __init__(self, id: int, path: str) -> None:
        """
        Initialize a Relay instance.

        Args:
            id (int): The ID of the relay.
            path (str): The initial path of the relay.
        """
        self.__id = id
        self.__status = "off"
        self.__path = path

    @property
    def id(self) -> int:
        """Return the ID of the relay."""
        return self.__id

    @property
    def status(self) -> str:
        """Return the status of the relay."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """
        Set the status of the relay.

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
    def path(self) -> str:
        """Return the path of the relay."""
        return self.__path

    @path.setter
    def path(self, value: str) -> None:
        """
        Set the path of the relay.

        Args:
            value (str): The path to set.
        """
        self.__path = value

    def on(self) -> None:
        """Turn the relay on and update its status."""
        self.__status = "on"
        return f"Relay {self.__id} is now ON."

    def off(self) -> None:
        """Turn the relay off and update its status."""
        self.__status = "off"
        return f"Relay {self.__id} is now OFF."

    def perform_action(self, path: str) -> None:
        """
        Set the relay path and return the change.

        Args:
            path (str): The path to set.
        """
        self.__path = path
        return f"Path of relay {self.__id} changed to {self.__path}"

    def device_status(self) -> DeviceStatus:
        """
        Return the current status of the relay, including its path.

        Returns:
            DeviceStatus: The status of the relay.
        """
        return DeviceStatus(
            id=self.__id,
            status=self.__status,
            path=self.__path
        )


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
