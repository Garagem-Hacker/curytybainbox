import os
import time
import socket

import multiprocessing
from multiprocessing import Process, Event

from .led import RGBLEDProcess
from .weather import WeatherProcess


class BoxProcess(Process):

    def __init__(self, unix_path, sleep=60, name='BoxProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.sleep = sleep
        self.unix_path = unix_path
        self.thunderstorm = None
        self.sunny = None
        self.demo = None
        self.weather = None

    def _thunderstorm(self):
        self.logger.debug('Creating a thunderstorm weather')
        return RGBLEDProcess(red=200, green=200, blue=255, strobe=True,
                             sleep=0.5, name='ThunderstormProcess')

    def _sunny(self):
        self.logger.debug('Creating a sunny weather')
        return RGBLEDProcess(red=200, green=200, blue=255, strobe=False, sleep=1)

    def _demo(self):
        self.logger.debug("Creating a demo weather for Hell's Kitchen")
        city = "Hell's Kitchen"
        return WeatherProcess(city)

    def _weather(self, city):
        self.logger.debug('Creating a weather for city: {}'.format(city))
        return WeatherProcess(city)

    def _terminate_processes(self):
        self.logger.debug('Trying stop processes')
        if self.thunderstorm:
            self.thunderstorm.terminate()
            self.thunderstorm = None
        if self.sunny:
            self.sunny.terminate()
            self.sunny = None
        if self.demo:
            self.demo.terminate()
            self.demo = None
        if self.weather:
            self.weather.terminate()
            self.weather = None

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        if os.path.exists(self.unix_path):
            os.remove(self.unix_path)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.unix_path)
        self.server.settimeout(1)

        while self.event.is_set():

            try:
                command = self.server.recv(1024)
            except socket.timeout:
                self.logger.debug('No command received, continue...')
                continue

            if command == 'thunderstorm':
                self.logger.debug('Received command: {}'.format(command))
                self._terminate_processes()
                self.thunderstorm = self._thunderstorm()
                self.thunderstorm.start()

            if command == 'sunny':
                self.logger.debug('Received command: {}'.format(command))
                self._terminate_processes()
                self.sunny = self._sunny()
                self.sunny.start()

            if command == 'demo':
                self.logger.debug('Received command: {}'.format(command))
                self._terminate_processes()
                self.demo = self._demo()
                self.demo.start()

            if command.startswith('weather:'):
                self.logger.debug('Received command: {}'.format(command))
                self._terminate_processes()
                _, city = command.split(':')
                self.weather = self._weather(city)
                self.weather.start()

            if command == 'stop':
                self.logger.debug('Received command: {}'.format(command))
                self._terminate_processes()

            time.sleep(1)

    def stop(self):
        self.logger.debug('Process will halt.')
        self.event.clear()
        self.server.close()
        self._terminate_processes()
        os.remove(self.unix_path)
        self.terminate()
