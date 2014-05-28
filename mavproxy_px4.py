#!/usr/bin/env python
'''
mavproxy_px4.py

Author: Charles Kiorpes
Date: May 28th, 2014

Provides additional commands for PX4FMU in MAVProxy
'''

from MAVProxy.modules.lib import mp_module

# Custom mode definitions from PX4 code base
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

# mavlink base_mode flags
MAV_MODE_FLAG_DECODE_POSITION_SAFETY      = 0b10000000
MAV_MODE_FLAG_DECODE_POSITION_MANUAL      = 0b01000000
MAV_MODE_FLAG_DECODE_POSITION_HIL         = 0b00100000
MAV_MODE_FLAG_DECODE_POSITION_STABILIZE   = 0b00010000
MAV_MODE_FLAG_DECODE_POSITION_GUIDED      = 0b00001000
MAV_MODE_FLAG_DECODE_POSITION_AUTO        = 0b00000100
MAV_MODE_FLAG_DECODE_POSITION_TEST        = 0b00000010
MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE = 0b00000001

# masks to prevent accidental arm/disarm of motors
DISARM_MASK                               = 0b01111111
ARMED_MASK                                = 0b10000000

class PX4Module(mp_module.MPModule):
    def __init__(self, mpstate):
        super(PX4Module, self).__init__(mpstate, "px4", "px4 mode changes", public = True)
        # set some default values (will be overwritten by information from the autopilot)
        self.custom_mode = { 'main_mode' : 1, 'sub_mode' : 0 }
        self.base_mode = 81
        self._mpstate = mpstate
        self.add_command('px4_arm', self.cmd_px4_arm, "arm the PX4", [])
        self.add_command('px4_disarm', self.cmd_px4_disarm, "disarm the px4", [])
        self.add_command('px4_manual', self.cmd_px4_manual, "set px4 flight mode to manual", [])
        self.add_command('px4_seatbelt', self.cmd_px4_seatbelt, "set px4 flight mode to seatbelt", [])
        self.add_command('px4_easy', self.cmd_px4_easy, "set px4 flight mode to easy", [])
        self.add_command('px4_ready', self.cmd_px4_auto_ready, "set px4 flight mode to auto - ready submode", [])
        self.add_command('px4_takeoff', self.cmd_px4_auto_takeoff, "set px4 flight mode to auto - takeoff", [])
        self.add_command('px4_loiter', self.cmd_px4_auto_loiter, "set px4 flight mode to auto - loiter submode", [])
        self.add_command('px4_mission', self.cmd_px4_auto_mission, "set px4 flight mode to auto - mission submode", [])
        self.add_command('px4_rtl', self.cmd_px4_auto_rtl, "set px4 flight mode to auto - RTL submode", [])
        self.add_command('px4_land', self.cmd_px4_auto_land, "set px4 flight mode to auto - land submode", [])

    def custom_mode_value(self, sub_mode, main_mode):
        '''build the 32-bit custom_mode value from the sub and main modes'''
        return ((sub_mode << 8) | main_mode) << 16

    def base_mode_value(self, new_custom_mode):
        '''build the 8-bit base_mode value'''
        if new_custom_mode == PX4_CUSTOM_MAIN_MODE_AUTO:
            return (self.base_mode & ARMED_MASK | MAV_MODE_FLAG_DECODE_POSITION_STABILIZE | MAV_MODE_FLAG_DECODE_POSITION_GUIDED | MAV_MODE_FLAG_DECODE_POSITION_AUTO | MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE) #_0011101
        else:
            return (self.base_mode & ARMED_MASK | MAV_MODE_FLAG_DECODE_POSITION_MANUAL | MAV_MODE_FLAG_DECODE_POSITION_STABILIZE | MAV_MODE_FLAG_DECODE_POSITION_CUSTOM_MODE) #_1010001
        
    def cmd_px4_arm(self, args):
        '''arm the PX4 (uses mavlink mode flags)'''
        print(self.custom_mode)                                                                              
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode | MAV_MODE_FLAG_DECODE_POSITION_SAFETY, self.custom_mode_value(self.custom_mode['sub_mode'], self.custom_mode['main_mode']))
        print("Arming the PX4")

    def cmd_px4_disarm(self, args):
        '''disarm the px4'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode & DISARM_MASK, self.custom_mode_value(self.custom_mode['sub_mode'], self.custom_mode['main_mode']))
        print("Disarming the PX4")

    def cmd_px4_manual(self, args):
        '''set px4 mode to MANUAL'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_MANUAL), self.custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_MANUAL))
        print("Switching to MANUAL mode.")

    def cmd_px4_seatbelt(self, args):
        '''set px4 mode to SEATBELT'''
        self_mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_SEATBELT), self.custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_SEATBELT))
        print("Switching to SEATBELT mode.")

    def cmd_px4_easy(self, args):
        '''set px4 mode to EASY'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_EASY), self.custom_mode_value(0, PX4_CUSTOM_MAIN_MODE_EASY))
        print("Switching to EASY mode.")

    def cmd_px4_auto_ready(self, args):
        '''set px4 mode to AUTO - READY'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_READY, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 in AUTO mode and READY")

    def cmd_px4_auto_takeoff(self, args):
        '''switch px4 to AUTO - TAKEOFF mode'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_TAKEOFF, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 launching in AUTO mode. -- TAKEOFF")

    def cmd_px4_auto_loiter(self, args):
        '''switch px4 to AUTO - LOITER mode'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_LOITER, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 switching to AUTO - LOITER mode.")

    def cmd_px4_auto_mission(self, args):
        '''switch px4 to AUTO - MISSION mode'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_MISSION, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 on MISSION in AUTO mode.")

    def cmd_px4_auto_rtl(self, args):
        '''switch px4 to AUTO - RTL mode'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_RTL, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 returning to launch in AUTO mode. -- RTL")

    def cmd_px4_auto_land(self, args):
        '''switch px4 to AUTO - LAND mode'''
        self._mpstate.master().mav.set_mode_send(self._mpstate.status.target_system, self.base_mode_value(PX4_CUSTOM_MAIN_MODE_AUTO), self.custom_mode_value(PX4_CUSTOM_SUB_MODE_AUTO_LAND, PX4_CUSTOM_MAIN_MODE_AUTO))
        print("PX4 LANDING in AUTO mode.")

    def mavlink_packet(m):
        '''handle an incoming mavlink packet'''
        if m.get_type() == 'HEARTBEAT':
            if self.custom_mode != m.custom_mode :
                self.custom_mode['sub_mode'] = m.custom_mode >> 24
                self.custom_mode['main_mode'] = (m.custom_mode >> 16) & 255
            if self.base_mode != m.base_mode:
                self.base_mode = m.base_mode

def init(mpstate):
    '''initialise module'''
    return PX4Module(mpstate)



