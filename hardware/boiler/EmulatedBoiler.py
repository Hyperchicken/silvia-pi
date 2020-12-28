
class EmulatedBoiler:
  last_mode = False
  def __init__(self, control_pin):
    self.control_pin = control_pin

  def __del__(self):
    self.cleanup()

  def heat_on(self):
    if self.last_mode == False:
      pass
    self.last_mode = True

  def heat_off(self):
    if self.last_mode == True:
      pass
    self.last_mode = False

  def force_heat_off(self):
    print("Heating element forced off")
    self.last_mode = False

  def cleanup(self):
    print("Cleaning up GPIO boiler " + str(self.control_pin))