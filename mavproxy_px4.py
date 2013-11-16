#!/usr/bin/env python
'''Additional commands for PX4FMU and IO for MAVProxy'''

PX4_CUSTOM_MAIN_MODE_MANUAL   = 1
PX4_CUSTOM_MAIN_MODE_SEATBELT = 2
PX4_CUSTOM_MAIN_MODE_EASY     = 3
PX4_CUSTOM_MAIN_MODE_AUTO     = 4

PX4_CUSTOM_SUB_MODE_AUTO_READY   = 1
PX4_CUSTOM_SUB_MODE_AUTO_TAKEOFF = 2
PX4_CUSTOM_SUB_MODE_AUTO_LOITER  = 3
PX4_CUSTOM_SUB_MODE_AUTO_MISSION = 4
PX4_CUSTOM_SUB_MODE_AUTO_RTL     = 5
PX4_CUSTOM_SUB_MODE_AUTO_LAND    = 6

MAV_MODE_FLAG_DECODE_POSITION_SAFETY      = 0b10000000
MAV_MODE_FLAG_DECODE_POSITION_MANUAL      = 0b01000000
MAV_MODE_FLAG_DECODE_POSITION_HIL         = 0b00100000
MAV_MODE_FLAG_DECODE_POSITION_STABILIZE   = 0b00010000
MAV_MODE_FLAG_DECODE_POSITION_GUIDED      = 0b00001000
MAV_MODE_FLAG_DECODE_POSITION_AUTO        = 0b00000100
MAV_MODE_FLAG_DECODE_POSITION_TEST        = 0b00000010
MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE = 0b00000001

DISARM_MASK                               = 0b01111111
ARMED_MASK                                = 0b10000000

PX4_BASE_DISARMED = 0b01010001 #81
PX4_BASE_ARMED = 0b11010001 #209
PX4_AUTO       = 0b00011101 #29

PX4_CUSTOM_SEATBELT = 0b100000000000000000 #131072 -> on the wire, this is transmitted in the following order: 00000000 00000000 00000010
PX4_CUSTOM_MANUAL   = 0b10000000000000000 #65536
PX4_CUSTOM_AUTO     = 0b1000000000000000000 #262144
PX4_CUSTOM_AUTO     = 4  # 00000100 (custom_mode.main_mode)


mpstate = None
custom_mode = { 'main_mode' : 1, 'sub_mode' : 0 }
base_mode = 81

def cmd_px4_init_usb():
    '''start mavlink over USB'''
    global mpstate
    mpstate.mav_master[0].mav.file.write('\r')
    mpstate.mav_master[0].mav.file.write('\r')
    mpstate.mav_master[0].mav.file.write('\r')
    mpstate.mav_master[0].mav.file.write('sh /etc/init.d/rc.usb')

def name():
    '''return module name'''
    return "px4"

def description():
    '''return module description'''
    return "PX4 commands"

def custom_mode_value(sub_mode, main_mode):
    '''build the 32-bit custom_mode value from the sub and main modes'''
    return ((sub_mode << 8) | main_mode) << 16

def base_mode_value(new_custom_mode):
    '''build the 8-bit base_mode value'''
    global base_mode
    if new_custom_mode == PX4_CUSTOM_MAIN_MODE_AUTO:
        return (base_mode & ARMED_MASK | MAV_MODE_FLAG_DECODE_POSITION_STABILIZE | MAV_MODE_FLAG_DECODE_POSITION_GUIDED | MAV_MODE_FLAG_DECODE_POSITION_AUTO | MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE) #_0101101
    else:
        return (base_mode & ARMED_MASK | MAV_MODE_FLAG_DECODE_POSITION_MANUAL | MAV_MODE_FLAG_DECODE_POSITION_STABILIZE | MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE) #_1010001
        

def cmd_px4_arm(args):
    '''arm the PX4 (uses mavlink mode flags)'''
    global mpstate
    global custom_mode
    global base_mode
    #
    print(custom_mode)                                                                              
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode | MAV_MODE_FLAG_DECODE_POSITION_SAFETY, custom_mode_value(custom_mode['sub_mode'], custom_mode['main_mode']))
    print("Arming the PX4")

def cmd_px4_disarm(args):
    '''disarm the px4'''
    global mpstate
    global custom_mode
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode & DISARM_MASK, custom_mode_value(custom_mode['sub_mode'], custom_mode['main_mode']))
    print("Disarming the PX4")

def cmd_px4_manual(args):
    '''set px4 mode to MANUAL'''
    global mpstate
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_MANUAL), custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_MANUAL))
    print("Switching to MANUAL mode.")

def cmd_px4_seatbelt(args):
    '''set px4 mode to SEATBELT'''
    global mpstate
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_SEATBELT), custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_SEATBELT))
    print("Switching to SEATBELT mode.")

def cmd_px4_easy(args):
    '''set px4 mode to EASY'''
    global mpstate
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_EASY), custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_EASY))
    print("Switching to EASY mode.")

def cmd_px4_auto_ready(args):
    '''set px4 mode to AUTO - READY'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_READY, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 in AUTO mode and READY")

def cmd_px4_auto_takeoff(args):
    '''switch px4 to AUTO - TAKEOFF mode'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_TAKEOFF, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 launching in AUTO mode. -- TAKEOFF")

def cmd_px4_auto_loiter(args):
    '''switch px4 to AUTO - LOITER mode'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_LOITER, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 switching to AUTO - LOITER mode.")

def cmd_px4_auto_mission(args):
    '''switch px4 to AUTO - MISSION mode'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_MISSION, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 on MISSION in AUTO mode.")

def cmd_px4_auto_rtl(args):
    '''switch px4 to AUTO - RTL mode'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_RTL, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 returning to launch in AUTO mode. -- RTL")

def cmd_px4_auto_land(args):
    '''switch px4 to AUTO - LAND mode'''
    global mpstate
    global base_mode
    mpstate.master().mav.set_mode_send(mpstate.status.target_system, base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_LAND, PX4_CUSTOM_MAIN_MODE_AUTO))
    print("PX4 LANDING in AUTO mode.")

def init(_mpstate):
    '''initialise module'''
    global mpstate
    mpstate = _mpstate
    mpstate.command_map['px4_arm'] = (cmd_px4_arm, "arm the PX4")
    mpstate.command_map['px4_disarm'] = (cmd_px4_disarm, "disarm the px4")
    mpstate.command_map['px4_manual'] = (cmd_px4_manual, "set px4 flight mode to manual")
    mpstate.command_map['px4_seatbelt'] = (cmd_px4_seatbelt, "set px4 flight mode to seatbelt")
    mpstate.command_map['px4_easy'] = (cmd_px4_easy, "set px4 flight mode to easy")
    mpstate.command_map['px4_ready'] = (cmd_px4_auto_ready, "set px4 flight mode to auto - ready submode")
    mpstate.command_map['px4_takeoff'] = (cmd_px4_auto_takeoff, "set px4 flight mode to auto - takeoff")
    mpstate.command_map['px4_loiter'] = (cmd_px4_auto_loiter, "set px4 flight mode to auto - loiter submode")
    mpstate.command_map['px4_mission'] = (cmd_px4_auto_mission, "set px4 flight mode to auto - mission submode")
    mpstate.command_map['px4_rtl'] = (cmd_px4_auto_rtl, "set px4 flight mode to auto - RTL submode")
    mpstate.command_map['px4_land'] = (cmd_px4_auto_land, "set px4 flight mode to auto - land submode")
    # mpstate.command_map['px4_init_usb'] = (cmd_px4_init_usb, "start mavlink over the usb serial connection")
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
            custom_mode['sub_mode'] = m.custom_mode >> 24
            custom_mode['main_mode'] = (m.custom_mode >> 16) & 255
        if base_mode != m.base_mode:
            base_mode = m.base_mode


