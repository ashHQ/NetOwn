from pywifi import PyWiFi, const
import time
import subprocess

def get_wifi_interfaces():
    """Get a list of Wi-Fi interfaces using iwconfig."""
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        interfaces = []
        for line in result.stdout.splitlines():
            if 'IEEE 802.11' in line:
                iface_name = line.split()[0]
                if 'p2p' not in iface_name.lower():
                    interfaces.append(iface_name)
        return interfaces
    except subprocess.CalledProcessError:
        return []

def main():
    wifi = PyWiFi()
    interfaces = wifi.interfaces()

    print("Available pywifi interfaces:", [iface.name() for iface in interfaces])

    wifi_ifaces = get_wifi_interfaces()
    if not wifi_ifaces:
        print("No Wi-Fi interfaces found. Ensure a Wi-Fi adapter is connected and drivers are installed.")
        exit(1)
    print("Detected Wi-Fi interfaces from iwconfig:", wifi_ifaces)

    iface = None
    for i in interfaces:
        if i.name() in wifi_ifaces:
            iface = i
            break

    if not iface:
        print("No suitable Wi-Fi interface found for pywifi. Check adapter compatibility.")
        exit(1)

    print(f"Using interface: {iface.name()}")

    try:
        iface.scan()
        time.sleep(5) 
        results = iface.scan_results()
    except Exception as e:
        print(f"Scan failed: {e}")
        exit(1)

    if not results:
        print("No networks found. Ensure Wi-Fi is enabled and the adapter supports scanning.")
        try:
            subprocess.run(['iwlist', iface.name(), 'scan'], check=True)
            print("Note: iwlist scan ran successfully; issue may be with pywifi.")
        except subprocess.CalledProcessError:
            print("iwlist scan also failed. Check adapter or drivers.")
    else:
        for network in results:
            print(f"SSID: {network.ssid}, Signal: {network.signal} dBm")

if __name__ == "__main__":
    main()