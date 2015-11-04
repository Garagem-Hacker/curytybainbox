# curytybainbox

Curytyba in a box in a clone of tempoescope using Python and Intel Edison.

This is used to mimetize Curitiba crazy weather ;D


How it works
------------

It have a pair o services:

* ``curytybainboxd``: A daemon who know howto talk to GPIO.
* ``curytybainboxweb``: A web interface that let user control the box.


Features
--------

**This is a work in progress, please feel free to help!**

Manually control:

* ``Rain``: Starts the water pump.
* ``Mist``: Starts ultrasonic diffuser.
* ``Wind``: Starts the cpu fan.
* ``Thunderstorm``: Starts the RGB LED in thunder mode.
* ``Sun``: Starts the RGB LED in sunny mode.


Setup
-----

To discovery in what port it is connected:

```
tail -f /var/log/syslog
```

Use this information to connect using serial to the board:

```
screen /dev/ttyUSB0 115200

```

The login in GaragemHacker board use `root` as user and `rapadura` a pass.


Installation
------------


Install setuptools:

```
wget https://bootstrap.pypa.io/ez_setup.py
python ez_setup.py
```

Intall pip:

```
https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

Get the code:

```
git clone https://github.com/Garagem-Hacker/curytybainbox.git
```

Install it:

```
python setup.py install
```

Start it:

```
systemctl start curytybainboxd
systemctl stary curytybainboxweb
```


Troubleshooting
---------------

To enable debug change `CURYTYBAINBOX_DEBUG` to `True` in
`/etc/curytybainbox/environment`. and look the logs using:

```
journalctl -fn
```


LICENSE
-------

Licensed under the GPLv3.

Copyright 2015 Curytyba in a box Authors.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
