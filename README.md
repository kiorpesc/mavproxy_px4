mavproxy_px4
============

This MAVProxy module adds support for some of the basic functions of the PX4FMU.

Installation:
-------------

Place the mavproxy_px4.py file in your MAVProxy/modules/ directory.
If you have installed MAVProxy as a Python module (i.e. via pip), the modules directory will be in your python dist-packages directory.
For example, on a Ubuntu system, it should be located at:

    /usr/local/lib/python2.7/dist-packages/MAVProxy/modules/

Using the Plugin:
-----------------

### 1) Using mavlink over the built-in USB:

   NOTE: The PX4 startup may have changed since these instructions were written, as firmware development is EXTREMELY active.

   If you are using the USB serial port, you will need to start mavlink over USB.
   This can be done by starting MAVProxy in setup mode, which give access to the nsh shell.
   First:

    mavproxy.py --master=<USB_serial_port> --baud=57600 --quadcopter --dialect=pixhawk --setup

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

### 2) Using mavlink over another serial connection (assumes that your startup scripts already start mavlink):

   If you are already set up with mavlink over a different output (one of the many UARTs on the PX4),
   you can run MAVProxy with:

    mavproxy.py --master=<your_serial_port> --baud=57600 --quadcopter --dialect=pixhawk --load-module px4


Commands:
---------

After either of these methods, you will now have some extra commands:

    px4_arm      -> arms the PX4
    px4_disarm   -> disarms the PX4
    px4_manual   -> sets the flight mode to 'MANUAL'
    px4_seatbelt -> sets the flight mode to 'SEATBELT'
    px4_easy     -> sets the flight mode to 'EASY'
    px4_ready    -> sets the flight mode to 'AUTO', submode 'READY'
    px4_takeoff  -> tells PX4 to take off in AUTO mode
    px4_loiter   -> tells PX4 to loiter in AUTO mode (untested)
    px4_mission  -> tells PX4 to fly mission in AUTO mode (untested)
    px4_rtl      -> sends return to launch command (untested)
    px4_land     -> tells PX4 to land in AUTO mode (untested)

MAVProxy may not display the flight modes correctly, because the PX4 is using custom modes.  


  
