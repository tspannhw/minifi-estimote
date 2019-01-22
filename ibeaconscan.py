# -*- coding: utf-8 -*-
from beacontools import parse_packet
from beacontools import IBeaconFilter
from beacontools import BeaconScanner, EstimoteTelemetryFrameA, EstimoteTelemetryFrameB, EstimoteFilter
import os.path
import re
import sys
import tarfile
import os
import datetime
import math
import random, string
import base64
import json
import time
from time import sleep
from time import gmtime, strftime
import sys
import datetime
import subprocess
import os
import base64
import uuid
import traceback
import socket
import psutil
###

# yyyy-mm-dd hh:mm:ss
currenttime= strftime("%Y-%m-%d %H:%M:%S",gmtime())

host = os.uname()[1]

def randomword(length):
  return ''.join(random.choice(string.lowercase) for i in range(length))

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

def getCPUtemperature():
    # Raspberry Pi Only
    #res = os.popen('vcgencmd measure_temp').readline()
    #return(res.replace("temp=","").replace("'C\n",""))
    res = os.popen('sensors -f').readline()
    return (res)

# - start timing
starttime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
start = time.time()
external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

def callback(bt_addr, rssi, packet, additional_info):
  row = { }
  ipaddress = IP_address()

  # iBeacon Advertisement
  ibeacon_packet = b"\x02\x01\x06\x1a\xff\x4c\x00\x02\x15\x41\x41\x41\x41\x41\x41\x41\x41\x41" \
                 b"\x41\x41\x41\x41\x41\x41\x41\x00\x01\x00\x01\xf8"
  adv = parse_packet(ibeacon_packet)

  end = time.time()
  uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
  usage = psutil.disk_usage("/")
  f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
  l = f.readline()
  ctemp = 1.0 * float(l)/1000

  row['cputemp1'] = round(ctemp,2)
  row['iuuid'] = adv.uuid
  row['major'] = adv.major
  row['minor'] = adv.minor
  row['tx_power'] = adv.tx_power
  row['bt_addr'] = bt_addr
  row['rssi'] = rssi
  row['systemtime'] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
  row['starttime'] = starttime
  row['diskusage'] = "{:.1f}".format(float(usage.free) / 1024 / 1024)
  row['memory'] = psutil.virtual_memory().percent
  row['uuid'] = str(uuid2)
  row['host'] = os.uname()[1]
  row['cputemp'] = psutil.sensors_temperatures()['radeon'][0][1]
  row['ipaddress'] = ipaddress
  row['end'] = '{0}'.format( str(end ))
  row['te'] = '{0}'.format(str(end-start))
  json_string = json.dumps(row)
  print(json_string)
  fh = open("/opt/demo/logs/ibeacon.log", "a")
  fh.writelines('{0}\n'.format(json_string))
  fh.close

#     packet_filter=[EstimoteTelemetryFrameA, EstimoteTelemetryFrameB]
# scan for all Estimote telemetry packets from a specific beacon
scanner = BeaconScanner(callback)
scanner.start()
time.sleep(30)
scanner.stop()
