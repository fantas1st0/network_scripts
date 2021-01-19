import os
from pprint import pprint
import re


if __name__ == "__main__":
	arr = os.listdir()
	for directory in arr:
		if "Raw" in directory:
			raw_inv = directory
	os.chdir("./" + raw_inv)
	cwd = os.getcwd()
	arr = os.listdir()
	os.chdir("./Config")
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
			abcd = file.split("-")[0]
			regex = "(?P<ip_add>\S+)-(?P<type>\S+)"
			match = re.search(regex, file)
			if match:
				newname = device + "-" + match.group("type")
				pprint(newname)
				os.rename(file, newname)
		os.chdir("../")
