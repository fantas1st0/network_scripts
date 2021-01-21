import os
import sys
from pprint import pprint
import re

def get_devices():
	devices = {}
	for ip in os.listdir():
		os.chdir("./" + ip)
		for config in os.listdir():
			if "running.txt" in config:
				with open(config) as f:
					for line in f:
						if "hostname" in line:
							devicename = line.split()[-1]
							devices[ip] = devicename
							break
				break
		os.chdir("../")
	return (devices)

def rename_dir(directory, devices):
	os.chdir("./" + directory)
	ip_dev = {}
	for device in os.listdir():
		k = device.split("-")[0]
		v = devices[k]
		ip_dev[k] = v
		os.rename(device, v)
	for device in ip_dev.values():
		os.chdir("./" + device)
		files = os.listdir()
		for file in files:
			regex = "(?P<ip_add>\S+)-(?P<type>\S+)"
			match = re.search(regex, file)
			if match:
				newname = device + "-" + match.group("type")
				os.rename(file, newname)
		os.chdir("../")
	os.chdir("../")

if __name__ == "__main__":
	for directory in os.listdir():
		if "Raw" in directory:
			raw_inv = directory
	os.chdir("./" + raw_inv + "/Config")
	devices = get_devices()
	os.chdir("../")
	for directory in os.listdir():
		try:
			rename_dir(directory, devices)
		except NotADirectoryError:
			continue