from uuid_extensions import uuid7


class Connection:
    def __init__(self, sensor_address, sensor_connection):
        connection_uuid = uuid7(as_type="str").split("-")

        self.id = connection_uuid[len(connection_uuid) - 1]
        self.sensor_address = sensor_address
        self.sensor_connection = sensor_connection
