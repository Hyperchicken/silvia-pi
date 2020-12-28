import asyncio

class HeatingElementController():
  def __init__(self, log, boiler, pid):
    self.log = log
    self.boiler = boiler
    self.pid = pid

  async def update_he_from_pid(self):
    while True:
      if self.pid.avg_pid >= 100 :
        self.boiler.heat_on()
        await asyncio.sleep(1)
      elif self.pid.avg_pid > 0 and self.pid.avg_pid < 100:
        self.boiler.heat_on()
        await asyncio.sleep(self.pid.avg_pid / 100.)
        self.boiler.heat_off()
        await asyncio.sleep(1 - self.pid.avg_pid / 100.)
      else:
        self.boiler.heat_off()
        await asyncio.sleep(1)
