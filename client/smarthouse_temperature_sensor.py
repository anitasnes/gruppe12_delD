from datetime import datetime
import logging
import threading
import time
import math
import requests

from messaging import SensorMeasurement
import common


class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)

            logging.info(f"Sensor {self.did}: {temp}")
            self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        # TODO: START
        # send temperature to the cloud service with regular intervals
        url = f"http://127.0.0.1:8000/smarthouse/sensor/{self.did}/current"
    
        while True:
            try:
                value = float(self.measurement.value)
                timestamp = datetime.utcnow().isoformat()
                payload = {
                    "timestamp": timestamp,
                    "value": value,
                    "unit": "°C"
                    }
                print(payload)
                response = requests.post(url, json=payload, auth=("user", "pass"))
                response.raise_for_status()
                logging.info(f"Sent temperature {value} to server.")
            except Exception as e:
                logging.error(f"Failed to send measurement: {e}")
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)
        
        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):

        # TODO: START

        # create and start thread simulating physical temperature sensor
        sim_thread = threading.Thread(target=self.simulator, daemon=True)
        sim_thread.start()
        
        # create and start thread sending temperature to the cloud service
        client_thread = threading.Thread(target=self.client, daemon=True)
        client_thread.start()

        sim_thread.join()
        client_thread.join()

        # TODO: END

