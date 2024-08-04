NSF REU: Collaborative Human-Robot Interaction for Robots in the Field at University of Nevada, Reno

For information about the full research project: [Paper](url)

# Motor-Thrust-Test
The goal of the Motor Thrust Test is to determine the reliability of the motors chosen for a solar-powered UAV called the Gannet. Wind Tunnel and Cyclic Marine Testing will evaluate the performace of the motor-propeller combination that is reported to produce 0.8 kg of thrust at a speed of 14 m/s and cruise power of 110 W.

## Test Stand Design
Completed Solidworks CAD Assembly and BOM is uploaded

Manufacturing methods: horizontal bandsaw, mill, CNC mill (for Motor Mount)

Important Features:
* Motor Mount: Machined aluminum, cross mounting pattern to fit motors from 19 mm to 25 mm
* Single-Point Load Cell: withstand up to 10 kg of pressure
* Z-bar Configuration: accounts for the lip of the test tank, COG allows for the motor to fall back into the tank when disengaged
* Base Angle Brackets: bearings to allow the Z-bar to rotate, slots on top for hardstops
* Hardstops: two slots to press fit into Base Angle Brackets to contrain movement
* Pitot Tube: measures air speed and ground speed, not included in CAD

## Wind Tunnel Testing - Dynamic Thrust 
Dynamic thrust testing will conduct a Wind Tunnel Test using various motor and propeller combinations. The Test Stand will be strapped on top of the car while driving at the Gannet's cruise speed of 14 m/s. 

## Cyclic Marine Testing - Static Thrust
Static thrust of the motor will be evaluated through Cyclic Marine Testing that simulates a multi-day mission at sea to validate corrosion mitigation. The motor will run continuously for 24 hours while the Test Stand dunks the motor in and out of the test tank filled with salt water.

## Test Script
Python, ROS and MAVROS was used to automate testing and log data to a csv file.

Libraries used for setting up the Load Cell:
* [smbus2](https://pypi.org/project/smbus2/)
* [PyNAU7802](https://github.com/BrunoB81HK/PyNAU7802/tree/main)
