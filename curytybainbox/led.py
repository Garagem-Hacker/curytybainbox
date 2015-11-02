import time

import multiprocessing
from multiprocessing import Process, Event

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
        self.blue_gpio = 3
        self.green_gpio = 5
        self.red_gpio = 6
        self.red_pwm = mraa.Pwm(self.red_gpio, owner=False)
        self.green_pwm = mraa.Pwm(self.green_gpio, owner=False)
        self.blue_pwm = mraa.Pwm(self.blue_gpio, owner=False)
        self.red_pwm.period_us(700)
        self.green_pwm.period_us(700)
        self.blue_pwm.period_us(700)
        self.red_pwm.enable(True)
        self.green_pwm.enable(True)
        self.blue_pwm.enable(True)

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

            data = self.queue.get()
            self.logger.debug('Received configuration: {}'.format(data))
            if data:
                red = data['red']
                green = data['green']
                blue = data['blue']
                self.sleep = data['sleep']
                self.strobe = data['False']

                # TODO: Fix this ugly workaround
                if red == 255:
                    self.red = 1
                else:
                    self.red = float(red * DUTYCYCLE)

                if green == 255:
                    self.green = 1
                else:
                    self.green = float(green * DUTYCYCLE)

                if blue == 255:
                    self.blue = 1
                else:
                    self.blue = float(blue * DUTYCYCLE)

                self._led_on()
                time.sleep(self.sleep)
                if self.strobe:
                    self._led_off()
                    time.sleep(self.sleep)

            time.sleep(1)

    def stop(self):
        self.logger.debug('Process {} will halt.'.format(self.name))
        self.event.clear()
        self._led_off()
        self.red_pwm.enable(False)
        self.green_pwm.enable(False)
        self.blue_pwm.enable(False)
