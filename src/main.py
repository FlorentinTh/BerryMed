import os
import sys

import _bleio
import adafruit_ble
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_ble_berrymed_pulse_oximeter import BerryMedPulseOximeterService
from dotenv import load_dotenv

from core import Connection, Data
from helpers import Logger

load_dotenv()

SCAN_TIMEOUT = os.getenv("SCAN_TIMEOUT")
SENSOR_ADDRESS = os.getenv("SENSOR_ADDRESS")
DATA_OUTPUT_PATH = os.getenv("DATA_OUTPUT_PATH")

if not SCAN_TIMEOUT:
    SCAN_TIMEOUT = 10
else:
    SCAN_TIMEOUT = int(SCAN_TIMEOUT)

if not SENSOR_ADDRESS:
    raise ValueError("SENSOR_ADDRESS environment variable is not set")

if not DATA_OUTPUT_PATH:
    DATA_OUTPUT_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data"
    )
else:
    DATA_OUTPUT_PATH = os.path.abspath(DATA_OUTPUT_PATH)

connection_error = ConnectionError

if hasattr(_bleio, "ConnectionError"):
    connection_error = _bleio.ConnectionError

ble = adafruit_ble.BLERadio()

connections = []

try:
    while True:
        Logger.write(f"scan is started (timeout: {SCAN_TIMEOUT}s)")

        for adv in ble.start_scan(Advertisement, timeout=SCAN_TIMEOUT):
            sensor_address = adv.address.string

            if not sensor_address:
                continue

            if sensor_address == SENSOR_ADDRESS:
                sensor_connection = ble.connect(adv)

                connection = Connection(sensor_address, sensor_connection)
                connections.append(connection)

                Logger.write(f"connected to sensor: {sensor_address}")

                # break

        ble.stop_scan()
        Logger.write("scan is stopped, end of timeout")

        for connection in connections:
            try:
                if (
                    connection.sensor_connection
                    and connection.sensor_connection.connected
                ):
                    pulse_ox_service = connection.sensor_connection[
                        BerryMedPulseOximeterService
                    ]

                    while connection.sensor_connection.connected:
                        data_values = pulse_ox_service.values

                        if data_values is not None:
                            data = Data(connection, data_values, DATA_OUTPUT_PATH)

            except connection_error:
                try:
                    connection.sensor_connection.disconnect()
                except connection_error:
                    pass

                connection.sensor_connection = None
except KeyboardInterrupt:
    Logger.write("program interrupted", break_line=True)
    sys.exit(1)
