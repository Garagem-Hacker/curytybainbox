import time

import multiprocessing
from multiprocessing import Process, Event


class WeatherProcess(Process):

    def __init__(self, city, name='WeatherProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.name = name
        self.city = city

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)
        while self.event.is_set():
            time.sleep(1)

    def stop(self):
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
