Нахождение связки MAC - IP. Поиск производится по всем VRF.

Входные данные:\
device_inventory/device_list.xlsx - файл с именами устройств;\
resolve_mac_by_ip/resolve_mac_by_ip.py , лист ip_list - список IP адресов для поиска;

Скрипт составляет Excel-файл, в котором перечислены:\
IP, MAC, L3 INTERFACE, DEVICE, VRF