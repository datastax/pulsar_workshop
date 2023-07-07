from pulsar.schema import *


class IoTSensorDataRaw(Record):
    ts = String()
    device = String()
    co = Float()
    humidity = Float()
    light = Boolean()
    lpg = Float()
    motion = Boolean()
    smoke = Float()
    temp = Float()

    def __int__(self):
        self.ts
