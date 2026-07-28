#!/usr/bin/env python3
from pymavlink import mavutil
import time

master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
master.wait_heartbeat()
print(f"[+] Connecté — sys={master.target_system}")

master.mav.command_long_send(
  master.target_system, master.target_component,
  mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
  0, 0, 21196, 0, 0, 0, 0, 0)
print("[+] DISARM forcé en vol")
