import time
import multiprocessing
from multiprocessing import Process, Event
from Queue import Empty

import mraa

DUTYCYCLE = 0.003921569


class RGBLEDProcess(Process):

    def __init__(self, queue, sleep=1, name='RGBLEDProcess'):
        Process.__init__(self, name=name)
        self.logger = multiprocessing.get_logger()
        self.event = Event()
        self.name = name
        self.queue = queue
        self.sleep = sleep
        self.strobe = False

        self.blue = None
        self.green = None
        self.red = None

        self.blue_gpio = 3
        self.green_gpio = 6
        self.red_gpio = 5

        self.red_pwm = mraa.Pwm(self.red_gpio, owner=False)
        self.green_pwm = mraa.Pwm(self.green_gpio, owner=False)
        self.blue_pwm = mraa.Pwm(self.blue_gpio, owner=False)

        self.red_pwm.period_us(700)
        self.green_pwm.period_us(700)
        self.blue_pwm.period_us(700)

        self.red_pwm.enable(True)
        self.green_pwm.enable(True)
        self.blue_pwm.enable(True)

        self.color_set = False

    def _led_on(self):
        self.logger.debug('LED on')
        self.logger.debug('RED {}'.format(self.red))
        self.red_pwm.write(self.red)
        self.logger.debug('GREEN {}'.format(self.green))
        self.green_pwm.write(self.green)
        self.logger.debug('BLUE {}'.format(self.blue))
        self.blue_pwm.write(self.blue)

    def _led_off(self):
        self.logger.debug('LED off')
        if self.red_pwm:
            self.red_pwm.write(0)

        if self.green_pwm:
            self.green_pwm.write(0)

        if self.blue_pwm:
            self.blue_pwm.write(0)

    def run(self):
        self.event.set()
        self.logger.debug('PID: %d' % multiprocessing.current_process().pid)

        while self.event.is_set():
            self.logger.debug('Looping')

            try:
                data = self.queue.get(timeout=1)
                self.logger.debug('Received configuration: {}'.format(data))

                red = data['red']
                green = data['green']
                blue = data['blue']
                self.sleep = data['sleep']
                self.strobe = data['strobe']

                # TODO: Fix this ugly workaround
                if red == 255:
                    self.red = 1
                else:
                    self.red = float(red * DUTYCYCLE)

                self.logger.debug('RED {}'.format(self.red))

                if green == 255:
                    self.green = 1
                else:
                    self.green = float(green * DUTYCYCLE)

                self.logger.debug('GREEN {}'.format(self.green))

                if blue == 255:
                    self.blue = 1
                else:
                    self.blue = float(blue * DUTYCYCLE)

                self.logger.debug('BLUE {}'.format(self.blue))

                self.red_pwm.enable(True)
                self.green_pwm.enable(True)
                self.blue_pwm.enable(True)

                self.color_set = True

            except Empty:
                self.logger.debug('No configuration received')

            if self.color_set:
                self._led_on()
                time.sleep(self.sleep)
                if self.strobe:
                    self._led_off()
                    time.sleep(self.sleep)

    def stop(self):
        self.logger.debug('Process {} will turn off LED.'.format(self.name))
        self._led_off()
        self.red_pwm.enable(False)
        self.green_pwm.enable(False)
        self.blue_pwm.enable(False)
