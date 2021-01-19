# !/usr/bin/python

import os, sys
import csv

devices = {}
# listing directories
#print("The dir is: %s"%os.listdir(os.getcwd()))

directories = os.listdir(os.getcwd())

with open('list_of_devices.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ';')
    for line in reader: 
        devices[line['deviceIp']] = line['deviceSysname']

for folder in directories: 
    if folder in devices:
        os.rename(folder, folder + '___' + devices[folder])
        print(f'replace {folder} with {folder}___{devices[folder]}')
    else:
        print(f'folder: {folder}')

# # renaming directory ''tutorialsdir"
# os.rename("tutorialsdir","tutorialsdirectory")

# print "Successfully renamed."

# # listing directories after renaming "tutorialsdir"
# print "the dir is: %s" %os.listdir(os.getcwd())


# with open('names.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)