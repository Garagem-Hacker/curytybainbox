import os
import time
import socket
import multiprocessing
from multiprocessing import Process, Event, Queue
from Queue import Full

from .led import RGBLEDProcess
from .weather import WeatherProcess
from .rain import RainProcess
from .mist import MistProcess
from .wind import WindProcess


class BoxProcess(Process):

    def __init__(self, unix_path, sleep=60, name='BoxProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.name = name
        self.sleep = sleep
        self.unix_path = unix_path
        self.rgb_led = None
        self.rain = None
        self.mist = None
        self.wind = None
        self.demo = None
        self.weather = None
        self.led_queue = None

        if os.path.exists(self.unix_path):
            os.remove(self.unix_path)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(self.unix_path)
        self.server.settimeout(1)

    def _rain(self):
        self.logger.debug('Creating a rain weather')
        return RainProcess(gpio=11, sleep=1)

    def _mist(self):
        self.logger.debug('Creating a mist weather')
        return MistProcess(gpio=12, sleep=1)

    def _wind(self):
        self.logger.debug('Creating a wind weather')
        return WindProcess(gpio=10, sleep=1)

    def _demo(self):
        self.logger.debug("Creating a demo weather for Hell's Kitchen")
        city = "Hell's Kitchen"
        return WeatherProcess(city)

    def _weather(self, city):
        self.logger.debug('Creating a weather for city: {}'.format(city))
        return WeatherProcess(city)

    def _terminate_processes(self):
        self.logger.debug('Trying terminate processes')

        if self.rgb_led:
            self.rgb_led.stop()

        if self.rain:
            self.rain.stop()
            self.rain.terminate()
            self.rain = None

        if self.mist:
            self.mist.stop()
            self.mist.terminate()
            self.mist = None

        if self.wind:
            self.wind.stop()
            self.wind.terminate()
            self.wind = None

        if self.demo:
            self.demo.stop()
            self.demo.terminate()
            self.demo = None

        if self.weather:
            self.weather.stop()
            self.weather.terminate()
            self.weather = None

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        self.led_queue = Queue()
        self.logger.debug('Creating a RGB LED process')
        self.rgb_led = RGBLEDProcess(self.led_queue)
        self.rgb_led.start()

        while self.event.is_set():

            try:
                command = self.server.recv(1024)
            except socket.timeout:
                self.logger.debug('No command received, continue...')
                continue

            if command == 'thunderstorm':
                self.logger.debug('Received command: {}'.format(command))
                self.logger.debug('Starting thunderstorm weather')
                try:
                    self.led_queue.put({'red': 200, 'green': 200, 'blue': 255, 'strobe': True, 'sleep': 0.3}, False)
                except Full:
                    self.logger.debug('LED queue is full')

            if command == 'sunny':
                self.logger.debug('Received command: {}'.format(command))
                self.logger.debug('Staring a sunny weather')
                try:
                    self.led_queue.put({'red': 255, 'green': 100, 'blue': 0, 'strobe': False, 'sleep': 1}, False)
                except Full:
                    self.logger.debug('LED queue is full')

            if command == 'rain':
                self.logger.debug('Received command: {}'.format(command))
                self.rain = self._rain()
                self.rain.start()

            if command == 'mist':
                self.logger.debug('Received command: {}'.format(command))
                self.mist = self._mist()
                self.mist.start()

            if command == 'wind':
                self.logger.debug('Received command: {}'.format(command))
                self.wind = self._wind()
                self.wind.start()

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
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
        self.server.close()
        self._terminate_processes()
        os.remove(self.unix_path)
