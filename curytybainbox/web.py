import sys
import socket
import logging

from prettyconf import config

from flask import Flask
from flask import (redirect, url_for, render_template,
                   flash)

app = Flask(__name__)

log = logging.getLogger('curytybainbox')

unix_path = config('CURYTYBAINBOX_UNIX_PATH', default='/var/run/curytybainbox')

client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
try:
    client.connect(unix_path)
except socket.error:
    print('Can not connect to curytybainbox daemon.\nStart it using: curytybainboxd')
    sys.exit(1)


def send_command(command):
    try:
        client.send(command)
    except socket.error:
        flash('Error sending command: "{}", check if "curytybainboxd" process is running.'.format(command), 'bg-danger')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/thunderstorm')
def thunderstorm():
    flash('Starting a thunderstorm weather', 'bg-info')
    send_command('thunderstorm')
    return redirect(url_for('index'))


@app.route('/sunny')
def sunny():
    flash('Starting a sunny weather', 'bg-info')
    send_command('sunny')
    return redirect(url_for('index'))


@app.route('/rain')
def rain():
    flash('Starting a rain weather', 'bg-info')
    send_command('rain')
    return redirect(url_for('index'))


@app.route('/mist')
def mist():
    flash('Starting a mist weather', 'bg-info')
    send_command('mist')
    return redirect(url_for('index'))


@app.route('/wind')
def wind():
    flash('Starting a wind weather', 'bg-info')
    send_command('wind')
    return redirect(url_for('index'))


@app.route('/demo')
def demo():
    flash('Starting a demo weather', 'bg-info')
    send_command('demo')
    return redirect(url_for('index'))


@app.route('/weather/<city>')
def weather(city):
    flash('Starting a weather for city: {}'.format(city), 'bg-info')
    weather = 'weather:{}'.format(city)
    send_command(weather)
    return redirect(url_for('index'))


@app.route('/stop')
def stop():
    flash('Stoping the box', 'bg-info')
    send_command('stop')
    return redirect(url_for('index'))
