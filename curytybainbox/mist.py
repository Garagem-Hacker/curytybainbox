import time

import multiprocessing
from multiprocessing import Process, Event

import mraa


class MistProcess(Process):

    def __init__(self, gpio, sleep=1, name='MistProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.gpio = gpio
        self.mist = None
        self.sleep = sleep

    def _mist_on(self):
        self.logger.debug('Mist on')
        self.mist.write(1)

    def _mist_off(self):
        self.logger.debug('Mist off')
        self.mist.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        self.mist = mraa.Gpio(self.gpio)
        self.mist.dir(mraa.DIR_OUT)

        while self.event.is_set():
            self._mist_on()
            time.sleep(self.sleep)

    def stop(self):
        self._mist_off()
        self.logger.debug('Process will halt.')
        self.event.clear()
        self.terminate()
