import subprocess

def activate_latency(interface, delay):
    command1 = f"powershell -Command \"netsh interface ipv4 set interface '{interface}' mtu=1500 store=persistent\""
    command2 = f"powershell -Command \"netsh interface ipv4 add neighbors '{interface}' '192.168.1.1' '11-22-33-44-55-66' store=persistent\""

    subprocess.call(command1, shell=True)
    subprocess.call(command2, shell=True)

def deactivate_latency(interface):
    command1 = f"powershell -Command \"netsh interface ipv4 delete neighbors '{interface}' '192.168.1.1' '11-22-33-44-55-66' store=persistent\""
    command2 = f"powershell -Command \"netsh interface ipv4 set interface '{interface}' mtu=1500 store=persistent\""

    subprocess.call(command1, shell=True)
    subprocess.call(command2, shell=True)

# Usage example
interface = "Wi-Fi"
delay = 100

# Activate latency
activate_latency(interface, delay)


# Deactivate latency
deactivate_latency(interface)
