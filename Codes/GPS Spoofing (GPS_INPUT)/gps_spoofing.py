#!/usr/bin/env python3
import math, time
from pymavlink import mavutil

# Port 14552 dedie au script — 14550 reste libre pour QGroundControl
master = mavutil.mavlink_connection("udpin:0.0.0.0:14552")
print("[*] En attente heartbeat SITL sur port 14552...")
master.wait_heartbeat(timeout=30)
print(f"[+] Connecte — sysid={master.target_system}")

center_lat = 483579000   # lat x1e7  (IMT Atlantique Brest)
center_lon = -45714000   # lon x1e7
radius = 50000  # ~500 m
angle = 0

while True:
  lat = int(center_lat + radius * math.cos(math.radians(angle)))
  lon = int(center_lon + radius * math.sin(math.radians(angle)))
  t_us = int(time.time() * 1e6)
  master.mav.gps_input_send(
    t_us, 0, 0, 0, 0,
    3,          # fix_type 3D
    lat, lon,
    30.0,       # alt (m)
    1.0, 1.5,   # hdop vdop
    0.0, 0.0, 0.0,
    0.3, 0.5, 0.8,
    10
  )
  print(f"[>] angle={angle:3d} lat={lat/1e7:.5f} lon={lon/1e7:.5f}")
  angle = (angle + 2) % 360
  time.sleep(1.0)
