# -*- coding: utf-8 -*-
"""
функция find_mac_by_ip возвращает список словарей, состоящий из IP, MAC и INTERFACE
каждый словарь определяется L3 интерфейсом (для случая если один IP живет в нескольких VRF)

[{'IP': '10.8.5.18', 'MAC': '8478.ac5a.7fc2', 'L3 INTERFACE': 'Vlan501'},
{'IP': '10.8.5.18', 'MAC': '8478.ac5a.7fc3', 'L3 INTERFACE': 'Vlan501'},
{'IP': '10.8.5.19', 'MAC': '8478.ac5a.7fc2', 'L3 INTERFACE': 'Vlan501'},
{'IP': '10.8.5.19', 'MAC': '8478.ac5a.7fc3', 'L3 INTERFACE': 'Vlan501'}
]

после этого необходимо найти VRF для каждого L3 INTERFACE

функция find_vrf ищет VRF для каждого ранее найденного L3 INTERFACE и возвращает список словарей вида

[{'L3 INTERFACE': 'Vlan500', 'VRF': 'default'},
 {'L3 INTERFACE': 'Vlan501', 'VRF': 'GLOBAL'},
 {'L3 INTERFACE': 'Vlan502', 'VRF': 'ALIEN'},
 {'L3 INTERFACE': 'Vlan503', 'VRF': 'VTB-DOS-CS'},
 {'L3 INTERFACE': 'Vlan504', 'VRF': 'NPB-GRE'}]

функция dict_merge возвращает список словареий вида
[{'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan500',
  'MAC': '8478.ac5a.7fc2',
  'VRF': 'default'},
 {'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan501',
  'MAC': '8478.ac5a.7fc3',
  'VRF': 'GLOBAL'},
 {'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan502',
  'MAC': '8478.ac5a.7fc3',
  'VRF': 'ALIEN'},
 {'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan503',
  'MAC': '8478.ac5a.7fc3',
  'VRF': 'VTB-DOS-CS'},
 {'IP': '10.8.5.18',
  'L3 INTERFACE': 'Vlan504',
  'MAC': '8478.ac5a.7fc3',
  'VRF': 'default'}]

"""
from pprint import pprint

def find_mac_by_ip(devicename, ip):
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

def find_vrf(ip_mac, ip_int_device):
	vrf_list = []
	for arp_vrf in ip_mac:
		l3_intf = arp_vrf["L3 INTERFACE"]
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
					vrf_list.append(vrf_dict)
	return(vrf_list)

def dict_merge(ip_mac, vrf):
	new_list = []
	for vrfs_dict in vrf:
		vrf_fin = vrfs_dict["VRF"]
		for ips in ip_mac:
			if vrfs_dict["L3 INTERFACE"] == ips["L3 INTERFACE"]:
				new_dict = {}
				ips["VRF"] = vrf_fin
				new_list.append(ips)
	return (new_list)

device_list = ["dev1_show_arp.txt", "dev2_show_arp.txt"]
ip_int_br_list = ["dev1_show_ip_int.txt", "dev2_show_ip_int.txt"]
ip_list = ["10.8.5.18", "10.8.5.19", "10.8.5.254", "99.99.99.99"]
total_dict = {}
for device, ip_int_br in zip(device_list, ip_int_br_list):
	ip_mac_list = []
	vrf_list = []
	vrf_ip_mac_list = []
	for ip in ip_list:
		ip_mac_list.append(find_mac_by_ip(device, ip))
	ip_mac_list = list(filter(None, ip_mac_list))
	for ip_mac in ip_mac_list:
		vrf_list.append(find_vrf(ip_mac, ip_int_br))
	for ip_mac, vrf in zip(ip_mac_list, vrf_list):
		vrf_ip_mac_list.append(dict_merge(ip_mac, vrf))
	total_dict[device] = vrf_ip_mac_list
pprint(total_dict)
