from pywifi import PyWiFi, const
import time

wifi = PyWiFi()
interfaces = wifi.interfaces()

if not interfaces:
    print("No Wi-Fi interfaces found. Check your Wi-Fi adapter or drivers.")
    exit(1)

iface = interfaces[0]
print(f"Using interface: {iface.name()}")  

iface.scan()
time.sleep(10)  
results = iface.scan_results()

if not results:
    print("No networks found. Ensure Wi-Fi is enabled and try running with sudo.")
else:
    for network in results:
        print(f"SSID: {network.ssid}, Signal: {network.signal}")