class EmulatedTemperatureSensor:
  mult = 0
  class Sensor:
    temperature = 25

  def __init__(self, boiler):
    self.sensor = self.Sensor()
    self.boiler = boiler

  def get_temperature(self):
    self.mult += 0.01 if self.boiler.last_mode else -0.01
    if self.mult < -1:
      self.mult = -1
    if self.mult > 1:
      self.mult = 1
    self.sensor.temperature += 0.05 * self.mult
    return self.sensor.temperature