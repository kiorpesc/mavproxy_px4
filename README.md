mavproxy_px4
============

This MAVProxy module adds support for some of the basic functions of the PX4FMU.

Installation:
=============

Place the mavproxy_px4.py file in your MAVProxy/modules/ directory.

Using the Plugin:
=================

1) Using mavlink over the built-in USB:

   If you are using the USB serial port, you will need to start mavlink over USB.
   This can be done by starting MAVProxy in setup mode, which give access to the nsh shell.
   First:

    python mavproxy.py --master=<USB_serial_port> --baud=57600 --quadcopter --dialect=pixhawk --setup

   Hitting return will show the nsh prompt.
   Once you have the prompt, simply type:

    sh /etc/init.d/rc.usb

   to start mavlink on the usb serial connection.

   You should see some garbled characters in the terminal - this is fine.
   Just type '.' (without the quotes) and hit return.  This will exit setup mode.
   MAVProxy should now recognize that there is an autopilot present, and allow you to enter commands.

   Once you are out of setup mode, type:

    load module px4

   to initialize the module.

2) Using mavlink over another serial connection (assumes that your startup scripts already start mavlink):

   If you are already set up with mavlink over a different output (one of the many UARTs on the PX4),
   you can run MAVProxy with:

    python mavproxy.py --master=<your_serial_port> --baud=57600 --quadcopter --dialect=pixhawk --load-module px4


After either of these methods, you will now have some extra commands:

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
  

  
