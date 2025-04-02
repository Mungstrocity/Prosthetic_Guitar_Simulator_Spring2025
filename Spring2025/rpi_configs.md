# RPI Configuration Steps

## Python Packages
### Worm Gear Control
#### Global: dpkg --get-selections
##### Query specific package details with: dpkg-query -W -f='${binary:Package}\t${Version}\t${Status}\t${Installed-Size}\t${Architecture}\t${Date}\n' python3
##### python-apt-common                               install
##### python-babel-localedata                         install
##### python-is-python3                               install
##### python3                                         install
##### python3-apt                                     install
##### python3-asgiref                                 install
##### python3-attr                                    install
##### python3-av                                      install
##### python3-babel                                   install
##### python3-importlib-metadata                      install
##### python3-itsdangerous                            install
##### python3-jinja2                                  install
##### python3-json-pointer                            install
##### python3-jsonschema                              install
##### python3-jwt                                     install
##### python3-kms++                                   install
##### python3-lgpio                                   install
##### python3-lib2to3                                 install
##### python3-libarchive-c                            install
##### python3-libcamera:arm64                         install
##### python3-libevdev                                install
##### python3-libgpiod:arm64                          install
##### python3-lxml:arm64                              install
##### python3-markupsafe                              install
##### python3-minimal                                 install
##### python3-more-itertools                          install
##### python3-numpy                                   install
##### python3-oauthlib                                install
##### python3-olefile                                 install
##### python3-opengl                                  install
##### python3-openssl                                 install
##### python3-pexpect                                 install
##### python3-pgzero                                  install
##### python3-picamera2                               install
##### python3-pidng                                   install
##### python3-piexif                                  install
##### python3-pigpio                                  install
##### python3-pil:arm64                               install
##### python3-pip                                     install
##### python3-pip-whl                                 install
##### python3-pkg-resources                           install
##### python3-prctl                                   install
##### python3-ptyprocess                              install
##### python3-pycryptodome                            install
##### python3-pygame                                  install
##### python3-pyinotify                               install
##### python3-pyqt5                                   install
##### python3-pyqt5.sip                               install
##### python3-pyrsistent:arm64                        install
##### python3-pyudev                                  install
##### python3-renderpm:arm64                          install
##### python3-reportlab                               install
##### python3-reportlab-accel:arm64                   install
##### python3-requests                                install
##### python3-requests-oauthlib                       install
##### python3-responses                               install
##### python3-rfc3987                                 install
##### python3-rpi-lgpio                               install
##### python3-rtimulib                                install
##### python3-sense-hat                               install
##### python3-serial                                  install
##### python3-setuptools                              install
##### python3-setuptools-whl                          install
##### python3-simplejpeg                              install
##### python3-simplejson                              install
##### python3-six                                     install
##### python3-smbc                                    install
##### python3-smbus:arm64                             install
##### python3-smbus2                                  install
##### python3-soupsieve                               install
##### python3-spidev                                  install
##### python3-tk:arm64                                install
##### python3-toml                                    install
##### python3-tqdm                                    install
##### python3-twython                                 install
##### python3-typing-extensions                       install
##### python3-tz                                      install
##### python3-uritemplate                             install
##### python3-urllib3                                 install
##### python3-v4l2                                    install
##### python3-venv                                    install
##### python3-webcolors                               install
##### python3-webencodings                            install
##### python3-werkzeug                                install
##### python3-wheel                                   install
##### python3-zipp                                    install
##### python3.11                                      install
##### python3.11-dev                                  install
##### python3.11-minimal                              install
##### python3.11-venv                                 install

#### Local to .venv: pip list
##### Package                                         Version
##### ----------------------------------------------- -------
##### Adafruit-Blinka                                 8.55.0
##### adafruit-circuitpython-busdevice                5.2.11
##### adafruit-circuitpython-connectionmanager        3.1.3
##### adafruit-circuitpython-motor                    3.4.15
##### adafruit-circuitpython-pca9685                  3.4.17
##### adafruit-circuitpython-register                 1.10.2
##### adafruit-circuitpython-requests                 4.1.10
##### adafruit-circuitpython-servokit                 1.3.19
##### adafruit-circuitpython-typing                   1.11.2
##### Adafruit-PlatformDetect                         3.77.0
##### Adafruit-PureIO                                 1.1.11
##### binho-host-adapter                              0.1.6
##### colorzero                                       2.0
##### gpiozero                                        2.0.1
##### lgpio                                           0.2.2.0
##### pip                                             25.0.1
##### pyftdi                                          0.56.0
##### pyserial                                        3.5
##### pyusb                                           1.3.1
##### RPi.GPIO                                        0.7.1
##### rpi_ws281x                                      5.0.0
##### setuptools                                      66.1.1
##### sysv_ipc                                        1.1.0
##### typing_extensions                               4.12.2

## GPIO Access Without SuperUser (sudo) designation
### Check access: ls -l /dev/gpio*
#### Known working output
#### crw-rw----+ 1 root gpio 254,  0 Mar 13 13:32 /dev/gpiochip0
#### crw-rw----+ 1 root gpio 254, 10 Mar 13 13:32 /dev/gpiochip10
#### crw-rw----+ 1 root gpio 254, 11 Mar 13 13:32 /dev/gpiochip11
#### crw-rw----+ 1 root gpio 254, 12 Mar 13 13:32 /dev/gpiochip12
#### crw-rw----+ 1 root gpio 254, 13 Mar 13 13:32 /dev/gpiochip13
#### lrwxrwxrwx  1 root root       9 Mar 13 13:32 /dev/gpiochip4 -> gpiochip0
#### crw-rw----  1 root gpio 234,  0 Mar 13 13:32 /dev/gpiomem0
#### crw-rw----  1 root gpio 238,  0 Mar 13 13:32 /dev/gpiomem1
#### crw-rw----  1 root gpio 237,  0 Mar 13 13:32 /dev/gpiomem2
#### crw-rw----  1 root gpio 236,  0 Mar 13 13:32 /dev/gpiomem3
#### crw-rw----  1 root gpio 235,  0 Mar 13 13:32 /dev/gpiomem4
### Correct these settings with these command:
#### sudo chown root:gpio /dev/gpiochip*
#### sudo chmod g+rw /dev/gpiochip*


