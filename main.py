from pywifi import PyWiFi, const

wifi = PyWiFi()
iface = wifi.interfaces()[0]
iface.scan()
results = iface.scan_results()

for network in results:
    print(network.ssid, network.signal)
