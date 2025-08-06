import subprocess

# ⚙️ Sử dụng iptables đơn giản
def block_ip(ip):
    try:
        # Kiểm tra đã chặn chưa
        result = subprocess.run(
            ["iptables", "-C", "INPUT", "-s", ip, "-j", "DROP"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return  # Đã chặn rồi

        # Thêm rule chặn IP
        subprocess.run(["iptables", "-I", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"[+] Blocked IP: {ip}")
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed to block {ip}")

