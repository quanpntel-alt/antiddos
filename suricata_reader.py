import json
import os
from collections import defaultdict
from datetime import datetime, timedelta

EVE_LOG = "/var/log/suricata/eve.json"

# Đọc snapshot TTL, size, count cho mỗi IP
def read_eve_snapshot(interval_sec=10):
    ip_stats = defaultdict(lambda: {"count": 0, "size": 0, "ttl_list": []})

    if not os.path.exists(EVE_LOG):
        print(f"[ERROR] Không tìm thấy file {EVE_LOG}")
        return {}

    try:
        with open(EVE_LOG, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Không đọc được {EVE_LOG}: {e}")
        return {}

    time_threshold = datetime.utcnow() - timedelta(seconds=interval_sec)

    for line in reversed(lines):
        try:
            data = json.loads(line)
            if data.get("event_type") != "flow":
                continue

            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S.%f%z")
            if timestamp.replace(tzinfo=None) < time_threshold:
                break

            src_ip = data["src_ip"]
            ttl = data.get("ip_ttl")
            pkt_size = data.get("flow", {}).get("bytes_toserver", 0)

            ip_stats[src_ip]["count"] += 1
            ip_stats[src_ip]["size"] += pkt_size
            if ttl:
                ip_stats[src_ip]["ttl_list"].append(ttl)

        except Exception:
            continue

    return ip_stats
