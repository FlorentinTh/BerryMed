import os
from datetime import datetime

from helpers import Logger


class Data:
    def __init__(self, connection, data_values, output_file_path="data.csv"):
        self.connection_id = connection.id
        self.timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        self.sensor_address = connection.sensor_address
        self.spo2 = data_values.spo2
        self.pulse_rate = data_values.pulse_rate
        self.pleth = data_values.pleth
        self.output_file_path = os.path.join(output_file_path, "data.csv")

        if data_values.valid and data_values.finger_present:
            if self.spo2 < 127 and self.pulse_rate < 255:
                self.write_to_file()
                Logger.write(f"data written to {self.output_file_path}")

    def write_to_file(self):
        directory = os.path.dirname(self.output_file_path)

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        file_exists = os.path.exists(self.output_file_path)

        with open(self.output_file_path, "a") as file:
            if not file_exists:
                file.write("connection_id,timestamp,sensor,spo2,pulse_rate,pleth\n")

            file.write(
                f"{self.connection_id},{self.timestamp},{self.sensor_address},{self.spo2},{self.pulse_rate},{self.pleth}\n"
            )
