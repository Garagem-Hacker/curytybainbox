import time

import multiprocessing
from multiprocessing import Process, Event


class RGBLEDProcess(Process):

    def __init__(self, red, green, blue, strobe, sleep=0.5, name='RGBLEDProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.red = red
        self.green = green
        self.blue = blue
        self.sleep = sleep
        self.strobe = strobe

    def _led_on(self):
        self.logger.debug('LED on')

    def _led_off(self):
        self.logger.debug('LED off')

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            self._led_on()
            time.sleep(self.sleep)
            if self.strobe:
                self._led_off()
                time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process will halt.')
        self.event.clear()
        self.terminate()
