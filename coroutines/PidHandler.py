import PID as PID
import asyncio
import logging
from collections import deque
from time import time

class PidHandler:
  i=0
  pidhist = deque([0.]*10)
  avg_pid = 0.
  temphist = deque([0.]*5)
  avg_temp = 0.
  lasttime = time()
  lastcold = 0
  lastwarm = 0
  cold = True

  def __init__(self, log, temperature_sensor, pc, pw, ic, iw, dc, dw, set_point, sample_time):
    self.log = log
    self.temperature_sensor = temperature_sensor
    self.cpid = PID.PID(pc, ic, dc)
    self.cpid.SetPoint = set_point
    self.cpid.setSampleTime(sample_time * 5)
    self.wpid = PID.PID(pc, ic, dc)
    self.wpid.SetPoint = set_point
    self.wpid.setSampleTime(sample_time * 5)
    self.set_point = set_point
    self.sample_time = sample_time

  def set_set_point(self, set_point):
    import pickle

    self.cpid.SetPoint = set_point
    self.wpid.SetPoint = set_point
    self.set_point = set_point
    pickle.dump({"set_point": set_point}, open( "./setpoint.p", "wb" ))

  def update(self, avg_temp):
    if self.cold:
      self.cpid.update(avg_temp)
    else:
      self.wpid.update(avg_temp)

  def get_cur_pid(self):
    return self.cpid if self.cold else self.wpid

  def output(self):
    return self.cpid.output if self.cold else self.wpid.output

  async def pid_loop(self):
    while True:
      temp = self.temperature_sensor.get_temperature()

      self.temphist.popleft()
      self.temphist.append(temp)
      self.avg_temp = sum(self.temphist) / len(self.temphist)

      if self.avg_temp < 40 :
        self.lastcold = self.i

      if self.avg_temp > min(self.set_point, 80) :
        self.lastwarm = self.i

      # if it's cold and it's been more than 1.5 minutes since it was last cold
      if self.cold and (self.i - self.lastcold) * self.sample_time > 60 * 15 :
        self.cold = False

      # if it's warm and it's been more than 1.5 minutes since it was last warm
      if not self.cold and (self.i - self.lastwarm) * self.sample_time > 60 * 15 : 
        self.cold = True

      if self.i % 10 == 0 :
        self.update(self.avg_temp)
        self.pidout = self.output()
        self.pidhist.popleft()
        self.pidhist.append(self.pidout)
        self.avg_pid = sum(self.pidhist) / len(self.pidhist)

      sleeptime = self.lasttime + self.sample_time - time()
      if sleeptime < 0 :
        sleeptime = 0
      await asyncio.sleep(sleeptime)
      self.i += 1
      self.lasttime = time()

