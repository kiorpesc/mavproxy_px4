#!/usr/bin/env python
'''Additional commands for PX4FMU and IO for MAVProxy'''

'''
128	MAV_MODE_FLAG_DECODE_POSITION_SAFETY	First bit: 10000000

64	MAV_MODE_FLAG_DECODE_POSITION_MANUAL	Second bit: 01000000

32	MAV_MODE_FLAG_DECODE_POSITION_HIL	Third bit: 00100000

16	MAV_MODE_FLAG_DECODE_POSITION_STABILIZE	Fourth bit: 00010000

8	MAV_MODE_FLAG_DECODE_POSITION_GUIDED	Fifth bit: 00001000

4	MAV_MODE_FLAG_DECODE_POSITION_AUTO	Sixt bit: 00000100

2	MAV_MODE_FLAG_DECODE_POSITION_TEST	Seventh bit: 00000010

1	MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE	Eighth bit: 00000001
'''

MAV_MODE_FLAG_DECODE_POSITION_SAFETY      = 0b10000000
MAV_MODE_FLAG_DECODE_POSITION_MANUAL      = 0b01000000
MAV_MODE_FLAG_DECODE_POSITION_HIL         = 0b00100000
MAV_MODE_FLAG_DECODE_POSITION_STABILIZE   = 0b00010000
MAV_MODE_FLAG_DECODE_POSITION_GUIDED      = 0b00001000
MAV_MODE_FLAG_DECODE_POSITION_AUTO        = 0b00000100
MAV_MODE_FLAG_DECODE_POSITION_TEST        = 0b00000010
MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE = 0b00000001

DISARM_MASK                               = 0b01111111
ARMED_MASK                                  = 0b10000000

PX4_BASE_DISARMED = 0b01010001 #81
PX4_BASE_ARMED = 0b11010001 #209
PX4_AUTO       = 0b00011101 #29
PX4_CUSTOM_SEATBELT = 0b100000000000000000 #131072
PX4_CUSTOM_MANUAL   = 0b10000000000000000 #65536
PX4_CUSTOM_AUTO     = 0b1000000000000000000 #262144

mpstate = None
custom_mode = 65536
base_mode = 81

def name():
    '''return module name'''
    return "px4"

def description():
    '''return module description'''
    return "PX4 commands"

def cmd_px4_arm(args):
    '''arm the PX4 (uses mavlink mode flags)'''
    global mpstate
    global custom_mode
    global base_mode
    #
    print(custom_mode)                                                                              
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode | MAV_MODE_FLAG_DECODE_POSITION_SAFETY, custom_mode + 1)
    print("Arming the PX4")

def cmd_px4_disarm(args):
    '''disarm the px4'''
    global mpstate
    global custom_mode
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode & DISARM_MASK, custom_mode + 1)
    print("Disarming the PX4")

def cmd_px4_manual(args):
    '''set px4 mode to MANUAL'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode, PX4_CUSTOM_MANUAL)
    print("Switching to MANUAL mode.")

def cmd_px4_seatbelt(args):
    '''set px4 mode to SEATBELT'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode, PX4_CUSTOM_SEATBELT)
    print("Switching to SEATBELT mode.")

def cmd_px4_auto(args):
    '''set px4 mode to AUTO'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode & ARMED_MASK | MAV_MODE_FLAG_DECODE_POSITION_STABILIZE | MAV_MODE_FLAG_DECODE_POSITION_GUIDED |
                                                                       MAV_MODE_FLAG_DECODE_POSITION_AUTO | MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE, PX4_CUSTOM_AUTO)
    print("Switching to AUTO mode.")

def init(_mpstate):
    '''initialise module'''
    global mpstate
    mpstate = _mpstate
    mpstate.command_map['px4_arm'] = (cmd_px4_arm, "arm the PX4")
    mpstate.command_map['px4_disarm'] = (cmd_px4_disarm, "disarm the px4")
    mpstate.command_map['px4_manual'] = (cmd_px4_manual, "set px4 flight mode to manual")
    mpstate.command_map['px4_seatbelt'] = (cmd_px4_seatbelt, "set px4 flight mode to seatbelt")
    mpstate.command_map['px4_auto'] = (cmd_px4_auto, "set px4 flight mode to auto")
    print("PX4 module initialised")

def unload():
    if 'px4_arm,' in mpstate.command_map:
        mpstate.command_map.pop('px4_arm')
    if 'px4_disarm' in mpstate.command_map:
        mpstate.command_map.pop('px4_disarm')

def mavlink_packet(m):
    '''handle an incoming mavlink packet'''
    global custom_mode
    global base_mode
    if m.get_type() == 'HEARTBEAT':
        if custom_mode != m.custom_mode :
            custom_mode = m.custom_mode
        if base_mode != m.base_mode:
            base_mode = m.base_mode


