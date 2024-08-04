#!/usr/bin/env python3
# Test Script for Cyclic Testing
import rospy
import time, csv
import load_cell
from mavros_msgs.srv import CommandBool, CommandLong
from mavros_msgs.msg import State
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

thrust_gannet = None
voltage = None
current = None

def arming_state_callback(data):
    if data.armed:
        return True
    else:
        return False

def battery_callback(data):
    global voltage, current
    voltage = data.voltage
    current = data.current

def main():
    rospy.init_node("open_loop_test", anonymous = True)
    arming_state = rospy.Subscriber("/mavros/state", State, arming_state_callback)
    arming_proxy = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
    battery_info = rospy.Subscriber("/mavros/battery", BatteryState, battery_callback)    
    motor_command = rospy.ServiceProxy('/mavros/cmd/command', CommandLong)

    load_cell # sets up load cell

    # log data to a file
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        field = ['Time', 'Thrust from Gannet', 'Thrust from load cell', 'Voltage', 'Current']
        writer.writerow(field)

        one_day = 24*60*60
        current_time = time.time()

        while (not rospy.is_shutdown()) and (current_time <= one_day):
            if arming_state == False:
                arming_proxy(True)

            # PWM is set between 1000-2000
            max_motor = 2000
            motor_output = 1000 # starting
            increment = 0.05*max_motor
            decrement = 0.1*max_motor
            motor_output_cmd(motor_command, max_motor)  

            start = time.time()
            while (not rospy.is_shutdown()) and (time.time() - start) <= 60:
                if motor_output < max_motor:
                    motor_output += increment
                    motor_output_cmd(motor_command, motor_output) 
                    ramp_time = time.time()-start
                else:
                    #print('{0:0.4f}' .format(time.time()-start), loadcell.take_thrust(), voltage, current, motor_output, ramp_time)
                    writer.writerow(['{0:0.4f}' .format(time.time()-start), load_cell.take_thrust(), voltage, current, motor_output, ramp_time])
                time.sleep(0.2)

            end = time.time()
            while (not rospy.is_shutdown()) and (time.time() - end) <= 60:
                motor_output -= decrement
                motor_output_cmd(motor_command, motor_output) 
                if motor_output == 0:
                    break 
                time.sleep(0.2)
            
            time.sleep(5)
            arming_proxy(False)
            time.sleep(60)
            
            current_time = time.time()
        
        file.close()

if __name__ == '__main__':
    main()