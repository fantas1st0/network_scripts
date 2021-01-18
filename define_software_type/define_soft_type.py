# -*- coding: utf-8 -*-
"""
функция find_ver возвращает словарь вида:
{
'dev1': 'IOS', 
'dev2': 'NX-OS'
}
"""
from pprint import pprint
import os
import sys
sys.path.append('../device_inventory')
from device_list import get_devices

def find_ver(device_list):
	ver_dict = {}
	show_ver_list = []
	os.chdir("../define_software_type")
	cwd = os.getcwd()
	for device in device_list:
		ver_file = device + "-show_version" + ".txt"
		with open (ver_file) as f:
			for line in f:
				if "Cisco Nexus Operating System" in line:
					software = "NX-OS"
					break
				if "Cisco IOS Software" in line:
					software = "IOS"
					break
		ver_dict[device] = software
	return(ver_dict)

if __name__ == '__main__':
	device_file = "/Users/alexguse/Documents/Python/Scripts/network_scripts/device_inventory/device_list.xlsx"
	device_list = get_devices(device_file)
	soft = find_ver(device_list)
	pprint(soft)
