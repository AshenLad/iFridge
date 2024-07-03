import sys

import Adafruit_DHT

def cond():
    sensor = Adafruit_DHT.DHT11
    pin = 4

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        return humidity, temperature
    else:
        print('Failed to get reading. Try again!')
    sys.exit(1)

if __name__ == '__main__':
    humidity, temperature = cond()
    print(temperature, humidity)