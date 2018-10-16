#!/bin/python
import sys
import struct
import json
import time
p = None
def connectPeripheral():
  from bluepy.btle import Peripheral
  global p
  if p is None:
    for _ in range(10):
      try:
        p = Peripheral("a0:14:3d:cd:c4:61")
        break
      except Exception as e:
        print e
        time.sleep(1)
        pass
  if p is None:
    raise
  return p


LiveServiceUUID = "39e1FA00-84a8-11e2-afba-0002a5d5c51b"

SUNLIGHT_UUID                   = "39e1fa01-84a8-11e2-afba-0002a5d5c51b"
SOIL_EC_UUID                    = "39e1fa02-84a8-11e2-afba-0002a5d5c51b"
SOIL_TEMPERATURE_UUID           = "39e1fa03-84a8-11e2-afba-0002a5d5c51b"
AIR_TEMPERATURE_UUID            = "39e1fa04-84a8-11e2-afba-0002a5d5c51b"
SOIL_MOISTURE_UUID              = "39e1fa05-84a8-11e2-afba-0002a5d5c51b"

LED_UUID                        = "39e1fa07-84a8-11e2-afba-0002a5d5c51b"

CALIBRATED_SOIL_MOISTURE_UUID   = "39e1fa09-84a8-11e2-afba-0002a5d5c51b"
CALIBRATED_AIR_TEMPERATURE_UUID = "39e1fa0a-84a8-11e2-afba-0002a5d5c51b"
CALIBRATED_DLI_UUID             = "39e1fa0b-84a8-11e2-afba-0002a5d5c51b"
CALIBRATED_EA_UUID              = "39e1fa0c-84a8-11e2-afba-0002a5d5c51b"
CALIBRATED_ECB_UUID             = "39e1fa0d-84a8-11e2-afba-0002a5d5c51b"
CALIBRATED_EC_POROUS_UUID       = "39e1fa0e-84a8-11e2-afba-0002a5d5c51b"

ClockServiceUUID = "39e1FD00-84a8-11e2-afba-0002a5d5c51b"
CURRENT_TIME_UUID = "39e1FD01-84a8-11e2-afba-0002a5d5c51b"

WateringServiceUUID = "39e1f900-84a8-11e2-afba-0002a5d5c51b"
WAT_CMD_UUID = "39e1f906-84a8-11e2-afba-0002a5d5c51b"
WAT_LVL_UUID = "39e1f907-84a8-11e2-afba-0002a5d5c51b"


READ_ALL = [
  "CURRENT_TIME",
  "SUNLIGHT",
  "SOIL_EC",
  "SOIL_TEMPERATURE",
  "AIR_TEMPERATURE",
  "SOIL_MOISTURE",
  "CALIBRATED_SOIL_MOISTURE",
  "CALIBRATED_AIR_TEMPERATURE",
  "CALIBRATED_DLI",
  "WAT_LVL",
  #"CALIBRATED_EA",
  #"CALIBRATED_ECB",
  #"CALIBRATED_EC_POROUS",
]


cache_file_path = "/var/www/html/plugins/script/core/ressources/flower_power_cache.json"

try:
  cached_values = json.load(open(cache_file_path, "r+"))
except Exception as e:
  print "Warning during load", e
  cached_values = {}

def getValF32(ServiceUUID,UUID):
  characterisitics = connectPeripheral().getServiceByUUID(ServiceUUID).getCharacteristics(UUID)
  readVal = characterisitics[0].read()
  return float(struct.unpack("f", readVal)[0])

def getVal(ServiceUUID,UUID):
  characterisitics = connectPeripheral().getServiceByUUID(ServiceUUID).getCharacteristics(UUID)
  readVal = characterisitics[0].read()
  return float(struct.unpack("<B" if len(readVal) == 1 else "<H" if len(readVal) == 2 else "<I", readVal)[0])

def convertSunlight(rawValue):
    sunlight = 0.08640000000000001 * (192773.17000000001 * pow(rawValue, -1.0606619)) if (rawValue > 0.1) else 0.0
    return sunlight

def convertWaterLevel(rawValue):
    # TODO
    return rawValue
  
def convertSoilElectricalConductivity(rawValue):
    # TODO: convert raw (0 - 1771) to 0 to 10 (mS/cm)
    soilElectricalConductivity = rawValue
    return soilElectricalConductivity

def convertTemperature(rawValue):
    temperature = 0.00000003044 * pow(rawValue, 3.0) - 0.00008038 * pow(rawValue, 2.0) + rawValue * 0.1149 - 30.449999999999999
    return min(max(-10.0,temperature),55.0)

def convertSoilMoisture(rawValue):
    soilMoisture = 11.4293 + (0.0000000010698 * pow(rawValue, 4.0) - 0.00000152538 * pow(rawValue, 3.0) +  0.000866976 * pow(rawValue, 2.0) - 0.169422 * rawValue)
    soilMoisture = 100.0 * (0.0000045 * pow(soilMoisture, 3.0) - 0.00055 * pow(soilMoisture, 2.0) + 0.0292 * soilMoisture - 0.053)
    return min(max(0.0,soilMoisture),100.0)

def getVals(args):
  cache_dict = {}
  for arg in args:
    val = None
    if arg == "AIR_TEMPERATURE":
      raw = getVal(LiveServiceUUID, AIR_TEMPERATURE_UUID)
      val = convertTemperature(raw)
    elif arg == "SOIL_TEMPERATURE":
      raw = getVal(LiveServiceUUID, SOIL_TEMPERATURE_UUID)
      val = convertTemperature(raw)
    elif arg == "SOIL_EC":
      raw = getVal(LiveServiceUUID, SOIL_EC_UUID)
      val = convertSoilElectricalConductivity(raw)
    elif arg == "SOIL_MOISTURE":
      raw = getVal(LiveServiceUUID, SOIL_MOISTURE_UUID)
      val = convertSoilMoisture(raw)
    elif arg == "SUNLIGHT":
      raw = getVal(LiveServiceUUID, SUNLIGHT_UUID)
      val = convertSunlight(raw)
    elif arg == "CALIBRATED_DLI":
      val = getValF32(LiveServiceUUID, CALIBRATED_DLI_UUID)
    elif arg == "CALIBRATED_SOIL_MOISTURE":
      val = getValF32(LiveServiceUUID, CALIBRATED_SOIL_MOISTURE_UUID)
    elif arg == "CALIBRATED_AIR_TEMPERATURE":
      val = getValF32(LiveServiceUUID, CALIBRATED_AIR_TEMPERATURE_UUID)
    elif arg == "CALIBRATED_EA":
      val = getValF32(LiveServiceUUID, CALIBRATED_EA_UUID)
    elif arg == "CALIBRATED_ECB":
      val = getValF32(LiveServiceUUID, CALIBRATED_ECB_UUID)
    elif arg == "CALIBRATED_EC_POROUS":
      val = getValF32(LiveServiceUUID, CALIBRATED_EC_POROUS_UUID)
    elif arg == "WAT_LVL":
      raw = getVal(WateringServiceUUID, WAT_LVL_UUID)
      val = convertWaterLevel(raw)
    if val: cache_dict[arg] = val
  #print cache_dict
  return cache_dict

force_read = False
show = False
val = None
for arg in sys.argv[1:]:
  args = READ_ALL if arg == "ALL" else [arg]
  for arg in args:
    val = None
    if arg == "LED":
      connectPeripheral().getServiceByUUID(LiveServiceUUID).getCharacteristics(LED_UUID)[0].write("\x01")
    elif arg == "WATER":
      connectPeripheral().getServiceByUUID(WateringServiceUUID).getCharacteristics(WAT_CMD_UUID)[0].write("\x0A\x00")
    elif arg == "CACHE":
      json.dump(getVals(READ_ALL), open(cache_file_path, "w+"))
      val = cache_file_path
    elif arg == "FORCE":
      force_read = True
    elif arg == "SHOW":
      show = True
    elif arg == "CURRENT_TIME":
      val = getVal(ClockServiceUUID, CURRENT_TIME_UUID)
    else:
      if force_read or arg not in cached_values: val = getVals([arg])[arg]
      else: val = cached_values[arg]
    if show: print arg, val

print val

if p is not None: p.disconnect()
