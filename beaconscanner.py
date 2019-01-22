# -*- coding: utf-8 -*-
from beacontools import parse_packet
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
  telemetry_b_packet = b"\x02\x01\x04\x03\x03\x9a\xfe\x17\x16\x9a\xfe\x22\x47\xa0\x38\xd5"\
                     b"\xeb\x03\x26\x40\x01\xd8\x42\xed\x73\x49\x25\x66\xbc\x2e\x50"
  telemetry_b = parse_packet(telemetry_b_packet)
  telemetry_a_packet = b"\x02\x01\x04\x03\x03\x9a\xfe\x17\x16\x9a\xfe\x22\x47\xa0\x38\xd5"\
                     b"\xeb\x03\x26\x40\x00\x00\x01\x41\x44\x47\xfa\xff\xff\xff\xff"
  telemetry = parse_packet(telemetry_a_packet)
  end = time.time()
  uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
  usage = psutil.disk_usage("/")
  f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
  l = f.readline()
  ctemp = 1.0 * float(l)/1000

  row['cputemp1'] = round(ctemp,2)
  row['bt_addr'] = bt_addr
  row['rssi'] = rssi
  row['id'] = telemetry.identifier
  row['magnetic_fieldx'] =  telemetry_b.magnetic_field[0]
  row['magnetic_fieldy'] =  telemetry_b.magnetic_field[1]
  row['magnetic_fieldz'] =  telemetry_b.magnetic_field[2]
  row['temperature'] = telemetry_b.temperature
  row['battery'] =  telemetry_b.battery_level
  row['id'] = telemetry.identifier
  row['bt_addr'] = bt_addr
  row['rssi'] = rssi
  row['protocol_version'] =  telemetry.protocol_version
  row['accelerationx'] =   telemetry.acceleration[0]
  row['accelerationy'] =   telemetry.acceleration[1]
  row['accelerationz'] =   telemetry.acceleration[2]
  row['is_moving'] = telemetry.is_moving
  row['current_motion'] = telemetry.current_motion_state
  row['uptime'] =  telemetry_b.uptime
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
  fh = open("/opt/demo/logs/estimote.log", "a")
  fh.writelines('{0}\n'.format(json_string))
  fh.close

# scan for all Estimote telemetry packets from a specific beacon
scanner = BeaconScanner(callback,
    packet_filter=[EstimoteTelemetryFrameA, EstimoteTelemetryFrameB]
)
scanner.start()
time.sleep(30)
scanner.stop()
