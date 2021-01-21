import os
from pprint import pprint
import re

def rename_dir(directory):
	os.chdir("./" + directory)
	arr = os.listdir()
	ip_dev = {}
	for device in arr:
		if "___" in device:
			k = device.split("___")[0]
			v = device.split("___")[1]
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
	os.chdir("./" + raw_inv)
	for directory in os.listdir():
		rename_dir(directory)
