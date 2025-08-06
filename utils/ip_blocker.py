import subprocess

IPSET_NAME = "ddos_blacklist"

# ⚙️ Tạo ipset nếu chưa tồn tại
def create_ipset():
    try:
        subprocess.run(["ipset", "list", IPSET_NAME],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
    except subprocess.CalledProcessError:
        # Chưa có thì tạo
        subprocess.run(["ipset", "create", IPSET_NAME, "hash:ip", "timeout", "3600"], check=True)
        subprocess.run(["iptables", "-C", "INPUT", "-m", "set", "--match-set", IPSET_NAME, "src", "-j", "DROP"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["iptables", "-I", "INPUT", "-m", "set", "--match-set", IPSET_NAME, "src", "-j", "DROP"],
                       check=False)
        print(f"[+] Created ipset and attached to iptables: {IPSET_NAME}")

# 🚫 Chặn IP (tự động timeout sau 1h)
def block_ip(ip):
    try:
        subprocess.run(["ipset", "add", IPSET_NAME, ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] Blocked IP via ipset: {ip}")
    except Exception as e:
        print(f"[ERROR] Failed to block {ip}: {e}")
