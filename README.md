mavproxy_px4
============

This MAVProxy module adds support for some of the basic functions of the PX4FMU.

Installation:
=============

Place the mavproxy_px4.py file in your MAVProxy/modules/ directory.

Using the Plugin:
=================

For now, I have not found a way to get mavlink running over USB without first linking the PX4 with QGroundControl.
This should be sorted out within the next few days.

To use, run MAVProxy with:

    python mavproxy.py --master=<your_serial_port> --baud=57600 --quadcopter --dialect=pixhawk --load-module px4
  
This will provide some extra commands:

    px4_arm      -> arms the PX4
    px4_disarm   -> disarms the PX4
    px4_manual   -> sets the flight mode to 'MANUAL'
    px4_seatbelt -> sets the flight mode to 'SEATBELT'
    px4_auto     -> sets the flight mode to 'AUTO' (currently untested)

More functions will be available in later versions.

MAVProxy will not display the flight modes correctly, because the PX4 is using custom modes that are not
currently in the git master mavlink common or dialect definitions.

If you want to be able to see the current flight mode, you have to make a modification to a file in
the mavlink directory.

Edit mavlink/pymavlink/mavutil.py

Where you see: 


    mode_mapping_acm = {
        0 : 'STABILIZE',
        1 : 'ACRO',
        2 : 'ALT_HOLD',
        3 : 'AUTO',
        4 : 'GUIDED',
        5 : 'LOITER',
        6 : 'RTL',
        7 : 'CIRCLE',
        8 : 'POSITION',
        9 : 'LAND',
        10 : 'OF_LOITER',
        11 : 'APPROACH'
    }

add a few lines at the bottom of the map, so that it looks like:
    
    mode_mapping_acm = {
        0 : 'STABILIZE',
        1 : 'ACRO',
        2 : 'ALT_HOLD',
        3 : 'AUTO',
        4 : 'GUIDED',
        5 : 'LOITER',
        6 : 'RTL',
        7 : 'CIRCLE',
        8 : 'POSITION',
        9 : 'LAND',
        10 : 'OF_LOITER',
        11 : 'APPROACH',
        65536 : 'PX4_MANUAL',
        131072 : 'PX4_SEATBELT',
        262144 : 'PX4_AUTO'
    }
  
This modification will allow you to see the current flight mode.   
  

  
