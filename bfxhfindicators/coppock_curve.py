from bfxhfindicators.indicator import Indicator
from bfxhfindicators.wma import WMA
from bfxhfindicators.roc import ROC
from math import isfinite

class CoppockCurve(Indicator):
  def __init__(self, args = []):
    [ wmaLength, longROCLength, shortROCLength ] = args

    self._wma = WMA([wmaLength])
    self._shortROC = ROC([shortROCLength])
    self._longROC = ROC([longROCLength])

    super().__init__({
      'args': args,
      'id': 'coppockcurve',
      'name': 'Coppock Curve(%f, %f, %f)' % (wmaLength, longROCLength, shortROCLength),
      'seed_period': max([longROCLength + wmaLength, shortROCLength + wmaLength])
    })
  
  def reset(self):
    super().reset()
    self._wma.reset()
    self._shortROC.reset()
    self._longROC.reset()

  def update(self, v):
    self._shortROC.update(v)
    self._longROC.update(v)

    short = self._shortROC.v()
    long = self._longROC.v()

    if not isfinite(short) or not isfinite(long):
      return
    
    self._wma.update(short + long)
    super().update(self._wma.v())
    return self.v()

  def add(self, v):
    self._shortROC.add(v)
    self._longROC.add(v)

    short = self._shortROC.v()
    long = self._longROC.v()
    
    
    if not isfinite(short) or not isfinite(long) or short is None or long is None:
      return
    
    self._wma.add(short + long)
    super().add(self._wma.v())
    return self.v()
