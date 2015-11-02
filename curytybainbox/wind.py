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
        self.sleep = sleep
        self.wind = mraa.Gpio(self.gpio)
        self.wind.dir(mraa.DIR_OUT)

    def _wind_on(self):
        self.logger.debug('Wind on')
        self.wind.write(1)

    def _wind_off(self):
        self.logger.debug('Wind off')
        if self.wind:
            self.wind.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        while self.event.is_set():
            self._wind_on()
            time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
        self._wind_off()
