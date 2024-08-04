#!/usr/bin/env python3
# Test Script for Wind Tunnel Testing

import rospy
import time, csv
import load_cell
from mavros_msgs.srv import CommandBool, CommandLong
from mavros_msgs.msg import Thrust, State, ESCTelemetry, VFR_HUD, RCIn, ESCTelemetryItem
from sensor_msgs.msg import BatteryState
from pymavlink import mavutil

# Command Long 
def motor_output_cmd(motor_command, set_pwm):
    motor_command( # Parameters based on MAVROS
        0,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO, # command
        0,    # confirmation
        8,    # Servo number
        set_pwm, # PWM
        0, 0, 0, 0, 0
    )

voltage = None
current = None
airspeed = None
groundspeed = None
esc_rmp = None
throttle = None

def arming_state_callback(data):
    if data.armed:
        return True
    else:
        return False

def battery_callback(data):
    global voltage, current
    voltage = data.voltage
    current = data.current

def esc_callback(data):
    global esc_rmp
    esc_rmp = data.esc_telemetry[8].rpm

def vfr_callback(data):
    global airspeed, groundspeed
    airspeed = data.airspeed
    groundspeed = data.groundspeed

def RC_callback(data):
    global throttle
    throttle = data.channels[2]

def main():
    rospy.init_node("wind_tunnel_test", anonymous = True)
    arming_state = rospy.Subscriber("/mavros/state", State, arming_state_callback)
    arming_proxy = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    rospy.Subscriber("/mavros/battery", BatteryState, battery_callback)    
    motor_command = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)
    rospy.Subscriber("/mavros/esc_telemetry", ESCTelemetry, esc_callback)    
    rospy.Subscriber("/mavros/vfr_hud", VFR_HUD, vfr_callback)    
    rospy.Subscriber("/mavros/rc/in", RCIn, RC_callback)    


    if arming_state == False:
            arming_proxy(True)

    max_motor = 2000   
    motor_output_cmd(motor_command, max_motor)   

    load_cell # sets up load cell

    # log data to a file
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        field = ['Time (s)', 'Thrust from load cell (kg)', 'Voltage (V)', 'Current (A)', 'Air Speed (m/s)', 'Ground Speed (m/s)', 'ESC RPM (1/min)', 'Throttle (PWM)']
        writer.writerow(field)
        
        start_time = time.time()
        while not rospy.is_shutdown():
            #print('{0:0.4f}' .format(time.time()-start_time), load_cell.take_thrust(), voltage, current, airspeed, groundspeed, esc_rmp, throttle)
            writer.writerow(['{0:0.4f}' .format(time.time()-start_time), load_cell.take_thrust(), voltage, current, airspeed, groundspeed, esc_rmp, throttle])
            time.sleep(0.1)        
        
        file.close()

if __name__ == '__main__':
    main()