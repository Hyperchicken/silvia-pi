import board, busio, digitalio, adafruit_max31855, sys

class TemperatureSensor:
  def __init__(self):
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    cs = digitalio.DigitalInOut(board.D8)
    self.sensor = adafruit_max31855.MAX31855(spi=spi, cs=cs)

  def get_temperature(self): 
    return self.sensor.temperature