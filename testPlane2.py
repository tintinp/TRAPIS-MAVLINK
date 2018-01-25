from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time


# Set up option parsing to get connection string
import argparse

CUSTOM_TRAPIS_ID = 999

parser = argparse.ArgumentParser(description="Commands vehicle using vehicle.simple_goto.")
parser.add_argument("--connect",
                    help="First vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect


''' -------------------------------------------------------------------
                          Connect
---------------------------------------------------------------------'''

# Connect to the Vehicle (in this case a simulator running the same computer)
#vehicle = connect(connection_string, wait_ready=True)
vehicle = connect(connection_string, wait_ready=False)

@vehicle.on_message('CUSTOM_TRAPIS')
def listener(self, name, message):
    print(message)


''' ------------------------------------------------------------------
                            MAVLINK Message
--------------------------------------------------------------------'''
#mavutil.mavlink.MAV_CMD_DO_SET_ROI
#msg = vehicle.message_factory.custom_trapis_encode(123,321,99)
msg = vehicle.message_factory.command_long_encode(
    0, 0,    # target system, target component
    CUSTOM_TRAPIS_ID, #command
    0, #confirmation
    123,    
    123,
    1,
    0,
    0, 0, 0)

# send command to vehicle
vehicle.send_mavlink(msg)
print("Custom Trapis Mavlink sent")
time.sleep(5)


''' ------------------------------------------------------------------
                           CLOSE VEHICLE
--------------------------------------------------------------------'''

#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
print("Completed")
