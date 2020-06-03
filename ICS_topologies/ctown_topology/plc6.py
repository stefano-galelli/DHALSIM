from minicps.devices import PLC
from utils import PLC6_DATA, STATE, PLC6_PROTOCOL
from utils import T4, PLC6_ADDR
import csv
from datetime import datetime
import logging
from decimal import Decimal
import time
import signal
import sys


logging.basicConfig(filename='plc6_debug.log', level=logging.DEBUG)
logging.debug("testing")
plc6=_log_path = 'plc6.log'

class PLC6(PLC):

    def sigint_handler(self, sig, frame):
        self.write_output()
        sys.exit(0)

    def write_output(self):
        print 'DEBUG plc6 shutdown'
        with open('output/plc6_saved_tank_levels_received.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.saved_tank_levels)
        exit(0)

    def pre_loop(self):
        print 'DEBUG: plc6 enters pre_loop'
        self.local_time = 0
        self.saved_tank_levels = [["iteration", "timestamp", "T4"]]
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGTERM, self.sigint_handler)

    def main_loop(self):

        while True:
            self.t4 = Decimal(self.get(T4))
            self.local_time += 1
            self.saved_tank_levels.append([self.local_time, datetime.now(), self.t4])

            print("Tank Level %f " % self.t4)
            print("ITERATION %d ------------- " % self.local_time)
            self.send(T4, self.t4, PLC6_ADDR)

if __name__ == "__main__":
    plc6 = PLC6(
        name='plc6',
        state=STATE,
        protocol=PLC6_PROTOCOL,
        memory=PLC6_DATA,
        disk=PLC6_DATA)