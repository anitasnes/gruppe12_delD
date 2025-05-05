import logging
import threading
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:

            logging.info(f"Actuator {self.did}: {self.state.state}")

            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # TODO: START
        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response

        url = f"http://127.0.0.1:8000/smarthouse/actuator/{self.did}/current"
        while True:
            data = requests.get(url)
            state = data.json

            self.state = ActuatorState(state)
            
            time.sleep(3)

        logging.info(f"Client {self.did} finishing")

        # TODO: END

    def run(self):

        # TODO: START

        # start thread simulating physical light bulb
        simulating_thread = threading.Thread(target=self.simulator)
        simulating_thread.start()

        # start thread receiving state from the cloud
        client_thread = threading.Thread(target = self.client)
        client_thread.start()

        simulating_thread.join()
        client_thread.join()

        # TODO: END


