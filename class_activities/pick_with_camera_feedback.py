#!/usr/bin/env python3
# Software License Agreement (BSD License)
#
# Copyright (c) 2024, UFACTORY, Inc.
# All rights reserved.
#
# Author: Vinman <vinman.wen@ufactory.cc> <vinman.cub@gmail.com>

"""
# Notice
#   1. Changes to this file on Studio will not be preserved
#   2. The next conversion will overwrite the file with the same name
"""
import sys
import math
import time
import datetime
import random
import traceback
import threading
import socket


"""
# xArm-Python-SDK: https://github.com/xArm-Developer/xArm-Python-SDK
# git clone git@github.com:xArm-Developer/xArm-Python-SDK.git
# cd xArm-Python-SDK
# python setup.py install
"""

HOST = "192.168.1.125"  # The server's hostname or IP address
PORT = 20000  # The port used by the server
x_mm = 0
y_mm = 0
r = 0

try:
	from xarm.tools import utils
except:
	pass
from xarm import version
from xarm.wrapper import XArmAPI

def pprint(*args, **kwargs):
	try:
    	stack_tuple = traceback.extract_stack(limit=2)[0]
    	print('[{}][{}] {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), stack_tuple[1], ' '.join(map(str, args))))
	except:
    	print(*args, **kwargs)

pprint('xArm-Python-SDK Version:{}'.format(version.__version__))

arm = XArmAPI('192.168.1.201')
arm.clean_warn()
arm.clean_error()
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)
time.sleep(1)

variables = {}
params = {'speed': 100, 'acc': 2000, 'angle_speed': 20, 'angle_acc': 500, 'events': {}, 'variables': variables, 'callback_in_thread': True, 'quit': False}


# Register error/warn changed callback
def error_warn_change_callback(data):
	if data and data['error_code'] != 0:
    	params['quit'] = True
    	pprint('err={}, quit'.format(data['error_code']))
    	arm.release_error_warn_changed_callback(error_warn_change_callback)
arm.register_error_warn_changed_callback(error_warn_change_callback)


# Register state changed callback
def state_changed_callback(data):
	if data and data['state'] == 4:
    	if arm.version_number[0] > 1 or (arm.version_number[0] == 1 and arm.version_number[1] > 1):
        	params['quit'] = True
        	pprint('state=4, quit')
        	arm.release_state_changed_callback(state_changed_callback)
arm.register_state_changed_callback(state_changed_callback)


# Register counter value changed callback
if hasattr(arm, 'register_count_changed_callback'):
	def count_changed_callback(data):
    	if not params['quit']:
        	pprint('counter val: {}'.format(data['count']))
	arm.register_count_changed_callback(count_changed_callback)


# Register connect changed callback
def connect_changed_callback(data):
	if data and not data['connected']:
    	params['quit'] = True
    	pprint('disconnect, connected={}, reported={}, quit'.format(data['connected'], data['reported']))
    	arm.release_connect_changed_callback(error_warn_change_callback)
arm.register_connect_changed_callback(connect_changed_callback)



# Define GPIO callback handle thread
class EventGPIOThread(threading.Thread):
	def __init__(self, *args, **kwargs):
    	threading.Thread.__init__(self, *args, **kwargs)
    	self.daemon = True
    	self.alive = False
    	self.is_init_tgpio_digital = False
    	self.is_init_tgpio_analog = False
    	self.is_init_cgpio_state = False
    	self.listen_tgpio_digital = False
    	self.listen_tgpio_analog = False
    	self.listen_cgpio_state = False
    	self.values = {'tgpio': {'digital': [0] * 2, 'analog': [0] * 2, 'digital_o': [0] * 2, 'analog_o': [0] * 2},'cgpio': {'digital': [1] * 16, 'analog': [0] * 2, 'digital_o': [1] * 16, 'analog_o': [0] * 2}}
    	self.tgpio_digital_callbacks = []
    	self.tgpio_analog_callbacks = []
    	self.cgpio_callbacks = []

	def cgpio_digitals_is_matchs_bin(self, bin_val):
    	digitals_bin = ''.join(map(str, self.values['cgpio']['digital']))
    	length = min(len(digitals_bin), len(bin_val))
    	bin_val_ = bin_val[::-1]
    	for i in range(length):
        	if bin_val_[i] != digitals_bin[i]:
            	return False
    	return True

	def run(self):
    	self.alive = True
    	while arm.connected and arm.error_code == 0 and not params['quit']:
        	if self.listen_tgpio_digital or len(self.tgpio_digital_callbacks) > 0:
            	_, values = arm.get_tgpio_digital()
            	if _ == 0:
                	if self.is_init_tgpio_digital:
                    	for item in self.tgpio_digital_callbacks:
                        	for io in range(2):
                            	if item['io'] == io and eval('{} {} {}'.format(values[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['tgpio']['digital'][io], item['op'], item['trigger'])):
                                	item['callback']()
                	self.values['tgpio']['digital'] = values
                	self.is_init_tgpio_digital = True
        	if self.listen_tgpio_analog or len(self.tgpio_analog_callbacks) > 0:
            	_, values = arm.get_tgpio_analog()
            	if _ == 0:
                	if self.is_init_tgpio_analog:
                    	for item in self.tgpio_analog_callbacks:
                        	for io in range(2):
                            	if item['io'] == io and eval('{} {} {}'.format(values[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['tgpio']['analog'][io], item['op'], item['trigger'])):
                                	item['callback']()
                	self.values['tgpio']['analog'] = values
                	self.is_init_tgpio_analog = True
        	if self.listen_cgpio_state or len(self.cgpio_callbacks) > 0:
            	_, values = arm.get_cgpio_state()
            	if _ == 0:
                	digitals = [values[3] >> i & 0x0001 if values[10][i] in [0, 255] else 1 for i in range(len(values[10]))]
                	digitals_o = [values[5] >> i & 0x0001 for i in range(len(values[11]))]
                	analogs = [values[6], values[7]]
                	analogs_o = [values[8], values[9]]
                	if self.is_init_cgpio_state:
                    	for item in self.cgpio_callbacks:
                        	if item['type'] == 'digital':
                            	for io in range(len(digitals)):
                                	if item['io'] == io and eval('{} {} {}'.format(digitals[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['cgpio']['digital'][io], item['op'], item['trigger'])):
                                    	item['callback']()
                        	elif item['type'] == 'analog':
                            	for io in range(2):
                                	if item['io'] == io and eval('{} {} {}'.format(analogs[io], item['op'], item['trigger'])) and not eval('{} {} {}'.format(self.values['cgpio']['analog'][io], item['op'], item['trigger'])):
                                    	item['callback']()
                	self.values['cgpio']['digital'] = digitals
                	self.values['cgpio']['analog'] = analogs
                	self.values['cgpio']['digital_o'] = digitals_o
                	self.values['cgpio']['analog_o'] = analogs_o
                	self.is_init_cgpio_state = True
        	time.sleep(0.1)

params['events']['gpio'] = EventGPIOThread()
if not params['quit']:
	params['angle_speed'] = 50
if not params['quit']:
	params['angle_acc'] = 500
if arm.error_code == 0 and not params['quit']:
	arm.set_pause_time(1)


def get_camera_position():
	global x_mm
	global y_mm
	global r
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    	s.connect((HOST, PORT))
    	s.settimeout(None)
    	s.sendall(b"cmd Online")
    	s.sendall(b"cmd trigger")
    	data = s.recv(24)
        	#IMPORTANTE REVISAR EL TAMAÑO DEL STRING QUE SE ENVÍA PARA SELECCIONAR LOS BITES ADECUADOS

	print(f"Received2 {data!r}")

	str1 = data.decode('UTF-8')
	t=str1.split(" ")   #IMPORTANTE REVISAR CUAL ES EL CARACTER USADO PARA DELIMITAR CADA DATO
	x=float(t[0])
	y=float(t[1])
	r=float(t[2])

	image_width = 1280
	image_height = 1024

	x_centered = x - image_width / 2
	y_centered = y - image_height / 2

	x_mm = x_centered / 8.9790
	y_mm = y_centered / 8.9790

	arm_offset_x = 90
	x_mm = x_mm + arm_offset_x
	arm_offset_y = 9.5
	y_mm = y_mm + arm_offset_y

if not params['quit']:
	params['variables']['active'] = 0
# Define Contoller GPIO-7 DIGITAL is LOW callback
def controller_gpio_7_digital_is_changed_callback_1():
	def _callback():
    	while params['variables'].get('active', 0) == 1 and not params['quit']:
        	pass
    	if not params['quit']:
        	params['variables']['active'] = 1
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_cgpio_digital(0, 0, delay_sec=0)
        	code = arm.set_servo_angle(angle=[0.0, -80.0, -10.0, 0.0, 90.0, 0.0], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=True, radius=20.0)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_servo_angle, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_position(*[-69.6, 243.5, 96.8, 179.8, 0.8, 92.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_position, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
         	code = arm.set_cgpio_digital(2, 1, delay_sec=0)
        	get_camera_position()
        	time.sleep(2)

        	if code != 0:
            	params['quit'] = True
            	pprint('set_cgpio_digital, code={}'.format(code)
    	if arm.error_code == 0 and not params['quit']:
        	arm.set_pause_time(2)
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_cgpio_digital(2, 0, delay_sec=0)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_cgpio_digital, code={}'.format(code))
           	 
    	if arm.error_code == 0 and not params['quit']:
        	arm.set_pause_time(1)
    	if arm.error_code == 0 and not params['quit']:
        	print(x_mm)
        	print(y_mm)
        	print(r)
        	code = arm.set_position(*[(-69.6 + y_mm),(243.5 + x_mm),86.6,179.8,0.8,(92 - r)], speed=params['speed'], mvacc=params['acc'], radius=-1, wait=True)
        	code = arm.set_position(*[(-69.6 + y_mm),(243.5 + x_mm),-51.9,179.8,0.8,(92 - r)], speed=params['speed'], mvacc=params['acc'], radius=-1, wait=True)
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_cgpio_digital(0, 1, delay_sec=0)
        	code = arm.set_position(*[-69.6, 243.5, 96.8, 179.8, 0.8, 92.0], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)  
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_position(*[218.8, 63.1, 76.6, 179.7, 1.1, 1.4], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_position, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_position(*[217.1, 62.3, -67.1, 179.9, 0.4, 1.3], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_position, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_cgpio_digital(0, 0, delay_sec=0)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_cgpio_digital, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_position(*[218.8, 63.1, 76.6, 179.7, 1.1, 1.4], speed=params['speed'], mvacc=params['acc'], radius=-1.0, wait=True)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_position, code={}'.format(code))
    	if arm.error_code == 0 and not params['quit']:
        	code = arm.set_servo_angle(angle=[0.0, -80.0, -10.0, 0.0, 90.0, 0.0], speed=params['angle_speed'], mvacc=params['angle_acc'], wait=True, radius=20.0)
        	if code != 0:
            	params['quit'] = True
            	pprint('set_position, code={}'.format(code))
    	if not params['quit']:
        	params['variables']['active'] = 0
	_callback() if not params['callback_in_thread'] else threading.Thread(target=_callback, daemon=True).start()
params['events']['gpio'].cgpio_callbacks.append({'type': 'digital', 'io': 7, 'trigger': 0, 'op': '==', 'callback': controller_gpio_7_digital_is_changed_callback_1})
if not params['events']['gpio'].alive:
	params['events']['gpio'].start()
# Main loop
while arm.connected and arm.error_code == 0 and not params['quit']:
	time.sleep(0.5)
# release all event
if hasattr(arm, 'release_count_changed_callback'):
	arm.release_count_changed_callback(count_changed_callback)
arm.release_error_warn_changed_callback(state_changed_callback)
arm.release_state_changed_callback(state_changed_callback)
arm.release_connect_changed_callback(error_warn_change_callback)
