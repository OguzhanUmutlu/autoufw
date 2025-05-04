import os
import re
import subprocess
import sys
import threading

pending_ips = set()
pending_lock = threading.Lock()
tcpdump_processes = []

for filename in ["ips.txt", "bad_ips.txt", "ports.txt"]:
    if not os.path.exists(filename):
        open(filename, "a").close()


def read_ip_file(file):
    with open(file, "r") as f:
        return {
            re.sub(r"#.*", "", line).strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        }


allowed_ips = read_ip_file("ips.txt")
bad_ips = read_ip_file("bad_ips.txt")

with open("ports.txt", "r") as f:
    ports = [line.strip() for line in f if line.strip()]

if len(ports) == 0:
    print("No ports found in ports.txt.")
    sys.exit(1)


def monitor_port(port):
    tcpdump = subprocess.Popen(
        ["sudo", "tcpdump", "-nn", "-l", "-i", "any", f"port {port}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=1,
    )
    tcpdump_processes.append(tcpdump)
    for line in tcpdump.stdout:
        line = line.strip()
        if not line:
            continue
        match = re.search(r"IP (\d+\.\d+\.\d+\.\d+)\.\d+ > ", line)
        if match:
            ip = match.group(1)
            with pending_lock:
                if ip not in allowed_ips and ip not in bad_ips:
                    pending_ips.add(ip)


for port in ports:
    threading.Thread(target=monitor_port, args=(port,), daemon=True).start()


def cleanup_and_exit():
    print("\nShutting down... Killing tcpdump processes.")
    for proc in tcpdump_processes:
        proc.terminate()
    sys.exit(0)


try:
    while True:
        cmd = input("\n[Press Enter to check rules / type 'clear' to discard seen IPs] ").strip().lower()

        if cmd == "clear":
            with pending_lock:
                pending_ips.clear()
            print("Pending IP queue cleared.")
            continue

        while True:
            ufw_output = subprocess.check_output(["sudo", "ufw", "status", "numbered"], text=True)
            found = False
            for line in ufw_output.splitlines():
                match = re.match(r"\[\s*(\d+)\]\s+(\d+)/tcp\s+ALLOW\s+\S+\s+(\d+\.\d+\.\d+\.\d+)", line)
                if match:
                    rule_num, port, ip = match.groups()
                    if port in ports and ip not in allowed_ips:
                        print(f"Deleting rule: {line.strip()}")
                        subprocess.run(["sudo", "ufw", "delete", rule_num])
                        found = True
                        break
            if not found:
                break

        current_status = subprocess.check_output(["sudo", "ufw", "status"], text=True)
        for port in ports:
            for ip in allowed_ips:
                rule_pattern = f"{port}/tcp.*{ip}"
                if not re.search(rule_pattern, current_status):
                    print(f"Adding rule: allow from {ip} to port {port}/tcp")
                    subprocess.run(["sudo", "ufw", "allow", "from", ip, "to", "any", "port", port, "proto", "tcp"])

        with pending_lock:
            for ip in list(pending_ips):
                action = input(f"\nNew IP detected: {ip}\n[A]llow, [B]an, [S]kip? ").lower().strip()
                if action == "a":
                    description = input("Enter description for this IP (optional): ").strip()
                    allowed_ips.add(ip)
                    with open("ips.txt", "a") as f:
                        comment = f" # {description}" if description else ""
                        f.write(f"{ip}{comment}\n")
                    for port in ports:
                        subprocess.run(["sudo", "ufw", "allow", "from", ip, "to", "any", "port", port, "proto", "tcp"])
                    pending_ips.remove(ip)
                elif action == "b":
                    bad_ips.add(ip)
                    with open("bad_ips.txt", "a") as f:
                        f.write(f"{ip}\n")
                    pending_ips.remove(ip)
                else:
                    print(f"Skipped: {ip}")

except KeyboardInterrupt:
    cleanup_and_exit()
