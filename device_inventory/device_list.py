# -*- coding: utf-8 -*-
"""
Функция get_data составляет список устройств для анализа. Excel-файл со списком устройств передается как входной аргумент.
В файле - устройства должны находиться в закладке "devices"
Возвращается список устройств вида ['dev1', 'dev2']
"""
from openpyxl import load_workbook

def get_data(device_file):
	wb = load_workbook(device_file)
	sheet = wb["devices"]
	device_list = []
	for row in sheet.rows:
		device_list.append(row[0].value)
	return(device_list)

if __name__ == "__main__":
	devices = get_devices("device_list.xlsx")
