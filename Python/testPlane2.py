from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import argparse
import socket
import re

# Define variables
CUSTOM_TRAPIS_ID = 999
UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 15000

''' -------------------------------------------------------------------
        Set up option parsing to get connection string
---------------------------------------------------------------------'''

parser = argparse.ArgumentParser(description="Commands vehicle using vehicle.simple_goto.")
parser.add_argument("--connect",
                    help="First vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect


''' -------------------------------------------------------------------
                        Set up UDP Listener
---------------------------------------------------------------------'''

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind((UDP_IP_ADDRESS, UDP_PORT_NO))


''' -------------------------------------------------------------------
                          Connect
---------------------------------------------------------------------'''

# Connect to the vehicle
vehicle = connect(connection_string, wait_ready=False)


''' ------------------------------------------------------------------
                            MAVLINK Message
--------------------------------------------------------------------'''
# Regular expression pattern
# Location: (lat)N (lon)W (alt)
regex = r"[A-Za-z]+[:]\s([0-9]+[\.][0-9]+)[N]\s([0-9]+[\.][0-9]+)[W]\s([0-9]+[\.][0-9]+)"

while True:
    # Listen for data from UDP
    data, addr = serverSocket.recvfrom(1024)
    messageReceived = data.decode("hex")
    match = re.search(regex, messageReceived)
    lat = float(match.group(1))
    lon = float(match.group(2))
    alt = float(match.group(3))

    # Packing Mavlink message
    msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    CUSTOM_TRAPIS_ID, #command
    0, #confirmation
    lat,
    lon,
    alt,
    0,
    0, 0, 0)

    # Send command to vehicle
    vehicle.send_mavlink(msg)
    print("Custom Trapis Mavlink sent")


''' ------------------------------------------------------------------
                           CLOSE VEHICLE
--------------------------------------------------------------------'''

#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
print("Completed")
