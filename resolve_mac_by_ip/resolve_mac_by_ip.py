# -*- coding: utf-8 -*-
"""
функция find_mac_by_ip возвращает список словарей, состоящий из IP, MAC и INTERFACE
каждый словарь определяется L3 интерфейсом (для случая если один IP живет в нескольких VRF)

[{'IP': '10.8.5.18', 'L3 INTERFACE': 'Vlan500', 'MAC': 'd867.d96f.05c1'},
 {'IP': '10.8.5.18', 'L3 INTERFACE': 'Vlan501', 'MAC': 'd867.d96f.05c1'}]

после этого необходимо найти VRF для каждого L3 INTERFACE

функция find_vrf ищет VRF для каждого ранее найденного L3 INTERFACE 

dict_list - список словарей вида, из которого происходит запись в .csv файл
[{'DEVICE': 'dev1',
  'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan500',
  'MAC': 'd867.d96f.05c1',
  'VRF': 'default'},
 {'DEVICE': 'dev2',
  'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan501',
  'MAC': 'd867.d96f.05c1',
  'VRF': 'GLOBAL'}]

def find_ver(device_list):

"""
from pprint import pprint
import csv
import os
import sys
sys.path.append('../device_inventory')
sys.path.append('../define_software_type')
from device_list import get_data
from define_soft_type import find_ver
from xlsxwriter import Workbook

def find_mac_by_ip_nxos(devicename, ip):
	dict_list = []
	with open (devicename) as f:
		for line in f:
			if ip in line:
				arp_dict = {}
				ip, age, mac, intf = line.strip().split()
				arp_dict["IP"] = ip
				arp_dict["MAC"] = mac
				arp_dict["L3 INTERFACE"] = intf
				dict_list.append(arp_dict)
	res = list(filter(None, dict_list))
	return(res)

def find_mac_by_ip_ios(devicename, ip):
	dict_list = []
	with open (devicename) as f:
		for line in f:
			if ip in line:
				arp_dict = {}
				inet, ip, age, mac, arpa, intf = line.strip().split()
				arp_dict["IP"] = ip
				arp_dict["MAC"] = mac
				arp_dict["L3 INTERFACE"] = intf
				dict_list.append(arp_dict)
	res = list(filter(None, dict_list))
	return(res)

def find_vrf(ip_mac, ip_int_device):
	vrf_list = []
	l3_intf = ip_mac["L3 INTERFACE"]
	with open (ip_int_device) as f:
		for line in f:
			if "VRF" in line:
				vrf = line.split()[-1]
				position = vrf.find("(")
				vrf = vrf[:position].strip('"')
			if l3_intf in line:
				vrf_dict = {}
				vrf_dict["L3 INTERFACE"] = l3_intf
				vrf_dict["VRF"] = vrf
	res = vrf_dict["VRF"]
	return(res)

# входные данные
device_file = "/Users/alexguse/Documents/Python/Scripts/network_scripts/device_inventory/device_list.xlsx"
device_list = get_data(device_file)
soft = find_ver(device_list)

os.chdir("../resolve_mac_by_ip")
show_arp_list = []
ip_int_br_list = []

ip_file = "/Users/alexguse/Documents/Python/Scripts/network_scripts/device_inventory/ip_find_list.xlsx"
ip_list = get_data(ip_file)

for device in device_list:
	arp = device + "_show_ip_arp" + ".txt"
	ip_int = device + "_show_ip_int" + ".txt"
	show_arp_list.append(arp)
	ip_int_br_list.append(ip_int)

dict_list = []
for device, arp, ip_int_br in zip(device_list, show_arp_list, ip_int_br_list):
	if soft[device] == "NX-OS":
		ip_mac_list = []
		vrf_list = []
		vrf_ip_mac_list = []
		for ip in ip_list:
			ip_mac_list = ip_mac_list + find_mac_by_ip_nxos(arp, ip)
		ip_mac_list = list(filter(None, ip_mac_list))
		for ip_mac in ip_mac_list:
			vrf = find_vrf(ip_mac, ip_int_br)
			ip_mac["VRF"] = vrf
			ip_mac["DEVICE"] = device
			ip_mac["SOFTWARE"] = soft[device]
			vrf_ip_mac_list.append(ip_mac)
		dict_list = dict_list + vrf_ip_mac_list
	if soft[device] == "IOS":
		ip_mac_list = []
		vrf_list = []
		vrf_ip_mac_list = []
		for ip in ip_list:
			ip_mac_list = ip_mac_list + find_mac_by_ip_ios(arp, ip)
		ip_mac_list = list(filter(None, ip_mac_list))
		for ip_mac in ip_mac_list:
			vrf = find_vrf(ip_mac, ip_int_br)
			ip_mac["VRF"] = vrf
			ip_mac["DEVICE"] = device
			ip_mac["SOFTWARE"] = soft[device]
			vrf_ip_mac_list.append(ip_mac)
		dict_list = dict_list + vrf_ip_mac_list
		
#dict_list = [{'DEVICE': 'dev1',
#  'IP': '10.8.5.18',
#  'L3 INTERFACE': 'Vlan500',
#  'MAC': '64ae.0c40.47c0',
#  'SOFTWARE': 'IOS',
#  'VRF': 'default'}]

ordered_list=["DEVICE","IP","L3 INTERFACE","MAC", "SOFTWARE", "VRF"]
wb=Workbook("RESULT/results_ips.xlsx")
ws=wb.add_worksheet("IPs")
first_row=0
for header in ordered_list:
    col=ordered_list.index(header) # we are keeping order.
    ws.write(first_row,col,header) # we have written first row which is the header of worksheet also.
row=1
for element in dict_list:
    for k, v in element.items():
        col=ordered_list.index(k)
        ws.write(row,col,v)
    row = row + 1 #enter the next row
wb.close()
