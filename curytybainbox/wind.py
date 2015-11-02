import time

import multiprocessing
from multiprocessing import Process, Event

import mraa


class WindProcess(Process):

    def __init__(self, gpio, sleep=1, name='WindProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.name = name
        self.gpio = gpio
        self.fan = None
        self.sleep = sleep

    def _wind_on(self):
        self.logger.debug('LED on')
        self.fan.write(1)

    def _wind_off(self):
        self.logger.debug('LED off')
        self.fan.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        self.fan = mraa.Gpio(self.gpio)
        self.fan.dir(mraa.DIR_OUT)

        while self.event.is_set():
            self._wind_on()
            time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
        self._wind_off()
