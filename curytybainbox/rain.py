import time

import multiprocessing
from multiprocessing import Process, Event

import mraa


class RainProcess(Process):

    def __init__(self, gpio, sleep=1, name='RainProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.gpio = gpio
        self.pump = None
        self.sleep = sleep

    def _rain_on(self):
        self.logger.debug('LED on')
        self.pump.write(1)

    def _rain_off(self):
        self.logger.debug('LED off')
        self.pump.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        self.pump = mraa.Gpio(self.gpio)
        self.pump.dir(mraa.DIR_OUT)

        while self.event.is_set():
            self._rain_on()
            time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
        self._rain_off()
